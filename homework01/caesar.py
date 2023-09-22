import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    alph = ""
    alphabet1, alphabet2 = "abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    n = len(alphabet1)
    
    for i in plaintext:
        if i in alphabet1:
            pos = alphabet1.find(i)
            if 0 <= pos + shift < n:
                ciphertext += (alphabet1[pos + shift])
            else:
                ciphertext += (alphabet1[(pos + shift) % n])
        elif i in alphabet2:
            pos = alphabet2.find(i)
            if 0 <= pos + shift < n:
                ciphertext += (alphabet2[pos + shift])
            else:
                ciphertext += (alphabet2[(pos + shift) % n])
        else:
            ciphertext += (i)
            
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    alph = ""
    alphabet1, alphabet2 = "abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    n = len(alphabet1)
    
    for i in ciphertext:
        if i in alphabet1:
            pos = alphabet1.find(i)
            if 0 <= pos - shift < n:
                plaintext += (alphabet1[pos - shift])
            else:
                plaintext += (alphabet1[(pos - shift) % n])
        elif i in alphabet2:
            pos = alphabet2.find(i)
            if 0 <= pos - shift < n:
                plaintext += (alphabet2[pos - shift])
            else:
                plaintext += (alphabet2[(pos - shift) % n])
        else:
            plaintext += (i)
    
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
