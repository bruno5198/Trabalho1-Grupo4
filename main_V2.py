#!/usr/bin/python3

from colorama import Fore, Back, Style
from datetime import datetime
import readchar
import string
import random
import time
import signal
import argparse
import pprint
from collections import namedtuple

# Global variables initialization.
number_of_hits = 0                                                      # Variable to save the number of correct answers.
wrong_answers = 0                                                       # Variable to save the number of wrong answers.
number_of_types = 0                                                     # Variable to save the total number of answers.
start_time = 0                                                          # Variable to sae the time at the start of the test.
answers_time_list = []                                                  # List to save each answer time.
input_requested = []                                                    # List to save each answer time.
input_received = []                                                     # List to save each answer time.
test_start = 0                                                          # Variable to save test start date and time.
entry = []                                                              # Create an empty list to save all the inputs.
Input = namedtuple('Input', ['requested', 'received', 'duration'])      # Creation of a namedtuple.
answers_time_OK = 0                                                     # Variable to save the total time of ok answer.
answers_time_NOK = 0                                                    # Variable to save the total time of not ok answer.

def typingKey(stop_key):

    # Helpper definitions.
    parser = argparse.ArgumentParser(description='Definitions of test mode')
    parser.add_argument('-utm', '--use_time_mode', action='store_true', help='Max number of secs for time mode or maximum number of inputs for number of inputs mode.')
    parser.add_argument('-mv', '--max_value', type=int, help='Max number of seconds for time mode or maximum number of inputs for number of inputs mode.')
    parser.add_argument('-tdv', '--test_difficulty_value', type=int, help='Test difficulty: 1 - Begging for Daddy; 2 - Normal; 3 - Hard; 4 - Extreme.')
    global args
    args = vars(parser.parse_args())

    if args.get('max_value') is None:                                                               # Check if users maximum value value input it isn't empty.
        print(Fore.RED + Style.BRIGHT + '\n Missing argument: max_value, -mv' + Style.RESET_ALL)    # Error message.
        exit()                                                                                      # Stops program.

    if args.get('test_difficulty_value') is None:                                                   # Check if users test difficulty value input it isn't empty.
        print(Fore.RED + Style.BRIGHT + '\n Missing argument: test_difficulty_value, -tdv' + Style.RESET_ALL)   # Error message.
        exit()                                                                                      # Stops program.

    if not args.get('max_value') > 0:
        print(Fore.RED + Style.BRIGHT + 'Invalid input parameters' + Style.RESET_ALL)               # Error message.
        exit()

    if (args.get('test_difficulty_value') > 0) and (args.get('test_difficulty_value') < 5):         # Check if users test difficulty value input it's valid.

        # Variables initialization.
        global number_of_hits                               # Make variable to save the number of correct answers global.
        global wrong_answers                                # Make variable to save the number of wrong answers global.
        global number_of_types                              # Make variable to save the total number of answers global.
        global start_time                                   # Make variable to save the total number of answers global.
        global answers_time_list                            # Make list to save each answer time global.
        global test_start                                   # Make variable to save test start date and time global.
        global answers_time_OK                              # Make variable to save the total time of ok answer global.
        global answers_time_NOK                             # Make variable to save the total time of not ok answer global.

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
        print('\n==================== Test Starts ====================\n')  # Initial message.
        test_start = datetime.now()                                         # Get test start date and time.

        if args.get('use_time_mode'):                                       # Check if user wants a time mode test.
            signal.signal(signal.SIGALRM, timeOut)                          # To stop test after test duration time.
            signal.alarm(args.get('max_value'))                             # Starts counting test duration.

        start_time = time.time()                                            # Check the time at the start of the test.

        while True:
            try:
                if args.get('test_difficulty_value') == 1:                                  # Check what's the test difficulty chosen.
                    random_character = random.choice(string.digits)                         # Generate a random character (numbers only).
                    enter_needed = False
                elif args.get('test_difficulty_value') == 2:                                # Check what's the test difficulty chosen.
                    random_character = random.choice(string.ascii_letters + string.digits)  # Generate a random character (letters or numbers).
                    enter_needed = False
                elif args.get('test_difficulty_value') == 3:                                # Check what's the test difficulty chosen.
                    file = open("words.txt")                                                # Open the .txt file that contain the random words.
                    random_character = str(file.readlines()[random.randint(0, 1050)])       # Choose a random word.
                    random_character = random_character.rstrip('\n')                        # Remove the new line character ("\n") from string.
                    file.close()                                                            # Close the file that contain the random words.
                    enter_needed = True
                elif args.get('test_difficulty_value') == 4:                                # Check what's the test difficulty chosen.
                    file = open("Sentences.txt")                                            # Open the .txt file that contain the random sentences.
                    random_character = str(file.readlines()[random.randint(0, 155)])        # Choose a random sentence.
                    random_character = random_character.rstrip('\n')                        # Remove the new line character ("\n") from string.
                    file.close()                                                            # Close the file that contain the random sentences.
                    enter_needed = True

                print('Type character ' + Fore.BLUE + Style.BRIGHT + str(random_character) + Style.RESET_ALL)   # Prints the character/word that user must type.

                input_requested.append(random_character)                    # Add the requested character to the list inputRequested.

                answersStartTime = time.time()                              # Check the time at the start of answer.

                if enter_needed:                                            # Check whats the value of enter_needed variable, True or False.
                    pressed_key = input()                                   # Gets user typed word.
                    print("\x1B[F\x1B[2K", end="")                          # To hide the input text.
                else:
                    pressed_key = readchar.readchar()                       # Gets user typed character.

                answers_stop_time = time.time()                             # Check the time at the end of answer.
                answers_time = answers_stop_time - answersStartTime         # Calculate the answers duration time.
                answers_time_list.append(answers_time)                      # Add answers duration time to list answersTimeList.
                input_received.append(pressed_key)                          # Add the input character to the list inputReceived.

                if pressed_key == stop_key or pressed_key == '\x03':        # Check if user pressed the test keys to finish (Space or CTRL+C).
                    timeOut(0, 0)                                           # Call timeOut function.
                elif pressed_key == random_character:                       # Checks if user typed key it's equal to random key generated.
                    color = Fore.GREEN                                      # Green color, it means correct answer.
                    number_of_hits += 1                                     # Add 1 to the number of correct answers.
                    number_of_types += 1                                    # Add 1 to the total number of answers.
                    answers_time_OK = answers_time_OK + answers_time        # Total times of ok answers.
                else:
                    color = Fore.RED                                        # Red color, it means incorrect answer.
                    wrong_answers += 1                                      # Add 1 to the number of wrong answers.
                    number_of_types += 1                                    # Add 1 to the total number of answers.
                    answers_time_NOK = answers_time_NOK + answers_time      # Total times of not ok answers.

                print('You typed ' + color + Style.BRIGHT + str(pressed_key) + Style.RESET_ALL)             # Print user typed key.

                entry.append(Input(str(random_character), pressed_key, answers_time))                       # Add the inputs to previously created list (Requested character/word/phrase, Pressed character/word/phrase, Ellapsed time).

                if (args.get('use_time_mode') == False) and (number_of_types == args.get('max_value')):     # Check if user choose a test with maximum inputs number duration and if those number it was already hit.
                    timeOut(0, 0)                                                                           # Call timeOut function.

            except KeyboardInterrupt:                                                   # To allow CTRL+C to stop test.
                timeOut(0, 0)                                                           # Call timeOut function.

    else:
        print(Fore.YELLOW + Style.BRIGHT + 'Test finished!' + Style.RESET_ALL)          # Test finished message.
        print(Fore.RED + Style.BRIGHT + 'Invalid input parameters' + Style.RESET_ALL)   # Error message.
        exit()                                                                          # Stops program.


