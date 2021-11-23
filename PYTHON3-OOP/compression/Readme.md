# About

In this project we build a basic image compression tool. It will take black white image (with
1 bit per pixel, either on or off) and attempt to compress it using a very basic form of compression known as run-length encoding.
Included are a black and white BMP images (which are easy to read data into and present the number plenty of opportunity to improve on file size)

## Run-length encoding

Run-length encoding takes a sequence of bits and replaces any strings of repeated bits with the number of bits that are repeated.

For eg, the string 000011000 might be replace with 04 12 03 to indicate that four zeros are followed by two ones and then three zeros. We break each row into 127-bit chunks, we did not pick 127 bits arbitrarily. 127 different values can be encoded into 7 bits, which means that if a row contains all ones or zeros, we can store in a single byte, with the first bit indicating whether it is a row of 0s or a row of 1s and the remaining seven bits indicating how many of that bit exists.

Breaking up the images into block has another advantage:
*we can process individuals blocks into parallel without them depending on each other
Breaking up the images into block has another disadvantage:
*If a run has just a few ones and zeros in it, then it will take up more space in the compressed file. When breakup long runs into block, we may end up creating more of these small runs and bloat the size of the file.

In this excercise, our compressed file will store two bytes little-endian integers at the beginning of the file representating the width and height of the completed file. Then, it will write bytes representating the 127 bit chunks of each row.
