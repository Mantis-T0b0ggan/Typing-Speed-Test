import curses             #Note 1
from curses import wrapper
import time
import random



def start_screen(stdscr):                          #Note 6
	stdscr.clear()        #Note 3
	stdscr.addstr("Welcome to the Speed Typing Test")
	stdscr.addstr("\nPress any key to begin!")
	stdscr.refresh()
	stdscr.getkey()             #Note 4

def display_text(stdscr, target, current, wpm=0):
		stdscr.addstr(target)
		stdscr.addstr(1, 0, f"WPM: {wpm}")

		for i, char in enumerate(current):             #Note 9 & 10
			correct_char = target[i]
			color = curses.color_pair(1)
			if char != correct_char:
				color = curses.color_pair(2)

			stdscr.addstr(0, i, char, color)


def load_text():                                   #Notes
	with open("test_text.txt", "r") as f:
		lines = f.readlines()
		return random.choice(lines).strip()

def wpm_test(stdscr):                         #Note 7
	target_text = load_text()
	current_text = []
	wpm = 0
	start_time = time.time()
	stdscr.nodelay(True)                                     #Note 12

	while True:
		time_elapsed = max(time.time() - start_time, 1)            #Note 11
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5 )  

		stdscr.clear()
		display_text(stdscr, target_text, current_text, wpm)
		stdscr.refresh()

		if "".join(current_text) == target_text:                   #Note 14
			stdscr.nodelay(False)
			break

		try:
				key = stdscr.getkey()
		except:
				continue                                           #Note 13

		if ord(key) == 27:            #Note 8
			break

		if key in ("KEY_BACKSPACE", '\b', '\x7f'):
			if len(current_text) > 0:
				current_text.pop()
		elif len(current_text) < len(target_text):
			current_text.append(key)


def main(stdscr):         #Note 2
	curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)            # note 5
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLUE)

	start_screen(stdscr)

	while True:                                         #Note 15
		wpm_test(stdscr)

		stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
		key = stdscr.getkey()

		if ord(key) == 27:
			break

wrapper(main)
