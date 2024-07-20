import speech_recognition as sr
import os
import wikipedia
from gtts import gTTS
import random 
import datetime
import calendar
import warnings
warnings.filterwarnings('ignore')

#recording the audio and return it as a string
def recordAudio():

    #record the audio 
    r=sr.Recognizer() # creating a recognizer object

    #now open th mic and start recording
    with sr.Microphone() as source:
        print('Say something !')
        audio = r.listen(source)

    #use googles speech recognition
    data = ''
    try:
        data=r.recognize_google(audio)
        print('You said : '+data)
    except sr.UnknowValueError:
        print('Google Speech recognition could not understand the audio, unknown error!')
    except sr.RequestError as e:
        print('Request results from Google Speech recognition service error '+e)

    return data 

# A function to get the virtual assistant response
def assistantResponse(text):

    print(text)

    # converting the text to speech
    myobj = gTTS(text = text , lang='en', slow=False)

    # saving the converted audio into a file
    myobj.save('assistant_virtual.mp3')

    # playing the converted file
    os.system('start assistant_virtual.mp3')

# A function for wake word(s) or phrase
def wakeWord(text):
    Wake_Words= ['hey computer', 'ok computer']

    text =text.lower() # Converting the text to all lower

    # checking to see if the users command has the wake words
    for phrase in Wake_Words:
        if phrase in text:
            return True
        
    return False # if the wake word isn't found in the text from the loop and it returns false

# A function to give current date
def getDate():

    now=datetime.datetime.now()
    my_date=datetime.datetime.today()
    weekday=calendar.day_name[my_date.weekday()] # friday
    monthNum = now.month
    dayNum = now.day

    # month lists
    months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"]

    ordinal_numbers = [
    "1st", "2nd", "3rd", "4th", "5th", "6th",
    "7th", "8th", "9th", "10th", "11th", "12th",
    "13th", "14th", "15th", "16th", "17th",
    "18th", "19th", "20th", "21st", "22nd",
    "23rd", "24th", "25th", "26th",
    "27th", "28th", "29th", "30th",
    "31st"]

    return 'Today is'+ ' ' + weekday + ' ' + months[monthNum - 1] + ' ' + 'the' + ' ' + ordinal_numbers[dayNum - 1]+ ' . '

# A function to return a random greeting text
def greetings(text):

    #greetings input
    greetings_input= ['hi','hello','hey','greetings','wassup','hola']

    #greetings response
    greetings_response = ['hello' , 'hey there','howdy']

    # if the users input is greeting then randomly return a greeting response
    for word in text.split():
        if word.lower() in greetings_input:
            return random.choice(greetings_response)+ ' . '
    
    return ' '

# A function to get a persons first and last name from the text
def getPerson(text):

    wordList = text.split() # splitting the text into list of words

    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i+1] == 'is':
            return wordList[i+2] + ' ' + wordList[i+3]
        
while True:
    text = recordAudio()
    response = ' '

    # check for the wake word/phrase
    if (wakeWord(text) == True):
        
        # check the greetings by the user
        response = response + greetings(text)

        # check to see if the user said related to date
        if('date' in text):
            get_date = getDate()
            response = response + get_date

        # check to see if user said anything related to time
        if('time' in text):
            now=datetime.datetime.now()
            meridiem = ' '
            if now.hour >= 12:
                meridiem = ' p.m ' # post meridiem after midday
                hour = now.hour - 12
            else:
                meridiem = ' a.m ' # after meridiem before midday
                hour = now.hour

            # convert minute into proper string
            if now.minute < 10:
                minute = '0' + str(now.minute)
            else:
                minute = str(now.minute)

            response = response + ' ' + 'It is '+ str(hour) + ':' + minute + ' ' + meridiem + ' . '

        # check to see if the user said 'who is'
        if('who is' in text):
            person = getPerson(text)
            wiki =wikipedia.summary(person, sentences=3)
            response = response + ' ' + wiki

        # have the assistant respond back using audio and the text from response
        assistantResponse(response)