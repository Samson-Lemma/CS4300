def calculate_discount(price, discount):
    if price < 0:
        raise ValueError("Price cannot be negative.")

    if discount < 0 or discount > 100:
        raise ValueError("Discount must be between 0 and 100.")

    return price - (price * discount / 100)


if __name__ == "__main__":
    print(calculate_discount(100, 20))