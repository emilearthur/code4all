"""
The open() built-in function is used to open a file and return a file object. 

we could supply the value "a" as a mode arg, to append to the end of the file, rather 
than completely overwriting existing file content.

"b" as mode arg to open binary file.  

"wb" as mode arg to write binary file 
"rb" as mode arg to read binary file 

Once the file is open for reading, we can call read, readline or readlines method to get 
content of the file. 
The read method returns the entire contents of the file as a string or byte object depending
on whether there is "b" in the mode argument. 
It's also possible to read a fixed number of bytes from a file. We pass an integer arg to 
the read mthod, describing how many bytes we want to read.  The next call to read will load 
the next sequence of bytes and so on. We can do this inside a while loop to read the entire 
file in manageable chunks. 
The readline method returns a single line from the file (where each line ends in a newline, 
carriage return or both depending the os on which the file was created).
The readlines method returns a list of all the lines in the file. It's not safe to apply on 
a large file because of memory issues. 
For readability, and to avoid reading a large file into memory at once, it is often better 
to use a for loop directly on a file object. For text files, it will read each line, one at 
a time, and we can process it inside the loop body. For binary files, it's better to read 
fixed-sized chunks of data using the read() method, passing a parameter for the maximum 
number of bytes to read.

The write method on file objects writes a string(or bytes, for binary data) object to the
file. It can called repeatedly to write multiple string, one after the other. 
The writelines method does not append a new line after each item in the sequence.

The close method should be called when one finishes reading or writing the file, to ensure 
any buffered writes are written to the disk, that the file has been properly clearn up and 
all resources assocaited with the file are released back to the OS. 

"""

contents = "Some file contents"
file = open("filename","w") 
file.write(contents) 
file.close() 