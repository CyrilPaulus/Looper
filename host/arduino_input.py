import serial
import threading
import serial.tools.list_ports


class ArduinoInput:
    _port = None
    _baudrate = None
    _serial = None
    _running = False
    _callback = None

    def __init__(self, callback, port='COM4', baudrate=9600):
        self._port = port
        self._baudrate = baudrate
        self._callback = callback

    def choose_port(self):
        ports = sorted(serial.tools.list_ports.comports())

        print("Please choose a port\n")
        for idx, port in enumerate(ports):
            print("{}: {} [{}]".format(idx, port.device, port.description))
        index = 0
        input(index)

        self._port = ports[index].device

    def start(self):
        self._serial = serial.Serial(self._port, self._baudrate)
        self._running = True
        threading.Thread(target=self._loop).start()

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
