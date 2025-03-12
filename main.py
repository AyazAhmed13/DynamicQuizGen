import time
from utils.pdf_parser import extract_text_from_pdf
from utils.qg_pipeline import generate_questions_ollama
from utils.evaluator import evaluate_answer
from utils.db_utils import store_user_response

def main():
    
  
    text = extract_text_from_pdf("pdf_text")
    if not text:
        return
    print('starting  the quiz')
    print("PDF text loaded successfully.")

    # Initialize variables
    difficulty = "easy"
    score = 0
    num_questions = 5

    for i in range(num_questions):
        print(f"\nGenerating Question {i + 1} ({difficulty} level)...")

        # Generate one question at a time
        question_data = generate_questions_ollama(text, difficulty)
        
        if not question_data:
            print("❌ Error: Failed to generate a question. Try again.")
            return

        # Extract question details
        question_text = question_data["question"]
        options = question_data["options"]

        # Display question and options
        print(f"\n{question_text}")
        for option in options:
            print(option)

        # Get user's answer
        start_time = time.time()
        user_answer = input("Your Answer (A/B/C/D): ").strip().upper()
        response_time = time.time() - start_time

        # Evaluate correctness
        is_correct, correct_answer = evaluate_answer(question_data, user_answer)

        if is_correct:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Incorrect! The correct answer was: {correct_answer}")

        # Store response
        store_user_response(question_text, user_answer, is_correct, response_time)

        # Adjust difficulty dynamically
        if is_correct and response_time < 30:  # If user answers quickly, increase difficulty
            if difficulty == "easy":
                difficulty = "medium"
            elif difficulty == "medium":
                difficulty = "hard"
        elif not is_correct and difficulty != "easy":  # If user gets it wrong, decrease difficulty
            if difficulty == "hard":
                difficulty = "medium"
            elif difficulty == "medium":
                difficulty = "easy"

    print(f"\nQuiz completed. Your final score: {score}/{num_questions}")

if __name__ == "__main__":
    main()
