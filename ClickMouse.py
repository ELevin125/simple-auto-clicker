import time
import threading
from pynput.mouse import Button
import tkinter as tk

class ClickMouse(threading.Thread):
    def __init__(self, mouse, delay, hold_time):
        super(ClickMouse, self).__init__()
        self.mouse = mouse
        self.delay = delay
        self.hold_time = hold_time;
        self.button = Button.left
        self.running = False
        self.program_running = True
        self.max_clicks = tk.StringVar()
        self.max_clicks.set(str(float("inf")))
        self._current_click = 0

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self._current_click = 0
        self.running = False

    def run(self):
        while self.program_running:
            while self.can_run():
                self._current_click += 1
                self.mouse.press(self.button)
                time.sleep(self.hold_time)
                self.mouse.release(self.button)
                time.sleep(self.delay)
            else:
                self.stop_clicking()
            time.sleep(0.1)

    def can_run(self):
        return self.running and (self._current_click < float(self.max_clicks.get()))
    
    def update_max_clicks(self, new_max):
        self.max_clicks.set(new_max)

    def exit(self):
        self.stop_clicking()
        self.program_running = False