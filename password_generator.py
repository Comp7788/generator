import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

# --- Настройки ---
HISTORY_FILE = "history.json"
MIN_LENGTH = 4
MAX_LENGTH = 32

# --- Функции ---
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def generate_password(length, use_digits, use_letters, use_special):
    chars = ''
    if use_letters: chars += string.ascii_letters
    if use_digits: chars += string.digits
    if use_special: chars += string.punctuation
    if not chars:
        return ''
    return ''.join(random.choices(chars, k=length))

def on_generate():
    length = int(scale_length.get())
    use_digits = var_digits.get()
    use_letters = var_letters.get()
    use_special = var_special.get()

    if not (use_digits or use_letters or use_special):
        messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов!")
        return

    password = generate_password(length, use_digits, use_letters, use_special)
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)

    # Добавляем в историю
    history.append({
        "password": password,
        "length": length,
        "digits": use_digits,
        "letters": use_letters,
        "special": use_special
    })
    save_history(history)
    update_history_table()

def update_history_table():
    for i in tree_history.get_children():
        tree_history.delete(i)
    for item in history:
        tree_history.insert('', 'end', values=(
            item["password"],
            item["length"],
            "✓" if item["digits"] else "✗",
            "✓" if item["letters"] else "✗",
            "✓" if item["special"] else "✗"
        ))

# --- Основное окно ---
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("600x450")
root.resizable(False, False)

# Загрузка истории
history = load_history()

# --- Виджеты ---
frame_settings = tk.LabelFrame(root, text="Настройки", padx=10, pady=10)
frame_settings.pack(pady=10, padx=10, fill="x")

tk.Label(frame_settings, text="Длина пароля:").grid(row=0, column=0, sticky="w")
scale_length = tk.Scale(frame_settings, from_=MIN_LENGTH, to=MAX_LENGTH, orient=tk.HORIZONTAL)
scale_length.set(12)
scale_length.grid(row=0, column=1, columnspan=2, sticky="we")

var_digits = tk.BooleanVar(value=True)
var_letters = tk.BooleanVar(value=True)
var_special = tk.BooleanVar(value=True)

tk.Checkbutton(frame_settings, text="Цифры", variable=var_digits).grid(row=1, column=0, sticky="w")
tk.Checkbutton(frame_settings, text="Буквы", variable=var_letters).grid(row=1, column=1, sticky="w")
tk.Checkbutton(frame_settings, text="Спецсимволы", variable=var_special).grid(row=1, column=2, sticky="w")

btn_generate = tk.Button(root, text="Сгенерировать", command=on_generate)
btn_generate.pack(pady=5)

frame_password = tk.Frame(root)
frame_password.pack(pady=10)

tk.Label(frame_password, text="Ваш пароль:").pack(side="left")
entry_password = tk.Entry(frame_password, width=40)
entry_password.pack(side="left", padx=5)

# Таблица истории
frame_history = tk.LabelFrame(root, text="История", padx=5, pady=5)
frame_history.pack(padx=10, pady=10, fill="both", expand=True)

columns = ("Пароль", "Длина", "Цифры", "Буквы", "Спецсимволы")
tree_history = ttk.Treeview(frame_history, columns=columns, show="headings")
for col in columns:
    tree_history.heading(col, text=col)
tree_history.column("Пароль", width=200)
tree_history.column("Длина", width=50)
tree_history.column("Цифры", width=50)
tree_history.column("Буквы", width=50)
tree_history.column("Спецсимволы", width=80)
tree_history.pack(fill="both", expand=True)

# Заполнение таблицы истории при запуске
update_history_table()

# --- Запуск ---
root.mainloop()