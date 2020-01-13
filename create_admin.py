import sys
from getpass import getpass

from app import create_app, db
from app.user.models import User


app = create_app()

with app.app_context():
    username = input("Введите ваш никнейм: ")
    if User.query.filter(User.username == username).count():
        print("Пользователь с таким никнеймом уже существует.")
        sys.exit(0)

    first_name = input("Введите ваше имя: ")
    last_name = input("Введите вашу фамилию: ")

    email = input("Введите ваш email: ")
    if User.query.filter(User.email == email).count():
        print("Пользователь с таким почтовым адресом уже зарегистрирован.")
        sys.exit(0)

    password = getpass("Ваш пароль: ")
    submit_password = getpass("Повторите ваш пароль: ")
    if password != submit_password:
        print("Пароли не совпадают.")
        sys.exit(0)

    new_admin = User(username=username, first_name=first_name,
                     last_name=last_name, email=email, role="admin")
    new_admin.set_password(password)

    db.session.add(new_admin)
    db.session.commit()

    print(
        f"Пользователь с никнеймом '{username}' был создан с правами администратора с id: {new_admin.id}.")
