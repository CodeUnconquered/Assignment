import tkinter as tk
import math


class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("420x650")
        self.root.resizable(False, False)

        # ---------------- DISPLAY ----------------
        self.expression = tk.StringVar()

        display = tk.Entry(
            root,
            textvariable=self.expression,
            font=("Arial", 24),
            justify="right",
            bd=10,
            relief=tk.FLAT
        )
        display.pack(
            fill="x",
            padx=15,
            pady=20,
            ipady=15
        )

        # ---------------- BUTTON FRAME ----------------
        button_frame = tk.Frame(root)
        button_frame.pack(padx=10, pady=5)

        # Button layout
        buttons = [
            ["sin", "cos", "tan", "√"],
            ["log", "ln", "x²", "xʸ"],
            ["(", ")", "!", "%"],
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "−"],
            ["0", ".", "=", "+"],
            ["AC", "DEL"]
        ]

        for row, button_row in enumerate(buttons):
            for col, button_text in enumerate(button_row):

                button = tk.Button(
                    button_frame,
                    text=button_text,
                    font=("Arial", 15, "bold"),
                    width=6,
                    height=2,
                    command=lambda value=button_text:
                        self.button_click(value)
                )

                button.grid(
                    row=row,
                    column=col,
                    padx=4,
                    pady=4
                )

        # Keyboard support
        root.bind("<Return>", lambda event: self.calculate())
        root.bind("<BackSpace>", lambda event: self.delete())
        root.bind("<Escape>", lambda event: self.clear())

    # ---------------- BUTTON HANDLER ----------------

    def button_click(self, value):

        if value == "=":
            self.calculate()

        elif value == "AC":
            self.clear()

        elif value == "DEL":
            self.delete()

        elif value == "√":
            self.add("sqrt(")

        elif value == "x²":
            self.add("**2")

        elif value == "xʸ":
            self.add("**")

        elif value == "sin":
            self.add("sin(")

        elif value == "cos":
            self.add("cos(")

        elif value == "tan":
            self.add("tan(")

        elif value == "log":
            self.add("log(")

        elif value == "ln":
            self.add("ln(")

        elif value == "!":
            self.add("!")

        elif value == "×":
            self.add("*")

        elif value == "÷":
            self.add("/")

        elif value == "−":
            self.add("-")

        elif value == "%":
            self.add("/100")

        else:
            self.add(value)

    # ---------------- ADD TEXT ----------------

    def add(self, value):
        self.expression.set(
            self.expression.get() + value
        )

    # ---------------- CLEAR ----------------

    def clear(self):
        self.expression.set("")

    # ---------------- DELETE ----------------

    def delete(self):
        current = self.expression.get()

        if current:
            self.expression.set(current[:-1])

    # ---------------- CALCULATE ----------------

    def calculate(self):

        expression = self.expression.get()

        try:

            # Replace calculator functions
            expression = expression.replace(
                "sqrt(", "math.sqrt("
            )

            expression = expression.replace(
                "sin(", "math.sin(math.radians("
            )

            expression = expression.replace(
                "cos(", "math.cos(math.radians("
            )

            expression = expression.replace(
                "tan(", "math.tan(math.radians("
            )

            expression = expression.replace(
                "log(", "math.log10("
            )

            expression = expression.replace(
                "ln(", "math.log("
            )

            # Handle factorial
            expression = self.handle_factorial(expression)

            # Fix trig parentheses
            expression = self.fix_trig_parentheses(expression)

            result = eval(
                expression,
                {
                    "__builtins__": {},
                    "math": math
                }
            )

            # Clean floating point results
            if isinstance(result, float):

                if result.is_integer():
                    result = int(result)

                else:
                    result = round(result, 10)

            self.expression.set(str(result))

        except ZeroDivisionError:
            self.expression.set("Error: Division by zero")

        except ValueError:
            self.expression.set("Error: Invalid value")

        except Exception:
            self.expression.set("Error")

    # ---------------- FACTORIAL ----------------

    def handle_factorial(self, expression):

        while "!" in expression:

            index = expression.find("!")

            # Find number before !
            start = index - 1

            while start >= 0 and (
                expression[start].isdigit()
            ):
                start -= 1

            number = expression[start + 1:index]

            if not number:
                raise ValueError

            factorial_result = math.factorial(
                int(number)
            )

            expression = (
                expression[:start + 1]
                + str(factorial_result)
                + expression[index + 1:]
            )

        return expression

    # ---------------- TRIG PARENTHESES ----------------

    def fix_trig_parentheses(self, expression):

        # sin(x) was converted to:
        # math.sin(math.radians(x

        expression = expression.replace(
            "math.radians(", "math.radians("
        )

        # Add the missing closing parenthesis
        # for simple trig expressions.
        for func in [
            "math.sin(math.radians(",
            "math.cos(math.radians(",
            "math.tan(math.radians("
        ]:

            if func in expression:
                expression += ")"

        return expression


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":

    root = tk.Tk()

    calculator = ScientificCalculator(root)

    root.mainloop()