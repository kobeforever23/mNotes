#!/usr/bin/env python3
"""
Crypto Exposure Finder (EDGAR) — Hardened
Run -> enter company name/ticker/CIK -> confirm match -> scan recent filings + exhibits
Outputs: JSON + Markdown with evidence snippets and links

Install:
  pip install requests beautifulsoup4 lxml
"""

import os, re, json, time, textwrap
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple
import requests
from bs4 import BeautifulSoup

SEC_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SEC_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik10}.json"
ARCHIVES_BASE = "https://www.sec.gov/Archives/edgar/data"

DEFAULT_USER_AGENT = "CryptoExposureFinder/1.1 (yourname your@email.com)"
REQUEST_SLEEP_SECONDS = 0.35
MAX_RETRIES = 4

CRYPTO_KEYWORDS = [
    r"\bcrypto\b", r"\bcryptocurrency\b", r"\bdigital asset(s)?\b",
    r"\bbitcoin\b", r"\bBTC\b", r"\bethereum\b", r"\bETH\b",
    r"\bstablecoin(s)?\b", r"\bUSDC\b", r"\bUSDT\b", r"\bTether\b",
    r"\bblockchain\b", r"\bweb3\b", r"\bwallet(s)?\b",
    r"\bcustody\b", r"\bstaking\b", r"\bminer(s|ing)?\b",
    r"\btoken(s)?\b", r"\bNFT(s)?\b",
    r"\bcoinbase\b", r"\bbinance\b", r"\bkraken\b",
]

EXPOSURE_CATEGORIES = {
    "Direct holdings / treasury": [
        r"\bheld\b.*\b(bitcoin|ethereum|digital asset|crypto)\b",
        r"\btreasury\b.*\b(bitcoin|ethereum|digital asset|crypto)\b",
        r"\bimpairment\b.*\b(digital asset|crypto|bitcoin)\b",
        r"\bfair value\b.*\b(digital asset|crypto|bitcoin)\b",
    ],
    "Revenue / business model": [
        r"\bcustody\b.*\bfees?\b",
        r"\btrading\b.*\bfees?\b",
        r"\bexchange\b.*\brevenue\b",
        r"\bmining\b.*\brevenue\b",
        r"\bstaking\b.*\breward(s)?\b",
    ],
    "Custody / safeguarding": [
        r"\bacts? as custodian\b",
        r"\bsafeguard(ing|ed)\b.*\b(digital asset|crypto)\b",
        r"\bqualified custodian\b",
    ],
    "Counterparty / credit exposure": [
        r"\b(counterparty|credit exposure)\b.*\b(crypto|digital asset|exchange)\b",
        r"\bloans?\b.*\b(crypto|digital asset)\b",
        r"\bdeposits?\b.*\b(crypto|exchange)\b",
    ],
    "Derivatives / structured exposure": [
        r"\bfutures?\b.*\b(bitcoin|crypto)\b",
        r"\boptions?\b.*\b(bitcoin|crypto)\b",
        r"\bswap(s)?\b.*\b(bitcoin|crypto)\b",
        r"\bderivative(s)?\b.*\b(digital asset|crypto|bitcoin)\b",
    ],
    "Risk factor disclosures": [
        r"\brisk factor(s)?\b",
        r"\bmaterial adverse\b",
        r"\bregulatory\b.*\b(crypto|digital asset)\b",
        r"\bvolatil(e|ity)\b.*\b(crypto|digital asset|bitcoin)\b",
    ],
}

@dataclass
class FilingHit:
    form: str
    filing_date: str
    accession: str
    primary_doc: str
    accession_nodash: str
    cik_int: int
    filing_url: str
    index_url: str

@dataclass
class Snippet:
    category: str
    keyword: str
    text: str
    form: str
    filing_date: str
    source_doc: str
    url: str

def get_user_agent() -> str:
    return os.getenv("SEC_USER_AGENT", "").strip() or DEFAULT_USER_AGENT

