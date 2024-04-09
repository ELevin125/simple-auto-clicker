import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

delay = 0.01
button = Button.left
start_stop_key = KeyCode(char='1')
stop_key = KeyCode(char='2')

delay_up_key = KeyCode(char='=')
delay_down_key = KeyCode(char='-')

class ClickMouse(threading.Thread):
	def __init__(self, delay, button):
		super(ClickMouse, self).__init__()
		self.delay = delay
		self.button = button
		self.running = False
		self.program_running = True

	def start_clicking(self):
		self.running = True

	def stop_clicking(self):
		self.running = False

	def exit(self):
		self.stop_clicking()
		self.program_running = False

	def run(self):
		while self.program_running:
			while self.running:
				mouse.press(self.button)
				# Hold the mouse button for 0.2 seconds
				# Not holding too long will cause click to not register sometimes
				time.sleep(0.2)
				mouse.release(self.button)
				time.sleep(self.delay)
			time.sleep(0.1)

mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()


def on_press(key):
	if key == start_stop_key:
		if click_thread.running:
			click_thread.stop_clicking()
		else:
			click_thread.start_clicking()
	elif key == stop_key:
		click_thread.exit()
		listener.stop()
	elif key == delay_up_key:
		click_thread.delay += 0.01
	elif key == delay_down_key:
		click_thread.delay = max(click_thread.delay - 0.01, 0.001)

with Listener(on_press=on_press) as listener:
	listener.join()
