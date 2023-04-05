import wifi
#import tts
#import i2s_audio
#import urequests
#import time
import gc

print("Allocated Memory 0:")
# websocket to to use asr
# https://ai.baidu.com/ai-doc/SPEECH/2k5dllqxj
print(gc.mem_alloc())
# while True:
#     i2s_audio.play_audio_from_file("text2audio.wav")
#     time.sleep(1)
#with open('text2audio.wav', 'rb') as speech_file:
#    speech_data = speech_file.read()

def main():
    # wifi.connect_wifi()
    print("Allocated Memory 1:")
    print(gc.mem_alloc())
    # a = 3
    # print("Allocated Memory 1:")
    # print(gc.mem_alloc())
    # print("Free Memory:")
    # print(gc.mem_free())
    # tts.getasr("text2audio.wav")
    # question = "你好， 我是傻妞！ 我是来自2025年的智能手机，how are you! 哈哈哈。我正在测试一些长的文本：：："
    # conversation_id = perform_a_conversation(question)
    # question = "帮我测试一下翻译的功能"
    # conversation_id = perform_a_conversation(question, conversation_id=conversation_id)
    # question = "齐天大圣"
    # conversation_id = perform_a_conversation(question, conversation_id=conversation_id)

def perform_a_conversation(question, conversation_id=None):
    question = question.encode("utf-8")
    conversation_id, answer = ask_chatgpt(question, conversation_id)
    response = tts.get_tts(answer)
    i2s_audio.play_audio_from_http_stream(response)
    return conversation_id


def ask_chatgpt(question, conversation_id=None):
    url = "http://192.168.1.13:5001/conversations"
    if conversation_id:
        url += "?conversation_id=" + str(conversation_id)
    response = urequests.post(url, data=question)
    reply = response.json()
    return reply['conversation'], reply['reply']


main()
