def classify_number(number):
    if number > 0:
        return "positive"
    elif number < 0:
        return "negative"
    else:
        return "zero"


def first_ten_primes():
    primes = []
    number = 2

    while len(primes) < 10:
        is_prime = True

        for divisor in range(2, int(number ** 0.5) + 1):
            if number % divisor == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(number)

        number += 1

    return primes


def sum_one_to_one_hundred():
    total = 0
    number = 1

    while number <= 100:
        total += number
        number += 1

    return total


if __name__ == "__main__":
    print(classify_number(5))
    print(first_ten_primes())
    print(sum_one_to_one_hundred())