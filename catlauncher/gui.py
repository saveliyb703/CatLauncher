from __future__ import annotations

import os
import tkinter as tk
from tkinter import filedialog, messagebox

from .launcher import LaunchConfig, detect_java, launch_game


class CatLauncherApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("CatLauncher")
        self.geometry("760x620")
        self.minsize(680, 560)
        self.configure(bg="#0b1020")

        self.username_var = tk.StringVar(value=os.environ.get("USERNAME", "Player"))
        self.java_var = tk.StringVar(value=detect_java())
        self.jar_var = tk.StringVar(value="")
        self.game_dir_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), ".minecraft"))
        self.server_var = tk.StringVar(value="")
        self.memory_var = tk.StringVar(value="2048")
        self.width_var = tk.StringVar(value="1280")
        self.height_var = tk.StringVar(value="720")

        self._build_ui()

    def _build_ui(self) -> None:
        shell = tk.Frame(self, bg="#0b1020", padx=20, pady=18)
        shell.pack(fill="both", expand=True)

        header = tk.Frame(shell, bg="#121a2b", padx=22, pady=18)
        header.pack(fill="x")

        tk.Label(header, text="CATLAUNCHER", fg="#f8fafc", bg="#121a2b",
                 font=("Segoe UI", 22, "bold")).pack(anchor="w")
        tk.Label(header, text="Minecraft launcher", fg="#9fb3d1", bg="#121a2b",
                 font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

        body = tk.Frame(shell, bg="#0b1020", pady=18)
        body.pack(fill="both", expand=True)

        left = tk.Frame(body, bg="#121a2b", padx=16, pady=16)
        left.pack(side="left", fill="both", expand=True)

        right = tk.Frame(body, bg="#121a2b", padx=16, pady=16)
        right.pack(side="right", fill="y", padx=(16, 0))

        fields = [
            ("Никнейм", "username", self.username_var),
            ("Java", "java", self.java_var),
            ("Minecraft JAR", "jar", self.jar_var),
            ("Папка игры", "dir", self.game_dir_var),
            ("Сервер", "server", self.server_var),
            ("Память (МБ)", "memory", self.memory_var),
            ("Ширина", "width", self.width_var),
            ("Высота", "height", self.height_var),
        ]

        for label_text, field_name, variable in fields:
            row = tk.Frame(left, bg="#121a2b", pady=8)
            row.pack(fill="x")

            tk.Label(row, text=label_text, width=18, anchor="w", bg="#121a2b", fg="#dfe7ff",
                     font=("Segoe UI", 10, "bold")).pack(side="left")

            entry = tk.Entry(row, textvariable=variable, bg="#0c1628", fg="#f8fafc", bd=0,
                             insertbackground="#f8fafc", highlightthickness=1,
                             highlightbackground="#24314d", highlightcolor="#36d399")
            entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

            if field_name in {"java", "jar", "dir"}:
                btn = tk.Button(row, text="Обзор", command=lambda n=field_name: self._browse(n),
                                bg="#1f5cff", fg="white", bd=0, padx=12, pady=6,
                                font=("Segoe UI", 9, "bold"))
                btn.pack(side="left")

        status = tk.Frame(right, bg="#0d1424", padx=14, pady=14)
        status.pack(fill="both", expand=True)

        tk.Label(status, text="Статус", bg="#0d1424", fg="#8fb8ff",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tk.Label(status, text="Готов к запуску", bg="#0d1424", fg="#8ff7c1",
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(10, 18))

        launch_btn = tk.Button(status, text="ЗАПУСК", command=self._launch,
                               bg="#22c55e", fg="white", bd=0, height=2, width=18,
                               font=("Segoe UI", 12, "bold"))
        launch_btn.pack(fill="x", pady=(8, 10))

        close_btn = tk.Button(status, text="Закрыть", command=self.destroy,
                              bg="#374151", fg="#f3f4f6", bd=0, height=2, width=18,
                              font=("Segoe UI", 10, "bold"))
        close_btn.pack(fill="x")

    def _browse(self, field_name: str) -> None:
        if field_name == "java":
            path = filedialog.askopenfilename(
                title="Выберите Java",
                filetypes=[("Executable", ["java", "java.exe"]), ("All files", "*.*")],
            )
            if path:
                self.java_var.set(path)
        elif field_name == "jar":
            path = filedialog.askopenfilename(
                title="Выберите JAR клиента",
                filetypes=[("Java archive", "*.jar"), ("All files", "*.*")],
            )
            if path:
                self.jar_var.set(path)
        elif field_name == "dir":
            path = filedialog.askdirectory(title="Выберите папку игры")
            if path:
                self.game_dir_var.set(path)

    def _launch(self) -> None:
        try:
            config = LaunchConfig(
                username=self.username_var.get().strip() or "Player",
                java_path=self.java_var.get().strip(),
                game_dir=self.game_dir_var.get().strip() or os.path.join(os.path.expanduser("~"), ".minecraft"),
                minecraft_jar=self.jar_var.get().strip(),
                memory_mb=int(self.memory_var.get() or 2048),
                width=int(self.width_var.get() or 1280),
                height=int(self.height_var.get() or 720),
                server=self.server_var.get().strip(),
            )
            launch_game(config)
            messagebox.showinfo("CatLauncher", "Minecraft запущен.")
        except ValueError as exc:
            messagebox.showerror("Ошибка настройки", str(exc))
        except Exception as exc:  # pragma: no cover - GUI fallback
            messagebox.showerror("Ошибка запуска", f"Не удалось запустить игру: {exc}")


def main() -> None:
    app = CatLauncherApp()
    app.mainloop()
