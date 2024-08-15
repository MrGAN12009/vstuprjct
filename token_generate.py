import jwt

# Секретный ключ для подписи токенов
SECRET_KEY = 'piska_mamonta_ebiot_tvoyu_mamu'

def create_token(user_id):
    # Определение полезной нагрузки токена
    payload = {'user_id': user_id}
    # Создание токена
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    try:
        # Расшифровка токена
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # Токен истёк
        return None
    except jwt.InvalidTokenError:
        # Невалидный токен
        return None

# Пример использования
user_id = 'root'
token = create_token(user_id)
print(f"Created token: {token}")

decoded_payload = decode_token(token)
if decoded_payload:
    print(f"{decoded_payload['user_id']}")
else:
    print("Invalid or expired token")