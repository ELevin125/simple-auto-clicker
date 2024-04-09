from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, Key
import tkinter as tk
from ClickMouse import ClickMouse

class AutoClickerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Auto Clicker")
        self.defaults = {
            "click_interval_s": 0.1,
            "hold_time_s": 0.01,
            "mouse_button": "Left"
        }
        self.click_thread = ClickMouse(Controller(), self.defaults["click_interval_s"], self.defaults["hold_time_s"])
        self.click_thread.start()
        self.autoclick_start_stop_key = Key.f6

        self.create_widgets()

        self.listener = Listener(on_press=self.on_press)
        self.listener.start()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def create_widgets(self):
        # Click Interval
        self.click_interval_label = tk.Label(self.root, text="Click Interval (ms):")
        self.click_interval_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.click_interval_entry = tk.Entry(self.root, width=7)
        self.click_interval_entry.grid(row=0, column=1, padx=5, pady=5)
        self.click_interval_entry.bind('<FocusOut>', self.update_click_interval)
        self.click_interval_entry.insert(tk.END, str(self.defaults["click_interval_s"] * 1000))

        # Hold Time
        self.hold_time_label = tk.Label(self.root, text="Hold Time (ms):")
        self.hold_time_label.grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.hold_time_entry = tk.Entry(self.root, width=7)
        self.hold_time_entry.grid(row=0, column=3, padx=5, pady=5)
        self.hold_time_entry.insert(tk.END, str(self.defaults["hold_time_s"] * 1000))
        self.hold_time_entry.bind('<FocusOut>', self.update_hold_time)

        # Mouse Click Type
        self.mouse_click_label = tk.Label(self.root, text="Mouse Click Type:")
        self.mouse_click_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.mouse_click_var = tk.StringVar()
        self.mouse_click_var.set(self.defaults["mouse_button"])
        self.mouse_click_dropdown = tk.OptionMenu(self.root, self.mouse_click_var, "Left", "Right", command=self.update_mouse_click_type)
        self.mouse_click_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Repeat Options
        self.repeat_label = tk.Label(self.root, text="Repeat Mode:")
        self.repeat_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.repeat_var = tk.StringVar()
        self.repeat_var.set("Until Stopped")
        self.repeat_radio1 = tk.Radiobutton(self.root, text="Until Stopped", variable=self.repeat_var, value="Until Stopped", command=self.update_repeat_option)
        self.repeat_radio1.grid(row=3, column=0, padx=5, pady=5)
        self.repeat_radio2 = tk.Radiobutton(self.root, text="Repeat For:", variable=self.repeat_var, value="Repeat For:", command=self.update_repeat_option)
        self.repeat_radio2.grid(row=3, column=1, padx=5, pady=5)
        self.repeat_count_entry = tk.Entry(self.root, width=14, textvariable=str(self.click_thread.max_clicks))
        self.repeat_count_entry.grid(row=3, column=2, padx=5, pady=5)
        self.update_repeat_option()  # Disable repeat count entry initially

        # Start/Stop Button
        self.start_stop_button = tk.Button(self.root, text="Press F6 to start / stop", command=self.start_stop_auto_clicker)
        self.start_stop_button.grid(row=4, column=0, padx=5, pady=10, columnspan=4)

    def on_press(self, key):
        if key == self.autoclick_start_stop_key:
            if self.click_thread.running:
                self.click_thread.stop_clicking()
            else:
                self.click_thread.start_clicking()

    def update_click_interval(self, event=None):
        self.click_thread.delay = int(self.click_interval_entry.get()) / 1000

    def update_hold_time(self, event=None):
        self.click_thread.hold_time = int(self.hold_time_entry.get()) / 1000

    def update_mouse_click_type(self, event=None):
        self.click_thread.button = Button.left if self.mouse_click_var.get() == "Left" else Button.right

    def update_repeat_option(self, event=None):
        if self.repeat_var.get() == "Until Stopped":
            self.repeat_count_entry.config(state=tk.DISABLED)
            self.click_thread.update_max_clicks(float("inf"))
        else:
            self.repeat_count_entry.config(state=tk.NORMAL)

    def start_stop_auto_clicker(self):
        if self.click_thread.running:
            self.click_thread.stop_clicking()
        else:
            self.click_thread.start_clicking()

    def on_closing(self):
        self.click_thread.exit()
        self.listener.stop()
        self.root.quit()
