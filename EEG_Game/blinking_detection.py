"""import socket

# Define the IP address and port number for the UDP server
UDP_IP = "127.0.0.1"  # The IP address configured in the OpenBCI GUI
UDP_PORT = 12345      # The port number configured in the OpenBCI GUI

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for UDP packets on {UDP_IP}:{UDP_PORT}")

# Function to process received data
def process_data(data):
    print("Received data:", data)

try:
    while True:
        # Receive data from the OpenBCI GUI
        data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
        process_data(data)
except KeyboardInterrupt:
    print("Server stopped.")
    sock.close()"""

import socket
import json
from datetime import datetime
import time
import statistics

# Define the IP address and port number for the UDP server
UDP_IP = "127.0.0.1"  # The IP address configured in the OpenBCI GUI
UDP_PORT = 12345  # The port number configured in the OpenBCI GUI

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for UDP packets on {UDP_IP}:{UDP_PORT}")

def filter_unconsious_blink(list):
    ### Return True if amplitude is all below True. We will consider this as unconsious blinkning 
    threshold = 10
    for i in list:
        if i >= threshold:
            return False
    return True

# Function to process received data
def process_data(data):
    try:
        # Decode the received data
        data_str = data.decode('utf-8')
        # Parse JSON data
        parsed_data = json.loads(data_str)
        # print(parsed_data)

        if parsed_data.get('type') == 'fft' and 'data' in parsed_data:
            fft_data = parsed_data['data']
            # print(datetime.now())

            second_channel_amplitude = fft_data[1]
            
            frequencies = [(i * 200 / len(second_channel_amplitude)) for i in range(len(second_channel_amplitude))]

            #Frequency from 4.8 to 17.6
            amplitude_interest = second_channel_amplitude[3:12]
            frequencies_interest = frequencies[3:12]

            if filter_unconsious_blink(amplitude_interest):
                # print('unconcious_blink')
                return 0
            # elif max(amplitude_interest) > 30:
            #     print("THAT WAS A HARD BLINK")
            #     print(max(amplitude_interest))
            else:
                # print("BLINK DETECTED")
                # print(max(amplitude_interest))
                return statistics.mean(amplitude_interest) 

                # Further processing can be done here
        else:
            print("Invalid data format received.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

try:
    # last_snapshot_time = time.time()
    # while True:
    #     current_time = time.time()
    #     snapshot_interval = 0.5
    #     if current_time - last_snapshot_time >= snapshot_interval:
    #         # Receive data from the OpenBCI GUI
    #         data, addr = sock.recvfrom(8196)  # Buffer size is 1024 bytes
    #         process_data(data)
    #  
    #        last_snapshot_time = current_time

    # Receive data from the OpenBCI GUI
    avr_amplitude = 0
    blink_count = 0
    while True:
        data, addr = sock.recvfrom(8196)  # Buffer size is 1024 bytes
        avr_amplitude_2 = process_data(data)

        if (avr_amplitude == avr_amplitude_2) and (avr_amplitude_2 == 0):
            #The user is not blinking, skip
            avr_amplitude = 0
            blink_count = 0
            continue
        elif avr_amplitude < avr_amplitude_2:
            #This means that blinks are starting to be detected
            # print("Blink Detected")
            # print("Blinking started")
            if blink_count == 0:
                print("Blinking DETECTED!!!")


                blink_count += 1
                avr_amplitude = avr_amplitude_2
            else:
                avr_amplitude = avr_amplitude_2
                # print("Blinking_ending")
            # print(avr_amplitude, avr_amplitude_2)
            avr_amplitude = avr_amplitude_2
        elif (avr_amplitude > avr_amplitude_2):
            avr_amplitude = avr_amplitude_2
            blink_count = 0
            # print(avr_amplitude, avr_amplitude_2)
            #This means that the peak ended. 
            # if blink_count == 0:
            #     print("Blinking DETECTED!!!")
            #     blink_count += 1
            #     avr_amplitude = avr_amplitude_2
            # else:
            #     avr_amplitude = avr_amplitude_2
            #     # print("Blinking_ending")

except KeyboardInterrupt:
    print("Server stopped.")
    sock.close()