def sec_get(url: str, session: requests.Session) -> requests.Response:
    headers = {
        "User-Agent": get_user_agent(),
        "Accept-Encoding": "gzip, deflate",
        "Accept": "application/json,text/html,*/*",
        "Connection": "keep-alive",
    }

    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.get(url, headers=headers, timeout=30)
            time.sleep(REQUEST_SLEEP_SECONDS)

            # handle rate limiting / bot protection gracefully
            if resp.status_code in (403, 429, 500, 502, 503):
                last_err = f"HTTP {resp.status_code}"
                backoff = min(2 ** attempt, 16)
                time.sleep(backoff)
                continue

            resp.raise_for_status()
            return resp
        except Exception as e:
            last_err = str(e)
            time.sleep(min(2 ** attempt, 16))

    raise RuntimeError(f"SEC request failed after retries: {url} | last error: {last_err}")

def normalize_cik10(cik: int) -> str:
    return str(cik).zfill(10)

def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ")
    return re.sub(r"\s+", " ", text).strip()

def load_tickers(session: requests.Session) -> List[Dict[str, Any]]:
    return list(sec_get(SEC_TICKERS_URL, session).json().values())

def canonicalize_query(q: str) -> str:
    q = q.strip().lower()
    q = re.sub(r"[^a-z0-9\s\.\-&]", " ", q)
    q = re.sub(r"\s+", " ", q).strip()
    return q

def search_companies(tickers_data: List[Dict[str, Any]], query: str, limit: int = 25) -> List[Dict[str, Any]]:
    q = canonicalize_query(query)
    q_nospace = q.replace(" ", "")

    # Allow exact ticker match, partial name match, and token match
    tokens = [t for t in q.split(" ") if t]

    hits = []
    for row in tickers_data:
        title = canonicalize_query(str(row.get("title", "")))
        ticker = canonicalize_query(str(row.get("ticker", "")))
        cik = row.get("cik_str")

        score = 0
        if q and ticker == q:
            score += 100
        if q and q in title:
            score += 30
        if q_nospace and q_nospace in title.replace(" ", ""):
            score += 25
        # token scoring
        for t in tokens:
            if len(t) >= 3 and t in title:
                score += 5

        if score > 0:
            hits.append({"title": row.get("title"), "ticker": row.get("ticker"), "cik_str": cik, "score": score})

    hits.sort(key=lambda r: (-r["score"], len(r["title"] or "")))
    return hits[:limit]

def choose_company(hits: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not hits:
        return None
    print("\nMatches found:")
    for i, h in enumerate(hits, start=1):
        print(f"  [{i}] {h['title']} | Ticker: {h['ticker']} | CIK: {h['cik_str']}")
    while True:
        raw = input("\nSelect a company number (or 'r' to retry search, 'c' to enter CIK, 'q' to quit): ").strip().lower()
        if raw == "q":
            return None
        if raw == "r":
            return {"__retry__": True}
        if raw == "c":
            cik_raw = input("Enter CIK (digits only): ").strip()
            if cik_raw.isdigit():
                return {"title": "(CIK provided)", "ticker": None, "cik_str": int(cik_raw)}
            print("Invalid CIK.")
            continue
        if raw.isdigit():
            idx = int(raw)
            if 1 <= idx <= len(hits):
                return hits[idx - 1]
        print("Invalid selection. Try again.")

def get_recent_filings(session: requests.Session, cik10: str, forms: List[str], limit: int = 8) -> List[FilingHit]:
    sub = sec_get(SEC_SUBMISSIONS_URL.format(cik10=cik10), session).json()
    recent = sub.get("filings", {}).get("recent", {})
    form_list = recent.get("form", [])
    date_list = recent.get("filingDate", [])
    acc_list = recent.get("accessionNumber", [])
    doc_list = recent.get("primaryDocument", [])

    hits: List[FilingHit] = []
    cik_int = int(cik10)

    for form, fdate, acc, doc in zip(form_list, date_list, acc_list, doc_list):
        if form in forms:
            accession_nodash = acc.replace("-", "")
            filing_url = f"{ARCHIVES_BASE}/{cik_int}/{accession_nodash}/{doc}"
            index_url = f"{ARCHIVES_BASE}/{cik_int}/{accession_nodash}/{acc}-index.html"
            hits.append(FilingHit(form, fdate, acc, doc, accession_nodash, cik_int, filing_url, index_url))
        if len(hits) >= limit:
            break
    return hits

def parse_index_for_docs(index_html: str) -> List[Tuple[str, str]]:
    """
    Returns list of (doc_name, doc_url_suffix) from the index page table.
    """
    soup = BeautifulSoup(index_html, "lxml")
    docs = []

    table = soup.find("table", class_=re.compile("tableFile", re.I))
    if not table:
        return docs

    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) >= 3:
            link = cols[2].find("a")
            if link and link.get("href"):
                href = link["href"]
                name = link.get_text(strip=True)
                docs.append((name, href))
    return docs

