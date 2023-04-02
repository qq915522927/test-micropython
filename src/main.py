from ssd1306 import SSD1306_I2C
import machine
from wifi import connect_wifi
import urequests 
# micropython on ESP32 call request to baidu.com and show the result in the  SSD1306 display


def main():
    connect_wifi()
    display  = init_ssd_1306()
    text = send_request_to_baidu()
    display.text(text, 40, 40)
    display.show()


def init_ssd_1306():
    i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
    display = SSD1306_I2C(128, 64, i2c)
    return display


def send_request_to_baidu():

    response = urequests.get('https://example.com')
    print(response.text)
    return response.text
 

main()



