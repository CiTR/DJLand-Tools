import sys
import os
from pydub import AudioSegment
import ntpath

# Yes, this is Windows only right now, sue me
# this is where the one second clips go
working_directory = ("e:/converted-test/")

#this is the source audio file
working_file = ntpath.basename(sys.argv[1])

#log file location
#for now, we don't have the option of disabling this
log_file = "audioslicer-log.txt"

# pydub does things in milliseconds
one_second = 1000

def slice_file( infile, workingdir):
    #find the duration of the input clip in millliseconds
    duration_in_milliseconds = len(infile)

    print ("Converting " + working_file + "  (", end="", flush=True)

    song = infile
    #grab each one second slice and save it from the first second to the last whole second in the file
    for i in range(0,duration_in_milliseconds,1*one_second):
        offset = (i + one_second)
        current_second = song[i:offset]
        filename = os.path.normpath(working_directory + str(int(i/1000)) + "-second.mp3")
        current_second.export(filename, bitrate='128k', format='mp3', parameters=['-codec:a', 'libmp3lame'])

        #indicate some sort of progress is happening by printing a dot every three minutes processed
        if( i % (3*60*one_second) == 0 ):
            print ('.', end="",  flush=True)

    print (")")

#helper function to ensure the working directory exists where f is the input directory
def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def main():
    print("\nLoading Audio File ... \n")
    #Prep the output directory
    ensure_dir(working_directory)
    slice_file( AudioSegment.from_mp3(sys.argv[1]), working_directory)
if __name__ == "__main__":
    main()
