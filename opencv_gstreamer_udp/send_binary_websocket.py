import array
import threading
import time

import cv2
import numpy as np
from PIL import Image, ImageDraw
from websocket import create_connection

ws = create_connection("ws://test2.ayafuji.com:8082")
h = []

test_144 = 'C:/Users/yuukitakada/Documents/td-broad-caster\example/test_144p.mp4'
test_360 = 'C:/Users/yuukitakada/Documents/td-broad-caster\example/test_360p.mp4'
cap = cv2.VideoCapture(test_360)

SIZE = [140, 140]


def draw_image():
    global h
    global lock

    x_pos = 0
    counter = 0

    while True:
        lock.acquire()
        h = []
        img = Image.new('RGB', (SIZE[0], SIZE[1]))
        draw = ImageDraw.Draw(img)
        x_offset = x_pos  # 100 * math.sin(counter)
        y_offset = 100  # 100 * math.cos(counter)
        draw.ellipse((x_offset - 50, y_offset - 50, x_offset, y_offset), fill=(255, 0, 0), outline=(0, 0, 0))
        pixels = list(img.getdata())

        for d in pixels:
            h.append(d[0])
            h.append(d[1])
            h.append(d[2])

        x_pos = x_pos + 3
        if x_pos > 500:
            x_pos = 0
        counter = counter + 0.1
        lock.release()

        time.sleep(1 / 15)


ratio = 1.0
SIZE = (255 * ratio, 144 * ratio)


def video_capture_loop():
    global h
    while cap.isOpened():
        h = []
        ret, data = cap.read()
        data = cv2.resize(data, dsize=(int(SIZE[0]), int(SIZE[1])))
        if ret:
            h = np.array(data).reshape(-1, ).astype(np.uint8)
        time.sleep(1 / 15)

mean_arr = []
mean_window = 30
mean_counter = 0

t1 = threading.Thread(target=video_capture_loop)
t1.start()
while True:
    start_time = time.time()

    if len(h) != 0.0 and len(h) == int(SIZE[0]) * int(SIZE[1]) * 3:
        arr = array.array('B', h).tobytes()
        send_time = time.time()
        ws.send_binary(arr)
        send_elapsed_time = time.time() - send_time

        if len(mean_arr) < mean_window:
            mean_arr.append(send_elapsed_time)
        else:
            mean_arr[mean_counter] = send_elapsed_time
            mean_counter = mean_counter + 1
            if mean_counter > len(mean_arr) - 1 or mean_counter > mean_window:
                mean_counter = 0

        print("[SEND] byte[kb] : " + str(len(arr) / 1000) + ", send time : " + str(
            send_elapsed_time * 1000) + ", mean fps: " + str(1000 / (sum(mean_arr) / mean_window * 1000)))

    elapsed_time = time.time() - start_time
    time.sleep(1 / 10)
