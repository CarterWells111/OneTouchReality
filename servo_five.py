import socket
import serial
import time
from serial.serialutil import SerialException

SERIAL_PORT = 'COM6'
BAUD_RATE = 9600
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

def send_to_arduino(ser,data):
    if not ser.is_open:
        try:
            ser.open()
        except SerialException:
            print("cannot onpen serial")
            return False
    try:
        command = f"{data}\n"  
        ser.write(command.encode('utf-8'))
        print(f"Sent: {data}")
    except SerialException as e:
        print(f"write error: {e}")
        print(f"fail sent: {e}")

def handle_client(connection,add,ser):
    try:
        print(f'Client connected: {add}')
        while True:
            data = connection.recv(1024)
            if not data:
                print(f'Client {add} disconnected')
                break
            
            decoded_data = data.decode('utf-8').strip()
            print(f"Received: {decoded_data}")

            commands = decoded_data.splitlines()
            for cmd in commands:
                if ',' in cmd:
                    parts = cmd.split(',')
                    if len(parts) == 2:
                        finger = parts[0].strip()
                        angle = parts[1].strip()
                        cmd_str = f"{finger} {angle}\n"
                        send_to_arduino(ser,cmd_str)
                        print(f"Sent to Arduino: {cmd_str.strip()}")
                    else:
                        print(f"Ignoring invalid command: {cmd}")
                else:
                    print(f"Ignoring invalid format: {cmd}")
                
    except ConnectionResetError:
        print(f"Client {add} forcibly closed the connection")
    except Exception as e:
        print(f'Error with client {add}: {e}')
    finally:
        connection.close()
        print(f"Connection to {add} closed")


def main():
    ser = None
    try:
        ser = serial.Serial(SERIAL_PORT,BAUD_RATE,timeout=1,exclusive=True)
        print(f"Serial port {SERIAL_PORT} opened at {BAUD_RATE} baud")
    except SerialException as e:
        print(f"Failed to open serial port: {e}")
        print("Continuing without serial connection...")

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as ss:
        ss.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        
        try:
            ss.bind((SERVER_HOST,SERVER_PORT))
            ss.listen(5)
            print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}...")

            while True:
                try:
                    connection,add = ss.accept()
                    handle_client(connection,add,ser)
                except KeyboardInterrupt:
                    print("Server shutting down by user request...")
                    break
                except Exception as e:
                    print(f"Server error: {e}")
                    time.sleep(1)

        except Exception as e:
            print(f"Server setup failed: {e}")
        finally:
            ser.close()
            print("Serial port closed")

if __name__ == "__main__":
    main()