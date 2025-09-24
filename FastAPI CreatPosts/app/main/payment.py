# app/payment.py
import base64

# Заглушка проверки оплаты
# В реальной жизни сюда интегрируется Show или другая платежная система
async def is_paid(post_id: str) -> bool:
    # Пока все посты с show_link считаются неоплаченными
    return False

# Шифрование/дешифрование контента
def encrypt_content(content: str) -> str:
    """Простейшее шифрование base64"""
    return base64.b64encode(content.encode("utf-8")).decode("utf-8")

def decrypt_content(content: str) -> str:
    """Дешифрование base64"""
    return base64.b64decode(content.encode("utf-8")).decode("utf-8")