import tkinter as tk
import generator   # your password generator file


def generate_clicked():
    """Called when user presses Generate"""

    try:
        # validate length
        length = int(length_var.get())

        if length <= 0:
            result_label.config(text="Length must be greater than 0")
            return

        # call generator (catching errors from generator.py)
        password = generator.generate_password(
            length,
            lower_var.get(),
            upper_var.get(),
            digits_var.get(),
            symbols_var.get(),
            emojis_var.get()   # added (your generator supports this)
        )

        result_label.config(text=password)

    except ValueError as e:
        # catches invalid number OR no charset selected
        result_label.config(text=str("Invalid Input"))


def main():
    root = tk.Tk()
    root.title("Password Generator")
    root.geometry("350x300")   # slightly bigger for extra checkbox

    # Title
    tk.Label(
        root,
        text="Insert password specifications:"
    ).grid(row=0, column=0, columnspan=2, pady=10)

    # ---- length input ----
    tk.Label(root, text="Password Length:").grid(row=1, column=0, sticky="w")

    global length_var
    length_var = tk.StringVar()
    tk.Entry(root, textvariable=length_var).grid(row=1, column=1, sticky="ew")

    # ---- character set options ----
    tk.Label(root, text="Use characters:").grid(row=2, column=0, sticky="w", pady=(10, 0))

    global lower_var, upper_var, digits_var, symbols_var, emojis_var

    lower_var = tk.BooleanVar(value=True)
    upper_var = tk.BooleanVar(value=True)
    digits_var = tk.BooleanVar(value=True)
    symbols_var = tk.BooleanVar(value=False)
    emojis_var = tk.BooleanVar(value=False)   # added

    tk.Checkbutton(root, text="Lowercase (a-z)", variable=lower_var)\
        .grid(row=3, column=0, columnspan=2, sticky="w")

    tk.Checkbutton(root, text="Uppercase (A-Z)", variable=upper_var)\
        .grid(row=4, column=0, columnspan=2, sticky="w")

    tk.Checkbutton(root, text="Digits (0-9)", variable=digits_var)\
        .grid(row=5, column=0, columnspan=2, sticky="w")

    tk.Checkbutton(root, text="Symbols (!@#)", variable=symbols_var)\
        .grid(row=6, column=0, columnspan=2, sticky="w")

    tk.Checkbutton(root, text="Emojis 🐶", variable=emojis_var)\
        .grid(row=7, column=0, columnspan=2, sticky="w")

    # ---- generate button ----
    tk.Button(root, text="Generate Password", command=generate_clicked)\
        .grid(row=8, column=0, columnspan=2, pady=15)

    # ---- result ----
    global result_label
    result_label = tk.Label(root, text="", wraplength=300)
    result_label.grid(row=9, column=0, columnspan=2)

    root.columnconfigure(1, weight=1)

    root.mainloop()


if __name__ == "__main__":
    main()