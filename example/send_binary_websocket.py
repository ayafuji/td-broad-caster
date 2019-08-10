import threading
import time

from PIL import Image, ImageDraw
from websocket import create_connection

ws = create_connection("ws://test2.ayafuji.com:8082")
h = []
lock = threading.Lock()
SIZE = [300, 300]
prev_send_time = time.time()


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


t1 = threading.Thread(target=draw_image)
t1.start()
while True:
    start_time = time.time()
    if len(h) != 0 and len(h) == SIZE[0] * SIZE[1] * 3:
        byte = len(h)
        print(h)
        send_time = time.time()
        ws.send_binary(h)
        send_elapsed_time = time.time() - send_time
        diff = (time.time() - prev_send_time)
        fps = 1 / diff
        prev_send_time = time.time()
        print(" fps :" + str(fps) + ", byte[kb] : " + str(byte / 1000) + ", sendo time : " + str(
            send_elapsed_time * 1000000))

    elapsed_time = time.time() - start_time
    time.sleep(1 / 15)