# Function called when times out is reached.
def timeOut(signum, stack):
    test_end = datetime.now()                                                                                   # Get test end date and time.
    end_time = time.time()                                                                                      # Check the time at the end of the test.
    print(Fore.YELLOW + Style.BRIGHT + '\nTest finished!' + Style.RESET_ALL)                                    # Test finished message.
    print('\r\n================================= Results =================================')                    # Initial message.

    testDuration = str(end_time - start_time)                                                                   # Calculate the test duration time.

    if number_of_types == 0:                                                                                    # Check zero divison.
        type_average_duration = 0                                                                               # Sets the value of "type_average_duration" variable.
        accuracy = 0                                                                                            # Sets the value of "accuracy" variable.
    else:
        type_average_duration = (float(testDuration)/float(number_of_types))                                    # Calculate test average duration.
        accuracy = number_of_hits / number_of_types                                                             # Calculate user accuracy.

    if number_of_hits == 0:                                                                                     # Check zero divison.
        type_hit_average_duration = 0                                                                           # Sets the value of "type_hit_average_duration" variable.
    else:
        type_hit_average_duration = (answers_time_OK / number_of_hits)                                          # Calculate correct answers average times.

    if wrong_answers == 0:                                                                                      # Check zero divison.
        type_miss_average_duration = 0                                                                          # Sets the value of "type_miss_average_duration" variable.
    else:
        type_miss_average_duration = answers_time_NOK / wrong_answers                                           # Calculate wrong answers average times.

    dic_result = {'accuracy': accuracy, 'inputs': entry,
                  'number_of_hits': number_of_hits, 'number_of_types': number_of_types,
                  'test_duration': testDuration, 'test_end': str(test_end), 'test_start': str(test_start),
                  'type_average_duration': type_average_duration,'type_hit_average_duration': type_hit_average_duration,
                  'type_miss_average_duration': type_miss_average_duration}                                     # Creation of the dictionary.

    signal.alarm(0)                                                                                             # Stops counting test duration.

    if args.get('use_time_mode'):
        if not dic_result['inputs']:
            print('\r' + Fore.YELLOW + Style.BRIGHT + 'No characters entered!' + Style.RESET_ALL + '\n\r')      # Test finished message.
            exit()

        # This part of code is necessary because of the formatting error when we combine signals (to end text after a user defined amount of time) and Readchar function.
        for key, value in dic_result.items():                                                                   # Cycle that runs through the contents of the previously created dictionary.
            if key == 'accuracy':                                                                               # Check if the key in analysis it's 'accuracy' key.
                print('\r' + "{'" + key + "'" + ':', str(value) + ',')                                          # Prints the desired text.
            elif key == 'inputs':                                                                               # Check if the key in analysis it's 'inputs' key.
                print('\r')                                                                                     # Prints a carriage return.
                print("\x1B[F\x1B[2K", end="")                                                                  # To hide the input text.
                if len(value) > 1:
                    print(" '" + key + "'" + ': [' + str(value[0]) + ',')                                       # Prints the desired text.
                    for i in range(1, len(value)-1):                                                            # Cycle that runs through the contents of the previously created list.
                        print("\r            " + str(value[i]) + ',')                                           # Prints the desired text.
                    print("\r            " + str(value[len(value)-1]) + '],')                                   # Prints the desired text.
                else:
                    print(" '" + key + "'" + ': [' + str(value[0]) + '],')                                      # Prints the desired text.
            elif key == 'type_miss_average_duration':                                                           # Check if the key in analysis it's 'type_miss_average_duration' key.
                print('\r', "'" + key + "'" + ': ' + str(value) + "}\r")                                        # Prints the desired text.
            else:
                print('\r', "'" + key + "'" + ':', str(value) + ',')                                            # Prints the desired text.
    else:
        pp = pprint.PrettyPrinter(indent=1)                                                                     # Set's dictionary initial indentation.
        pp.pprint(dic_result)                                                                                   # Print all the dictionary.
    exit()                                                                                                      # Stops program.


def main():
    typingKey(' ')                              # Start typingKey function.


if __name__ == "__main__":
    main()
