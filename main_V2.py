#!/usr/bin/python3

#from random_word import RandomWords
from colorama import Fore, Back, Style
from datetime import datetime
import readchar
import string
import random
import time
import signal
import argparse

# Global variables initialization.
number_of_hits = 0                                  # Variable to save the number of correct answers.
wrong_Answers = 0                                   # Variable to save the number of wrong answers.
number_of_types = 0                                 # Variable to save the total number of answers.
startTime = 0                                       # Variable to sae the time at the start of the test.
answersTimeList = []                                # List to save each answer time.
inputRequested = []                                 # List to save each answer time.
inputReceived = []                                  # List to save each answer time.
test_start = 0                                      # Variable to save test start date and time.


def typingKey(stop_key):

    # Helpper definitions.
    parser = argparse.ArgumentParser(description='Definitions of test mode')
    parser.add_argument('-utm', '--use_time_mode', action='store_true', help='Max number of secs for time mode or maximum number of inputs for number of inputs mode.')
    parser.add_argument('-mv', '--max_value', type=int, help='Max number of seconds for time mode or maximum number of inputs for number of inputs mode.')
    parser.add_argument('-tdv', '--test_difficulty_value', type=int, help='Test difficulty: 1 - Begging for Daddy; 2 - Normal; 3 - Hard; 4 - Extreme.')
    args = vars(parser.parse_args())

    if (args.get('test_difficulty_value') > 0) and (args.get('test_difficulty_value') < 5):     # Check if users test difficulty value input it's valid.

        # Variables initialization.
        global number_of_hits                               # Make variable to save the number of correct answers global.
        global wrong_Answers                                # Make variable to save the number of wrong answers global.
        global number_of_types                              # Make variable to save the total number of answers global.
        global startTime                                    # Make variable to save the total number of answers global.
        global answersTimeList                              # Make list to save each answer time global.
        global test_start                                   # Make variable to save test start date and time global.

        print('\n==================== PSR typing test (Grupo 4) ====================')  # Initial message.

        if args.get('test_difficulty_value') == 1:          # Check what's the test difficulty chosen.
            Text = ' Do not must'                           # Set text to type at the preliminary informations.
        elif args.get('test_difficulty_value') == 2:        # Check what's the test difficulty chosen.
            Text = ' Do not must'                           # Set text to type at the preliminary informations.
        elif args.get('test_difficulty_value') == 3:        # Check what's the test difficulty chosen.
            Text = ' Must'                                  # Set text to type at the preliminary informations.
        elif args.get('test_difficulty_value') == 4:        # Check what's the test difficulty chosen.
            Text = ' Must'                                  # Set text to type at the preliminary informations.


        print('\n=> You must type the character/word corresponding to the one indicated.\n=>' + Fore.YELLOW + Style.BRIGHT +
            Text + ' press enter' + Style.RESET_ALL + ' to validate your answer.\n=> Must press CTRL + C or SPACE (+ '
            'ENTER, for difficulty level 3 and 4) any time to stop test.\n=> Press any key to start.')  # Preliminary notes.
        readchar.readkey()                                                  # Waits for any user key press.
        print('\n')                                                         # Line change.
        test_start = datetime.now()                                         # Get test start date and time.
        print('==================== Test Starts ====================\n')    # Initial message.

        if args.get('use_time_mode'):                                       # Check if user wants a time mode test.
            signal.signal(signal.SIGALRM, timeOut)                          # To stop test after test duration time.
            signal.alarm(args.get('max_value'))                             # Starts counting test duration.

        startTime = time.time()                                             # Check the time at the start of the test.

        while True:
            try:
                if args.get('test_difficulty_value') == 1:                                  # Check what's the test difficulty chosen.
                    random_Character = random.choice(string.digits)                         # Generate a random character (numbers only).
                    enter_Needed = False
                elif args.get('test_difficulty_value') == 2:                                # Check what's the test difficulty chosen.
                    random_Character = random.choice(string.ascii_letters + string.digits)  # Generate a random character (letters or numbers).
                    enter_Needed = False
                elif args.get('test_difficulty_value') == 3:                                # Check what's the test difficulty chosen.
                    file = open("words.txt")
                    random_Character = str(file.readlines()[random.randint(0, 1050)])
                    random_Character = random_Character.rstrip('\n')                        # Remove the new line character ("\n") from string.
                    file.close()
                    enter_Needed = True
                elif args.get('test_difficulty_value') == 4:                                # Check what's the test difficulty chosen.
                    file = open("Sentences.txt")
                    random_Character = str(file.readlines()[random.randint(0, 155)])
                    random_Character = random_Character.rstrip('\n')                        # Remove the new line character ("\n") from string.
                    file.close()
                    enter_Needed = True

                print('Type character ' + Fore.BLUE + Style.BRIGHT + str(random_Character) + Style.RESET_ALL)   # Prints the character/word that user must type.

                inputRequested.append(random_Character)                     # Add the requested character to the list inputRequested.

                answersStartTime = time.time()                              # Check the time at the start of answer.

                if enter_Needed:                                            # Check whats the value of enter_Needed variable, True or False.
                    pressed_key = input()                                   # Gets user typed word.
                    print("\x1B[F\x1B[2K", end="")                          # To hide the input text.
                else:
                    pressed_key = readchar.readchar()                       # Gets user typed character.

                answersStopTime = time.time()                               # Check the time at the end of answer.
                answersTime = answersStopTime - answersStartTime            # Calculate the answers duration time.
                answersTimeList.append(answersTime)                         # Add answers duration time to list answersTimeList.
                inputReceived.append(pressed_key)                           # Add the input character to the list inputReceived.

                if pressed_key == stop_key:
                    timeOut(0, 0)                                           # Call timeOut function.
                elif pressed_key == random_Character:                       # Checks if user typed key it's equal to random key generated.
                    color = Fore.GREEN                                      # Green color, it means correct answer.
                    number_of_hits += 1                                     # Add 1 to the number of correct answers.
                    number_of_types += 1                                    # Add 1 to the total number of answers.
                else:
                    color = Fore.RED                                        # Red color, it means incorrect answer.
                    wrong_Answers += 1                                      # Add 1 to the number of wrong answers.
                    number_of_types += 1                                    # Add 1 to the total number of answers.

                print('You typed ' + color + Style.BRIGHT + str(pressed_key) + Style.RESET_ALL)    # Print user typed key.

                if (args.get('use_time_mode') == False) and (number_of_types == args.get('max_value')):    # Check if user choose a test with maximum inputs number duration and if those number it was already hit.
                    timeOut(0, 0)  # Call timeOut function.

            except KeyboardInterrupt:                                                   # To allow CTRL+C to stop test.
                timeOut(0, 0)                                                           # Call timeOut function.

    else:
        print(Fore.YELLOW + Style.BRIGHT + 'Test finished!' + Style.RESET_ALL)          # Test finished message.
        print(Fore.RED + Style.BRIGHT + 'Invalid input parameters' + Style.RESET_ALL)   # Error message.
        exit()                                                                          # Stops program.


