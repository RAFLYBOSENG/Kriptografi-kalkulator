from typing import Dict, List


def _extend_key(text: str, keyword: str) -> List[int]:
    key_nums = []
    k = 0
    for c in text:
        if c.isalpha():
            key_nums.append(ord(keyword[k % len(keyword)].lower()) - ord('a'))
            k += 1
        else:
            key_nums.append(None)
    return key_nums


def encrypt(text: str, keyword: str) -> Dict[str, object]:
    steps: List[str] = []
    if not keyword:
        raise ValueError("Keyword required")
    key_nums = _extend_key(text, keyword)
    out_chars: List[str] = []
    steps.append(f"Keyword: {keyword}")
    for i, c in enumerate(text):
        k = key_nums[i]
        if k is None:
            out_chars.append(c)
            steps.append(f"{i}: '{c}' (non-alpha) kept")
            continue
        base = 'A' if c.isupper() else 'a'
        p = ord(c) - ord(base)
        ciph = chr((p + k) % 26 + ord(base))
        out_chars.append(ciph)
        steps.append(f"{i}: '{c}' (p={p}) + k={k} -> '{ciph}'")
    return {"result": ''.join(out_chars), "steps": steps}


def decrypt(text: str, keyword: str) -> Dict[str, object]:
    steps: List[str] = []
    if not keyword:
        raise ValueError("Keyword required")
    key_nums = _extend_key(text, keyword)
    out_chars: List[str] = []
    steps.append(f"Keyword: {keyword}")
    for i, c in enumerate(text):
        k = key_nums[i]
        if k is None:
            out_chars.append(c)
            steps.append(f"{i}: '{c}' (non-alpha) kept")
            continue
        base = 'A' if c.isupper() else 'a'
        ci = ord(c) - ord(base)
        p = (ci - k) % 26
        plain = chr(p + ord(base))
        out_chars.append(plain)
        steps.append(f"{i}: '{c}' (ci={ci}) - k={k} -> '{plain}'")
    return {"result": ''.join(out_chars), "steps": steps}
