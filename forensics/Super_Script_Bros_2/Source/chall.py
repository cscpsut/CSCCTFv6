import os
import sys

# SIEM Part 2
questions_and_answers = [
    {"question": "What is the connection token used by the vscode shell?\n", "answer": "Kkjd64k5aAnIU3BiyVlMLTlpzyY1Q0yDN3TKoZUyIXA"},
    {"question": "What was the name of the existing service the attacker edited/reconfigured?\n", "answer": "Note"},
    {"question": "What was the new binary path of the service?\n", "answers": "C:\\Users\\Developer\\Downloads\\hidden.bat"},
    {"question": "What is the username, password and group of the new user created by the attacker? Format: group/username:password\n", "answer": "Administrators/checkmate:Ch3ckM@t31234"},
    {"question": "After the creation of the user the attacker connected to the machine via what protocol?\n", "answer": ["rdp","remote desktop protocol", "RDP", "Remote Desktop Protocol"]}
]

def ask_question(question, correct_answers):
    while True:
        user_answer = input(question + " ").strip()
        if isinstance(correct_answers, list):
            if user_answer in correct_answers:
                break
        elif user_answer == correct_answers:
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