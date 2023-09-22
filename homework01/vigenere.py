def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
 
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    j = 0
    i = 0
    n_t, n_k = len(plaintext), len(keyword)
    while i < n_t:

        if j >= n_k:
            j = 0

        code = ord(keyword[j])
        if code >= ord("A") and code <= ord("Z"):
            shift = code - ord("A")
        elif code >= ord("a") and code <= ord("z"):
            shift = code - ord("a")
        else:
            shift = 0
        
        code_mod = ord(plaintext[i]) + shift
        if (code_mod>= ord("A") + shift and code_mod<= ord("Z") + shift) or (
            code_mod>= ord("a") + shift and code_mod<= ord("z") + shift
        ):
            if (code_mod>= ord("Z") + 1 and code_mod<= ord("Z") + shift) or (
                code_mod>= ord("z") + 1 and code_mod<= ord("z") + shift
            ):
                code_mod -= 26
                ciphertext += chr(code_mod)
            else:
                ciphertext += chr(code_mod)
        else:
            ciphertext += plaintext[i]
        
        j += 1
        i += 1

    return ciphertext
 
 
def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
 
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    j = 0
    i = 0
    n_t, n_k = len(ciphertext), len(keyword)
    while i < (len(ciphertext)):
 
        if j >= n_k:
            j = 0

        code = ord(keyword[j])
        if code >= ord("A") and code <= ord("Z"):
            shift = code - ord("A")
        elif code >= ord("a") and code <= ord("z"):
            shift = code - ord("a")
        else:
            shift = 0
        code_mod= ord(ciphertext[i]) - shift
        if (code_mod>= ord("A") - shift and code_mod<= ord("Z") - shift) or (
            code_mod>= ord("a") - shift and code_mod<= ord("z") - shift
        ):
            if (code_mod>= ord("A") - shift and code_mod<= ord("A") - 1) or (
                code_mod>= ord("a") - shift and code_mod<= ord("a") - 1
            ):
                code_mod+= 26
                plaintext += chr(code_mod)
            else:
                plaintext += chr(code_mod)
        else:
            plaintext += ciphertext[i]
        
        j += 1
        i += 1

    return plaintext