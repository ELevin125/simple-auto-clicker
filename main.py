from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, Key
import tkinter as tk
from ClickMouse import ClickMouse

def on_press(key):
    if key == autoclick_start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()


def update_click_interval(event=None):
    click_thread.delay = int(click_interval_entry.get()) / 1000


def update_mouse_click_type(event=None):
    click_thread.button = Button.left if mouse_click_var.get() == "Left" else Button.right


def update_repeat_option(event=None):
    if repeat_var.get() == "Until Stopped":
        repeat_count_entry.config(state=tk.DISABLED)
        click_thread.update_max_clicks(float("inf"))
    else:
        repeat_count_entry.config(state=tk.NORMAL)


def start_stop_auto_clicker():
    if click_thread.running:
        click_thread.stop_clicking()
    else:
        click_thread.start_clicking()

def on_closing():
    click_thread.exit()
    listener.stop()
    root.quit()

root = tk.Tk()
root.title("Auto Clicker")
root.protocol("WM_DELETE_WINDOW", on_closing)

# Create ClickMouse instance
# mouse = Controller()
click_thread = ClickMouse(Controller())
click_thread.start()

# Click Interval
click_interval_label = tk.Label(root, text="Click Interval (ms):")
click_interval_label.grid(row=0, column=0, padx=5, pady=5)
click_interval_entry = tk.Entry(root)
click_interval_entry.grid(row=0, column=1, padx=5, pady=5)
click_interval_entry.insert(tk.END, "10")
click_interval_entry.bind('<FocusOut>', update_click_interval)

# Mouse Click Type
mouse_click_label = tk.Label(root, text="Mouse Click Type:")
mouse_click_label.grid(row=1, column=0, padx=5, pady=5)
mouse_click_var = tk.StringVar()
mouse_click_var.set("Left")
mouse_click_dropdown = tk.OptionMenu(root, mouse_click_var, "Left", "Right", command=update_mouse_click_type)
mouse_click_dropdown.grid(row=1, column=1, padx=5, pady=5)

# Repeat Options
repeat_var = tk.StringVar()
repeat_var.set("Until Stopped")
repeat_radio1 = tk.Radiobutton(root, text="Until Stopped", variable=repeat_var, value="Until Stopped", command=update_repeat_option)
repeat_radio1.grid(row=2, column=0, padx=5, pady=5)
repeat_radio2 = tk.Radiobutton(root, text="Repeat For:", variable=repeat_var, value="Repeat For:", command=update_repeat_option)
repeat_radio2.grid(row=3, column=0, padx=5, pady=5)
repeat_count_entry = tk.Entry(root, textvariable=str(click_thread.max_clicks))
repeat_count_entry.grid(row=3, column=1, padx=5, pady=5)
update_repeat_option()  # Disable repeat count entry initially

# Start/Stop Button
autoclick_start_stop_key = Key.f6
start_stop_button = tk.Button(root, text="Press F6 to start / stop", command=start_stop_auto_clicker)
start_stop_button.grid(row=4, columnspan=2, padx=5, pady=10)

listener = Listener(on_press=on_press)
listener.start()

root.mainloop()
