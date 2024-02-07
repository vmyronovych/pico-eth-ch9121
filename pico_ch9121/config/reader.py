import time
from machine import UART, Pin

class ConfigReader:
    def __init__(self):
        self.__uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
        self.__configPin = Pin(14, Pin.OUT,Pin.PULL_UP)

    def begin_read(self):        
        self.__uart.read(self.__uart.any()) # flusing uart buffer before reading settings
        self.__configPin.value(0)
        time.sleep(0.01)
    
    def end_read(self):
        self.__leave_port_config_mode()
        self.__configPin.value(0)
        time.sleep(0.01)

    def device_ip(self):
        return self.__readIpString(0x61)
    
    def subnet_mask(self):
        return self.__readIpString(0x62)

    def gateway_ip(self):
        return self.__readIpString(0x63)
    
    def device_mac(self):
        return self.__readMacAddressString(0x81)
    
    # Possible values: 
    #   0x00: TCP server
    #   0x01: TCP client
    #   0x02: UDP server
    #   0x03: UDP client
    def port1_network_mode(self):
        return self.__readInt(0x60)
    
    def port1_device_port_number(self):
        return self.__readInt(0x64)
    
    def port1_destination_port_number(self):
        return self.__readInt(0x66)
    
    def port1_destination_ip(self):
        return self.__readIpString(0x65)
    
    def port1_uart_baud_rate(self):
        return self.__readInt(0x71)
    
    # Read port 1 serial port check bit data bit stop bit
    # 0x01 0x04 0x08
    # (1stop,noproofreading,8data)
    # Check:: 
    #   0x00: even
    #   0x01: add
    #   0x02: mark
    #   0x03: Space
    #   0x04: None
    def port1_uart_bits(self):
        return self.__readUartBitsString(0x72)
    
    # Serial port's timeout time in milliseconds
    # 0x01 (Serial timeout 1*5ms)
    def port1_timeout(self):
        return self.__readInt(0x73)
    
    def port2_enabled(self):
        return self.__readInt(0x90)

    # Possible values: 
    #   0x00: TCP server
    #   0x01: TCP client
    #   0x02: UDP server
    #   0x03: UDP client
    def port2_network_mode(self):
        return self.__readInt(0x90)
    
    def port2_device_port_number(self):
        return self.__readInt(0x91)
    
    def port2_destination_port_number(self):
        return self.__readInt(0x93)
    
    def port2_destination_ip(self):
        return self.__readIpString(0x92)
    
    def port2_uart_baud_rate(self):
        return self.__readInt(0x94)
    
    # Read port 2 serial port check bit data bit stop bit
    # 0x01 0x04 0x08
    # (1stop,noproofreading,8data)
    # Check:: 
    #   0x00: even
    #   0x01: add
    #   0x02: mark
    #   0x03: Space
    #   0x04: None
    def port2_uart_bits(self):
        return self.__readUartBitsString(0x95)
    
    # Serial port's timeout time in milliseconds
    # 0x01 (Serial timeout 1*5ms)
    def port2_timeout(self):
        return self.__readInt(0x96)
    
    def print(self):
        self.begin_read()

        print("\nDevice Network")
        print("==============")
        
        print(f'IP:                      {self.device_ip()}')
        print(f'Gateway:                 {self.gateway_ip()}')
        print(f'Subnet:                  {self.subnet_mask()}')
        print(f'MAC:                     {self.device_mac()}')

        print("\nUART 1")
        print("======")

        print(f'Network mode:             {self.port1_network_mode()}')
        print(f'Device port:              {self.port1_device_port_number()}')
        print(f'Destination port:         {self.port1_destination_port_number()}')
        print(f'Destination IP:           {self.port1_destination_ip()}')
        print(f'Baud rate:                {self.port1_uart_baud_rate()}')
        print(f'Bits (stop, check, data): {self.port1_uart_bits()}')
        print(f'Timeout:                  {self.port1_timeout()}ms')
        
        print("\nUART 2")
        print("======")

        print(f'Network mode:             {self.port2_network_mode()}')
        print(f'Device port:              {self.port2_device_port_number()}')
        print(f'Destination port:         {self.port2_destination_port_number()}')
        print(f'Destination IP:           {self.port2_destination_ip()}')
        print(f'Baud rate:                {self.port2_uart_baud_rate()}')
        print(f'Bits (stop, check, data): {self.port2_uart_bits()}')
        print(f'Timeout:                  {self.port2_timeout()}ms')

        self.end_read()
    
    # Leave serial port configuration mode (Only on the serial port negotiating side Formula is valid)
    def __leave_port_config_mode(self):
        self.__read(0x5e)

    def __readIpString(self, command):
        ipBytes = self.__read(command)
        return "{}.{}.{}.{}".format(ipBytes[0], ipBytes[1], ipBytes[2], ipBytes[3])
    
    def __readInt(self, command):
        return int.from_bytes(self.__read(command),'little')

    def __readMacAddressString(self, command):
        ipBytes = self.__read(command)
        return "{:02X}:{:02X}:{:02X}:{:02X}:{:02X}:{:02X}".format(
            ipBytes[0], ipBytes[1], ipBytes[2], ipBytes[3], ipBytes[4], ipBytes[5])

    def __readUartBitsString(self, command):
        ipBytes = self.__read(command)
        return "{},{},{}".format(ipBytes[0], ipBytes[1], ipBytes[2])
    
    def __read(self, command):
        fullCommand = [0x57, 0xab]
        fullCommand.append(command)
        self.__uart.write(bytearray(fullCommand))
        while True:
            while self.__uart.any() > 0: # check if there is response
                return self.__uart.read() # read response
            time.sleep(0.01) # sleep before checking for response again


# Print configuration when this module is run as standalone python script
if __name__ == '__main__':
    config = ConfigReader()
    config.print()
