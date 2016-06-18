import os
from os.path import splitext

def increment_file_numbers(directory, start_timestamp):
        # iterate over every file name in the directory
        for file_name in os.listdir(os.path.abspath(directory)):
                split = splitext(file_name)
                #Files are 1.mp3 ... 2.mp3 .... etc
                file_number = int(split[0])
                #we must minus one because the first file is 1.mp3, not 0.mp3
                new_number = file_number + start_timestamp - 1
                new_name = str(new_number) + "-second.mp3"
                old_path = os.path.normpath(directory + "/" + file_name)
                new_path = os.path.normpath(directory + "/" + new_name)
                os.rename(old_path, new_path)

#path to the files to rename
PATH = ("e:/mp3splt/"")
start = 1466288035

# Let's increment all the files w/ numbers above 11
increment_file_numbers(PATH,start)
