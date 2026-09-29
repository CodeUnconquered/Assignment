def get_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("⚠ Invalid entry. Please enter a whole number.")


def multiplication_table(number, limit):
    print("\n" + "=" * 32)
    print(f"      TABLE OF {number}")
    print("=" * 32)

    for i in range(1, limit + 1):
        result = number * i
        print(f"{number:>3} × {i:>3} = {result:>5}")

    print("=" * 32)


def main():
    print("MATHEMATICAL TABLE GENERATOR")
    print("-" * 32)

    number = get_integer("Enter the number: ")
    limit = get_integer("Generate up to: ")

    multiplication_table(number, limit)


if __name__ == "__main__":
    main()