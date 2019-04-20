from channel import Channel, ChannelState
import pyaudio
import numpy
import threading


class Looper:
    CHUNK = 1024
    SAMPLE_RATE = 44000
    CHANNELS = 2
    FORMAT = pyaudio.paInt16

    def __init__(self, channels_count, default_record_device=0, debug_action=False):
        self._channels = []
        self._running = False
        self._debug_action = debug_action
        for i in range(0, channels_count):
            self._channels.append(
                Channel(str(i), default_record_device, self.SAMPLE_RATE, self.CHANNELS))
        self._current_channel_index = 0

    def get_current_channel(self):
        return self._channels[self._current_channel_index]

    def print_channel_info(self):
        if not self._debug_action:
            return

        self.get_current_channel().print_info()

    def get_channels(self):
        return self._channels

    def prev_channel(self):
        if(self._current_channel_index == 0):
            self._current_channel_index = len(self._channels) - 1
        else:
            self._current_channel_index -= 1

        self.print_channel_info()

    def next_channel(self):
        if(self._current_channel_index == len(self._channels) - 1):
            self._current_channel_index = 0
        else:
            self._current_channel_index += 1

        self.print_channel_info()

    def play(self):
        current_channel = self.get_current_channel()
        if(current_channel.get_state() != ChannelState.PLAYING):
            current_channel.play()
        else:
            current_channel.stop()
        self.print_channel_info()

    def record(self):
        current_channel = self.get_current_channel()
        if(current_channel.get_state() != ChannelState.RECORDING):
            current_channel.start_record()
        else:
            current_channel.stop_record()
            current_channel.play()
        self.print_channel_info()

    def stop(self):
        for channel in self._channels:
            channel.stop()

    def print_record_info(self):
        audio = pyaudio.PyAudio()
        info = audio.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ",
                      audio.get_device_info_by_host_api_device_index(0, i).get('name'))
