# Producer code
import random
import xml.etree.ElementTree as ET
import socket

class ITstudent:
    def __init__(self):
        self.name = ""
        self.student_id = ""
        self.program = ""
        self.courses = []
        self.marks = []

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

    def generate_random_data(self):
        # Generate random data for the student
        self.name = "Student " + str(random.randint(1, 100))
        self.student_id = str(random.randint(10000000, 99999999))
        self.program = "Program " + str(random.randint(1, 3))
        num_courses = random.randint(2, 5)
        self.courses = ["Course " + str(i) for i in range(1, num_courses + 1)]
        self.marks = [random.randint(40, 100) for _ in range(num_courses)]

def wrap_into_xml(student):
    # Create XML structure and populate with student information
    root = ET.Element("Student")
    name_element = ET.SubElement(root, "Name")
    name_element.text = student.name
    id_element = ET.SubElement(root, "ID")
    id_element.text = student.student_id
    program_element = ET.SubElement(root, "Program")
    program_element.text = student.program
    courses_element = ET.SubElement(root, "Courses")
    for course, mark in zip(student.courses, student.marks):
        course_element = ET.SubElement(courses_element, "Course")
        name_sub_element = ET.SubElement(course_element, "Name")
        name_sub_element.text = course
        mark_sub_element = ET.SubElement(course_element, "Mark")
        mark_sub_element.text = str(mark)
    # Return the XML representation
    return ET.tostring(root)

# Create a socket for communication with the consumer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 12345))
s.listen(1)
conn, addr = s.accept()

# Generate and send 10 instances of ITstudent to the consumer
for _ in range(10):
    # Generate a new instance of ITstudent with random data
    student = ITstudent()
    student.generate_random_data()

    # Wrap the student information into XML format
    xml_data = wrap_into_xml(student)

    # Send the XML data to the consumer
    conn.send(xml_data)

# Send a termination message to the consumer
conn.send(b'TERMINATE')

# Close the connection and the socket
conn.close()
s.close()

# Consumer code
import xml.etree.ElementTree as ET
import socket

# Create a socket for communication with the producer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 12345))

# Receive and process instances of ITstudent from the producer
while True:
    # Receive XML data from the producer
    xml_data = s.recv(1024)
    if xml_data == b'TERMINATE':
        break

    # Process the XML data (e.g., extract student information)
    root = ET.fromstring(xml_data)
    name_element = root.find('Name')
    id_element = root.find('ID')
    program_element = root.find('Program')
    courses_element = root.find('Courses')
    courses = []
    marks = []
    for course_element in courses_element.findall('Course'):
        name_sub_element = course_element.find('Name')
        mark_sub_element = course_element.find('Mark')
        courses.append(name_sub_element.text)
        marks.append(int(mark_sub_element.text))

    # Do something with the extracted data (e.g., print it)
    print(f"Name: {name_element.text}, ID: {id_element.text}, Program: {program_element.text}, Courses: {courses}, Marks: {marks}")

# Close the connection and the socket
s.close()
