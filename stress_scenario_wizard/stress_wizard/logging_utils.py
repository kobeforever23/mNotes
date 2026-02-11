from __future__ import annotations

import logging
from pathlib import Path


def setup_logging(log_dir: Path | str = "logs", level: int = logging.INFO) -> None:
    path = Path(log_dir)
    path.mkdir(parents=True, exist_ok=True)
    log_file = path / "stress_wizard.log"

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
