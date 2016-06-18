from pydub import AudioSegment

# pydub does things in milliseconds
ten_seconds = 10 * 1000
one_second = 1000
#Examples
#first_10_seconds = song[:ten_seconds]
#last_5_seconds = song[-5000:]

song = AudioSegment.from_mp3("2016.01.04-09.00.00-S.mp3")

#print("Test")

#last_second = song[-ten_seconds:]

#last_second.export("out/testing.mp3", format="mp3")

#Cool that worked, now lets try looping

#find the duration of the input clip in millliseconds
duration_in_milliseconds = len(song)

#grab each one second slice and save it from the first second to the last whole second in the file
for i in range(0,duration_in_milliseconds,1*one_second):
    print ("Second number %s \n" % (int(i/1000)) )
    offset = i + one_second
    current_second = song[i:offset];
    filename = "out/" + str(int(i/1000)) + ".mp3"
    current_second.export(filename, format="mp3")

    #it works! now we just have to combine it with the other stuff to start from the
    #right unix timestamp and check behaviour of last second (where there might not
    #be a complete second of audio left)
    
