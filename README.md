# CatLauncher

Простой Minecraft launcher-проект на Python.

## Возможности
- запуск клиента Minecraft из выбранного JAR файла;
- выбор Java, папки игры и никнейма;
- настройка памяти, разрешения окна и сервера;
- простой графический интерфейс на Tkinter.

## Установка через свой installer

```bash
cd /workspaces/CatLauncher
python installer.py --target C:\\CatLauncher
```

Это Windows-версия установщика. Он создаёт папку с готовой точкой запуска `run_catlauncher.bat`.

После запуска в целевой папке появятся:
- `run_catlauncher.bat` для Windows;
- `run_catlauncher.py` для запуска из Python.

## Запуск

```bash
cd /workspaces/CatLauncher
python -m catlauncher
```

## Тесты

```bash
cd /workspaces/CatLauncher
pytest -q
```

## Примечание

Это базовый launcher для локального запуска клиента. Для полноценной установки Minecraft-версий и модов потребуется отдельный механизм загрузки ресурсов и библиотеки вроде minecraft-launcher-lib.
