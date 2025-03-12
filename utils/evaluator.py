import re

def evaluate_answer(question_data, user_answer):
    """Evaluates the user's answer against the correct answer."""

    correct_answer = question_data["correct_answer"].split(")")[0].strip()
    user_choice = user_answer.split(")")[0].strip()

    is_correct = user_choice == correct_answer
    return is_correct, question_data["correct_answer"]
