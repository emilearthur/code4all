# we like to write a program that scale all the images in a ZIP file to 640x480. 
# put in mind that someday we might want to change unzip and zip methods since we might consider TAR files someday 

import sys 
import shutil 
import zipfile 
from pathlib import Path 
from PIL import Image

class ZipProcessor: 
    def __init__(self, zipname):
        self.zipname = zipname 
        self.temp_directory = Path(f"unzipped-{zipname[:-4]}") 
    
    def process_zip(self):
        self.unzip_file() 
        self.process_files()
        self.zip_files()
    
    def unzip_file(self):
        self.temp_directory.mkdir() 
        with zipfile.ZipFile(self.zipname) as zip:
            zip.extractall(self.temp_directory) 
    
    def zip_files(self):
        with zipfile.ZipFile(self.zipname,"w") as file:
            for filename in self.temp_directory.iterdir():
                file.write(filename, filename.name)
        shutil.rmtree(self.temp_directory)      

class ZipReplace(ZipProcessor):
    def __init__(self, filename, search_string, replace_string):
        super().__init__(filename)  
        self.search_string = search_string
        self.replace_string = replace_string
    
    def process_files(self):
        """perform a search and replace on all files in the 
        temporal direcotry 
        """
        for filename in self.temp_directory.iterdir():
            with filename.open() as file:
                contents = file.read()
            contents = contents.replace(self.search_string, self.replace_string)
            with filename.open("w") as file:
                file.write(contents)

class ScaleZip(ZipProcessor):
    def process_file(self):
        """Scale each image in the directory to 640x480
        """
        for filename in self.temp_directory.iterdir():
            im = Image.open(str(filename)) 
            scaled = im.resize((640,480)) 
            scaled.save(filename) 

if __name__ == "__main__":
    ScaleZip(*sys.argv[1:4]).process_file