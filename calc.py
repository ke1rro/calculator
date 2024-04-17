import constants
import tkinter as tk


class Calculator:

    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('375x667')
        self.window.resizable(0, 0)
        self.window.title('Calculator')
        self.total_expression = ''
        self.current_expression = ''
        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()
        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()
        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operation_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key),
                             lambda event,
                             digit=key: self.add_to_expressions(digit))

        for key in self.operations:
            self.window.bind(key,
                             lambda event,
                             operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_squareroot_button()

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame,
                               text=self.total_expression,
                               anchor=tk.E,
                               bg=constants.LIGHT_GRAY,
                               fg=constants.LABEL_COLOR,
                               padx=24,
                               font=constants.SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame,
                         text=self.current_expression,
                         anchor=tk.E,
                         bg=constants.LIGHT_GRAY,
                         fg=constants.LABEL_COLOR,
                         padx=24,
                         font=constants.LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')
        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=constants.LIGHT_GRAY)
        frame.pack(expand=True, fill='both')
        return frame

    def add_to_expressions(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame,
                               text=str(digit),
                               bg=constants.WHITE_COLOR,
                               fg=constants.LABEL_COLOR,
                               font=constants.DIGIT_FONT_STYLE,
                               borderwidth=0,
                               command=lambda x=digit:
                                   self.add_to_expressions(x))
            button.grid(row=grid_value[0],
                        column=grid_value[1],
                        sticky=tk.NSEW)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ''
        self.update_total_label()
        self.update_label()

    def create_operation_buttons(self):
        row_btn = 0
        for operation, sybmol in self.operations.items():
            button = tk.Button(self.buttons_frame,
                               text=str(sybmol),
                               bg=constants.OFF_WHITE,
                               fg=constants.LABEL_COLOR,
                               font=constants.DEFAULT_FONT_STYLE,
                               borderwidth=0,
                               command=lambda x=operation:
                                   self.append_operator(x))
            button.grid(row=row_btn, column=4, sticky=tk.NSEW)
            row_btn += 1

    def clear(self):
        self.current_expression = ''
        self.total_expression = ''
        self.update_total_label()
        self.update_label()

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}** 2"))
        self.update_label()

    def squareroot(self):
        self.current_expression = str(eval(f"{self.current_expression} ** 0.5"))
        self.update_label()

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))

            self.total_expression = ''
        except Exception:
            self.current_expression = "Error"
        self.update_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame,
                           text='C',
                           bg=constants.OFF_WHITE,
                           fg=constants.LABEL_COLOR,
                           font=constants.DEFAULT_FONT_STYLE,
                           borderwidth=0,
                           command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def create_square_button(self):
        button = tk.Button(self.buttons_frame,
                           text='x\u00b2',
                           bg=constants.OFF_WHITE,
                           fg=constants.LABEL_COLOR,
                           font=constants.DEFAULT_FONT_STYLE,
                           borderwidth=0,
                           command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def create_squareroot_button(self):
        button = tk.Button(self.buttons_frame,
                           text='\u221ax',
                           bg=constants.OFF_WHITE,
                           fg=constants.LABEL_COLOR,
                           font=constants.DEFAULT_FONT_STYLE,
                           borderwidth=0,
                           command=self.squareroot)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame,
                           text='=',
                           bg=constants.LIGHT_BLUE,
                           fg=constants.LABEL_COLOR,
                           font=constants.DEFAULT_FONT_STYLE,
                           borderwidth=0,
                           command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill='both')
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()
