
import threading
import random
import time
import xml.etree.ElementTree as ET

import socket

# Structure to hold student information
class ITStudent:
    def __init__(self, name, id, programme, courses, marks):
        self.name = name
        self.id = id
        self.programme = programme
        self.courses = courses
        self.marks = marks

# Global variables
buffer = []
empty = threading.Semaphore(10)
full = threading.Semaphore(0)
mutex = threading.Semaphore(1)

# Function to generate random student information
def generateStudentInfo():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    name = ''.join(random.choice(alphabet) for _ in range(5))
    id = str(random.randint(10000000, 99999999))
    programme = "Programme" + str(random.randint(1, 3))
    courses = ["CSC411", "CSC493", "CSC461", "CSC400", "CSC405"]
    marks = [random.randint(0, 100) for _ in range(5)]
    return ITStudent(name, id, programme, courses, marks)

# Function to convert student information to XML format
def convertToXML(student):
    root = ET.Element("student")
    
    nameElement = ET.SubElement(root, "name")
    nameElement.text = student.name
    
    idElement = ET.SubElement(root, "id")
    idElement.text = student.id
    
    programmeElement = ET.SubElement(root, "programme")
    programmeElement.text = student.programme
    
    coursesElement = ET.SubElement(root, "courses")
    for i in range(len(student.courses)):
        courseElement = ET.SubElement(coursesElement, "course")
        
        nameElement = ET.SubElement(courseElement, "name")
        nameElement.text = student.courses[i]
        
        markElement = ET.SubElement(courseElement, "mark")
        markElement.text = str(student.marks[i])
    
    xml = ET.tostring(root).decode()
    return xml

# Function to generate student XML files
def producer():
    for count in range(10):  # Iterate 10 times
        time.sleep(random.randint(1, 3))  # Sleep for random time

        # Generate student information
        student = generateStudentInfo()
        
        # Convert to XML format
        xml = convertToXML(student)
        
        # Create XML file
        filename = "student" + str(count) + ".xml"
        with open(filename, "w") as file:
            file.write(xml)
        
        # Insert integer to buffer
        empty.acquire()
        mutex.acquire()
        buffer.append(count)
        mutex.release()
        full.release()
        
        print("Producer: Created", filename)
        
        count += 1
        
        # Sleep for random time
        time.sleep(random.randint(1, 3))

# Function for the consumer thread
def consumer():
    count = 0
    while count < 10:
        # Remove integer from buffer
        full.acquire()
        mutex.acquire()
        count = buffer.pop(0)
        mutex.release()
        empty.release()

        # Read XML file
        filename = "student" + str(count) + ".xml"
        with open(filename, "r") as file:
            xml = file.read()
        
        # Delete XML file
        # os.remove(filename)
        
        # Parse XML and gather student information
        root = ET.fromstring(xml)
        name = root.find("name").text
        id = root.find("id").text
        programme = root.find("programme").text
        courses = []
        marks = []
        for courseElement in root.find("courses"):
            courses.append(courseElement.find("name").text)
            marks.append(int(courseElement.find("mark").text))
        
        student = ITStudent(name, id, programme, courses, marks)
        
        # Calculate average mark
        average = sum(student.marks) / len(student.marks)
        
        # Determine pass/fail
        passFail = "Pass" if average >= 50 else "Fail"
        
        # Print student information
        print("Consumer: Student Name:", student.name)
        print("Consumer: Student ID:", student.id)
        print("Consumer: Programme:", student.programme)
        print("Consumer: Courses and Marks:")
        for i in range(len(student.courses)):
            print("Consumer: -", student.courses[i] + ":", student.marks[i])
        print("Consumer: Average Mark:", average)
        print("Consumer: Pass/Fail:", passFail)
        
         #Sleep for random time
        time.sleep(random.randint(1, 3))

#Create producer and consumer threads
producerThread = threading.Thread(target=producer)
consumerThread = threading.Thread(target=consumer)

# Start threads
producerThread.start()
consumerThread.start()

# Wait for threads to finish
producerThread.join()
consumerThread.join()

#SOCKET PROGRAMMING

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5000))
server_socket.listen(1)
print('The server is ready to produce items')

client_socket, client_address = server_socket.accept()
print('Client connected:', client_address)

items = ['student1', 'student2', 'student3', 'student4', 'student5', 'student6', 'student7', 'student8', 'student9', 'student10']
for item in items:
    client_socket.send(item.encode())
    print('Producing:', item)

client_socket.close()
server_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5000))
print('Connected to the server')

while True:
    client_socket.listen(1)
    client_socket, client_address = server_socket.accept()
    item = client_socket.recv(1024).decode()
    if not item:
        break
    print('Consuming:', item)

client_socket.close()

