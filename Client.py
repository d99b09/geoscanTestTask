import socket
import time
import random
from Server import max_obstacles_coordinate
import numpy as np

def send_coordinates(client_socket):
    while True:
        x = random.uniform(-max_obstacles_coordinate, max_obstacles_coordinate)
        y = random.uniform(-max_obstacles_coordinate, max_obstacles_coordinate)
        msg = f'{x},{y}'.encode()
        client_socket.send(msg)
        time.sleep(1)

def send_quadcopter_path(client_socket):
    step = 0.2
    for x in np.arange(-max_obstacles_coordinate, max_obstacles_coordinate, step):
        for y in np.arange(-max_obstacles_coordinate, max_obstacles_coordinate, step):
            msg = f'{x},{y}'.encode()
            client_socket.send(msg)
            time.sleep(0.1)


def main():
    client_socket = socket.socket()
    connected = False
    while not connected:
        try:
            client_socket.connect(('localhost', 8000))
            connected = True
            print('Client connection')
        except ConnectionRefusedError:
            print('Waiting connection')
            time.sleep(1)

    send_quadcopter_path(client_socket)
    client_socket.close()

if __name__ == '__main__':
    main()

