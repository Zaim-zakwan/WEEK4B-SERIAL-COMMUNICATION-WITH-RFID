import serial
import time
import json

# Serial port for RFID reader and Arduino
RFID_PORT = "COM10"   
ARDUINO_PORT = "COM7"  
BAUD_RATE_RFID = 9600  
BAUD_RATE_ARDUINO = 9600  

# Load configuration
def load_config():

    with open("config.json", "r") as file:
        print(file)
        return json.load(file)

# Initialize RFID and Arduino connections
try:
    # Set up RFID serial connection
    rfid_serial = serial.Serial(RFID_PORT, BAUD_RATE_RFID, timeout=1)
    print(f"Connected to RFID reader on {RFID_PORT} with baud rate {BAUD_RATE_RFID}")

    # Set up Arduino serial connection
    arduino_serial = serial.Serial(ARDUINO_PORT, BAUD_RATE_ARDUINO, timeout=1)
    print(f"Connected to Arduino on {ARDUINO_PORT} with baud rate {BAUD_RATE_ARDUINO}")

    # Load config settings
    config = load_config()
    authorized_cards = config["authorized_cards"]
    servo_angle_granted = config["servo_angle_granted"]
    servo_angle_denied = config["servo_angle_denied"]

    last_card_id = None
    last_read_time = 0
    debounce_time = 3  # Seconds to wait before reading the next card

    # Main loop
    while True:
        if rfid_serial.in_waiting > 0:  # Check if data is available
            card_data = rfid_serial.read(rfid_serial.in_waiting).hex()
            current_time = time.time()

            # Check if the card ID is different or enough time has passed since the last read
            if (card_data != last_card_id or (current_time - last_read_time) >= debounce_time):
                last_card_id = card_data
                last_read_time = current_time
                print(f"Card ID: {card_data}")

                if card_data in authorized_cards:
                    print("Access granted.")
                    arduino_serial.write(b"G")  # Send 'G' for granted access
                    arduino_serial.write(str(servo_angle_granted).encode())
                else:
                    print("Access denied.")
                    arduino_serial.write(b"D")  # Send 'D' for denied access
                    arduino_serial.write(str(servo_angle_denied).encode())

            time.sleep(0.5)  # Short delay to avoid continuous reads

except Exception as e:
    print(f"Error: {e}")

finally:
    if 'rfid_serial' in locals():
        rfid_serial.close()
    if 'arduino_serial' in locals():
        arduino_serial.close()
    print("Serial connections closed.")
