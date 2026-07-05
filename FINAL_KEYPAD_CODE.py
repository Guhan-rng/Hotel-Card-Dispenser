import tkinter as tk
from tkinter import messagebox
from Adafruit_IO import Client, Feed, RequestError
#-------AdaFruit-Stuff----------------------------
ADAFRUIT_IO_USERNAME = "Goombastein"
ADAFRUIT_IO_KEY = "aio_hhaY48n2cE3Mk2c6Au2RTlPdpwpU"
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
FEED_NAME = "Keypad"
FEED_KEY = "keypad"
#-------
def add_digit(d):
    entry_var.set(entry_var.get() + d)

def clear_entry():
    entry_var.set("")

def send_to_adafruit():
    value = entry_var.get()

    if value == "":
        messagebox.showwarning("Error", "No input to send")
        return

    try:
        aio.send(FEED_KEY, value)
        messagebox.showinfo("Success", f"Sent '{value}' to Adafruit IO")
        clear_entry()
    except Exception as e:
        messagebox.showerror("Error", str(e))
#-----------------------------------------------
root = tk.Tk()
root.title("Keypad Input")
root.geometry("300x400")

entry_var = tk.StringVar()

entry = tk.Entry(
    root,
    textvariable=entry_var,
    font=("Arial", 20),
    justify="right"
)
entry.pack(fill="x", padx=10, pady=10)

keypad = tk.Frame(root)
keypad.pack()

buttons = [
    ("1", "2", "3"),
    ("4", "5", "6"),
    ("7", "8", "9"),
    ("0",)
]

for row in buttons:
    row_frame = tk.Frame(keypad)
    row_frame.pack()
    for digit in row:
        tk.Button(
            row_frame,
            text=digit,
            font=("Arial", 16),
            width=5,
            height=2,
            command=lambda d=digit: add_digit(d)
        ).pack(side="left", padx=5, pady=5)

control = tk.Frame(root)
control.pack(pady=10)

tk.Button(
    control,
    text="SEND",
    font=("Arial", 14),
    width=10,
    command=send_to_adafruit
).pack(side="left", padx=5)

tk.Button(
    control,
    text="CLEAR",
    font=("Arial", 14),
    width=10,
    command=clear_entry
).pack(side="left", padx=5)

root.mainloop()
