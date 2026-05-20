import sys
from pathlib import Path

root = Path(__file__).resolve().parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "app"))
sys.path.insert(0, str(root / "src"))

# Ejecutar main_page directamente
exec(open(root / "src" / "app" / "pages" / "main_page.py").read())