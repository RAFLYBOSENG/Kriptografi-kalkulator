from typing import Dict, List


def _shift_char(c: str, shift: int) -> str:
    if c.isalpha():
        base = 'A' if c.isupper() else 'a'
        return chr((ord(c) - ord(base) + shift) % 26 + ord(base))
    return c


def encrypt(text: str, shift: int) -> Dict[str, object]:
    steps: List[str] = []
    steps.append(f"Shift = {shift}")
    out_chars: List[str] = []
    for i, ch in enumerate(text):
        shifted = _shift_char(ch, shift)
        out_chars.append(shifted)
        steps.append(f"{i}: '{ch}' -> '{shifted}'")
    result = ''.join(out_chars)
    return {"result": result, "steps": steps}


def decrypt(text: str, shift: int) -> Dict[str, object]:
    steps: List[str] = []
    steps.append(f"Shift = {shift} (decrypt uses -shift)")
    out_chars: List[str] = []
    for i, ch in enumerate(text):
        shifted = _shift_char(ch, -shift)
        out_chars.append(shifted)
        steps.append(f"{i}: '{ch}' -> '{shifted}'")
    result = ''.join(out_chars)
    return {"result": result, "steps": steps}
