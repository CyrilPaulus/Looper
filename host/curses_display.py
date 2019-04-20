from looper import Looper
from time import sleep
from channel import ChannelState
import curses


class CursesDisplay:

    def __init__(self, looper):
        self._looper = looper

    def run(self):
        self._screen = curses.initscr()
        self._screen.clear()
        self._screen.refresh()
        self._height, self._width = self._screen.getmaxyx()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_RED)

        self.refresh()

    def refresh(self):
        while True:
            self._screen.clear()
            x, y = 0, 0
            cur_channel = self._looper.get_current_channel()
            for channel in self._looper.get_channels():
                color = curses.color_pair(1)
                if channel == cur_channel:
                    color = curses.color_pair(2)
                label = str(channel.get_label())

                self._screen.addstr(y, x, label, color)
                x = x + len(label) + 1
            x, y = 0, 1

            for channel in self._looper.get_channels():

                label = str(channel.get_label())
                state = channel.get_state()

                if state == ChannelState.IDLE:
                    state_str = "I"
                    color = curses.color_pair(3)
                elif state == ChannelState.PLAYING:
                    state_str = "P"
                    color = curses.color_pair(4)
                elif state == ChannelState.RECORDING:
                    state_str = "R"
                    color = curses.color_pair(5)

                self._screen.addstr(y, x + len(label) - 1, state_str, color)
                x = x + len(label) + 1

            self._screen.refresh()
            sleep(0.016)
