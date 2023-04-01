import network

# Define the WiFi network name and password
ssid = 'CU_UD7h'
password = '18301929561'

def connect_wifi():
    # Create a WiFi station interface object and connect to the network
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)

    # Wait until the interface is connected to the network
    while not sta_if.isconnected():
        pass

    # Print the IP address assigned to the interface by the DHCP server
    print('Connected to network', ssid)
    print('Network config:', sta_if.ifconfig())
