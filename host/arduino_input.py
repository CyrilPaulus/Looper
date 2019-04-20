import serial
import threading


class ArduinoInput:
    _serial = None
    _running = False
    _callback = None

    def __init__(self, callback, port='COM4', baudrate=9600):
        self._serial = serial.Serial(port, baudrate)
        self._callback = callback
        threading.Thread(target=self._loop).start()

    def start(self):
        self._running = True

    def stop(self):
        self._running = False

    def _loop(self):
        print('Reading Serial')
        last_data = ['0', '0', '0', '0', '0']
        while self._running:
            line = str(self._serial.readline().decode("utf-8"))
            data = line.split(' ')[:5][::-1]
            for i in range(0, 5):
                self._react(i, data[i], last_data[i])
            last_data = data

    def _react(self, i, data, last_data):
        if last_data == data:
            return

        if last_data == '0':
            self._callback(i)
        else:
            pass
