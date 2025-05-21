# LED.py

import serial
import serial.tools.list_ports
import time


class ArduinoController():
    def __init__(self):
        self.ser = None
        self.is_running = False
        port = self.find_arduino_port()
        self.connect_serial(port)

    def find_arduino_port(self):
        ports = serial.tools.list_ports.comports()
        arduino_ports = [port.device for port in ports if 'Arduino' in port.description or 'CH340' in port.description]
        if not arduino_ports:
            raise Exception("No Arduino port found.")
        print(f"Found Arduino port: {arduino_ports[0]}")
        return arduino_ports[0]

    def connect_serial(self, port):
        self.ser = serial.Serial(port, 9600, timeout=2)
        time.sleep(2)  # 等待 Arduino 重啟
        print("Serial connected.")

    def send_command(self, command):
        if self.ser and self.ser.is_open:
            self.ser.write((command + '\n').encode('utf-8'))
            time.sleep(0.5)

    # ===== 提供給 GUI 呼叫的控制函式 =====
    def start_led(self):
        self.send_command("start")
        self.is_running = True

    def exit_led(self):
        self.send_command("exit")
        self.stop_led()
        self.is_running = False


    def flash_led_3_times(self):
        if not self.is_running:
            print("LED is not running. Please start it first.")
            return
        self.send_command("flash_white_light_3_times")

    def cycle_flash(self):
        if not self.is_running:
            print("LED is not running. Please start it first.")
            return
        self.send_command("LED_cycle_3_times")

    def stop_led(self):
        if not self.is_running:
            print("LED is not running. Please start it first.")
            
        self.send_command("c")

    def close(self):
        if self.ser and self.ser.is_open:
            print("Close serial port")
            self.ser.close()

if __name__ == '__main__':
    controller = ArduinoController()
    try:
        while True:
            command = input("Enter command: ")
            if command == '1' or command == 'flash_white_light_3_times':
                controller.flash_led_3_times()
            elif command == '2' or command == 'LED_cycle_3_times':
                controller.cycle_flash()
            elif command == 'c':  # interrupt
                controller.stop_led()
            elif command == 'exit':
                controller.stop_led()
                controller.close()
                break
            elif command == 'start':
                controller.start_led()
            else:
                print("Invalid command. Please enter '1', '2', 'c' or 'exit'.")
    finally:
        controller.close()
    