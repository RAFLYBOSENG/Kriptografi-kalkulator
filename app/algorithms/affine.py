from typing import Dict, List


def _egcd(a: int, b: int):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = _egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def _modinv(a: int, m: int):
    g, x, _ = _egcd(a, m)
    if g != 1:
        return None
    return x % m


def encrypt(text: str, a: int, b: int) -> Dict[str, object]:
    steps: List[str] = []
    steps.append(f"E(x) = (a*x + b) mod 26, a={a}, b={b}")
    out: List[str] = []
    for i, ch in enumerate(text):
        if ch.isalpha():
            base = 'A' if ch.isupper() else 'a'
            x = ord(ch) - ord(base)
            c_val = (a * x + b) % 26
            c = chr(c_val + ord(base))
            out.append(c)
            steps.append(f"{i}: '{ch}' x={x} -> c={c_val} -> '{c}'")
        else:
            out.append(ch)
            steps.append(f"{i}: '{ch}' (non-alpha) kept")
    return {"result": ''.join(out), "steps": steps}


def decrypt(text: str, a: int, b: int) -> Dict[str, object]:
    steps: List[str] = []
    inv = _modinv(a, 26)
    if inv is None:
        raise ValueError("a is not invertible modulo 26")
    steps.append(f"D(c) = a_inv*(c - b) mod 26, a_inv={inv}, b={b}")
    out: List[str] = []
    for i, ch in enumerate(text):
        if ch.isalpha():
            base = 'A' if ch.isupper() else 'a'
            y = ord(ch) - ord(base)
            p = (inv * (y - b)) % 26
            plain = chr(p + ord(base))
            out.append(plain)
            steps.append(f"{i}: '{ch}' y={y} -> p={p} -> '{plain}'")
        else:
            out.append(ch)
            steps.append(f"{i}: '{ch}' (non-alpha) kept")
    return {"result": ''.join(out), "steps": steps}
