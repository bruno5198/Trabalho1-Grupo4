#!/usr/bin/python3
# --------------------------------------------------
# A python script that executes PSR Typing Test, made by Grupo 4!
# Bruno Mendes, Bruno Pereira, Daniel Gadelho, Germano Rodrigues.
# PSR, November 2021.
# --------------------------------------------------

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
start_time = 0                                                          # Variable to store the time at the start of the test.
answers_time_list = []                                                  # List to save each answer time.
input_requested = []                                                    # List to save each input requested.
input_received = []                                                     # List to save each input received.
test_start = 0                                                          # Variable to save the test start date and time.
entry = []                                                              # Create an empty list to save all the inputs.
Input = namedtuple('Input', ['requested', 'received', 'duration'])      # Creation of a namedtuple.
answers_time_OK = 0                                                     # Variable to save the total time of OK answer.
answers_time_NOK = 0                                                    # Variable to save the total time of not OK answer.
args = {}


def typingKey(stop_key):
    """
    Function of the PSR Typing Test program.
    :param stop_key:
    :return:
    """

    # Helper definitions.
    parser = argparse.ArgumentParser(description='Definitions of test mode')
    parser.add_argument('-utm', '--use_time_mode', action='store_true', help='Execute the program in time mode.')
    parser.add_argument('-mv', '--max_value', type=int, help='Max number of seconds for time mode or maximum number of inputs for number of inputs mode.')
    parser.add_argument('-tdv', '--test_difficulty_value', type=int, help='Test difficulty: 1 - Begging for Daddy; 2 - Normal; 3 - Hard; 4 - Extreme.')
    global args
    args = vars(parser.parse_args())

    if args.get('max_value') is None:                                                                               # Check if the user's maximum value input isn't empty.
        print(Fore.RED + Style.BRIGHT + 'error: missing argument -mv/--max_value' + Style.RESET_ALL)                # Error message.
        exit()                                                                                                      # Stop the program.

    if args.get('test_difficulty_value') is None:                                                                   # Check if the user's test difficulty value input isn't empty.
        print(Fore.RED + Style.BRIGHT + 'error: missing argument -tdv/--test_difficulty_value' + Style.RESET_ALL)   # Error message.
        exit()                                                                                                      # Stop the program.

    if not args.get('max_value') > 0:                                                                               # Check if the user's maximum value input isn't valid.
        print(Fore.RED + Style.BRIGHT + 'error: argument -mv/--max_value: invalid int value: \'' + str(args.get('max_value')) + '\'' + Style.RESET_ALL)   # Error message.
        exit()

    if not ((args.get('test_difficulty_value') > 0) and (args.get('test_difficulty_value') < 5)):                         # Check if the user's test difficulty value input is valid.
        print(Fore.RED + Style.BRIGHT + 'error: argument -tdv/--test_difficulty_value: invalid int value: \'' + str(args.get('test_difficulty_value')) + '\'' + Style.RESET_ALL)  # Error message.
        exit()  # Error message.

    # Variables initialization.
    global number_of_hits                               # Make variable to save the number of correct answers global.
    global wrong_answers                                # Make variable to save the number of wrong answers global.
    global number_of_types                              # Make variable to save the total number of answers global.
    global start_time                                   # Make variable to store the time at the start of the test global.
    global answers_time_list                            # Make the list variable to save each answer time global.
    global test_start                                   # Make variable to save the test start date and time global.
    global answers_time_OK                              # Make variable to save the total time of OK answer global.
    global answers_time_NOK                             # Make variable to save the total time of not OK answer global.
    text = ''
    random_character = ''
    enter_needed = False
    color = ''

    print('\n==================== PSR Typing Test (Grupo 4) ====================\n')        # Initial message.

    if args.get('test_difficulty_value') == 1 or args.get('test_difficulty_value') == 2:    # Check what's the test difficulty chosen.
        text = 'do not must'                                                                # Set the text to type at the preliminary information.
    elif args.get('test_difficulty_value') == 3 or args.get('test_difficulty_value') == 4:  # Check what's the test difficulty chosen.
        text = 'must'                                                                       # Set the text to type at the preliminary information.

    print('=> You must type the character/word/sentence corresponding to the one indicated.')                     # Preliminary notes.
    print('=> You ' + Fore.YELLOW + Style.BRIGHT + text + ' press ENTER' + Style.RESET_ALL + ' to validate your answer.')
    print('=> You must press CTRL + C or SPACE (+ ENTER for difficulty level 3 and 4) any time to stop test.')
    print('=> Press any key to start.')
    readchar.readkey()                                                                  # Wait for the user to key press.
    print('\n=========================== Test Starts ===========================\n')    # Initial message.
    test_start = datetime.now()                                                         # Get the test start date and time.

    if args.get('use_time_mode'):                                                       # Check if the user wants the test in the maximum time mode.
        signal.signal(signal.SIGALRM, timeOut)                                          # To stop the test after the test duration time.
        signal.alarm(args.get('max_value'))                                             # Start counting the test duration.

    start_time = time.time()                                                            # Check the time at the start of the test.

    while True:
        try:
            if args.get('test_difficulty_value') == 1:                                  # Check if the test difficulty chosen is 1 - Begging for Daddy.
                random_character = random.choice(string.digits)                         # Generate a random character (numbers only).
                text = 'character'
                enter_needed = False
            elif args.get('test_difficulty_value') == 2:                                # Check if the test difficulty chosen is 2 - Normal.
                random_character = random.choice(string.ascii_letters + string.digits)  # Generate a random character (letters or numbers).
                text = 'character'
                enter_needed = False
            elif args.get('test_difficulty_value') == 3:                                # Check if the test difficulty chosen is 3 - Hard.
                file = open("words.txt")                                                # Open the .txt file that contains the random words.
                random_character = str(file.readlines()[random.randint(0, 1050)])       # Choose a random word.
                random_character = random_character.rstrip('\n')                        # Remove the newline character ("\n") from the string.
                file.close()                                                            # Close the file that contains the random words.
                text = 'word'
                enter_needed = True
            elif args.get('test_difficulty_value') == 4:                                # Check if the test difficulty chosen is 4 - Extreme.
                file = open("sentences.txt")                                            # Open the .txt file that contains the random sentences.
                random_character = str(file.readlines()[random.randint(0, 155)])        # Choose a random sentence.
                random_character = random_character.rstrip('\n')                        # Remove the newline character ("\n") from the string.
                file.close()                                                            # Close the file that contains the random sentences.
                text = 'sentence'
                enter_needed = True

            print('Type ' + text + ': ' + Fore.BLUE + Style.BRIGHT + str(random_character) + Style.RESET_ALL)   # Print the character/word/sentence that the user must type.

            input_requested.append(random_character)                    # Add the requested character to the list 'input_requested'.

            answers_start_time = time.time()                            # Check the time at the start of the answer.

            if enter_needed:                                            # Check whats the value of the 'enter_needed' variable, True or False.
                pressed_key = input()                                   # Get user's typed word/sentence.
                print("\x1B[F\x1B[2K", end="")                          # To hide the input text.
            else:
                pressed_key = readchar.readchar()                       # Get user's typed character.

            answers_stop_time = time.time()                             # Checks the time at the end of the answer.
            answers_time = answers_stop_time - answers_start_time       # Calculate the answers duration time.
            answers_time_list.append(answers_time)                      # Add answers duration time to the list 'answers_time_list'.
            input_received.append(pressed_key)                          # Add the input character to the list 'input_received'.

            if pressed_key == stop_key or pressed_key == '\x03':        # Check if the user pressed the keys to interrupt the program (SPACE or CTRL+C).
                timeOut(0, 0)                                           # Call 'timeOut' function.
            elif pressed_key == random_character:                       # Check if the user typed the key that is equal to the random key generated.
                color = Fore.GREEN                                      # Green color, which means the answer is correct.
                number_of_hits += 1                                     # Add 1 to the number of correct answers.
                number_of_types += 1                                    # Add 1 to the total number of answers.
                answers_time_OK += answers_time                         # Total times of OK answers.
            else:
                color = Fore.RED                                        # Red color, which means the answer is wrong.
                wrong_answers += 1                                      # Add 1 to the number of wrong answers.
                number_of_types += 1                                    # Add 1 to the total number of answers.
                answers_time_NOK += answers_time                        # Total times of not OK answers.

            print('You typed: ' + color + Style.BRIGHT + str(pressed_key) + Style.RESET_ALL)            # Print user's typed character/word/sentence.

            entry.append(Input(str(random_character), pressed_key, answers_time))                       # Add the inputs to the previously created list (Requested character/word/sentence, Pressed character/word/sentence, Elapsed time).

            if (args.get('use_time_mode') is False) and (number_of_types == args.get('max_value')):     # Check if the user wants the test in the maximum number of inputs mode and if the user has already reached that limit.
                timeOut(0, 0)                                                                           # Call 'timeOut' function.

        except KeyboardInterrupt:                                       # To allow CTRL+C to stop the test.
            timeOut(0, 0)                                               # Call 'timeOut' function.

