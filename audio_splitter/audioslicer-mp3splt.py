# A tool that, given an input file and a precise start time, outputs a series of Unix-timestamped files to a specified directory meant for CiTR's archiver
# Setup - windows
#   download add libav to your PATH
#   install mp3splt and add it to your PATH
#   requires python packages dateutil and pytimezone - install with pip
#Setup - linux (NOT TESTED AT ALL ON LINUX)
#   install libav and mp3splt using your distro's package manager

import sys
import time
from time import sleep
import os
from os.path import splitext
from datetime import datetime
#because the standard datetime.strptime doesn't like timezones we bring in the big guns
from dateutil import parser,tz
import pytz
import ntpath

# Enter your given "constants" here

# default for now is in the user's home
# Yes, this is Windows only right now, sue me
# this is where the one second clips go
working_directory = ("e:/converted/")
#empty directory used by mp3splt to save files to temporarily
staging_dir = ("e:/mp3splt/")

#this is the source audio file - it can be anywhere really
#TODO: drag and drop file to convert (interface TBD)
working_file = ntpath.basename(sys.argv[1]) #set to this for filename specified via command line arg
#working_file = "" #set to this for filename specified here

#log file location
#for now, we don't have the option of disabling this
log_file = "audioslicer-log.txt"

# pydub does things in milliseconds
one_second = 1000

#TODO: Confirm archiver folder behaviour around leap days and DST
#@params: AudioSegment infile, String workingdir, String start
def slice_file( infile, workingdir, stagingdir, start ):

    print ("Converting " + working_file)

    mp3splitcommand = "mp3splt -xn -t 0.1 -d " + staging_dir + " -o @n \"" + infile +"\""
    #do the slicing by starting another command line, not sure if this is windows-only or not. Just care that it works for now
    os.system("start /wait cmd /c %s", mp3splitcommand)
    #rename them because mp3splt can't do custom incremented names the way we want
    increment_file_numbers(staging_dir, start)

    #loop to move files out of the staging directory and into the proper working directory - we don't just
    #bulk move them because we always can't assume the files are all from the same day
    for file_name in os.listdir(staging_dir):
        #get the timestamp from the file
        name = os.splitext(file_name)
        timestamp = int(isdigit(name))
        arr = datefolderfromtimestamp(timestamp)
        ensure_dir(working_directory + "/" + arr[0] + "/" + arr[1] + "/" + arr[2] + "/")
        source_filename = os.path.normpath(staging_dir + "/" + file_name )
        dest_filename = os.path.normpath(working_directory + "/" + arr[0] + "/" + arr[1] + "/" + arr[2] + "/" + file_name)
        #move that file
        os.rename(source_filename,dest_filename)

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
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

# Guides user to specifying the start time, without microseconds decimal - the archiver doesn't use microseconds
# @returns:  a POSIX timestamp as a string without decimals (timestamps are usually of type float)
def gettimestamp():
    confirm = 0
    while (confirm == 0):
        indate = input("\nEnter the (local!) start date of the audio file (format: MM-DD-YYYY) ")
        intime = input("Enter the (also local!) start time of the audio file to the nearest second, 24 hour clock. Midnight is 00:00:00. (format: HH:MM:SS) ")
        bool_in_is_dst = query_yes_no("\nIs DST active at the start of the audio file? (If you're past the point of \"spring forward\", then answer yes). \nIf you're not sure about DST, make sure to look up what second DST takes effect. Or just avoid having audio files starting during DST.", None)
        if bool_in_is_dst == True:
            in_is_dst = "PDT"
            offset="-0700" #yes I've painstainkingly confirmed that these offsets are working as intended. Programming with timezones, not even once.
        else:
            in_is_dst = "PST"
            offset = "-0800"
        print('\n')
        datestring = indate + " " + intime + offset
        human_readable_time = datetime.strptime(indate+" "+intime, "%d-%m-%Y %H:%M:%S")
        start_time = parser.parse(datestring)
        #convert the time we have to a posix timestamp
        start_timestamp = int(datetime.timestamp(start_time))

        temp_string = "You entered the following information: (YYYY-MM-DD HH:MM:SS) \n%s %s \nPOSIX TIMESTAMP - %s \nIs this information correct?" % (human_readable_time,in_is_dst,start_timestamp);
        response = query_yes_no(temp_string, None)
        if response == True:
            confirm = 1;
        else:
            print ("\n Okay, I'll ask you again ... \n \n")
            sleep(1)
            confirm = 0;

    return str(start_timestamp)

