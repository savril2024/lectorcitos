import sys
from pathlib import Path

root = Path(__file__).resolve().parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "app"))
sys.path.insert(0, str(root / "src"))

from src.app.pages.main_page import *