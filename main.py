import tkinter as tk
from tkinter import ttk, messagebox
from core import load_history, save_history, validate_length, generate_password, add_to_history

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.history = load_history()

        # Длина пароля
        tk.Label(root, text="Длина пароля:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.scale_var = tk.IntVar(value=12)
        scale = tk.Scale(root, from_=4, to=64, orient="horizontal", variable=self.scale_var, length=200)
        scale.grid(row=0, column=1, padx=5, pady=5)

        # Чекбоксы
        self.use_letters = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)

        ttk.Checkbutton(root, text="Буквы", variable=self.use_letters).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Checkbutton(root, text="Цифры", variable=self.use_digits).grid(row=1, column=1, padx=10, pady=5, sticky="w")
        ttk.Checkbutton(root, text="Спецсимволы", variable=self.use_special).grid(row=1, column=2, padx=10, pady=5, sticky="w")

        # Кнопка генерации
        btn_frame = tk.Frame(root)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="Сгенерировать пароль", command=self.on_generate).pack(padx=5)

        # Поле результата
        tk.Label(root, text="Результат:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.entry_result = tk.Entry(root, width=40)
        self.entry_result.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        # Таблица истории (Treeview)
        tk.Label(root, text="История паролей:").grid(row=4, column=0, sticky="w", padx=10, pady=(15, 5))
        tree_frame = tk.Frame(root)
        tree_frame.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)
        root.grid_rowconfigure(5, weight=1)
        root.grid_columnconfigure(1, weight=1)

        columns = ("password", "length", "digits", "letters", "special")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
        self.tree.column("password", width=250)
        self.tree.column("length", width=60)
        self.tree.column("digits", width=60)
        self.tree.column("letters", width=60)
        self.tree.column("special", width=80)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh_tree()

    def on_generate(self):
        length = self.scale_var.get()
        ok, msg = validate_length(length)
        if not ok:
            messagebox.showwarning("Ошибка", msg)
            return

        password = generate_password(
            length,
            self.use_digits.get(),
            self.use_letters.get(),
            self.use_special.get()
        )

        if password is None:
            messagebox.showwarning("Ошибка", "Не выбраны типы символов для генерации.")
            return

        self.entry_result.delete(0, tk.END)
        self.entry_result.insert(0, password)

        add_to_history(self.history, password, length,
                       self.use_digits.get(), self.use_letters.get(), self.use_special.get())
        save_history(self.history)
        self.refresh_tree()

    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        # показываем последние 50 записей
        for entry in reversed(self.history[-50:]):
            self.tree.insert("", "end", values=(
                entry["password"],
                entry["length"],
                str(entry["use_digits"]),
                str(entry["use_letters"]),
                str(entry["use_special"])
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
