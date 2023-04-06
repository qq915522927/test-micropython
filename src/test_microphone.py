import uos
import ustruct
import utime
import machine
from i2s_audio import play_audio_from_file

# Configure ADC pin and parameters
adc_pin = machine.Pin(35)
adc = machine.ADC(adc_pin)
adc.atten(machine.ADC.ATTN_11DB)
adc.width(machine.ADC.WIDTH_12BIT)

# Configure recording parameters
sampling_frequency = 8000
num_channels = 1
num_samples_per_buffer = 1024
num_bytes_per_sample = 2  # Each sample is 2 bytes (16 bits)

# Allocate a buffer to hold the audio data
buffer_size = num_channels * num_samples_per_buffer
audio_buffer = bytearray(buffer_size * num_bytes_per_sample)

# Record audio and save to internal flash memory
start_time = utime.ticks_ms()
file_name = "recording.wav"
with open(file_name, "wb") as f:
    # Write the WAV header
    f.write(b"RIFF")
    f.write(ustruct.pack("<I", 0))  # Placeholder for the file size
    f.write(b"WAVEfmt ")
    f.write(ustruct.pack("<I", 16))  # Size of format chunk
    f.write(ustruct.pack("<H", 1))  # Audio format (PCM)
    f.write(ustruct.pack("<H", num_channels))  # Number of channels
    f.write(ustruct.pack("<I", sampling_frequency))  # Sampling frequency
    f.write(ustruct.pack("<I", sampling_frequency * num_channels * num_bytes_per_sample))  # Data rate
    f.write(ustruct.pack("<H", num_channels * num_bytes_per_sample))  # Block align
    f.write(ustruct.pack("<H", num_bytes_per_sample * 8))  # Bits per sample
    f.write(b"data")
    f.write(ustruct.pack("<I", 0))  # Placeholder for the data size

    # Record audio and write to file
    print("Start recording (5 seconds)...")
    while utime.ticks_diff(utime.ticks_ms(), start_time) < 5000:  # Record for 5 seconds
        # Record a buffer of audio data
        for i in range(num_samples_per_buffer):
            sample = adc.read()
            ustruct.pack_into("<h", audio_buffer, i * num_bytes_per_sample, sample)
            utime.sleep_us(20)
        # Write the buffer to the file
        f.write(audio_buffer)
    print("Stop recording.")

    # Write the file size to the header
    data_size = utime.ticks_diff(utime.ticks_ms(), start_time) * sampling_frequency * num_channels * num_bytes_per_sample
    f.seek(4)
    f.write(ustruct.pack("<I", 36 + data_size))
    f.seek(40)
    f.write(ustruct.pack("<I", data_size))

play_audio_from_file(file_name)
