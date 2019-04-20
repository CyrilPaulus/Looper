from enum import Enum
import queue
import pyaudio
import threading
import wave


class ChannelState(Enum):
    IDLE = 1
    PLAYING = 2
    RECORDING = 3


class Channel:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16

    def __init__(self, label, device_index, sample_rate, channels):
        self._state = ChannelState.IDLE
        self._label = label
        self._filename = "channel_" + label + ".wav"
        self._channels = channels
        self._device_index = device_index
        self._record_queue = queue.Queue()
        self._sample_rate = sample_rate

        self._player_wave = None

    def get_state(self):
        return self._state

    def get_label(self):
        return self._label

    def print_info(self):

        state = ""
        if self._state == ChannelState.IDLE:
            state = 'Idle'
        elif self._state == ChannelState.PLAYING:
            state = 'Playing'
        elif self._state == ChannelState.RECORDING:
            state = 'Recording'

        print("Channel {}: {} ({})".format(
            self._label, state, self._device_index))

    def start_record(self):
        if(self._state == ChannelState.PLAYING):
            self.stop()

        self._state = ChannelState.RECORDING
        threading.Thread(target=self._record_thread).start()

    def stop_record(self):
        self._state = ChannelState.IDLE

    def play(self):
        if (self._state == ChannelState.RECORDING):
            self.stop_record()
        threading.Thread(target=self._play_loop).start()

    def _play_loop(self):
        player = pyaudio.PyAudio()
        stream = player.open(format=self.FORMAT,
                             channels=self._channels,
                             rate=self._sample_rate,
                             output=True)

        file = wave.open(self._filename, 'rb')
        self._state = ChannelState.PLAYING

        while self._state == ChannelState.PLAYING:
            data = file.readframes(self.CHUNK)
            if len(data) == 0:
                file.rewind()
                data = file.readframes(self.CHUNK)
            stream.write(bytes(data))

        stream.close()
        player.terminate()
        file.close()

    def stop(self):
        self._state = ChannelState.IDLE

    def _record_thread(self):
        file = wave.open(self._filename, 'wb')
        file.setnchannels(self._channels)
        file.setframerate(self._sample_rate)
        audio = pyaudio.PyAudio()
        file.setsampwidth(audio.get_sample_size(self.FORMAT))

        stream = audio.open(format=self.FORMAT, channels=self._channels,
                            rate=self._sample_rate, input=True, input_device_index=self._device_index,
                            frames_per_buffer=self.CHUNK)
        while self._state == ChannelState.RECORDING:
            data = stream.read(self.CHUNK)
            file.writeframes(data)
        stream.stop_stream()
        stream.close()
        audio.terminate()
        file.close()

    def _record_callback(self, indata, frame, time, status):
        self._record_queue.put(indata.copy())
