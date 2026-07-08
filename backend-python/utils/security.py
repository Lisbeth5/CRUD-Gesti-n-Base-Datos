import bcrypt


# bcrypt evita almacenar contrasenas en texto plano y agrega sal automaticamente.
MAX_BCRYPT_BYTES = 72


def generar_password_hash(password: str) -> str:
    """Genera un hash seguro para guardar la contrasena."""
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > MAX_BCRYPT_BYTES:
        raise ValueError("La contrasena no puede superar 72 bytes para bcrypt.")

    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def verificar_password(password: str, password_hash: str) -> bool:
    """Valida una contrasena contra su hash almacenado."""
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > MAX_BCRYPT_BYTES:
        return False

    return bcrypt.checkpw(password_bytes, password_hash.encode("utf-8"))
