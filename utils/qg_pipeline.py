import ollama
import random
import json

def generate_questions_ollama(text, difficulty):
    """Generate a single question dynamically based on difficulty."""
    print("🔄 Generating question...")  # Debugging print

    # Select a random 1000-character chunk to ensure variety
    if len(text) > 1000:
        start_idx = random.randint(0, len(text) - 1000)
        selected_text = text[start_idx : start_idx + 1000]
    else:
        selected_text = text  # Use full text if it's short

    # Define the prompt
    prompt = f"""
    Based on the following text, generate a SINGLE {difficulty} level question.

    **Rules for Question Generation:**
    - Do NOT repeat topics from previous questions.
    - The question should be **either** a **Multiple Choice Question (MCQ)** or a **True/False question** (randomly chosen).
    - Ensure MCQs have random correct answers (not always the first option).
    - Ensure True/False questions have a mix of True and False answers.

    **Difficulty Levels:**
    - **Easy:** Basic definitions or simple examples.
    - **Medium:** Conceptual differences, relationships, or explanations.
    - **Hard:** Deeper analytical questions requiring critical thinking.

    **Diversity in Topics:**
    - Questions should cover different Python topics (Variables, Functions, Loops, OOP, Exceptions, Modules, etc.).
    - Avoid repetitive questions on the same topic.

    **Text Context:**  
    {selected_text}

    Respond ONLY in the following JSON format:
    {{
        "question": "<question_text>",
        "options": ["A) <option1>", "B) <option2>", "C) <option3>", "D) <option4>"],  # For MCQ
        "correct_answer": "<correct_option>"  
    }}
    or
    {{
        "question": "<question_text>",
        "options": ["A) True", "B) False"],  # Only for True/False
        "correct_answer": "<correct_option>"
    }}
    """

    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    print("✅ Response received.")  # Debugging print

    # Parse the JSON response
    try:
        question_data = json.loads(response["message"]["content"])
        return question_data  # Returns a dictionary with question, options, and correct answer
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON response from the model.")
        return None  # Handle invalid responses gracefully
