import wifi
import tts
import i2s_audio

wifi.connect_wifi()
response = tts.get_tts("你好， 我是傻妞！ 我是来自2025年的智能手机，how are you! 哈哈哈。我正在测试一些长的文本：：：")
i2s_audio.play_audio_from_http_stream(response)


