def validate_caesar_shift(shift):
    return isinstance(shift, int) and 1 <= shift <= 25


def validate_affine_keys(a, b):
    return isinstance(a, int) and isinstance(b, int)
