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


def validate_product_data(product: ProductCreate):
    return all([
        product.name is None or length_name(product.name),
        product.quantity is None or quantity_product(product.quantity),
        product.description is None or length_description(product.description),
        product.price is None or check_price(product.price)
    ])