def fetch_doc_text(session: requests.Session, url: str) -> str:
    resp = sec_get(url, session)
    ct = resp.headers.get("Content-Type", "").lower()
    if "html" in ct or "<html" in resp.text.lower():
        return html_to_text(resp.text)
    return resp.text

def categorize_context(ctx: str) -> str:
    c = ctx.lower()
    for category, rules in EXPOSURE_CATEGORIES.items():
        for r in rules:
            if re.search(r, c, flags=re.IGNORECASE):
                return category
    # If it only says “digital assets” with no crypto keywords, keep it cautious
    if re.search(r"\bdigital assets?\b", c) and not re.search(r"(crypto|bitcoin|ethereum|stablecoin)", c):
        return "Ambiguous 'digital assets' mention"
    return "General crypto mention"

def extract_snippets(text: str, filing: FilingHit, source_doc: str, source_url: str, window: int = 320) -> List[Snippet]:
    snippets: List[Snippet] = []
    lowered = text.lower()

    for kw_pattern in CRYPTO_KEYWORDS:
        for m in re.finditer(kw_pattern, lowered, flags=re.IGNORECASE):
            start = max(0, m.start() - window)
            end = min(len(text), m.end() + window)
            ctx = text[start:end].strip()
            cat = categorize_context(ctx)

            snippets.append(Snippet(
                category=cat,
                keyword=kw_pattern,
                text=ctx,
                form=filing.form,
                filing_date=filing.filing_date,
                source_doc=source_doc,
                url=source_url
            ))

    # Dedup within doc
    out = []
    seen = set()
    for s in snippets:
        key = (s.category, s.form, s.filing_date, s.source_doc, re.sub(r"\s+", " ", s.text[:200]).lower())
        if key not in seen:
            seen.add(key)
            out.append(s)
    return out

def summarize(snippets: List[Snippet]) -> Dict[str, Any]:
    cats: Dict[str, int] = {}
    for s in snippets:
        cats[s.category] = cats.get(s.category, 0) + 1
    return {"total_snippets": len(snippets), "categories": dict(sorted(cats.items(), key=lambda x: -x[1]))}

