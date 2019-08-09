from websocket import create_connection

ws = create_connection("ws://test2.ayafuji.com:5001")
print("Sending 'Hello, World'...")

# ws.send("Hello, World")
ws.send_binary([100, 100, 100])
print("Sent")

ws.close()
