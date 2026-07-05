import tkinter as tk
from tkinter import messagebox
from Adafruit_IO import Client, Feed, RequestError

# ---------------- Adafruit IO Credentials ----------------
ADAFRUIT_IO_USERNAME = "Goombastein"
ADAFRUIT_IO_KEY = "aio_hhaY48n2cE3Mk2c6Au2RTlPdpwpU"
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Feed keys
CONTROL_FEED = "admin-control"
STATUS_FEED = "dispenser-status"
PASSWORD_FEED = "password-display"

# Create/get feeds
for feed_key in [CONTROL_FEED, STATUS_FEED, PASSWORD_FEED]:
    try:
        aio.feeds(feed_key)
    except RequestError:
        aio.create_feed(Feed(name=feed_key, key=feed_key))

# ---------------- Global Variables ----------------
system_running = True
password_locked = True
dispense_count = 0

# ---------------- Functions ----------------



def toggle_system():
    global system_running
    if system_running:
        system_running = False
    else:
        system_running = True


    if system_running:
        command = "SYSTEM_START"
        status_text = "ENABLED"
        status_color = "green"
        button_text = "DISABLE SYSTEM"
        button_color = "red"
    else:
        command = "SYSTEM_STOP"
        status_text = "DISABLED"
        status_color = "red"
        button_text = "ENABLE SYSTEM"
        button_color = "green"

    try:
        aio.send(CONTROL_FEED, command)

        system_status_label.config(
            text=f"System Status: {status_text}",
            fg=status_color
        )

        system_toggle_btn.config(
            text=button_text,
            bg=button_color
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))










def toggle_password_lock():
    global password_locked

    # Flip the lock state
    if password_locked:
        password_locked = False
    else:
        password_locked = True

    try:
        if password_locked:
            command = "PASSWORD_LOCK"
            status_text = "LCD Display: LOCKED"
            status_color = "red"
            button_text = "UNLOCK LCD"
            button_color = "green"
        else:
            command = "PASSWORD_UNLOCK"
            status_text = "LCD Display: UNLOCKED"
            status_color = "green"
            button_text = "LOCK LCD"
            button_color = "red"

        # Send command to Adafruit IO
        aio.send(CONTROL_FEED, command)

        # Update UI
        password_lock_status.config(
            text=status_text,
            fg=status_color
        )

        password_lock_btn.config(
            text=button_text,
            bg=button_color
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))










def update_status():
    global dispense_count

    # ---------- Read dispense count ----------
    try:
        data = aio.receive(STATUS_FEED)

        if data is not None:
            value = data.value

            if value.startswith("COUNT:"):
                dispense_count = int(value.split(":")[1])
                dispense_label.config(
                    text=f"Total Dispenses: {dispense_count}"
                )

    except Exception as e:
        print("Error reading dispense count:", e)

    # ---------- Read passwords ----------
    try:
        pwd_data = aio.receive(PASSWORD_FEED)

        if pwd_data is not None and pwd_data.value:
            # Expected format: Room1:1234|Room2:5678
            rooms = pwd_data.value.split("|")

            room1_password = rooms[0].split(":")[1]
            room2_password = rooms[1].split(":")[1]

            password_display.config(
                text=f"Room 1: {room1_password}\nRoom 2: {room2_password}"
            )

    except Exception as e:
        print("Error reading passwords:", e)

    # Call this function again after 2 seconds
    root.after(2000, update_status)


# ---------------- GUI ----------------
root = tk.Tk()
root.title("Admin Control Panel")
root.geometry("400x620")
root.config(bg="#236B5D")

# Title
tk.Label(
    root,
    text="ADMIN CONTROL PANEL",
    font=("Times", 18, "bold"),
    bg="#2BCCAC",
    fg="white"
).pack(pady=20)

# -------- System Control --------
system_frame = tk.LabelFrame(
    root, text="System Control",
    font=("Times", 12, "bold"),
    bg="#2BCCAC", fg="white", padx=20, pady=15
)
system_frame.pack(fill="x", padx=20, pady=10)

system_status_label = tk.Label(
    system_frame, text="System Status: ENABLED",
    font=("Times", 12), bg="#2BCCAC", fg="green"
)
system_status_label.pack(pady=5)

system_toggle_btn = tk.Button(
    system_frame, text="DISABLE SYSTEM",
    font=("Times", 12, "bold"),
    bg="red", fg="white",
    command=toggle_system
)
system_toggle_btn.pack(pady=5)

# -------- Password Control --------
password_frame = tk.LabelFrame(
    root, text="Password Control",
    font=("Times", 12, "bold"),
    bg="#2BCCAC", fg="white", padx=20, pady=15
)
password_frame.pack(fill="x", padx=20, pady=10)

password_lock_status = tk.Label(
    password_frame, text="LCD Display: LOCKED",
    font=("Times", 12), bg="#2BCCAC", fg="red"
)
password_lock_status.pack(pady=5)

password_lock_btn = tk.Button(
    password_frame, text="UNLOCK LCD",
    font=("Times", 12, "bold"),
    bg="green", fg="white",
    command=toggle_password_lock
)
password_lock_btn.pack(pady=5)

tk.Label(
    password_frame, text="(Lock only affects LCD display)",
    font=("Times", 8, "italic"),
    bg="#2BCCAC", fg="white"
).pack(pady=(0, 10))

password_display = tk.Label(
    password_frame,
    text="Room 1: ****\nRoom 2: ****",
    font=("Times", 14, "bold"),
    bg="#1a9177", fg="yellow", padx=10, pady=10
)
password_display.pack(pady=5)

# -------- Dispense Section --------
status_frame = tk.LabelFrame(
    root, text="Dispense Section",
    font=("Times", 12, "bold"),
    bg="#2BCCAC", fg="white", padx=20, pady=15
)
status_frame.pack(fill="x", padx=20, pady=10)

dispense_label = tk.Label(
    status_frame,
    text="Total Dispenses: 0",
    font=("Times", 12),
    bg="#2BCCAC", fg="white"
)
dispense_label.pack(pady=5)


# Start updates
update_status()
root.mainloop()
