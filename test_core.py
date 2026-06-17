import pytest
from core import validate_length, generate_password, add_to_history

def test_validate_length_ok():
    assert validate_length(8)[0] is True

def test_validate_length_too_short():
    ok, msg = validate_length(3)
    assert ok is False
    assert "не менее" in msg

def test_validate_length_too_long():
    ok, msg = validate_length(65)
    assert ok is False
    assert "не более" in msg

def test_generate_password_all_types():
    pwd = generate_password(12, True, True, True)
    assert pwd is not None
    assert len(pwd) == 12

def test_generate_password_no_types():
    pwd = generate_password(12, False, False, False)
    assert pwd is None

def test_add_to_history_limit():
    history = []
    for i in range(210):
        add_to_history(history, f"pwd{i}", 10, True, True, True)
    assert len(history) == 200