def write_outputs(company: Dict[str, Any], filings: List[FilingHit], snippets: List[Snippet], out_prefix: str) -> Tuple[str, str]:
    json_path = f"{out_prefix}.json"
    md_path = f"{out_prefix}.md"

    payload = {
        "company": company,
        "filings": [asdict(f) for f in filings],
        "summary": summarize(snippets),
        "snippets": [asdict(s) for s in snippets],
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    by_cat: Dict[str, List[Snippet]] = {}
    for s in snippets:
        by_cat.setdefault(s.category, []).append(s)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# Crypto Exposure Report — {company.get('title')} ({company.get('ticker')})\n\n")
        f.write(f"- CIK: {company.get('cik_str')}\n")
        f.write(f"- Filings scanned: {len(filings)}\n")
        f.write(f"- Snippets found: {len(snippets)}\n\n")

        f.write("## Category Summary\n\n")
        for cat, count in summarize(snippets)["categories"].items():
            f.write(f"- **{cat}**: {count}\n")
        f.write("\n## Evidence Snippets\n\n")

        for cat, items in sorted(by_cat.items(), key=lambda x: -len(x[1])):
            f.write(f"### {cat}\n\n")
            for s in items[:50]:
                f.write(f"- **{s.form} ({s.filing_date})** — Doc: `{s.source_doc}`\n")
                f.write(f"  - {s.url}\n\n")
                f.write("```text\n")
                f.write(textwrap.fill(s.text, width=110))
                f.write("\n```\n\n")

    return json_path, md_path

def main():
    print("\n=== Crypto Exposure Finder (SEC EDGAR) — Hardened ===")
    print("SEC requires a real User-Agent. Recommended:")
    print('  export SEC_USER_AGENT="Mo mo@email.com"\n')

    with requests.Session() as session:
        tickers_data = load_tickers(session)

        while True:
            query = input("Enter company name, ticker, or CIK: ").strip()
            if not query:
                print("No input. Exiting.")
                return

            # If numeric, treat as CIK
            if query.isdigit():
                company = {"title": "(CIK provided)", "ticker": None, "cik_str": int(query)}
                break

            hits = search_companies(tickers_data, query)
            if not hits:
                print("\nNo matches found. Tips:")
                print("- Try ticker instead of company name")
                print("- Try a shorter name (e.g., 'MicroStrategy' instead of full legal name)")
                print("- Enter CIK directly if you have it")
                continue

            choice = choose_company(hits)
            if not choice:
                print("Exiting.")
                return
            if "__retry__" in choice:
                continue

            company = choice
            break

        cik10 = normalize_cik10(int(company["cik_str"]))
        print(f"\nSelected CIK: {company['cik_str']}")

        forms = ["10-K", "10-Q", "8-K"]
        filings = get_recent_filings(session, cik10, forms=forms, limit=8)
        if not filings:
            print("No recent 10-K/10-Q/8-K filings found.")
            return

        all_snips: List[Snippet] = []

        for i, fil in enumerate(filings, start=1):
            print(f"\n[{i}/{len(filings)}] {fil.form} filed {fil.filing_date} — scanning primary doc + exhibits…")

            # 1) scan primary doc
            try:
                txt = fetch_doc_text(session, fil.filing_url)
                all_snips.extend(extract_snippets(txt, fil, fil.primary_doc, fil.filing_url))
            except Exception as e:
                print(f"  - Primary doc fetch failed: {e}")

            # 2) scan index & all docs
            try:
                idx_html = sec_get(fil.index_url, session).text
                docs = parse_index_for_docs(idx_html)
                for doc_name, href in docs:
                    # href is usually an absolute /Archives/... path
                    doc_url = f"https://www.sec.gov{href}" if href.startswith("/") else href
                    try:
                        dtxt = fetch_doc_text(session, doc_url)
                        sn = extract_snippets(dtxt, fil, doc_name, doc_url)
                        all_snips.extend(sn)
                    except Exception:
                        continue
            except Exception as e:
                print(f"  - Index/exhibit scan failed: {e}")

        # Final dedup
        deduped = []
        seen = set()
        for s in all_snips:
            key = (s.category, s.form, s.filing_date, s.source_doc, re.sub(r"\s+", " ", s.text[:220]).lower())
            if key not in seen:
                seen.add(key)
                deduped.append(s)

        out_prefix = f"crypto_exposure_{(company.get('ticker') or 'CIK')}_{company.get('cik_str')}"
        jp, mp = write_outputs(company, filings, deduped, out_prefix)

        print("\n=== DONE ===")
        print(f"Snippets found: {len(deduped)}")
        print(f"JSON: {jp}")
        print(f"Markdown: {mp}")
        print("\nCategory summary:")
        for cat, cnt in summarize(deduped)["categories"].items():
            print(f"  - {cat}: {cnt}")

if __name__ == "__main__":
    main()
