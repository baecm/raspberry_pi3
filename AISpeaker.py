import RPi.GPIO as GPIO
from Button import Button
from LED import LED

import pyaudio
import wave

import time

# parameters for recording
FORMAT = pyaudio.paInt16
CHANNELS = 2
SAMPLE_RATE = 44100
CHUNK = 4096
FILENAME = 'tmp.wav'


class AISpeaker(Button, LED):
    def __init__(self, button_pin=29, led_pin=31):
        # GPIO interaction
        Button.__init__(self, pin=button_pin)
        LED.__init__(self, pin=led_pin)
        GPIO.add_event_callback(self.button_pin, callback=self.listener)
        # record
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        # check button state
        self.button_pressed = None

        while True:
            time.sleep(.01)

    def recording(self):
        self.stream = self.pa.open(format=FORMAT, rate=SAMPLE_RATE, channels=CHANNELS,
                                   frames_per_buffer=CHUNK, input=True, stream_callback=self.callback)

    def write_wave_file(self):
        # write .wav file
        wav_file = wave.open(FILENAME, 'wb')
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(self.pa.get_sample_size(FORMAT))
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(b''.join(self.frames))
        wav_file.close()

    def initialize(self):
        # initialize audio and stream to next recording
        self.pa = pyaudio.PyAudio()
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()
        self.frames = []

    def send_to_server(self):
        # TODO: 서버로 .wav 파일 전송
        import os
        os.remove('./tmp.wav')
        # TODO: 서버에서 전송된 결과

    def callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return in_data, pyaudio.paContinue

    def listener(self, pin):
        # button pressed
        self.button_pressed = GPIO.input(self.button_pin) is GPIO.LOW
        if self.button_pressed:
            self.on()
            self.recording()
        # button released
        else:
            self.off()
            self.write_wave_file()
            self.initialize()
            self.send_to_server()




ai_speaker = AISpeaker()
