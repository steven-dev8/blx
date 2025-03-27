from src.schema.schemas import ProductCreate


def avaliable_product(quantity: int):
    return quantity >= 1


def length_name(name: str):
    return len(name) >= 3 and len(name) <= 70


def quantity_product(quantity: int):
    return quantity >= 0


def length_description(description: str):
    return len(description) <= 200


def check_price(price: float):
    return price >= 0


def create_product(product: ProductCreate):
    name = length_name(product.name)
    quantity = quantity_product(product.quantity)
    description = length_description(product.description)
    price = check_price(product.price)

    return name and quantity and description and price
