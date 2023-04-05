from machine import I2S
from machine import Pin
import struct


"""
sd -- DIN
sck --- BCLK
ws -- LRC
GND -- GND
5V或3.3V -- VCC
"""
 
# 初始化引脚定义
sck_pin = Pin(27) # 串行时钟输出
ws_pin = Pin(26)  # 字时钟
sd_pin = Pin(25)  # 串行数据输出


"""
sck 是串行时钟线的引脚对象
ws 是单词选择行的引脚对象
sd 是串行数据线的引脚对象
mode 指定接收或发送
bits 指定样本大小（位），16 或 32
format 指定通道格式，STEREO（左右声道） 或 MONO(单声道)
rate 指定音频采样率（样本/秒）
ibuf 指定内部缓冲区长度（字节）
"""

 

# wavtempfile = "maifu.wav"
wavtempfile = "test-sample.wav"
with open(wavtempfile,'rb') as f:
    # Read the WAV file header
    riff, size, fformat = struct.unpack('<4sI4s', f.read(12))
    fmt_header, fmt_size, audio_format, channels, samplerate, byterate, \
    block_align, bits_per_sample = struct.unpack('<4sIHHIIHH', f.read(24))
    print("声道数：", channels)
    print("采样宽度：", bits_per_sample)
    print("采样频率：", samplerate)
    # 跳过文件的开头的44个字节，直到数据段的第1个字节
    # 初始化i2s
    audio_out = I2S(1, sck=sck_pin, ws=ws_pin, sd=sd_pin, mode=I2S.TX, bits=16, format=I2S.MONO, rate=samplerate * channels, ibuf=20000)

    pos = f.seek(44)

    # 用于减少while循环中堆分配的内存视图
    wav_samples = bytearray(1024)
    wav_samples_mv = memoryview(wav_samples)
    print("开始播放音频...")
    #并将其写入I2S DAC
    while True:
        try:
            num_read = f.readinto(wav_samples_mv)
            # WAV文件结束
            if num_read == 0:
                break

            # 直到所有样本都写入I2S外围设备
            num_written = 0
            while num_written < num_read:
                num_written += audio_out.write(wav_samples_mv[num_written:num_read])
        except Exception as ret:
            print("产生异常...", ret)
            break
