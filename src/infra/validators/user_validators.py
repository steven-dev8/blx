from src.schema.schemas import UserCreate


def validate_password(password: str):
    return len(password) >= 8


def validate_login(login: str):
    return len(login) >= 5


def validate_name(name: str):
    return len(name.split()) >= 2


def validate_number(number: str):
    length_num = len(number)
    return number.isnumeric() and (length_num == 10 or length_num == 11)


def validate_create(user: UserCreate):
    name = validate_name(user.name) 
    login = validate_login(user.login) 
    password = validate_password(user.password)
    number = validate_number(user.number)

    return name and login and password and number