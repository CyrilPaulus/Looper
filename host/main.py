from arduino_input import ArduinoInput
from looper import Looper
from curses_display import CursesDisplay


def callback(button_id, looper, display):
    if (button_id == 0):
        looper.prev_channel()
    elif (button_id == 1):
        looper.next_channel()
    elif(button_id == 2):
        looper.record()
    elif (button_id == 3):
        looper.play()
    # display.refresh()


def main():
    looper = Looper(16, 4)
    display = CursesDisplay(looper)
    arduino_input = ArduinoInput(lambda x: callback(x, looper, display))

    #
    try:
        arduino_input.start()
        looper.print_record_info()
        input("Press any key to exit\n")
        display.run()
    except KeyboardInterrupt:
        pass

    arduino_input.stop()
    looper.stop()


if __name__ == "__main__":
    main()