# Function called when times out is reached.
def timeOut(signum, stack):

    test_end = datetime.now()                                                                                   # Get test end date and time.
    endTime = time.time()                                                                                       # Check the time at the end of the test.
    print(Fore.YELLOW + Style.BRIGHT + '\nTest finished!' + Style.RESET_ALL)                                    # Test finished message.
    print('\r\n\n================================= Results =================================')                  # Initial message.
    if number_of_types == 0:                                                                                    # Check if number of types it's equal to 0.
        accuracy = 0                                                                                            # Set's the accuracy equals to 0.
    else:
        accuracy = number_of_hits / number_of_types                                                             # Calculate the accuracy.
    print('\r=> Accuracy:   ' + str(accuracy))                                                                  # Prints the user accuracy.
    print('\r=> Requested characters:' + str(inputRequested))                                                                           # Prints the list of requested characters.
    print('\r=> Typed characters:    ' + str(inputReceived))                                                                            # Prints the list of typed characters.
    print('\r=> Total nº of answers:   ' + str(number_of_types))                                                # Prints the total number of answers.
    print('\r=> Nº of correct answers: ' + Fore.GREEN + Style.BRIGHT + str(number_of_hits) + Style.RESET_ALL)   # Prints the number of correct answers.
    print('\r=> Nº of wrong answers:   ' + Fore.RED + Style.BRIGHT + str(wrong_Answers) + Style.RESET_ALL)      # Prints the number of wrong answers.
    print('\r=> Test start: ' + str(test_start))
    print('\r=> Test end: ' + str(test_end))
    testDuration = str(endTime - startTime)                                                                     # Calculate the test duration time.
    test_duration = testDuration.split('.')                                                                     # Split answers time by minutes and seconds.
    print('\r=> Duration time of test: ' + str(test_duration[0]) + Style.DIM + 'sec ' + Style.RESET_ALL + str(test_duration[1])[:2] + Style.DIM + 'ms ' + Style.RESET_ALL)  # Prints the test duration time.
    for i in range(1, len(answersTimeList)):                                                                    # For loop to go through all answersTimeList list elemets.
        answersTimeListDivided = str(answersTimeList[i]).split('.')                                             # Split answers time by minutes and seconds.
        print('\r=> Time to ' + str(i) + 'ª answers:    ' + str(answersTimeListDivided[0]) + Style.DIM + 'sec ' + Style.RESET_ALL + str(answersTimeListDivided[1])[:2] + Style.DIM + 'ms\r' + Style.RESET_ALL)  # Prints each answer time.

    signal.alarm(0)                                                                                             # Stops counting test duration.
    exit()                                                                                                      # Stops program.

def main():
    typingKey(' ')                              # Start typingKey function.

if __name__ == "__main__":
    main()