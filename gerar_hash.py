from werkzeug.security import generate_password_hash

# Password simples para testar
password = "123456"
hashed = generate_password_hash(password)

print("Hash da password:", hashed)
