import os
import sys

# SIEM Part 3
questions_and_answers = [
    {"question": "What is the name of the APT group that first used this initial access method?\n", "answer": "Mustang Panda"},
    {"question": "What is the mitre ID for the privelege escalation technique? Format: T1234.003\n", "answer": "T1574.011"}
]

def ask_question(question, correct_answers):
    while True:
        user_answer = input(question + " ").strip()
        if user_answer.lower() == correct_answers.lower():
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