import socketio

sio = socketio.Client()


@sio.event
def connect():
    print("Connected to server")


@sio.event
def disconnect():
    print("Disconnected from server")


def send_message(message):
    sio.emit("update_map", message)


if __name__ == "__main__":
    server_url = "http://127.0.0.1:5000"

    sio.connect(server_url)

    while True:
        message = input(
            'Enter a message to send to the server (or type "exit" to quit): '
        )

        if message.lower() == "exit":
            break

        send_message(message)

    sio.disconnect()
