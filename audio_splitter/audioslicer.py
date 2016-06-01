# A tool that, given an input file and a precise start time, outputs a series of Unix-timestamped files to a specified directory meant for CiTR's archiver

import sys
import time
from datetime import datetime
from pydub import AudioSegment

# Enter your given "constants" here

# default for now is in the user's home
# Yes, this is Windows only right now, sue me
# this is where the one second clips go
working_directory = os.path.normpath("c:/Users/" + os.getenv('USERNAME') + "/audiosplitter/")

#this is the source audio file - it can be anywhere really
#TODO: expand to grabbing user input about first file in sequence and smartly iterate over files that are back-to-back using Concatenation
#TODO: drag and drop file to convert (interface TBD)
working_file = "insert_file_name_here"

# pydub does things in milliseconds
ten_seconds = 10 * 1000
one_second = 1000

#TODO: 	export files in directories by year, month,and day so they can be copypasted to the archiver
#		requires smartly tracking the unix timestamp and switching over between folders
#		(covert timestamp to the array format and extract the year, month, day and shove it into the filename string)
#TODO: Confirm archiver folder behaviour around leap days and DST
def slice_file( AudioSegment infile, String workingdir, String start ):
	#find the duration of the input clip in millliseconds
	duration_in_milliseconds = len(infile)

	song = infile
	#grab each one second slice and save it from the first second to the last whole second in the file
	for i in range(0,duration_in_milliseconds,1*one_second):
	    print ("Second number %s \n" % (int(i/1000)) )
	    offset = (i + one_second)
	    current_second = song[i:offset]
	    filename = working_directory + str(int(start) + (int(i/1000))) + ".mp3"
	    current_second.export(filename, format="mp3")

#helper function to ensure the working directory exists where f is the input directory
def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

#helper function to elicit a y/n response from the user given the question contained in the question string
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

# Guides user to specifying the start time, without microseconds decimal - the archiver doesn't use microseconds
#returns:  a POSIX timestamp as a string without decimals (timestamps are usually of type float)
def gettimestamp():
	confirm = 0
	while (confirm = 0):
		indate = input("Enter the (local!) start date of the audio file (format: DD-MM-YYYY) ")
	    intime = input("Enter the (also local!) start time of the audio file to the nearest second, 24 hour clock. Midnight is 00:00:00. (format: HH:MM:SS) ")
	    bool_in_is_dst = query_yes_no("Is DST active at the start of the audio file? (If you're past the point of \"spring forward\", then answer yes). \n If you're not sure about DST, make sure to look up what second DST takes effect. Or just avoid having audio files starting during DST.", None)
		if bool_in_is_dst = TRUE:
			in_is_dst = 1
		else:
			in_is_dst = 0
	    print('\n')
	    start_time = time.strptime(indate + " " + intime, "%d-%m-%Y %H:%M:%S")
	    start_time.tm_isdst = int(in_is_dst)

		temp_string = "You entered the following information: %s \n Is this information correct?" % (start_time);
		response = query_yes_no(temp_string, None)
		if (response = TRUE)
			confirm = 1;
		else
			print ("\n Okay, I'll ask you again ... \n \n")
			sleep(1)
			confirm = 0;

	#convert the time we have to a posix timestamp
	start_timestamp = datetime.timestamp(start_time)
	return str(int(start_timestamp))

def main():

	#Some timestamp information right now for the user to see how the archiver works (or really, get reminded because you only use this when the archiver has
	# a hard drive kick the bucket)
    current = datetime.now();
    current_utc = datetime.utcnow();

    #get those partial seconds out of the time to illustrate our point
    current = current.replace(microsecond=0)
    current_utc = current_utc.replace(microsecond=0)
    #strip the last two elements out so we can't see the .0 at the end, since the archiver doesn't use that
    current_timestamp = int(datetime.timestamp(current))

    print ("================================================\n=== CiTR Audio Archive File Preparation Tool ===\n================================================\n \n")
    print ("The CiTR Archiver conists of many second-long files which it has as mp3s, each with a unix timestamp. For example: %s-second.mp3 is the file from %s, local time, or %s UTC \n \nUNIX timestamps are by definition based on UTC." % ( current_timestamp,current,current_utc ) )
    print ("It is currently %s local time" % (current) )

	#timestamp returned from this function is a string, no decimals in the timestamp
    timestamp = gettimestamp()

	#Prep the output directory
	ensure_dir(working_direcory)

	#do the audio conversion now that we've carefully specified our parameters
	slice_file( AudioSegment.from_mp3(working_file), working_direcory, timestamp)

	print "\n JOB COMPLETE"
	sleep( 0.5 )

if __name__ == "__main__":
    main()
