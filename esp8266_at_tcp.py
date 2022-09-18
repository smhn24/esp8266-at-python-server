import sys
from serial import Serial


def serial_init(PORT: str, BAUDRATE: int) -> Serial:
    """Returns a connected Serial object"""
    try:
        serial = Serial(PORT, BAUDRATE)
    except:
        print("Can not connect to this port!")
        sys.exit(1)
    return serial


def create_tcp_server(serial: Serial) -> int:
    serial.write(b'AT+RST\r\n')
    serial.read_until(b'ready\r\n')
    serial.write(b'AT\r\n')
    serial.read_until(b'OK\r\n')
    serial.write(b'AT+CWMODE=3\r\n')
    serial.read_until(b'OK\r\n')
    serial.write(
        f'AT+CWSAP="{module_SSID}","{module_PASSWORD}",5,4\r\n'.encode()
    )
    serial.read_until(b'OK\r\n')
    serial.write(f'AT+CWJAP="{router_SSID}","{router_PASSWORD}"\r\n'.encode())
    serial.read_until(b'OK\r\n')
    serial.write(b'AT+CIPMUX=1\r\n')
    serial.read_until(b'OK\r\n')
    serial.write(b'AT+CIPSERVER=1,80\r\n')
    serial.read_until(b'OK\r\n')
    serial.write(b'AT+CIPSTA?\r\n')
    ip_result = serial.read_until(b'OK\r\n').decode().split('"')[1]
    return ip_result


router_SSID = input("Enter router SSID: ")
router_PASSWORD = input("Enter router password: ")
if len(router_PASSWORD) < 8:
    print("Password must be at least 8 characters long!")
    sys.exit(1)

module_SSID = input("Enter module SSID: ")
module_PASSWORD = input("Enter module password: ")
if len(module_PASSWORD) < 8:
    print("Password must be at least 8 characters long!")
    sys.exit(1)


PORT = input("Enter serial port: ")
BAUDRATE = input("Enter serial baudrate:(default is 115200) ") or 115200


serial = serial_init(PORT, BAUDRATE)
router_ip = create_tcp_server(serial)
local_ip = '192.168.4.1'

print(
    f"Server is running on: {router_ip}:80 in router & on: {router_ip}:80 on module"
)
