import random
import sys
import os
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

#   You will need to install the following packages from any terminal running the commands:
#       pip install colorama
#       pip install random
#
#   Command for running the program:
#   python program_path (file_path number_of_questions title)
#   default values:
#       numberOfQuestions = 10
#       Title = QUESTION
#
#   File Format
#       Question1;answer1;...;answerN;answerNumber(1,N)
#       Question2;answer1;...;answerN;answerNumber(1,N)
#       ...
#       QuestionM;answer1;...;answerN;answerNumber(1,N)

colorama_init()


def run(path_of_file, number_of_questions=10):
    questions = read_questions(path_of_file, number_of_questions)

    failed, correct_guesses = ask_questions(questions)

    number_of_questions = min(number_of_questions, len(questions))

    final_result = correct_guesses*100/number_of_questions

    color = get_color(final_result)

    show_results(correct_guesses, number_of_questions, failed, color, questions)

    exit()


def ask_questions(questions):
    if questions is None:
        raise Exception("No questions provided")

    counter = 1
    correct_guesses = 0
    failed_q_a = []
    for question in questions:
        print(f"\n\t{counter}. {question[0]}:", end="\n")
        i = 0
        for i in range(1, len(question) - 1):
            print(f"\t\t{i}) {question[i]}.")

        result = input("\n\t  What is your answer?: ")
        while not result.isnumeric() or int(result) > i or int(result) <= 0:
            if result == "q":
                print("\n\nExiting the test...")
                exit()
            print("\n\t  Your answer must be numeric and contained in the provided range.")
            result = input("\n\t  What is your answer?: ")

        if int(result) == int(question[-1]):
            correct_guesses += 1
        else:
            failed_q_a.append([question[0], question[int(question[-1])], question[int(result)]])
        counter += 1
    return failed_q_a, correct_guesses


def get_color(result):
    color = Fore.RED

    if result >= 80:
        color = Fore.GREEN

    elif result >= 50:
        color = Fore.YELLOW

    return color


def show_results(correct_guesses, number_of_questions, failed, color, questions):
    print(f"\n-------------------------------------------------------------------------------------------------------\n"
          f"You have guessed correctly {color}{correct_guesses}{Style.RESET_ALL} "
          f"out of a total of {Fore.CYAN}{number_of_questions}{Style.RESET_ALL}.\n"
          f"Your final mark is {color}{correct_guesses * 100 / number_of_questions}%{Style.RESET_ALL} "
          f"-> {color}{correct_guesses * 10 // number_of_questions}/10.{Style.RESET_ALL}")

    if correct_guesses < len(questions):
        print()
        for fail in failed:
            print(f"\n- On question: \"{fail[0]}\" the answer should be:"
                  f"\n\t\t{Fore.GREEN}-{fail[1]}{Style.RESET_ALL}"
                  f"\n\tBut you answered:"
                  f"\n\t\t{Fore.RED}-{fail[2]} {Style.RESET_ALL}")

    else:
        print(f"\n{color}Congratulations for answering all your questions correct!{Style.RESET_ALL}")


def read_questions(file_of_path, number_of_questions):
    fileData = read_file(file_of_path)
    selected_data = random.sample(fileData, k=min(number_of_questions, len(fileData)))
    parsed_data = []
    for line in selected_data:
        values = line.split(";")
        if (not values[-1].strip().isnumeric()) or int(values[-1]) > len(values) - 2:
            print(values[-1])
            raise Exception(f"{Fore.LIGHTRED_EX}\n\nInvalid question format on line\n"
                            f"\t\t-\"{line}\".\n"
                            f"Expected as last element an integer between 1 and {len(values)-2} "
                            f"and got ({values[-1]} -> isnumeric:{values[-1].strip().isnumeric()}).{Style.RESET_ALL}")
        parsed_data.append(values)

    return parsed_data


def read_file(file_of_path):
    try:
        file = open(file_of_path, "r")
        return file.readlines()
    except FileNotFoundError:
        raise Exception(f"\n\n\t{Fore.LIGHTRED_EX}Invalid file path: {file_of_path}{Style.RESET_ALL}")


if __name__ == "__main__":
    os.system("cls")

    if len(sys.argv) == 1:
        file_path = input("Enter the filePath for the questions: ")

    else:
        file_path = sys.argv[1]

    if len(sys.argv) == 4:
        print(f"\n------------------------- {sys.argv[3].upper()} -------------------------\n")
    else:
        print(f"\n------------------------- QUESTIONS -------------------------\n")

    if len(sys.argv) >= 3:
        run(sys.argv[1], int(sys.argv[2]))

    run(file_path)
