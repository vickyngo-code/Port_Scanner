# Port_Scanner
A multithreaded port scanner written in Python using socket

# TODO:
Add command line argument parser.

# Current Issue:
Results printed using multithread ended up printing in a messy order and layout.

A solution to this issue is to use lock, however this will reduce the speed of the program to that of a singlethread port scanner.
To enable the lock, uncomment the lines in the function port_scan()

