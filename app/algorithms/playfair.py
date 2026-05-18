from typing import Dict, List, Tuple


def _generate_table(keyword: str) -> Tuple[List[List[str]], dict]:
    # Use I/J combined: replace J with I
    seen = []
    table = []
    key = ''.join([c.upper() for c in keyword if c.isalpha()])
    for ch in key:
        ch = 'I' if ch == 'J' else ch
        if ch not in seen:
            seen.append(ch)
    for c in range(ord('A'), ord('Z') + 1):
        ch = chr(c)
        if ch == 'J':
            continue
        if ch not in seen:
            seen.append(ch)
    matrix = [seen[i:i + 5] for i in range(0, 25, 5)]
    pos = {matrix[r][c]: (r, c) for r in range(5) for c in range(5)}
    return matrix, pos


def _prepare_text(text: str) -> List[str]:
    s = ''.join([c.upper() for c in text if c.isalpha()])
    s = s.replace('J', 'I')
    pairs: List[str] = []
    i = 0
    while i < len(s):
        a = s[i]
        b = ''
        if i + 1 < len(s):
            b = s[i + 1]
        if b == '':
            pairs.append(a + 'X')
            i += 1
        elif a == b:
            pairs.append(a + 'X')
            i += 1
        else:
            pairs.append(a + b)
            i += 2
    return pairs


def encrypt(text: str, keyword: str) -> Dict[str, object]:
    steps: List[str] = []
    table, pos = _generate_table(keyword)
    steps.append(f"5x5 Table generated from keyword '{keyword}'")
    pairs = _prepare_text(text)
    steps.append(f"Prepared digraphs: {pairs}")
    out = []
    for p in pairs:
        a, b = p[0], p[1]
        ra, ca = pos[a]
        rb, cb = pos[b]
        if ra == rb:
            # same row
            ca2 = (ca + 1) % 5
            cb2 = (cb + 1) % 5
            ra2, rb2 = ra, rb
        elif ca == cb:
            # same column
            ra2 = (ra + 1) % 5
            rb2 = (rb + 1) % 5
            ca2, cb2 = ca, cb
        else:
            ra2, ca2 = ra, cb
            rb2, cb2 = rb, ca
        ca_char = table[ra2][ca2]
        cb_char = table[rb2][cb2]
        steps.append(f"Pair {p}: positions ({ra},{ca})({rb},{cb}) -> ({ra2},{ca2})({rb2},{cb2}) -> {ca_char}{cb_char}")
        out.append(ca_char + cb_char)
    result = ''.join(out)
    return {"result": result, "steps": steps, "table": table}


def decrypt(text: str, keyword: str) -> Dict[str, object]:
    steps: List[str] = []
    table, pos = _generate_table(keyword)
    steps.append(f"5x5 Table generated from keyword '{keyword}'")
    s = ''.join([c.upper() for c in text if c.isalpha()])
    pairs = [s[i:i + 2] for i in range(0, len(s), 2)]
    steps.append(f"Digraphs to decrypt: {pairs}")
    out = []
    for p in pairs:
        a, b = p[0], p[1]
        ra, ca = pos[a]
        rb, cb = pos[b]
        if ra == rb:
            ca2 = (ca - 1) % 5
            cb2 = (cb - 1) % 5
            ra2, rb2 = ra, rb
        elif ca == cb:
            ra2 = (ra - 1) % 5
            rb2 = (rb - 1) % 5
            ca2, cb2 = ca, cb
        else:
            ra2, ca2 = ra, cb
            rb2, cb2 = rb, ca
        ca_char = table[ra2][ca2]
        cb_char = table[rb2][cb2]
        steps.append(f"Pair {p}: positions ({ra},{ca})({rb},{cb}) -> ({ra2},{ca2})({rb2},{cb2}) -> {ca_char}{cb_char}")
        out.append(ca_char + cb_char)
    result = ''.join(out)
    return {"result": result, "steps": steps, "table": table}
