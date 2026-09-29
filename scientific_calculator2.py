import tkinter as tk
from tkinter import messagebox
import math
import re


class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator V2")
        self.root.geometry("520x760")
        self.root.resizable(False, False)

        self.expression = tk.StringVar()
        self.mode = "DEG"
        self.answer = 0
        self.history = []

        self.create_interface()

    # =========================================================
    # INTERFACE
    # =========================================================

    def create_interface(self):
        # ---------------- DISPLAY ----------------
        display_frame = tk.Frame(self.root)
        display_frame.pack(fill="x", padx=15, pady=15)

        self.display = tk.Entry(
            display_frame,
            textvariable=self.expression,
            font=("Arial", 24),
            justify="right",
            bd=8,
            relief=tk.RIDGE
        )

        self.display.pack(fill="x", ipady=15)

        # ---------------- MODE ----------------
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", padx=15, pady=5)

        self.mode_button = tk.Button(
            top_frame,
            text="DEG",
            font=("Arial", 11, "bold"),
            width=8,
            command=self.toggle_mode
        )

        self.mode_button.pack(side="left")

        tk.Label(
            top_frame,
            text="Scientific Calculator",
            font=("Arial", 13, "bold")
        ).pack(side="right")

        # ---------------- BUTTONS ----------------
        button_frame = tk.Frame(self.root)
        button_frame.pack(padx=10, pady=10)

        buttons = [
            ["sin", "cos", "tan", "log", "ln"],
            ["√", "x²", "xʸ", "(", ")"],
            ["π", "e", "!", "%", "ANS"],
            ["7", "8", "9", "÷", "DEL"],
            ["4", "5", "6", "×", "AC"],
            ["1", "2", "3", "−", "="],
            ["0", ".", "^", "", "+"]
        ]

        for row, button_row in enumerate(buttons):
            for col, text in enumerate(button_row):

                if text == "":
                    continue

                button = tk.Button(
                    button_frame,
                    text=text,
                    font=("Arial", 13, "bold"),
                    width=6,
                    height=2,
                    command=lambda value=text:
                    self.button_click(value)
                )

                button.grid(
                    row=row,
                    column=col,
                    padx=3,
                    pady=3
                )

        # ---------------- HISTORY ----------------
        tk.Label(
            self.root,
            text="Calculation History",
            font=("Arial", 12, "bold")
        ).pack(pady=(8, 2))

        self.history_box = tk.Listbox(
            self.root,
            height=8,
            font=("Arial", 10)
        )

        self.history_box.pack(
            fill="both",
            padx=15,
            pady=5
        )

        # Double-click history item
        self.history_box.bind(
            "<Double-Button-1>",
            self.use_history
        )

        # ---------------- KEYBOARD ----------------
        self.root.bind(
            "<Return>",
            lambda event: self.calculate()
        )

        self.root.bind(
            "<BackSpace>",
            lambda event: self.delete()
        )

        self.root.bind(
            "<Escape>",
            lambda event: self.clear()
        )

    # =========================================================
    # BUTTON HANDLING
    # =========================================================

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
            self.add("^2")

        elif value == "xʸ":
            self.add("^")

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

        elif value == "π":
            self.add("π")

        elif value == "e":
            self.add("e")

        elif value == "!":
            self.add("!")

        elif value == "×":
            self.add("*")

        elif value == "÷":
            self.add("/")

        elif value == "−":
            self.add("-")

        elif value == "ANS":
            self.add("ANS")

        else:
            self.add(value)

    # =========================================================
    # ADD TEXT
    # =========================================================

    def add(self, value):
        current = self.expression.get()

        if not current:
            self.expression.set(value)
            return

        last = current[-1]

        # Add multiplication automatically when appropriate.
        if value == "(":
            if last.isdigit() or last in ")πe":
                current += "*"

        elif value in ["π", "e"]:
            if last.isdigit() or last == ")":
                current += "*"

        self.expression.set(current + value)

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self):
        self.expression.set("")

    # =========================================================
    # DELETE
    # =========================================================

    def delete(self):
        current = self.expression.get()

        if current:
            self.expression.set(current[:-1])

    # =========================================================
    # DEG / RAD MODE
    # =========================================================

    def toggle_mode(self):

        if self.mode == "DEG":
            self.mode = "RAD"
        else:
            self.mode = "DEG"

        self.mode_button.config(
            text=self.mode
        )

    # =========================================================
    # TOKENIZER
    # =========================================================

    def tokenize(self, expression):
        tokens = []

        pattern = re.compile(
            r"""
            \s*
            (
                \d+(?:\.\d*)?
                |
                \.\d+
                |
                [A-Za-z]+
                |
                π
                |
                [()+\-*/^!%,]
            )
            """,
            re.VERBOSE
        )

        position = 0

        while position < len(expression):

            match = pattern.match(
                expression,
                position
            )

            if not match:
                raise ValueError(
                    f"Invalid character near: "
                    f"{expression[position:]}"
                )

            token = match.group(1)
            tokens.append(token)
            position = match.end()

        return tokens

    # =========================================================
    # IMPLICIT MULTIPLICATION
    # =========================================================

    def insert_implicit_multiplication(self, tokens):

        result = []

        def can_end_value(token):
            return (
                self.is_number(token)
                or token in [")", "π", "e", "ANS"]
                or token == "!"
            )

        def can_start_value(token):
            return (
                self.is_number(token)
                or token in ["(", "π", "e", "ANS"]
                or token in [
                    "sin",
                    "cos",
                    "tan",
                    "log",
                    "ln",
                    "sqrt"
                ]
            )

        for token in tokens:

            if result:
                previous = result[-1]

                if (
                    can_end_value(previous)
                    and can_start_value(token)
                ):
                    result.append("*")

            result.append(token)

        return result

    # =========================================================
    # NUMBER CHECK
    # =========================================================

    @staticmethod
    def is_number(token):
        try:
            float(token)
            return True
        except ValueError:
            return False

    # =========================================================
    # SHUNTING-YARD PARSER
    # =========================================================

    def to_rpn(self, tokens):

        output = []
        operators = []

        functions = {
            "sin",
            "cos",
            "tan",
            "log",
            "ln",
            "sqrt"
        }

        precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "u+": 3,
            "u-": 3,
            "^": 4,
            "!": 5
        }

        right_associative = {
            "^",
            "u+",
            "u-"
        }

        previous = None

        for token in tokens:

            # Number / constants
            if (
                self.is_number(token)
                or token in ["π", "e", "ANS"]
            ):
                output.append(token)

            # Function
            elif token in functions:
                operators.append(token)

            # Opening parenthesis
            elif token == "(":
                operators.append(token)

            # Closing parenthesis
            elif token == ")":

                while (
                    operators
                    and operators[-1] != "("
                ):
                    output.append(
                        operators.pop()
                    )

                if not operators:
                    raise ValueError(
                        "Mismatched parentheses."
                    )

                operators.pop()

                if (
                    operators
                    and operators[-1] in functions
                ):
                    output.append(
                        operators.pop()
                    )

            # Factorial
            elif token == "!":
                output.append(token)

            # Percentage
            elif token == "%":
                output.append("%")

            # Operators
            elif token in {
                "+",
                "-",
                "*",
                "/",
                "^"
            }:

                operator = token

                # Unary + or -
                if (
                    token in ["+", "-"]
                    and (
                        previous is None
                        or previous in {
                            "(",
                            "+",
                            "-",
                            "*",
                            "/",
                            "^"
                        }
                    )
                ):
                    operator = (
                        "u+" if token == "+"
                        else "u-"
                    )

                while operators:

                    top = operators[-1]

                    if top == "(":
                        break

                    if top in functions:
                        output.append(
                            operators.pop()
                        )
                        continue

                    top_precedence = precedence.get(
                        top,
                        0
                    )

                    current_precedence = precedence[
                        operator
                    ]

                    should_pop = (
                        top_precedence >
                        current_precedence
                        or (
                            top_precedence ==
                            current_precedence
                            and operator not in
                            right_associative
                        )
                    )

                    if not should_pop:
                        break

                    output.append(
                        operators.pop()
                    )

                operators.append(operator)

            else:
                raise ValueError(
                    f"Unknown token: {token}"
                )

            previous = token

        while operators:

            top = operators.pop()

            if top == "(":
                raise ValueError(
                    "Mismatched parentheses."
                )

            output.append(top)

        return output

    # =========================================================
    # RPN EVALUATION
    # =========================================================

    def evaluate_rpn(self, tokens):

        stack = []

        functions = {
            "sin",
            "cos",
            "tan",
            "log",
            "ln",
            "sqrt"
        }

        for token in tokens:

            # Numbers
            if self.is_number(token):
                stack.append(float(token))

            # Constants
            elif token == "π":
                stack.append(math.pi)

            elif token == "e":
                stack.append(math.e)

            elif token == "ANS":
                stack.append(float(self.answer))

            # Unary operators
            elif token in ["u+", "u-"]:

                if not stack:
                    raise ValueError(
                        "Missing value."
                    )

                value = stack.pop()

                if token == "u-":
                    value = -value

                stack.append(value)

            # Factorial
            elif token == "!":

                if not stack:
                    raise ValueError(
                        "Missing value before factorial."
                    )

                value = stack.pop()

                if value < 0 or not value.is_integer():
                    raise ValueError(
                        "Factorial requires a "
                        "non-negative integer."
                    )

                if value > 170:
                    raise ValueError(
                        "Factorial result is too large."
                    )

                stack.append(
                    math.factorial(int(value))
                )

            # Percentage
            elif token == "%":

                if not stack:
                    raise ValueError(
                        "Missing value before %."
                    )

                value = stack.pop()
                stack.append(value / 100)

            # Functions
            elif token in functions:

                if not stack:
                    raise ValueError(
                        "Missing function argument."
                    )

                value = stack.pop()

                if token == "sin":
                    if self.mode == "DEG":
                        value = math.radians(value)
                    result = math.sin(value)

                elif token == "cos":
                    if self.mode == "DEG":
                        value = math.radians(value)
                    result = math.cos(value)

                elif token == "tan":
                    if self.mode == "DEG":
                        value = math.radians(value)

                    # Prevent obvious undefined tan values.
                    if (
                        self.mode == "DEG"
                        and abs(
                            math.cos(
                                math.radians(value)
                            )
                        ) < 1e-12
                    ):
                        raise ValueError(
                            "Tangent is undefined."
                        )

                    result = math.tan(value)

                elif token == "log":
                    if value <= 0:
                        raise ValueError(
                            "log requires a positive number."
                        )
                    result = math.log10(value)

                elif token == "ln":
                    if value <= 0:
                        raise ValueError(
                            "ln requires a positive number."
                        )
                    result = math.log(value)

                elif token == "sqrt":
                    if value < 0:
                        raise ValueError(
                            "Square root requires "
                            "a non-negative number."
                        )
                    result = math.sqrt(value)

                stack.append(result)

            # Binary operators
            elif token in {
                "+",
                "-",
                "*",
                "/",
                "^"
            }:

                if len(stack) < 2:
                    raise ValueError(
                        "Incomplete expression."
                    )

                b = stack.pop()
                a = stack.pop()

                if token == "+":
                    result = a + b

                elif token == "-":
                    result = a - b

                elif token == "*":
                    result = a * b

                elif token == "/":
                    if b == 0:
                        raise ZeroDivisionError
                    result = a / b

                elif token == "^":
                    result = a ** b

                stack.append(result)

            else:
                raise ValueError(
                    f"Cannot evaluate {token}"
                )

        if len(stack) != 1:
            raise ValueError(
                "Invalid expression."
            )

        return stack[0]

    # =========================================================
    # MAIN CALCULATION
    # =========================================================

    def calculate(self):

        expression = self.expression.get().strip()

        if not expression:
            return

        try:
            tokens = self.tokenize(expression)

            tokens = self.insert_implicit_multiplication(
                tokens
            )

            rpn = self.to_rpn(tokens)

            result = self.evaluate_rpn(rpn)

            # Clean floating point noise
            if abs(result) < 1e-12:
                result = 0

            elif (
                isinstance(result, float)
                and result.is_integer()
            ):
                result = int(result)

            else:
                result = round(result, 10)

            self.answer = result

            result_text = str(result)

            self.expression.set(
                result_text
            )

            # Save history
            self.history.append(
                (expression, result_text)
            )

            self.history_box.insert(
                tk.END,
                f"{expression} = {result_text}"
            )

        except ZeroDivisionError:
            self.show_error(
                "Cannot divide by zero."
            )

        except ValueError as error:
            self.show_error(
                str(error)
            )

        except OverflowError:
            self.show_error(
                "The result is too large."
            )

        except Exception as error:
            self.show_error(
                f"Calculation error: {error}"
            )

    # =========================================================
    # ERROR MESSAGE
    # =========================================================

    def show_error(self, message):

        self.expression.set("Error")

        messagebox.showerror(
            "Calculation Error",
            message
        )

    # =========================================================
    # HISTORY
    # =========================================================

    def use_history(self, event=None):

        selection = self.history_box.curselection()

        if not selection:
            return

        index = selection[0]

        expression, result = self.history[index]

        self.expression.set(
            expression
        )


# =============================================================
# PROGRAM START
# =============================================================

if __name__ == "__main__":
    root = tk.Tk()

    calculator = ScientificCalculator(root)

    root.mainloop()