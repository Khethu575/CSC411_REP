import socket
import threading
import queue

# Global variables
HOST = 'localhost'  # Host address
PORT = 1234  # Port number
BUFFER_SIZE = 1024  # Buffer size for receiving messages
NUM_PRODUCERS = 2  # Number of producer threads
NUM_CONSUMERS = 1  # Number of consumer threads

# Queue to hold the messages
message_queue = queue.Queue()

# Function to handle client connections
def handle_client(client_socket):
    while True:
        try:
            # Receive message from the client
            message = client_socket.recv(BUFFER_SIZE)
            
            if message:
                # Add the message to the queue
                message_queue.put(message)

            else:
                # If no message is received, close the connection
                client_socket.close()
                break

        except:
            # In case of any error, close the connection
            client_socket.close()
            break


# Function for producer threads
def producer_thread():
    while True:
        # Accept a connection from a client
        client_socket, client_address = server_socket.accept()

        # Create a thread to handle the client connection
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


# Function for consumer threads
def consumer_thread(consumer_id):
    while True:
        # Get the message from the queue
        message = message_queue.get()

        # Process the message (in this example, we just print it)
        print(f"Consumer {consumer_id} received: {message.decode()}")


# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Listen for client connections
server_socket.listen()

# Create producer threads
for _ in range(NUM_PRODUCERS):
    threading.Thread(target=producer_thread).start()

# Create consumer threads
for i in range(NUM_CONSUMERS):
    threading.Thread(target=consumer_thread, args=(i+1,)).start()
