import tkinter as tk
import ceasar_code


def send_text():
    text = input_text.get("1.0", tk.END).strip()

    if encrypt_var.get():
        text = ceasar_code.caesar_encrypt(text)

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, text)


def main():
    root = tk.Tk()
    root.title("Sender Window")
    root.geometry("400x300")

    # ---- input window content ----
    tk.Label(root, text="Enter text:").pack(anchor="w", padx=10)

    global input_text
    input_text = tk.Text(root, height=8)
    input_text.pack(fill="both", expand=True, padx=10)

    global encrypt_var
    encrypt_var = tk.BooleanVar()

    tk.Checkbutton(
        root,
        text="Encrypt text (Caesar)",
        variable=encrypt_var
    ).pack(anchor="w", padx=10, pady=5)

    tk.Button(root, text="Send to second window", command=send_text)\
        .pack(pady=10)

    # ---- second window ----
    second_window = tk.Toplevel(root)
    second_window.title("Receiver Window")
    second_window.geometry("400x300")

    tk.Label(second_window, text="Received text:").pack(anchor="w", padx=10)

    global output_text
    output_text = tk.Text(second_window, height=8)
    output_text.pack(fill="both", expand=True, padx=10)

    root.mainloop()


if __name__ == "__main__":
    main()
