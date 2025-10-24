import sys
import os


def resource_path(relative_path):
    """Возвращает абсолютный путь к ресурсу, работает как в режиме разработки, так и для скомпилированного приложения."""
    if hasattr(sys, "_MEIPASS"):
        # Если запущено скомпилированное приложение PyInstaller
        base_path = os.path.dirname(sys.executable)
    else:
        # В режиме разработки (обычный запуск python main.py)
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
