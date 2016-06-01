#from pydub import AudioSegment
import sys
import time
from datetime import datetime

#filename

##Example use of the AudioSegment library
#sound = AudioSegment.from_mp3("/path/to/file.mp3")
#
## len() and slicing are in milliseconds
#halfway_point = len(sound) / 2
#second_half = sound[halfway_point:]
#
## Concatenation is just adding
#second_half_3_times = second_half + second_half + second_half
#
## writing mp3 files is a one liner
#second_half_3_times.export("/path/to/new/file.mp3", format="mp3")

#inputfile = Adio

def main():
    current = datetime.now();
    current_utc = datetime.utcnow();
    
    #get those partial seconds out of the time to illustrate our point
    current = current.replace(microsecond=0);
    current_utc = current_utc.replace(microsecond=0);
    #strip the last two elements out so we can't see the .0 at the end, since the archiver doesn't use that
    current_timestamp = int(datetime.timestamp(current));
        
    print ("========================================\n = CiTR Audio Archive File Preparation Tool = \n ======================================== \n \n");
    print ("The CiTR Archiver conists of many second-long files which is has as mp3s, each with a unix timestamp. For example: %s-second.mp3 is the file from %s, local time, or %s UTC \n \nUNIX timestamps are by definition based on UTC." % ( current_timestamp,current,current_utc ) );
    print ("It is currently %s local time" % (current) );
    
    indate = input("Enter the local start date of the audio file (format: DD-MM-YYYY) ");
    intime = input("Enter the local start time of the audio file to the nearest second, 24 hour clock. Midnight is 00:00:00. (format: HH:MM:SS) ");
    in_is_dst = input("Is DST currently active? (If you're past the point of spring forward, then answer yes). Yes=1,No=0.   ");
    print("If you're not sure about DST, make sure to look up what second DST takes effect. Or just avoid having audio files starting during DST");
    print('\n');
    start_timestamp = time.strptime(indate + " " + intime, "%d-%m-%Y %H:%M:%S");
    start_timestamp.tm_isdst = int(in_is_dst);
    print (start_timestamp.tm_isdst);
    
    #print (start_timestamp);

if __name__ == "__main__":
    main()
