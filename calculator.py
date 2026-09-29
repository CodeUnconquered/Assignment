import math


def calculator():
    print("=" * 50)
    print("        SCIENTIFIC CALCULATOR")
    print("=" * 50)

    while True:
        print("""
Choose an operation:

1.  Addition
2.  Subtraction
3.  Multiplication
4.  Division
5.  Power (x^y)
6.  Square root
7.  Logarithm (base 10)
8.  Natural logarithm (ln)
9.  Sine
10. Cosine
11. Tangent
12. Factorial
13. Percentage
14. Absolute value
15. Exponential (e^x)
16. Quit
""")

        choice = input("Enter your choice: ").strip()

        try:

            # Basic arithmetic
            if choice == "1":
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
                print("Result:", a + b)

            elif choice == "2":
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
                print("Result:", a - b)

            elif choice == "3":
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
                print("Result:", a * b)

            elif choice == "4":
                a = float(input("Enter numerator: "))
                b = float(input("Enter denominator: "))

                if b == 0:
                    print("Error: Cannot divide by zero.")
                else:
                    print("Result:", a / b)

            # Scientific functions
            elif choice == "5":
                x = float(input("Enter base: "))
                y = float(input("Enter exponent: "))
                print("Result:", x ** y)

            elif choice == "6":
                x = float(input("Enter number: "))

                if x < 0:
                    print("Error: Square root of a negative number.")
                else:
                    print("Result:", math.sqrt(x))

            elif choice == "7":
                x = float(input("Enter number: "))

                if x <= 0:
                    print("Error: Logarithm requires a positive number.")
                else:
                    print("Result:", math.log10(x))

            elif choice == "8":
                x = float(input("Enter number: "))

                if x <= 0:
                    print("Error: ln requires a positive number.")
                else:
                    print("Result:", math.log(x))

            elif choice == "9":
                angle = float(input("Enter angle in degrees: "))
                result = math.sin(math.radians(angle))
                print("Result:", result)

            elif choice == "10":
                angle = float(input("Enter angle in degrees: "))
                result = math.cos(math.radians(angle))
                print("Result:", result)

            elif choice == "11":
                angle = float(input("Enter angle in degrees: "))
                result = math.tan(math.radians(angle))
                print("Result:", result)

            elif choice == "12":
                n = int(input("Enter a non-negative integer: "))

                if n < 0:
                    print("Error: Factorial requires a non-negative integer.")
                else:
                    print("Result:", math.factorial(n))

            elif choice == "13":
                number = float(input("Enter number: "))
                percentage = float(input("Enter percentage: "))
                print("Result:", number * percentage / 100)

            elif choice == "14":
                x = float(input("Enter number: "))
                print("Result:", abs(x))

            elif choice == "15":
                x = float(input("Enter number: "))
                print("Result:", math.exp(x))

            elif choice == "16":
                print("\nThank you for using the Scientific Calculator!")
                break

            else:
                print("Invalid choice. Please select an option from 1–16.")

        except ValueError:
            print("Error: Please enter a valid number.")

        except OverflowError:
            print("Error: The result is too large to calculate.")

        print("\n" + "-" * 50)


# Start calculator
calculator()