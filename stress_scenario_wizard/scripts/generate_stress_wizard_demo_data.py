from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from stress_wizard.data.demo_data import write_demo_files


if __name__ == "__main__":
    out = write_demo_files(PROJECT_ROOT / "demo_data")
    print("Generated files:")
    for path in out:
        print(path)
