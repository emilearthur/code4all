# import library 
import sys
from bitarray import bitarray
from PIL import Image
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, futures
from pathlib import Path 

def compress_chunk(chunk) -> bytearray:
    """
    This method compresses that data using the run-length encoding and returns a bytearray containing the packed data. 
    Where bitarray is a like a list of ones and zeros, bytearray is like a list of bytes objects. 

    This algorithm; first set the last variable to the type of bit in the current run (either True or False).  It then 
    loops over the bits, counting each one, util it finds on e that is different. When it does, it constucts a new byte 
    by making the leftmost bit of the byte (the 128 position) eith a zero or a one, depending on what the last variable 
    contained. Then, it resets the counter and repeats the operation. Once the loop is done, it creates one last bytes 
    for the last run and returns the result. 
    """
    compressed = bytearray() 
    count = 1 
    last = chunk[0] 
    for bit in chunk[1:]:
        if bit != last:
            compressed.append(count | (128*last)) #bitwise OR operation performed 
            count = 0 
            last = bit 
        count += 1 
    compressed.append(count | (128*last)) 
    return compressed 


def compress_row(row:bytearray) -> bytearray:
    """
    A function that compresses a row of image data. 

    It accept bitaarray named row. It splits it into chunks that are each 127 bits wide using the split_bits function. 
    Then, it compresses each of thos chunks using the compress_chunk function, concatenating the results into bytearray, 
    which is returned. 
    """
    compressed = bytearray() 
    chunks = split_bits(row, 127)
    for chunk in chunks:
        compressed.extend(compress_chunk(chunk))
    return compressed


def split_bits(bits, widith):
    """
    This is a generator 
    """
    for i in range(0, len(bits), widith):
        yield bits[i : i+widith]


def compress_in_executor(executor, bits, width) -> bytearray:
    """
    Here we wrap the functions in a method that runs everything in a provided executor. 

    This function splits the incoming bits into row based on the width of the image using the same split_bits function
    above.

    Note: The function will compress any sequence of bits, although it would bloat, rather than compress binary data that 
    has frequent changes in bit value. Black and white images are definitely good candidates for compression algorithm in 
    question. 
    """
    row_compressors = [] 
    for row in split_bits(bits, width):
        compressor = executor.submit(compress_row, row)
        row_compressors.append(compressor) 
    
    compressed = bytearray() 
    for compressor in row_compressors:
        compressed.extend(compressor.result()) 
    return compressed


def compress_image(in_filename, out_filename, executor=None):
    """
    This function loads an image file using third-party pillow module, converts it to bits and compresses it. 

    """
    executor = executor if executor else ProcessPoolExecutor()
    #executor = executor if executor else ThreadPoolExecutor()
    with Image.open(in_filename) as image:
        bits = bitarray(image.convert('1').getdata()) # image.convert() call changes image to black and white (one bit) mode while getdata() returns an iterator over those values
        width, height = image.size # getting width and height of image 
    
    compressed = compress_in_executor(executor, bits, width) 

    with open(out_filename, 'wb') as file:
        file.write(width.to_bytes(2, 'little'))
        file.write(height.to_bytes(2, 'little'))
        file.write(compressed) 


def single_image_main():
    in_filename, out_filename = sys.argv[1:3]
    executor = ProcessPoolExecutor() 
    #executor  = ThreadPoolExecutor(4)
    compress_image(in_filename, out_filename, executor=executor)


def compress_dir(in_dir, out_dir):
    if not out_dir.exists():
        out_dir.mkdir() 
    
    executor = ProcessPoolExecutor() 
    #executor  = ThreadPoolExecutor(4)
    for file in (f for f in in_dir.iterdir() if f.suffix == ".bmp"):
        out_file = (out_dir / file.name).with_suffix(".rle") 
        executor.submit(compress_image, str(file), str(out_dir))
    #when using threadpool uncomment the code below and line 108 and comment on 107 and 109-111
    #futures = []
    #for file in (f for f in in_dir.iterdir() if f.suffix == ".bmp"):
    #    out_file = (out_dir / file.name).with_suffix(".rle") 
    #    executor.submit(compress_image, str(file), str(out_dir))
    #    futures.append(executor.submit(compress_image, str(file), str(out_file)))
    #    for future in futures:
    #        future.result()


def dir_images_main():
    in_dir, out_dir = (Path(p) for p in sys.argv[1:3]) 
    compress_dir(in_dir, out_dir)




if __name__ == "__main__":
    #single_image_main()
    dir_images_main()



    