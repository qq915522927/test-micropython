# coding=utf-8
import json
import urequests
from url_encode import url_encode
import binascii


# 百度api
API_KEY = ""  # will be set at set_api_key
SECRET_KEY = ""


def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config


def set_api_key():
    config = load_config()
    print(config)
    global API_KEY, SECRET_KEY
    API_KEY = config["baidu_api_key"]
    SECRET_KEY = config["baidu_secret_key"]


set_api_key()

ACCESS_TOKEN = ""  # need to get from baidu dynamicly

# 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
# 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美
PER = 4
# 语速，取值0-15，默认为5中语速
SPD = 5
# 音调，取值0-15，默认为5中语调
PIT = 5
# 音量，取值0-9，默认为5中音量
VOL = 7
# 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
AUE = 6

FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
FORMAT = FORMATS[AUE]

CUID = "123456PYTHON"

TTS_URL = 'http://tsn.baidu.com/text2audio'


def fetch_token():
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}"
    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = urequests.post(url, headers=headers, data=payload)
    result = response.json()
    return result['access_token']


def get_tts(text):
    text = url_encode(text)
    # print(f"Encoded Text: {text}")
    global ACCESS_TOKEN
    if not ACCESS_TOKEN:
        ACCESS_TOKEN = fetch_token()

    url = TTS_URL + "?"
    url += f'tok={ACCESS_TOKEN}&'
    url += f'tex={text}&'
    url += f'per={PER}&'
    url += f'spd={SPD}&'
    url += f'pit={PIT}&'
    url += f'vol={VOL}&'
    url += f'aue={AUE}&'
    url += f'cuid={CUID}&'
    url += 'lan=zh&ctp=1'

    # print('test on Web Browser' + TTS_URL + '?' + data)
    print(url)
    response = urequests.get(url, stream=True)

    if not response.status_code == 200:
        print("TTS failed: {}".format(response.text))
        print("TTS failed: HTTP Status {}".format(response.status_code))
        raise Exception("TTS failed: {}".format(response.text))
    return response

speech_data = None

def getasr(filename):
    global speech_data
    # https://ai.baidu.com/ai-doc/SPEECH/jkhq0ohzz
    format = filename[-3:]

    global ACCESS_TOKEN
    if not ACCESS_TOKEN:
        ACCESS_TOKEN = fetch_token()

    with open(filename, 'rb') as speech_file:
        speech_data = speech_file.read()

    length = len(speech_data)
    speech_data = binascii.b2a_base64(speech_data, newline=False)
    speech_data = str(speech_data, 'utf-8')

    params = {'dev_pid': 80001,
              # "lm_id" : LM_ID,    #测试自训练平台开启此项
              'format': format,
              'rate': 16000,
              'token': ACCESS_TOKEN,
              'cuid': CUID,
              'channel': 1,
              'speech': speech_data,
              'len': length
              }
    headers = {
        "Content-Type": 'application/json'
    }
    r = urequests.post(url="http://vop.baidu.com/server_api",
                       headers=headers, data=json.dumps(params))
    work = r.json()
    print(f"ASR Result: {work}")
    print(work)
    return (work['result'][0])
