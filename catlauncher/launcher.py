from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass
class LaunchConfig:
    username: str = "Player"
    java_path: str = "java"
    game_dir: str = "./.minecraft"
    minecraft_jar: str = ""
    memory_mb: int = 2048
    width: int = 1280
    height: int = 720
    server: str = ""
    extra_args: list[str] = field(default_factory=list)


def detect_java() -> str:
    env_java_home = os.environ.get("JAVA_HOME")
    if env_java_home:
        java_path = Path(env_java_home) / "bin" / ("java.exe" if os.name == "nt" else "java")
        if java_path.exists():
            return str(java_path)

    candidate = shutil.which("java")
    if candidate:
        return candidate

    return "java"


def validate_config(config: LaunchConfig) -> dict[str, str]:
    errors: dict[str, str] = {}

    if not config.username or not config.username.strip():
        errors["username"] = "Имя пользователя не может быть пустым."

    java_path = config.java_path or detect_java()
    if not java_path:
        errors["java_path"] = "Java не найдена. Укажите путь вручную."
    else:
        if not shutil.which(java_path) and not Path(java_path).exists():
            errors["java_path"] = "Указанный путь к Java не существует."

    if not config.minecraft_jar or not config.minecraft_jar.strip():
        errors["minecraft_jar"] = "Необходимо указать путь к jar клиента Minecraft."
    else:
        jar_path = Path(config.minecraft_jar)
        if not jar_path.exists():
            errors["minecraft_jar"] = "Файл клиента Minecraft не найден."

    if config.memory_mb <= 0:
        errors["memory_mb"] = "Объем выделенной памяти должен быть больше нуля."

    game_dir = Path(config.game_dir)
    if not game_dir.exists():
        game_dir.mkdir(parents=True, exist_ok=True)

    if config.width <= 0 or config.height <= 0:
        errors["resolution"] = "Ширина и высота окна должны быть больше нуля."

    return errors


def build_java_command(config: LaunchConfig) -> list[str]:
    java_path = config.java_path or detect_java()
    command = [
        java_path,
        f"-Xmx{config.memory_mb}M",
        "-Xms512M",
        "-Duser.language=en",
        "-Duser.country=US",
        "-jar",
        config.minecraft_jar,
        "--username",
        config.username,
        "--width",
        str(config.width),
        "--height",
        str(config.height),
    ]

    if config.server:
        command.extend(["--server", config.server])

    if config.extra_args:
        command.extend(config.extra_args)

    return command


def launch_game(config: LaunchConfig) -> list[str]:
    errors = validate_config(config)
    if errors:
        raise ValueError("Проверьте настройки запуска: " + "; ".join(errors.values()))

    command = build_java_command(config)
    game_dir = Path(config.game_dir)
    game_dir.mkdir(parents=True, exist_ok=True)

    subprocess.Popen(command, cwd=str(game_dir), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return command
