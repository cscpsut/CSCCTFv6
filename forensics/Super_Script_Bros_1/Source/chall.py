import os
import sys

# SIEM Part 1
questions_and_answers = [
    {"question": "What's the name of the script the developer stole from GitHub?\n", "answer": "automate.ps1"},
    {"question": "What's the name of the file that gave the attacker shell access when executed?\n", "answer": "automate.lnk"},
    {"question": "What legitimate application did the attacker leverage to gain access to the system?\n", "answers": ["VScode", "virtualstudiocode", "Visual Studio Code"]},
    {"question": "What developer platform did the script use for authentication?\n", "answer": "Github"}
]

def ask_question(question, correct_answers):
    while True:
        user_answer = input(question + " ").strip()
        if isinstance(correct_answers, list):
            if user_answer.lower() in [ans.lower() for ans in correct_answers]:
                break
        elif user_answer.lower() == correct_answers.lower():
            break
        print("Incorrect answer, please try again.")

def main():
    print("Investigate the exploit the attacker used for the initial access")
    for qa in questions_and_answers:
        correct_answers = qa.get("answers", qa.get("answer"))
        ask_question(qa["question"], correct_answers)

    flag = os.getenv("FLAG", "FLAG not set")
    print("Yayy! Here's your flag:", flag)

if __name__ == "__main__":
    main()