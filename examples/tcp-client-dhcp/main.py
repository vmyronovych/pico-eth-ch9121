import time
from pico_ch9121 import config
from pico_ch9121.config import reader, writer
from pico_ch9121.socket import ClientSocket

# CH9121 configuration
cw = writer.ConfigWriter()
cw.begin()
cw.dhcp_on() # Enable DHCP on CH9121 so the chip can automatically obtain IP address from your DHCP server (e.g. from home's router)
cw.gateway_ip("192.168.1.1") # Set here your's gateway ip address (e.g. router's ip)
cw.subnet_mask("255.255.255.0") # Set here your's subnet mask
cw.p1_tcp_client() # TCP Client Mode
cw.end()

# Print current configuration of CH9121
cr = reader.ConfigReader()
cr.print()

# Prepare socket for communication
socket = ClientSocket("192.168.1.51", 6969) # Change ip and port here to the ip and port of your TCP Server

# Send and read data to/from TCP Server
while True:
    response = socket.send("Hello from CH9121")
    print(response)
    time.sleep(10)