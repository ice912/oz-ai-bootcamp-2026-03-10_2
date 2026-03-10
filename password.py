import bcrypt  # r 추가

def hash_password(plain_password: str) -> str:
    password_hash_bytes: bytes = bcrypt.hashpw(
        plain_password.encode(),
        bcrypt.gensalt(),
    )
    return password_hash_bytes.decode()

def verify_password(plain_password: str, password_hash: str) -> bool:
    try: 
        return bcrypt.checkpw(
            plain_password.encode(), # encdoe -> encode 오타 수정
            password_hash.encode()
        ) 
    except Exception:
        return False # 들여쓰기 추가 (오른쪽으로 4칸)

