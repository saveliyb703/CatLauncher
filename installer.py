from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent


def find_system_python() -> str | None:
    for candidate in ("python", "py"):
        binary = shutil.which(candidate)
        if binary:
            return binary
    return None


def build_install_dir(target: Path) -> Path:
    target.mkdir(parents=True, exist_ok=True)
    return target


def copy_project(target: Path) -> None:
    for item in ("catlauncher", "README.md", "pytest.ini"):
        src = PROJECT_ROOT / item
        if src.is_dir():
            shutil.copytree(src, target / item, dirs_exist_ok=True)
        elif src.exists():
            shutil.copy2(src, target / item)


def write_launcher_scripts(target: Path, python_bin: str | None) -> None:
    run_py = target / "run_catlauncher.py"
    run_py.write_text(
        "from catlauncher.gui import main\n\n\nif __name__ == '__main__':\n    main()\n",
        encoding="utf-8",
    )

    bat_python = python_bin or "python"
    run_bat = target / "run_catlauncher.bat"
    run_bat.write_text(
        "@echo off\r\n"
        "cd /d \"%~dp0\"\r\n"
        f"\"{bat_python}\" run_catlauncher.py\r\n",
        encoding="utf-8",
    )


def write_installer_info(target: Path, python_bin: str | None) -> None:
    info = target / "INSTALL.txt"
    info.write_text(
        "CatLauncher custom installer for Windows\n\n"
        "1. Запустите run_catlauncher.bat\n"
        "2. Если Python не найден, установите Python 3.11+\n\n"
        f"Используемый Python: {python_bin or 'не найден'}\n\n"
        "Для ручного запуска:\n"
        "python run_catlauncher.py\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Windows installer for CatLauncher")
    parser.add_argument(
        "--target",
        type=Path,
        default=PROJECT_ROOT / "install",
        help="Папка для установки",
    )
    args = parser.parse_args()

    target = args.target.resolve()
    build_install_dir(target)
    copy_project(target)
    python_bin = find_system_python()
    write_launcher_scripts(target, python_bin)
    write_installer_info(target, python_bin)

    print(f"CatLauncher установлен в: {target}")
    print("Запуск: run_catlauncher.bat")
    if python_bin:
        print(f"Используется Python: {python_bin}")
    else:
        print("Python не найден. Установите Python 3.11+ и запустите run_catlauncher.bat")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
