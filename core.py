import random
import json
import os
from typing import List, Dict, Optional

HISTORY_FILE = "passwords_history.json"

def load_history() -> List[Dict]:
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, IOError):
        return []

def save_history(history: List[Dict]) -> bool:
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False

def validate_length(length: int, min_len: int = 4, max_len: int = 64) -> tuple[bool, str]:
    if length < min_len:
        return False, f"Длина пароля должна быть не менее {min_len} символов."
    if length > max_len:
        return False, f"Длина пароля должна быть не более {max_len} символов."
    return True, ""

def generate_password(length: int, use_digits: bool, use_letters: bool, use_special: bool) -> Optional[str]:
    chars = ""
    if use_letters:
        chars += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if use_digits:
        chars += "0123456789"
    if use_special:
        chars += "!@#$%^&*()-_=+[]{};:,.<>?"

    if not chars:
        return None  # ничего не выбрано

    return "".join(random.choice(chars) for _ in range(length))

def add_to_history(history: List[Dict], password: str, length: int,
                   use_digits: bool, use_letters: bool, use_special: bool) -> None:
    entry = {
        "password": password,
        "length": length,
        "use_digits": use_digits,
        "use_letters": use_letters,
        "use_special": use_special,
    }
    history.append(entry)
    # храним только последние 200 записей
    if len(history) > 200:
        history[:] = history[-200:]
