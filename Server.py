import math
import random
import socket
import time
from threading import Thread
import tkinter as tk

N = 8
max_obstacles_coordinate = math.sqrt(N * 8) / 2
L0 = 0.2
L0 /= 2
L1 = 1
L1 /= 2

CANVAS_SCALE = 50

def generate_obstacles(N):
    obstacles = []
    for i in range(N):
        obstacle = (random.uniform(-max_obstacles_coordinate, max_obstacles_coordinate),
                    random.uniform(-max_obstacles_coordinate, max_obstacles_coordinate))
        obstacles.append(obstacle)
    return obstacles
def check_collision(obstacle, quadcopter):
    x0 = quadcopter[0]
    y0 = quadcopter[1]
    x1 = obstacle[0]
    y1 = obstacle[1]

    # if (x1 - L1 <= x0 <= x1 + L1) and (y1 - L1 <= y0 <= y1 + L1):
    #     print(f'There is collision with obstacles ({x1}, {y1})')
    #     return True
    # else:
    #     return False

    if max(x0 - L0, x1 - L1) <= min(x0 + L0, x1 + L1) and max(y0 - L0, y1 - L1) <= min(y0 + L0, y1 + L1):
        print(f'There is collision with obstacles by coordinates ({x1}, {y1})')
        return True
    else:
        return False


def server(visualization):
    obstacles = generate_obstacles(N)
    visualization.draw_obstacles(obstacles)
    server_socket = socket.socket()
    server_socket.bind(('localhost', 8000))
    server_socket.listen(1)

    client_socket, _ = server_socket.accept()
    # print(f'Client {addr} connected')
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        quadcopter = tuple(float(i) for i in data.decode().split(','))


        for obstacle in obstacles:
            is_collision = check_collision(obstacle, quadcopter)
            visualization.draw_quadcopter(quadcopter, is_collision)
            if is_collision:
                break

    client_socket.close()
    server_socket.close()


class Visualization:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Visualization")
        self.canvas = tk.Canvas(self.root, width=max_obstacles_coordinate * 2 * CANVAS_SCALE,
                           height=max_obstacles_coordinate * 2 * CANVAS_SCALE, bg="white")
        self.quadcopter = None
        self.canvas.grid(row=0, column=0, padx=10, pady=10)
        self.root.update()

    def draw_obstacles(self, obstacles):
        for obstacle in obstacles:
            x = obstacle[0]
            y = obstacle[1]
            self.canvas.create_rectangle((x-L1+max_obstacles_coordinate)*CANVAS_SCALE,
                                         (y-L1+max_obstacles_coordinate)*CANVAS_SCALE,
                                         (x+L1+max_obstacles_coordinate)*CANVAS_SCALE,
                                         (y+L1+max_obstacles_coordinate)*CANVAS_SCALE,
                                         fill="green", outline="green")
            self.root.update()

    def draw_quadcopter(self, quadcopter, is_collision):
        x = quadcopter[0]
        y = quadcopter[1]
        self.canvas.delete(self.quadcopter)
        color = 'blue'
        if is_collision:
            color = 'red'

        self.quadcopter = (
            self.canvas.create_rectangle((x - L0 + max_obstacles_coordinate) * CANVAS_SCALE,
                                         (y - L0 + max_obstacles_coordinate) * CANVAS_SCALE,
                                         (x + L0 + max_obstacles_coordinate) * CANVAS_SCALE,
                                         (y + L0 + max_obstacles_coordinate) * CANVAS_SCALE,
                                         fill=color, outline=color))




def visualization():
    root = tk.Tk()
    root.title("Visualization")

    canvas = tk.Canvas(root, width=max_obstacles_coordinate*20*CANVAS_SCALE,
                       height=max_obstacles_coordinate*20*CANVAS_SCALE, bg="white")
    rec = canvas.create_rectangle(50, 250, 300, 500, fill="green", outline="green")
    canvas.grid(row=0, column=0, padx=10, pady=10)
    root.update()
    time.sleep(5)
    canvas.delete(rec)
    root.mainloop()

if __name__ == "__main__":
    print('Server started')
    viz = Visualization()
    server_thread = Thread(target=server, args=(viz, ))
    server_thread.start()
    viz.root.mainloop()