#Files from the logger are in the format "2016.01.09-15.30.00-S.mp3"
def gettimestampfromfile( name ):
    #parse the filename
    year = name[:4]
    month = name[5:7]
    day = name[8:10]
    hour = name[11:13]
    minute = name[14:16]
    second = name[17:19]

    indate = day + "-" + month + "-" + year
    intime = hour + ":" + minute + ":" + second
    local = pytz.timezone ("America/Los_Angeles")
    naive = datetime.strptime (indate+" "+intime, "%d-%m-%Y %H:%M:%S")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone (pytz.utc)
    start = datetime.timestamp(utc_dt)

    return str(int(start))

# @params: an integer POSIX timestamp. Returns the year, month, and day associated with the timestamp in Vancouver, BC. Takes into account DST. Returns as an array corresponding to the folder for that timestamp on the archiver
def datefolderfromtimestamp( timestamp ):
    #datetime.fromtimestamp appprently uses your system's locale to return the date relevant to your location AND IT DOES DST HALLELUJAH.
    # date_time is a string of YYYY-DD-MM HH:MM:SS
    date_time = str(datetime.fromtimestamp(timestamp))
    #
    year = date_time[:4]
    month = date_time[5:7]
    day = date_time[8:10]
    if (month[0] == '0'):
        month  = month[1]
    if (day[0] == '0'):
        day = day[1]
    retarray = [year, month, day]
    return retarray

from os.path import splitext

#Function to rename the files that mp3splt spits out - expects (for now) the directory to be empty except for the files we want to rename, and that each file is 01.mp3 ... 02.mp3, etc
def increment_file_numbers(directory, start_timestamp):
        for file_name in os.listdir(directory):
                split = splitext(file_name)
                #Files are 1.mp3 ... 2.mp3 .... etc
                file_number = int(split[0])
                new_number = file_number + start_timestamp - 1 #we must minus one because the first file is 1.mp3, not 0.mp3
                new_name = str(new_number) + "-second.mp3"
                old_path = directory + "\\" + file_name
                new_path = directory + "\\" + new_name
                os.rename(old_path, new_path)

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

    #print ("================================================\n=== CiTR Audio Archive File Preparation Tool ===\n================================================\n \n")
    #print ("The CiTR Archiver conists of many second-long files which it has as mp3s, each with a unix timestamp. For example: %s-second.mp3 is the file from %s, local time, or %s UTC \n \nUNIX timestamps are by definition based on UTC." % ( current_timestamp,current,current_utc ) )
    #print ("It is currently %s local time" % (current) )

    #get the user to define what the time stamp is for now.
    #timestamp returned from this function is a string, no decimals in the timestamp
    #TODO: use argc to know if there's command line arg passed or not
    #timestamp = gettimestamp()

    #get the timestamp from the filename
    timestamp = gettimestampfromfile(working_file)
    #print (timestamp)

    #Prep the output directory
    ensure_dir(working_directory)
    #and the staging directory
    ensure_dir(staging_dir)

    #write that we're starting a batch job to the log file
    log = open( os.path.normpath( working_directory + "/" + log_file), 'a' )
    log.write( str(datetime.now()) + "    ")
    log.write( "Converting " + working_file + "\n")
    log.close()

    #do the audio conversion now that we've carefully specified our parameters
    slice_file( sys.argv[1], working_directory, staging_dir, timestamp)
    
if __name__ == "__main__":
    main()
