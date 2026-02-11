from __future__ import annotations

from dataclasses import dataclass
import difflib


@dataclass(slots=True)
class MappingSuggestion:
    source: str
    target: str
    confidence: float
    reason: str


REQUIRED_FIELDS = {
    "positions": [
        "instrument_id",
        "asset_class",
        "sub_asset_class",
        "desk",
        "book",
        "notional",
        "direction",
        "maturity",
        "currency",
    ],
    "sensitivities": [
        "instrument_id",
        "delta",
        "gamma",
        "vega",
        "rho",
        "cs01",
        "dv01",
        "theta",
        "convexity",
    ],
    "market_data": ["driver_id", "asset_class", "level", "as_of"],
    "risk_drivers": ["driver_id", "name", "asset_class", "geography", "tenor", "sector"],
}


SYNONYMS = {
    "instrument_id": ["instrument", "trade_id", "position_id", "id"],
    "asset_class": ["asset", "class", "assetclass"],
    "sub_asset_class": ["subasset", "sub_class", "sub asset"],
    "desk": ["trading_desk", "desk_name"],
    "book": ["book_name", "portfolio"],
    "notional": ["quantity", "position_size", "notional_amt", "nominal"],
    "direction": ["side", "long_short", "position_direction"],
    "maturity": ["expiry", "maturity_date"],
    "currency": ["ccy", "curr"],
    "delta": ["d1"],
    "gamma": ["g2"],
    "vega": ["v1"],
    "rho": ["r1"],
    "cs01": ["credit_sens", "spread_sens"],
    "dv01": ["rate_sens"],
    "theta": ["time_decay"],
    "convexity": ["convex"],
    "driver_id": ["risk_driver_id", "factor_id"],
    "name": ["driver_name", "factor_name"],
    "geography": ["region", "country"],
    "tenor": ["bucket", "maturity_bucket"],
    "sector": ["industry"],
    "level": ["price", "value", "spot"],
    "as_of": ["asof", "timestamp", "date"],
}


def _normalize(text: str) -> str:
    return text.lower().replace(" ", "_").replace("-", "_")


def suggest_mappings(source_columns: list[str], category: str) -> list[MappingSuggestion]:
    targets = REQUIRED_FIELDS.get(category, [])
    suggestions: list[MappingSuggestion] = []
    normalized = {_normalize(col): col for col in source_columns}

    for target in targets:
        best_score = 0.0
        best_source = None
        target_candidates = [target] + SYNONYMS.get(target, [])

        for source_norm, source_original in normalized.items():
            for candidate in target_candidates:
                score = difflib.SequenceMatcher(None, source_norm, _normalize(candidate)).ratio()
                if score > best_score:
                    best_score = score
                    best_source = source_original

        if best_source and best_score >= 0.55:
            reason = "exact/near name match" if best_score > 0.8 else "synonym fuzzy match"
            suggestions.append(
                MappingSuggestion(
                    source=best_source,
                    target=target,
                    confidence=round(best_score, 2),
                    reason=reason,
                )
            )

    return suggestions