def timeOut(signum, stack):
    """
    Function called when times out is reached.
    :param signum:
    :param stack:
    :return:
    """

    test_end = datetime.now()                                                                                   # Get the test end date and time.
    end_time = time.time()                                                                                      # Check the time at the end of the test.
    print(Fore.YELLOW + Style.BRIGHT + '\nTest finished!' + Style.RESET_ALL)                                    # Test finished message.
    print('\r\n============================= Results =============================\n')                          # Results message.

    test_duration = str(end_time - start_time)                                                                  # Calculate the test duration time.

    if number_of_types == 0:                                                                                    # Check division by zero.
        type_average_duration = 0                                                                               # Set the value of 'type_average_duration' variable.
        accuracy = 0                                                                                            # Set the value of 'accuracy' variable.
    else:
        type_average_duration = (float(test_duration)/float(number_of_types))                                   # Calculate the test average duration.
        accuracy = number_of_hits / number_of_types                                                             # Calculate the user's accuracy.

    if number_of_hits == 0:                                                                                     # Check division by zero.
        type_hit_average_duration = 0                                                                           # Set the value of 'type_hit_average_duration' variable.
    else:
        type_hit_average_duration = (answers_time_OK / number_of_hits)                                          # Calculate correct answers average times.

    if wrong_answers == 0:                                                                                      # Check division by zero.
        type_miss_average_duration = 0                                                                          # Set the value of 'type_miss_average_duration' variable.
    else:
        type_miss_average_duration = answers_time_NOK / wrong_answers                                           # Calculate wrong answers average times.

    dic_result = {'accuracy': accuracy, 'inputs': entry,
                  'number_of_hits': number_of_hits, 'number_of_types': number_of_types,
                  'test_duration': test_duration, 'test_end': str(test_end), 'test_start': str(test_start),
                  'type_average_duration': type_average_duration, 'type_hit_average_duration': type_hit_average_duration,
                  'type_miss_average_duration': type_miss_average_duration}                                     # Creation of the dictionary.

    signal.alarm(0)                                                                                             # Stop counting the test duration.

    if args.get('use_time_mode'):
        if not dic_result['inputs']:
            print('\r' + Fore.YELLOW + Style.BRIGHT + 'No keys pressed!' + Style.RESET_ALL + '\n\r')            # No keys pressed message.
            exit()

        # This part of the code is necessary because of the formatting error when we combine signals (to end the text after an amount of time defined by the user) and because of the 'readchar' function.
        for key, value in dic_result.items():                                                                   # Cycle that cycles through the contents of the previously created dictionary.
            if key == 'accuracy':                                                                               # Check if the key in the analysis is the 'accuracy' key.
                print('\r' + '{\'' + key + '\'' + ': ' + str(value) + ',')                                      # Print the desired text.
            elif key == 'inputs':                                                                               # Check if the key in the analysis is the 'inputs' key.
                print('\r')                                                                                     # Print a carriage return.
                print("\x1B[F\x1B[2K", end="")                                                                  # To hide the input text.
                if len(value) > 1:
                    print(' \'' + key + '\'' + ': [' + str(value[0]) + ',')                                     # Print the desired text.
                    for i in range(1, len(value)-1):                                                            # Cycle that cycles through the contents of the previously created list.
                        print('\r            ' + str(value[i]) + ',')                                           # Print the desired text.
                    print('\r            ' + str(value[len(value)-1]) + '],')                                   # Print the desired text.
                else:
                    print(' \'' + key + '\'' + ': [' + str(value[0]) + '],')                                    # Print the desired text.
            elif key == 'type_miss_average_duration':                                                           # Check if the key in the analysis is the 'type_miss_average_duration' key.
                print('\r \'' + key + '\'' + ': ' + str(value) + '}\r')                                         # Print the desired text.
            else:
                print('\r \'' + key + '\'' + ': ' + str(value) + ',')                                           # Print the desired text.
    else:
        pp = pprint.PrettyPrinter(indent=1)                                                                     # Set the dictionary initial indentation.
        pp.pprint(dic_result)                                                                                   # Print the entire dictionary.

    print('')
    exit()                                                                                                      # Stop the program.

def main():
    typingKey(' ')                                                                                              # Start 'typingKey' function.

if __name__ == "__main__":
    main()
