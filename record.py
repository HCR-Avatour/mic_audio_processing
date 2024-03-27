import pyaudio
import wave
import numpy as np

from tuning import Tuning
import usb.core
import usb.util
import time

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
Mic_tuning = Tuning(dev)

RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 1 # change base on firmwares, 1_channel_firmware.bin as 1 or 6_channels_firmware.bin as 6
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 1  # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "test.wav"
dir = Mic_tuning.direction

p = pyaudio.PyAudio()

def calculate_volume_scaling_factor(dir):
    target_angle = 90
    # Calculate the absolute difference from the target angle
    if(dir > 180):
        dir = dir - 180
    angle_diff = abs(dir - target_angle)
    # Normalize the difference based on the maximum possible difference (180 degrees)
    normalized_diff = angle_diff / 90.0
    # Calculate scaling factor: 1.0 (no change) when doa is 90, decreasing to 0.0 at 0 or 180 degrees
    scaling_factor = 1.0 - normalized_diff
    return scaling_factor


stream = p.open(
            rate=RESPEAKER_RATE,
            format=p.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            input=True,
            input_device_index=RESPEAKER_INDEX,)

print("* recording")

frames = []

for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    np_data = np.fromstring(data, dtype=np.int16)

    #vol_scaling = calculate_volume_scaling_factor(dir)
    #scaled_data = np_data * vol_scaling
    #frames.append(scaled_data.astype(np.int16).tostring())

    
    if Mic_tuning.direction < 30 or Mic_tuning.direction > 150:
        #Lower volume from behind
        np_data = np_data * 0.3
        frames.append(np_data.astype(np.int16).tostring())

        #Generate silent data for the chunk
        #silent_data = np.zeros(chunk_size, dtype=np.int16).tobytes()
        #frames.append(silent_data)
    else:
        frames.append(data)
    
        
    #frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(RESPEAKER_CHANNELS)
wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
wf.setframerate(RESPEAKER_RATE)
wf.writeframes(b''.join(frames))
wf.close()