from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


def generate_hash(text_plan):
    return pwd_context.hash(text_plan)


def verify_hash(text_plan, text_hash):
    return pwd_context.verify(text_plan, text_hash)
