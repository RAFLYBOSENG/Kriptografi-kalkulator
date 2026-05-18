from typing import Dict, List


def _chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def _mod_inv(a, m=26):
    # Extended gcd
    t0, t1 = 0, 1
    r0, r1 = m, a
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        t0, t1 = t1, t0 - q * t1
    if r0 != 1:
        return None
    return t0 % m


def _matrix_mul(A, v):
    n = len(A)
    res = [0] * n
    for i in range(n):
        s = 0
        for j in range(n):
            s += A[i][j] * v[j]
        res[i] = s % 26
    return res


def _matrix_det(A):
    # compute determinant using recursive expansion (sufficient for small n)
    n = len(A)
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    det = 0
    for c in range(n):
        # build submatrix
        sub = [row[:c] + row[c + 1:] for row in (A[1:])]
        cofactor = ((-1) ** c) * A[0][c] * _matrix_det(sub)
        det += cofactor
    return det


def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


def _matrix_minor(A, i, j):
    sub = [row[:j] + row[j + 1:] for k, row in enumerate(A) if k != i]
    return _matrix_det(sub)


def _matrix_inverse_mod(A, mod=26):
    n = len(A)
    det = _matrix_det(A) % mod
    inv_det = _mod_inv(det, mod)
    if inv_det is None:
        return None
    # adjugate
    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            m = _matrix_minor(A, i, j)
            adj[j][i] = ((-1) ** (i + j) * m) % mod
    # multiply by inv_det
    inv = [[(adj[i][j] * inv_det) % mod for j in range(n)] for i in range(n)]
    return inv


def encrypt(text: str, key_matrix) -> Dict[str, object]:
    steps: List[str] = []
    n = len(key_matrix)
    steps.append(f"Using key matrix {n}x{n}")
    # prepare text: only letters used, keep case by mapping then reapply
    letters = [c for c in text if c.isalpha()]
    # pad with 'X'
    while len(letters) % n != 0:
        letters.append('X')
    out_letters: List[str] = []
    idx = 0
    for block in _chunks(letters, n):
        vec = [ord(c.upper()) - ord('A') for c in block]
        steps.append(f"Block {idx}: {block} -> nums {vec}")
        # detailed multiplication per row
        prod = []
        mult_details = []
        for i in range(n):
            row = key_matrix[i]
            terms = [f"{row[j]}*{vec[j]}" for j in range(n)]
            total = sum(row[j] * vec[j] for j in range(n))
            val_mod = total % 26
            prod.append(val_mod)
            mult_details.append(f"row{i}: ({' + '.join(terms)}) = {total} -> {val_mod}")
        steps.append(f"Multiply -> {prod}")
        for d in mult_details:
            steps.append(d)
        out = ''.join(chr(v + ord('A')) for v in prod)
        out_letters.extend(out)
        idx += 1
    # Merge non-letters from original text by replacing sequentially
    res_chars = list(text)
    letter_iter = iter(out_letters)
    for i, ch in enumerate(res_chars):
        if ch.isalpha():
            out_ch = next(letter_iter)
            # preserve case
            res_chars[i] = out_ch if ch.isupper() else out_ch.lower()
    # compute determinant and invertibility info
    det = _matrix_det(key_matrix)
    det_mod = det % 26
    invertible = _gcd(det_mod, 26) == 1
    inv_matrix = None
    if invertible:
        inv_matrix = _matrix_inverse_mod(key_matrix, 26)

    return {
        "result": ''.join(res_chars),
        "steps": steps,
        "matrix": key_matrix,
        "determinant": det,
        "det_mod26": det_mod,
        "invertible": invertible,
        "inverse": inv_matrix,
    }


def decrypt(text: str, key_matrix) -> Dict[str, object]:
    steps: List[str] = []
    n = len(key_matrix)
    steps.append(f"Using key matrix {n}x{n}")
    det = _matrix_det(key_matrix)
    det_mod = det % 26
    if _gcd(det_mod, 26) != 1:
        raise ValueError(f"det(K)={det} (mod26={det_mod}) not invertible modulo 26")
    inv = _matrix_inverse_mod(key_matrix, 26)
    steps.append(f"Inverse matrix mod26 computed")
    letters = [c for c in text if c.isalpha()]
    out_letters: List[str] = []
    idx = 0
    for block in _chunks(letters, n):
        vec = [ord(c.upper()) - ord('A') for c in block]
        steps.append(f"Block {idx}: {block} -> nums {vec}")
        # detailed multiplication with inverse
        prod = []
        mult_details = []
        for i in range(n):
            row = inv[i]
            terms = [f"{row[j]}*{vec[j]}" for j in range(n)]
            total = sum(row[j] * vec[j] for j in range(n))
            val_mod = total % 26
            prod.append(val_mod)
            mult_details.append(f"row{i}: ({' + '.join(terms)}) = {total} -> {val_mod}")
        steps.append(f"Multiply by inverse -> {prod}")
        for d in mult_details:
            steps.append(d)
        out = ''.join(chr(v + ord('A')) for v in prod)
        out_letters.extend(out)
        idx += 1
    res_chars = list(text)
    letter_iter = iter(out_letters)
    for i, ch in enumerate(res_chars):
        if ch.isalpha():
            out_ch = next(letter_iter)
            res_chars[i] = out_ch if ch.isupper() else out_ch.lower()
    return {
        "result": ''.join(res_chars),
        "steps": steps,
        "matrix": key_matrix,
        "determinant": det,
        "det_mod26": det_mod,
        "inverse": inv,
    }
