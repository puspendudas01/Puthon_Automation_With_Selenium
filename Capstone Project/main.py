"""Entry point: `python main.py` runs the whole suite and writes reports/ (HTML, XML, log, screenshots).

Optional flags are passed straight to pytest, e.g.:
    python main.py -k "Blue Top"
"""
import sys
import pytest

if __name__ == "__main__":
    sys.exit(pytest.main(sys.argv[1:]))
