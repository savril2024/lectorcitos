import sys
import os
from pathlib import Path

# Raíz del repo en Streamlit Cloud: /mount/src/lectorcitos
root = Path(__file__).resolve().parent

# Agregar todas las rutas necesarias
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "app"))
sys.path.insert(0, str(root / "src"))
sys.path.insert(0, str(root / "src" / "app"))

# Forzar __file__ correcto para que main_page.py calcule bien project_root
os.chdir(str(root))

# Compilar y ejecutar con __file__ correcto
main_page = root / "src" / "app" / "pages" / "main_page.py"
with open(main_page) as f:
    code = compile(f.read(), str(main_page), "exec")

exec(code, {"__file__": str(main_page), "__name__": "__main__"})