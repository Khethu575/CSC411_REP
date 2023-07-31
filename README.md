# CSC411_REP
bash
git clone https://github.com/Khethu575/CSC411
cd repository
npm install
System Integration project

Implementation of the Producer-Consumer:
The code is a Python program that simulates a producer-consumer problem using threads. The program generates random student information and converts it to an XML format. The producer thread creates 10 XML files, each containing student information. It then inserts an integer to a buffer, signalling the consumer thread that a file is ready for processing. The consumer thread removes the integer from the buffer, reads the corresponding XML file, parses it, and calculates the average mark for the student. It then determines whether the student passes or fails and prints their information. The program uses semaphores to control access to the buffer and mutexes’ to prevent race conditions.

More information on how this implmentation works is on the PDF file we submitted.
