import serial
import serial.tools.list_ports
import time


def find_arduino_ports():
    ports = serial.tools.list_ports.comports() # 列出所有串接埠

    arduino_ports = [port.device for port in ports if 'Arduino' in port.description or 'CH340' in port.description]
    print(f"Found Arduino port : {arduino_ports[0]}")
    return arduino_ports[0]

def serial_ports(port):
    ser = serial.Serial(port, 9600, timeout=2) # 開啟串列埠
    time.sleep(2) # 等待 Arduino 重啟
    return ser


def handleSerialCommand(ser, command):
    ser.write((command + '\n').encode('utf-8')) # 轉成bytes，並發送命令到 Arduino
    time.sleep(0.5)


def main():
    ser = None
    try:
        port = find_arduino_ports()
        ser = serial_ports(port)
        while True:
            command = input("Enter command : ") # 讀取使用者輸入的命令
            if command == '1' or command == 'flash_white_light_3_times': # flash_white_light_3_times
                handleSerialCommand(ser, 'flash_white_light_3_times')
            elif command == '2' or command == 'LED_cycle_3_times': # LED_cycle_3_times
                handleSerialCommand(ser, 'LED_cycle_3_times')
            elif command == 'c': # interrupt
                handleSerialCommand(ser, 'c')
            elif command == 'exit':
                handleSerialCommand(ser, 'c')
                break
            else:
                print("Invalid command. Please enter '1', '2', 'c' or 'exit'.")
    finally:
        if ser is not None:
            print("Close serial port")
            ser.close()

if __name__ == '__main__':
    main()

