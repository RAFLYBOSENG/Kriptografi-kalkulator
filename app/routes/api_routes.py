from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__)


# ─────────────────────────────────────────────
#  CAESAR CIPHER
# ─────────────────────────────────────────────


def caesar_encrypt(text: str, shift: int) -> str:
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)


def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, -shift)


# ─────────────────────────────────────────────
#  VIGENÈRE CIPHER
# ─────────────────────────────────────────────


def vigenere_encrypt(text: str, key: str) -> str:
    result = []
    key = key.upper()
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)


def vigenere_decrypt(text: str, key: str) -> str:
    result = []
    key = key.upper()
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base - shift) % 26 + base))
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)


# ─────────────────────────────────────────────
#  AFFINE CIPHER
# ─────────────────────────────────────────────


def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def _mod_inverse(a: int, m: int) -> int:
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"{a} has no inverse mod {m}")


AFFINE_VALID_A = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]


def affine_encrypt(text: str, a: int, b: int) -> str:
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            x = ord(char) - base
            result.append(chr((a * x + b) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)


def affine_decrypt(text: str, a: int, b: int) -> str:
    a_inv = _mod_inverse(a, 26)
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            y = ord(char) - base
            result.append(chr((a_inv * (y - b)) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)


# ─────────────────────────────────────────────
#  HILL CIPHER  (2×2, 3×3, and 6×6)
# ─────────────────────────────────────────────


def _det2(M: list) -> int:
    return M[0][0]*M[1][1] - M[0][1]*M[1][0]


def _det3(M: list) -> int:
    return (
        M[0][0] * (M[1][1]*M[2][2] - M[1][2]*M[2][1])
      - M[0][1] * (M[1][0]*M[2][2] - M[1][2]*M[2][0])
      + M[0][2] * (M[1][0]*M[2][1] - M[1][1]*M[2][0])
    )


def _det6(M: list) -> int:
    """Compute determinant of 6×6 matrix using cofactor expansion."""
    if len(M) != 6 or len(M[0]) != 6:
        raise ValueError("Matrix must be 6×6")
    det = 0
    for j in range(6):
        minor = [[M[i][k] for k in range(6) if k != j] for i in range(1, 6)]
        minor_det = _det5(minor)
        det += ((-1) ** j) * M[0][j] * minor_det
    return det


def _det5(M: list) -> int:
    """Compute determinant of 5×5 matrix using cofactor expansion."""
    det = 0
    for j in range(5):
        minor = [[M[i][k] for k in range(5) if k != j] for i in range(1, 5)]
        minor_det = _det4(minor)
        det += ((-1) ** j) * M[0][j] * minor_det
    return det


def _det4(M: list) -> int:
    """Compute determinant of 4×4 matrix using cofactor expansion."""
    det = 0
    for j in range(4):
        minor = [[M[i][k] for k in range(4) if k != j] for i in range(1, 4)]
        minor_det = _det3(minor)
        det += ((-1) ** j) * M[0][j] * minor_det
    return det


def _mat_inv2_mod26(M: list) -> list:
    det = _det2(M) % 26
    if _gcd(det, 26) != 1:
        raise ValueError(f"Key matrix determinant ({det}) is not invertible mod 26.")
    det_inv = _mod_inverse(det, 26)
    adj = [[M[1][1], -M[0][1]], [-M[1][0], M[0][0]]]
    return [[(det_inv * adj[r][c]) % 26 for c in range(2)] for r in range(2)]


def _mat_inv3_mod26(M: list) -> list:
    det = _det3(M) % 26
    if _gcd(det, 26) != 1:
        raise ValueError(f"Key matrix determinant ({det}) is not invertible mod 26.")
    det_inv = _mod_inverse(det, 26)
    cof = [[0]*3 for _ in range(3)]
    for r in range(3):
        for c in range(3):
            rows = [i for i in range(3) if i != r]
            cols = [j for j in range(3) if j != c]
            minor = [[M[i][j] for j in cols] for i in rows]
            cof[r][c] = ((-1) ** (r + c)) * _det2(minor)
    adj = [[cof[c][r] for c in range(3)] for r in range(3)]
    return [[(det_inv * adj[r][c]) % 26 for c in range(3)] for r in range(3)]


def _mat_inv6_mod26(M: list) -> list:
    """Compute inverse of 6×6 matrix modulo 26 using cofactor method."""
    det = _det6(M) % 26
    if _gcd(det, 26) != 1:
        raise ValueError(f"Key matrix determinant ({det}) is not invertible mod 26.")
    det_inv = _mod_inverse(det, 26)
    cof = [[0]*6 for _ in range(6)]
    for r in range(6):
        for c in range(6):
            rows = [i for i in range(6) if i != r]
            cols = [j for j in range(6) if j != c]
            minor = [[M[i][j] for j in cols] for i in rows]
            minor_det = _det5(minor)
            cof[r][c] = ((-1) ** (r + c)) * minor_det
    adj = [[cof[c][r] for c in range(6)] for r in range(6)]
    return [[(det_inv * adj[r][c]) % 26 for c in range(6)] for r in range(6)]


def _hill_process(text: str, key_matrix: list) -> str:
    n = len(key_matrix)
    letters = [c for c in text.upper() if c.isalpha()]
    while len(letters) % n != 0:
        letters.append('X')
    result = []
    for i in range(0, len(letters), n):
        block = [ord(letters[i + j]) - 65 for j in range(n)]
        for row in range(n):
            val = sum(key_matrix[row][col] * block[col] for col in range(n)) % 26
            result.append(chr(val + 65))
    return ''.join(result)


def hill_encrypt(text: str, key_matrix: list) -> str:
    return _hill_process(text, key_matrix)


def hill_decrypt(text: str, key_matrix: list) -> str:
    n = len(key_matrix)
    if n == 2:
        inv_key = _mat_inv2_mod26(key_matrix)
    elif n == 3:
        inv_key = _mat_inv3_mod26(key_matrix)
    elif n == 6:
        inv_key = _mat_inv6_mod26(key_matrix)
    else:
        raise ValueError("Key matrix size must be 2, 3, or 6")
    return _hill_process(text, inv_key)


# ─────────────────────────────────────────────
#  PLAYFAIR CIPHER
# ─────────────────────────────────────────────


def _build_playfair_table(key: str) -> list:
    seen = set()
    table = []
    for ch in (key.upper() + 'ABCDEFGHIKLMNOPQRSTUVWXYZ'):
        ch = 'I' if ch == 'J' else ch
        if ch.isalpha() and ch not in seen:
            seen.add(ch)
            table.append(ch)
    return [table[i*5:(i+1)*5] for i in range(5)]


def _playfair_pos(table: list, ch: str):
    ch = 'I' if ch == 'J' else ch
    for r, row in enumerate(table):
        if ch in row:
            return r, row.index(ch)
    raise ValueError(f"Character '{ch}' not found in Playfair table")


def _playfair_prepare(text: str) -> list:
    text = text.upper().replace('J', 'I')
    letters = [c for c in text if c.isalpha()]
    digrams = []
    i = 0
    while i < len(letters):
        a = letters[i]
        if i + 1 >= len(letters):
            digrams.append((a, 'X'))
            i += 1
        elif letters[i] == letters[i+1]:
            digrams.append((a, 'X'))
            i += 1
        else:
            digrams.append((a, letters[i+1]))
            i += 2
    return digrams


def playfair_encrypt(text: str, key: str) -> str:
    table = _build_playfair_table(key)
    digrams = _playfair_prepare(text)
    result = []
    for a, b in digrams:
        ra, ca = _playfair_pos(table, a)
        rb, cb = _playfair_pos(table, b)
        if ra == rb:
            result += [table[ra][(ca+1)%5], table[rb][(cb+1)%5]]
        elif ca == cb:
            result += [table[(ra+1)%5][ca], table[(rb+1)%5][cb]]
        else:
            result += [table[ra][cb], table[rb][ca]]
    return ''.join(result)


def playfair_decrypt(text: str, key: str) -> str:
    table = _build_playfair_table(key)
    digrams = _playfair_prepare(text)
    result = []
    for a, b in digrams:
        ra, ca = _playfair_pos(table, a)
        rb, cb = _playfair_pos(table, b)
        if ra == rb:
            result += [table[ra][(ca-1)%5], table[rb][(cb-1)%5]]
        elif ca == cb:
            result += [table[(ra-1)%5][ca], table[(rb-1)%5][cb]]
        else:
            result += [table[ra][cb], table[rb][ca]]
    return ''.join(result)


# ─────────────────────────────────────────────
#  ROUTES (JSON API)
# ─────────────────────────────────────────────


@api_bp.route('/caesar', methods=['POST'])
def caesar_route():
    data = request.get_json() or {}
    text = data.get('text', '')
    mode = data.get('mode', 'encrypt')
    try:
        shift = int(data.get('shift', 0)) % 26
    except (ValueError, TypeError):
        return jsonify({'error': 'Shift must be an integer'}), 400
    if not text:
        return jsonify({'error': 'Please provide text.'}), 400
    result = caesar_encrypt(text, shift) if mode == 'encrypt' else caesar_decrypt(text, shift)
    return jsonify({'result': result, 'mode': mode})


@api_bp.route('/vigenere', methods=['POST'])
def vigenere_route():
    data = request.get_json() or {}
    text = data.get('text', '')
    key = data.get('key', '')
    mode = data.get('mode', 'encrypt')
    if not text:
        return jsonify({'error': 'Please provide text.'}), 400
    if not key or not key.isalpha():
        return jsonify({'error': 'Keyword required (letters only).'}), 400
    result = vigenere_encrypt(text, key) if mode == 'encrypt' else vigenere_decrypt(text, key)
    return jsonify({'result': result, 'mode': mode})


@api_bp.route('/affine', methods=['POST'])
def affine_route():
    data = request.get_json() or {}
    text = data.get('text', '')
    mode = data.get('mode', 'encrypt')
    try:
        a = int(data.get('a', ''))
        b = int(data.get('b', ''))
    except (ValueError, TypeError):
        return jsonify({'error': 'Keys a and b must be integers.'}), 400
    if not text:
        return jsonify({'error': 'Please provide text.'}), 400
    if a not in AFFINE_VALID_A:
        return jsonify({'error': f'Key a must be coprime with 26. Valid values: {AFFINE_VALID_A}'}), 400
    result = affine_encrypt(text, a, b % 26) if mode == 'encrypt' else affine_decrypt(text, a, b % 26)
    return jsonify({'result': result, 'mode': mode})


@api_bp.route('/hill', methods=['POST'])
def hill_route():
    data = request.get_json() or {}
    text = data.get('text', '')
    mode = data.get('mode', 'encrypt')
    size = int(data.get('size', 2))
    key_flat = data.get('key_matrix', [])
    if size not in (2, 3, 6):
        return jsonify({'error': 'Matrix size must be 2, 3, or 6.'}), 400
    expected = size * size
    if not text:
        return jsonify({'error': 'Please provide text.'}), 400
    if len(key_flat) != expected:
        return jsonify({'error': f'Key matrix must have exactly {expected} values.'}), 400
    try:
        key_flat = [int(v) % 26 for v in key_flat]
    except (ValueError, TypeError):
        return jsonify({'error': 'All matrix values must be integers.'}), 400
    key_matrix = [[key_flat[r * size + c] for c in range(size)] for r in range(size)]
    
    if size == 2:
        det = _det2(key_matrix) % 26
    elif size == 3:
        det = _det3(key_matrix) % 26
    else:  # size == 6
        det = _det6(key_matrix) % 26
    
    if _gcd(det, 26) != 1:
        return jsonify({'error': f'Matrix determinant ({det}) must be coprime with 26.'}), 400
    letters_only = [c for c in text.upper() if c.isalpha()]
    if not letters_only:
        return jsonify({'error': 'Input must contain at least one letter.'}), 400
    result = hill_encrypt(text, key_matrix) if mode == 'encrypt' else hill_decrypt(text, key_matrix)
    return jsonify({'result': result, 'mode': mode, 'size': size})


@api_bp.route('/playfair', methods=['POST'])
def playfair_route():
    data = request.get_json() or {}
    text = data.get('text', '')
    key = data.get('key', '')
    mode = data.get('mode', 'encrypt')
    if not text:
        return jsonify({'error': 'Please provide text.'}), 400
    if not key or not key.isalpha():
        return jsonify({'error': 'Keyword required (letters only).'}), 400
    letters_only = [c for c in text.upper() if c.isalpha()]
    if not letters_only:
        return jsonify({'error': 'Input must contain at least one letter.'}), 400
    result = playfair_encrypt(text, key) if mode == 'encrypt' else playfair_decrypt(text, key)
    return jsonify({'result': result, 'mode': mode})
