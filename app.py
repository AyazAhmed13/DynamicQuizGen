'''import traceback  
import gradio as gr
from main import extract_text_from_pdf, generate_questions_ollama, evaluate_answer
print('started')
# Load text from PDF
pdf_path = r"C:\\Users\\AyazAhemed\\Downloads\\python-3.13-docs-pdf-a4\\docs-pdf\\reference.pdf"
text = extract_text_from_pdf(pdf_path)

# Global state variables
session_state = {
    "question_count": 0,
    "difficulty": "easy",
    "score": 0,
    "num_questions": 5,
    "quiz_started": False,
    "current_question": None
}

# Function to start/restart the quiz
def start_quiz(num_questions):
    session_state["question_count"] = 0
    session_state["difficulty"] = "easy"
    session_state["score"] = 0
    session_state["num_questions"] = num_questions
    session_state["quiz_started"] = True
    difficulty_level = session_state["difficulty"]
    # Generate first question
    response = generate_questions_ollama(text, session_state["difficulty"])
    session_state["current_question"] = response  # Store in session
    
    # Debugging: Print response in terminal
    print("🔄 Ollama Response:", response)
    print(f"📊 Difficulty Level: {difficulty_level}")

    
    # Ensure response contains options
    if response and "options" in response:
        options = response["options"]
    else:
        options = ["Error: No options generated"]  # Fallback
    
    return response["question"], gr.Radio(choices=options), "", ""


#def start_quiz(num_questions):
    session_state["question_count"] = 0
    session_state["difficulty"] = "easy"
    session_state["score"] = 0
    session_state["num_questions"] = num_questions
    session_state["quiz_started"] = True
    session_state["current_question"] = generate_questions_ollama(text, session_state["difficulty"])
    
    return get_question_display()

# Function to get the next question
def get_question_display():
    if not session_state["quiz_started"]:
        return "Click 'Start Quiz' to begin!", ["No options available"], ""
    
    question = session_state["current_question"]
    if not question:
        return "Error loading question!", ["No options available"], ""
    
    return f"Question {session_state['question_count'] + 1}: {question['question']}", question.get("options", ["No options available"]), ""


# Function to handle answer submission
def submit_answer(selected_option):
    try:
        correct_answer = session_state["current_question"]["correct_answer"]

        # Extract the selected letter from the option (e.g., "D) ..." -> "D")
        selected_letter = selected_option.split(")")[0].strip()

        is_correct = selected_letter == correct_answer  # Now the comparison is accurate!

        # Update score if correct
        if is_correct:
            session_state["score"] += 1
            feedback = "✅ Correct!"
        else:
            feedback = f"❌ Incorrect! The correct answer was: {correct_answer}"

        # Move to next question
        session_state["question_count"] += 1
        if session_state["question_count"] >= session_state["num_questions"]:
            return "Quiz Completed!", [], feedback, f"Final Score: {session_state['score']} / {session_state['num_questions']}"

        # Generate next question
        new_question = generate_questions_ollama(text, session_state["difficulty"])
        session_state["current_question"] = new_question

        return new_question["question"], new_question["options"], feedback, f"Score: {session_state['score']}"

    except Exception as e:
        print(f"❌ Error in submit_answer: {e}")
        return "Error: Something went wrong!", [], "Please try again.", f"Score: {session_state['score']}"

#def submit_answer(selected_option):
    try:
        # 🔹 Print the full question dictionary for debugging
        print(f"📝 Current Question Data: {session_state.get('current_question', 'MISSING')}")

        # Check if "answer" key exists before accessing
        if "correct_answer" not in session_state["current_question"]:
            raise KeyError("Missing 'correct_answer' key in current_question")
        
        correct_answer = session_state["current_question"]["correct_answer"]
        is_correct = selected_option == correct_answer

        # Update score and difficulty
        if is_correct:
            session_state["score"] += 1
            session_state["difficulty"] = "medium" if session_state["difficulty"] == "easy" else "hard"
            feedback = "✅ Correct!"
        else:
            session_state["difficulty"] = "easy" if session_state["difficulty"] == "medium" else "medium"
            feedback = f"❌ Incorrect! The correct answer was: {correct_answer}"

        # Debugging info
        print(f"🔹 Selected: {selected_option} | Correct: {correct_answer} | Is Correct: {is_correct}")
        print(f"🔹 Score Updated: {session_state['score']} | Difficulty: {session_state['difficulty']}")

        # Move to next question
        session_state["question_count"] += 1

        # If quiz is complete
        if session_state["question_count"] >= session_state["num_questions"]:
            final_score = f"🏆 Quiz Complete! Your Score: {session_state['score']} / {session_state['num_questions']}"
            session_state["quiz_started"] = False
            return final_score, [], feedback, f"Final Score: {session_state['score']} / {session_state['num_questions']}"

        # Generate next question based on updated difficulty
        session_state["current_question"] = generate_questions_ollama(text, session_state["difficulty"])

        return session_state["current_question"]["question"], session_state["current_question"]["options"], feedback, f"Score: {session_state['score']}"

    except Exception as e:
        print(f"❌ Error in submit_answer: {e}")
        traceback.print_exc()  # Print full error traceback
        return "Error: Something went wrong!", [], "Please try again.", f"Score: {session_state['score']}"'''

'''def submit_answer(selected_option):
    try:
        correct_answer = session_state["current_question"]["correct_answer"]
        is_correct = selected_option == correct_answer

        # Update score and difficulty
        if is_correct:
            session_state["score"] += 1
            session_state["difficulty"] = "medium" if session_state["difficulty"] == "easy" else "hard"
            feedback = "✅ Correct!"
        else:
            session_state["difficulty"] = "easy" if session_state["difficulty"] == "medium" else "medium"
            feedback = f"❌ Incorrect! The correct answer was: {correct_answer}"

        # Move to next question
        session_state["question_count"] += 1

        # If quiz is complete
        if session_state["question_count"] >= session_state["num_questions"]:
            final_score = f"🏆 Quiz Complete! Your Score: {session_state['score']} / {session_state['num_questions']}"
            session_state["quiz_started"] = False
            return final_score, [], feedback, f"Final Score: {session_state['score']} / {session_state['num_questions']}"

        # Generate next question based on updated difficulty
        session_state["current_question"] = generate_questions_ollama(text, session_state["difficulty"])

        return session_state["current_question"]["question"], session_state["current_question"]["options"], feedback, f"Score: {session_state['score']}"

    except Exception as e:
        print(f"❌ Error in submit_answer: {e}")
        return "Error: Something went wrong!", [], "Please try again.", f"Score: {session_state['score']}"
'''
'''def submit_answer(selected_option):
    try:
        correct_answer = session_state["current_question"]["correct_answer"]
        is_correct = selected_option == correct_answer
        
        # Update score if correct
        if is_correct:
            session_state["score"] += 1
            feedback = "✅ Correct!"
        else:
            feedback = f"❌ Incorrect! The correct answer was: {correct_answer}"

        # Move to next question
        session_state["question_count"] += 1
        if session_state["question_count"] >= session_state["num_questions"]:
            return "Quiz Completed!", [], feedback, f"Final Score: {session_state['score']} / {session_state['num_questions']}"
        
        # Generate next question
        new_question = generate_questions_ollama(text, session_state["difficulty"])
        session_state["current_question"] = new_question

        return new_question["question"], new_question["options"], feedback, f"Score: {session_state['score']}"

    except Exception as e:
        print(f"❌ Error in submit_answer: {e}")
        return "Error: Something went wrong!", [], "Please try again.", f"Score: {session_state['score']}" 
    # Update difficulty
    if is_correct:
        session_state["score"] += 1
        session_state["difficulty"] = "medium" if session_state["difficulty"] == "easy" else "hard"
        result = "✅ Correct!"
    else:
        session_state["difficulty"] = "easy" if session_state["difficulty"] == "medium" else "medium"
        result = f"❌ Incorrect. The correct answer was: {correct_answer}"
    
    # Move to next question
    session_state["question_count"] += 1
    
    # If quiz is complete
    if session_state["question_count"] >= session_state["num_questions"]:
        final_score = f"🏆 Quiz Complete! Your Score: {session_state['score']} / {session_state['num_questions']}"
        session_state["quiz_started"] = False
        return final_score, [], "", ""
    
    # Generate next question
    session_state["current_question"] = generate_questions_ollama(text, session_state["difficulty"])
    return get_question_display()

# Function to exit quiz
def exit_quiz():
    session_state["quiz_started"] = False
    session_state["question_count"] = 0
    session_state["score"] = 0
    session_state["current_question"] = None
    return "🎉 Thank you for participating! The quiz has ended.", [], "", ""

# Gradio Interface
with gr.Blocks() as quiz_app:
    gr.Markdown("# 📝 Dynamic Quiz Generator")
    
    num_questions_slider = gr.Slider(1, 10, value=5, step=1, label="Select Number of Questions")
    start_button = gr.Button("▶️ Start Quiz")
    
    question_display = gr.Textbox(label="Question", interactive=False)
    answer_options = gr.Radio(label="Select an Answer", choices=[])
    submit_button = gr.Button("✅ Submit Answer")
    score_display = gr.Textbox(label="Score", interactive=False)
    
    restart_button = gr.Button("🔄 Restart Quiz")
    exit_button = gr.Button("🚪 Exit")
    
    # Event Bindings
    start_button.click(start_quiz, inputs=[num_questions_slider], outputs=[question_display, answer_options, answer_options, answer_options])
    submit_button.click(submit_answer, inputs=[answer_options], outputs=[question_display, answer_options, answer_options, answer_options])
    restart_button.click(start_quiz, inputs=[num_questions_slider], outputs=[question_display, answer_options, answer_options, answer_options])
    exit_button.click(exit_quiz, inputs=[], outputs=[question_display, answer_options, answer_options, answer_options])

# Run Gradio App
if __name__ == "__main__":
    quiz_app.launch()
'''

#second edit working good adding time
'''import traceback  
import gradio as gr
from main import extract_text_from_pdf, generate_questions_ollama, evaluate_answer

print('started')

# Load text from PDF
pdf_path = r"C:\\Users\\AyazAhemed\\Downloads\\python-3.13-docs-pdf-a4\\docs-pdf\\reference.pdf"
text = extract_text_from_pdf(pdf_path)

# Global state variables
session_state = {
    "question_count": 0,
    "difficulty": "easy",
    "score": 0,
    "num_questions": 5,
    "quiz_started": False,
    "current_question": None,
    "show_score": False,
    "show_slider": True  # Controls visibility of slider
}

# Function to start/restart the quiz
def start_quiz(num_questions):
    session_state["question_count"] = 0
    session_state["difficulty"] = "easy"
    session_state["score"] = 0
    session_state["num_questions"] = num_questions
    session_state["quiz_started"] = True
    session_state["show_score"] = False  # Hide score initially
    session_state["show_slider"] = False  # Hide slider after selection

    print("🔄 Generating question...")
    response = generate_questions_ollama(text, session_state["difficulty"])
    print(f"✅ Response received.\n🔄 Ollama Response: {response}\n📊 Difficulty Level: {session_state['difficulty']}")

    if response and "options" in response:
        session_state["current_question"] = response
        return response["question"], gr.update(choices=response["options"]), "", "", gr.update(visible=False)
    
    return "Error generating question!", gr.update(choices=[]), "", "", gr.update(visible=False)

# Function to handle answer submission
def submit_answer(selected_option):
    try:
        if not session_state["quiz_started"]:
            return "Click 'Start Quiz' to begin!", gr.update(choices=[]), "", "", gr.update(visible=False)
        
        correct_answer = session_state["current_question"]["correct_answer"]
        selected_letter = selected_option.split(")")[0].strip()
        correct_letter = correct_answer.split(")")[0].strip()
        print(f"📝 User Selected: {selected_letter}")
        print(f"✅ Correct Answer: {correct_letter}")
        is_correct = selected_letter == correct_answer

        if is_correct:
            session_state["score"] += 1
            feedback = "✅ Correct!"
        else:
            feedback = f"❌ Incorrect! The correct answer was: {correct_answer}"

        session_state["question_count"] += 1
        session_state["show_score"] = True  # Show score after first answer

        # Check if quiz is completed
        if session_state["question_count"] >= session_state["num_questions"]:
            session_state["quiz_started"] = False
            return "🎉 Quiz Completed!", gr.update(choices=[]), feedback, f"Final Score: {session_state['score']} / {session_state['num_questions']}", gr.update(visible=True)

        # Generate next question
        print("🔄 Generating next question...")
        new_question = generate_questions_ollama(text, session_state["difficulty"])
        print(f"✅ Response received.\n🔄 Ollama Response: {new_question}")

        if new_question and "options" in new_question:
            session_state["current_question"] = new_question
            return new_question["question"], gr.update(choices=new_question["options"]), feedback, f"Score: {session_state['score']}", gr.update(visible=True)

        return "Error generating next question!", gr.update(choices=[]), feedback, f"Score: {session_state['score']}", gr.update(visible=True)

    except Exception as e:
        print(f"❌ Error in submit_answer: {e}")
        traceback.print_exc()
        return "Error: Something went wrong!", gr.update(choices=[]), "Please try again.", f"Score: {session_state['score']}", gr.update(visible=True)

import time

def check_answer(selected_option):
    if session_state["quiz_ended"]:
        return

    correct_answer = session_state["questions"][session_state["current_question_index"]]["answer"]
    is_correct = selected_option == correct_answer
    
    # Calculate response time
    end_time = time.time()
    time_taken = end_time - session_state["start_time"]

    if is_correct:
        session_state["score"] += 1

        # Increase difficulty only if time taken is less than 30 seconds
        if time_taken < 30:
            session_state["difficulty"] = "medium" if session_state["difficulty"] == "easy" else "hard"
        
        result = "✅ Correct!"
    else:
        # Decrease difficulty if the answer is incorrect
        session_state["difficulty"] = "easy" if session_state["difficulty"] == "medium" else "medium"
        result = f"❌ Incorrect. The correct answer was: {correct_answer}"
    
    session_state["feedback"] = result
    session_state["selected_answer"] = selected_option

import time

def load_next_question():
    if session_state["current_question_index"] < len(session_state["questions"]) - 1:
        session_state["current_question_index"] += 1
        session_state["selected_answer"] = None
        session_state["feedback"] = ""

        # Start the timer when a new question is displayed
        session_state["start_time"] = time.time()
    else:
        session_state["quiz_ended"] = True

def restart_quiz():
    session_state["quiz_started"] = False  # Start fresh
    session_state["quiz_ended"] = False  # Allow Start Quiz button to show
    session_state["num_questions"] = 0  # Reset question count
    session_state["score"] = 0
    session_state["question_count"] = 0
    session_state["current_question"] = None
    session_state["options"] = []
    session_state["feedback"] = ""
    session_state["score_display"] = ""
# Function to exit quiz
def exit_quiz():
    session_state["quiz_started"] = False
    session_state["quiz_ended"] = True  # Show only "Start Quiz" button
    session_state["current_question"] = None
    session_state["options"] = []
    session_state["score_display"] = ""

    return "🎉 Thank you for participating! The quiz has ended.", \
           gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

# Gradio Interface
with gr.Blocks() as quiz_app:
    gr.Markdown("# 📝 Dynamic Quiz Generator")
    
    num_questions_slider = gr.Slider(1, 10, value=5, step=1, label="Select Number of Questions", visible=True)
    start_button = gr.Button("▶️ Start Quiz")
    
    question_display = gr.Textbox(label="Question", interactive=False)
    answer_options = gr.Radio(label="Select an Answer", choices=[])  # Choices updated dynamically
    submit_button = gr.Button("✅ Submit Answer")
    score_display = gr.Textbox(label="Score", interactive=False, visible=False)  # Initially hidden
    
    restart_button = gr.Button("🔄 Restart Quiz")
    exit_button = gr.Button("🚪 Exit")
    
    # Event Bindings
    start_button.click(start_quiz, inputs=[num_questions_slider], outputs=[question_display, answer_options, answer_options, score_display, num_questions_slider])
    submit_button.click(submit_answer, inputs=[answer_options], outputs=[question_display, answer_options, answer_options, score_display, score_display])
    restart_button.click(start_quiz, inputs=[num_questions_slider], outputs=[question_display, answer_options, answer_options, score_display, num_questions_slider])
    exit_button.click(exit_quiz, inputs=[], outputs=[question_display, answer_options, answer_options, score_display, num_questions_slider])

# Run Gradio App
if __name__ == "__main__":
    quiz_app.launch()


'''

import traceback
import gradio as gr
from main import extract_text_from_pdf, generate_questions_ollama, evaluate_answer
import time  # Import time module for timing functionality

print('started')

# Load text from PDF
#pdf_path = r"C:\\Users\\AyazAhemed\\Downloads\\python-3.13-docs-pdf-a4\\docs-pdf\\reference.pdf"


# Global state variables
session_state = {
    "pdf_text": None,
    "question_count": 0,
    "difficulty": "easy",
    "score": 0,
    "num_questions": 5,
    "quiz_started": False,
    "current_question": None,
    "show_score": False,
    "show_slider": True,  # Controls visibility of slider
    "start_time": None,  # To track when a question is displayed
    "quiz_ended": False  # To track if the quiz has ended
}
#testing
def upload_pdf(pdf_file):
    """Extract text from uploaded PDF and store it in session state."""
    if pdf_file:  # pdf_file is now a file path
        session_state["pdf_text"] = extract_text_from_pdf(pdf_file)  # ✅ Use file path
        return "✅ PDF uploaded successfully! You can start the quiz now."
    return "⚠️ Please upload a valid PDF file."


# Function to start/restart the quiz
def start_quiz(num_questions):
    text = session_state.get("pdf_text")
    
    if not text:
        return "⚠️ No PDF uploaded! Please upload a PDF before starting.", gr.update(choices=[]), "", "", gr.update(visible=False)
    session_state["question_count"] = 0
    session_state["difficulty"] = "easy"
    session_state["score"] = 0
    session_state["num_questions"] = num_questions
    session_state["quiz_started"] = True
    session_state["show_score"] = False  # Hide score initially
    session_state["show_slider"] = False  # Hide slider after selection
    session_state["quiz_ended"] = False  # Reset quiz ended state

    print("🔄 Generating question...")
    response = generate_questions_ollama(text, session_state["difficulty"])
    print(f"✅ Response received.\n🔄 Ollama Response: {response}\n📊 Difficulty Level: {session_state['difficulty']}")

    if response and "options" in response:
        session_state["current_question"] = response
        # Timer will start after the question is displayed (handled in the Gradio interface)
        return response["question"], gr.update(choices=response["options"]), "", "", gr.update(visible=False)
    
    return "Error generating question!", gr.update(choices=[]), "", "", gr.update(visible=False)

# Function to handle answer submission
def submit_answer(selected_option):
    try:
        if not session_state["quiz_started"]:
            return "Click 'Start Quiz' to begin!", gr.update(choices=[]), "", "", gr.update(visible=False)
        text = session_state.get("pdf_text")
        
        if not text:
            return "⚠️ No PDF uploaded! Please upload a PDF first.", gr.update(choices=[]), "", "", gr.update(visible=False)
        # Calculate time taken to answer the question
        if session_state["start_time"] is not None:
            end_time = time.time()
            time_taken = end_time - session_state["start_time"]
            print(f"⏱️ Time taken to answer: {time_taken:.2f} seconds")
        else:
            time_taken = 0  # Fallback if timer wasn't started

        correct_answer = session_state["current_question"]["correct_answer"]
        selected_letter = selected_option.split(")")[0].strip()
        correct_letter = correct_answer.split(")")[0].strip()
        print(f"📝 User Selected: {selected_letter}")
        print(f"✅ Correct Answer: {correct_letter}")
        is_correct = selected_letter == correct_letter

        # Adjust difficulty based on time taken and correctness
        if is_correct:
            session_state["score"] += 1
            feedback = "✅ Correct!"
            if time_taken < 10:  # If answered quickly, increase difficulty
                session_state["difficulty"] = "medium" if session_state["difficulty"] == "easy" else "hard"
        else:
            feedback = f"❌ Incorrect! The correct answer was: {correct_answer}"
            session_state["difficulty"] = "easy"  # Reset to easy if incorrect

        session_state["question_count"] += 1
        session_state["show_score"] = True  # Show score after first answer

        # Check if quiz is completed
        if session_state["question_count"] >= session_state["num_questions"]:
            session_state["quiz_started"] = False
            return "🎉 Quiz Completed!", gr.update(choices=[]), feedback, f"Final Score: {session_state['score']} / {session_state['num_questions']}", gr.update(visible=True)

        # Generate next question
        print("🔄 Generating next question...")
        new_question = generate_questions_ollama(text, session_state["difficulty"])
        print(f"✅ Response received.\n🔄 Ollama Response: {new_question}")
        print(f"📊 Difficulty Level: {session_state['difficulty']}")  # Log difficulty level for the new question

        if new_question and "options" in new_question:
            session_state["current_question"] = new_question
            # Timer will start after the question is displayed (handled in the Gradio interface)
            return new_question["question"], gr.update(choices=new_question["options"]), feedback, f"Score: {session_state['score']}", gr.update(visible=True)

        return "Error generating next question!", gr.update(choices=[]), feedback, f"Score: {session_state['score']}", gr.update(visible=True)

    except Exception as e:
        print(f"❌ Error in submit_answer: {e}")
        traceback.print_exc()
        return "Error: Something went wrong!", gr.update(choices=[]), "Please try again.", f"Score: {session_state['score']}", gr.update(visible=True)


'''def submit_answer(selected_option):
    try:
        if not session_state["quiz_started"]:
            return "Click 'Start Quiz' to begin!", gr.update(choices=[]), "", "", gr.update(visible=False)
        
        # Calculate time taken to answer the question
        if session_state["start_time"] is not None:
            end_time = time.time()
            time_taken = end_time - session_state["start_time"]
            print(f"⏱️ Time taken to answer: {time_taken:.2f} seconds")
        else:
            time_taken = 0  # Fallback if timer wasn't started

        correct_answer = session_state["current_question"]["correct_answer"]
        selected_letter = selected_option.split(")")[0].strip()
        correct_letter = correct_answer.split(")")[0].strip()
        print(f"📝 User Selected: {selected_letter}")
        print(f"✅ Correct Answer: {correct_letter}")
        is_correct = selected_letter == correct_letter

        # Adjust difficulty based on time taken and correctness
        if is_correct:
            session_state["score"] += 1
            feedback = "✅ Correct!"
            if time_taken < 10:  # If answered quickly, increase difficulty
                session_state["difficulty"] = "medium" if session_state["difficulty"] == "easy" else "hard"
        else:
            feedback = f"❌ Incorrect! The correct answer was: {correct_answer}"
            session_state["difficulty"] = "easy"  # Reset to easy if incorrect

        session_state["question_count"] += 1
        session_state["show_score"] = True  # Show score after first answer

        # Check if quiz is completed
        if session_state["question_count"] >= session_state["num_questions"]:
            session_state["quiz_started"] = False
            return "🎉 Quiz Completed!", gr.update(choices=[]), feedback, f"Final Score: {session_state['score']} / {session_state['num_questions']}", gr.update(visible=True)

        # Generate next question
        print("🔄 Generating next question...")
        new_question = generate_questions_ollama(text, session_state["difficulty"])
        print(f"✅ Response received.\n🔄 Ollama Response: {new_question}")

        if new_question and "options" in new_question:
            session_state["current_question"] = new_question
            # Timer will start after the question is displayed (handled in the Gradio interface)
            return new_question["question"], gr.update(choices=new_question["options"]), feedback, f"Score: {session_state['score']}", gr.update(visible=True)

        return "Error generating next question!", gr.update(choices=[]), feedback, f"Score: {session_state['score']}", gr.update(visible=True)

    except Exception as e:
        print(f"❌ Error in submit_answer: {e}")
        traceback.print_exc()
        return "Error: Something went wrong!", gr.update(choices=[]), "Please try again.", f"Score: {session_state['score']}", gr.update(visible=True)
'''
# Function to exit quiz
def exit_quiz():
    session_state["quiz_started"] = False
    session_state["quiz_ended"] = True  # Mark quiz as ended
    return "🎉 Thank you for participating! The quiz has ended.", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

# Gradio Interface
with gr.Blocks() as quiz_app:
    gr.Markdown("# 📝 Dynamic Quiz Generator")
#testing
    pdf_uploader = gr.File(label="Upload PDF", type="filepath")
    upload_button = gr.Button("📤 Upload PDF")
    upload_status = gr.Textbox(interactive=False, label="Upload Status")
    
    num_questions_slider = gr.Slider(1, 10, value=5, step=1, label="Select Number of Questions", visible=True)
    start_button = gr.Button("▶️ Start Quiz")
    #testing
    upload_button.click(upload_pdf, inputs=[pdf_uploader], outputs=[upload_status])
    question_display = gr.Textbox(label="Question", interactive=False)
    answer_options = gr.Radio(label="Select an Answer", choices=[])  # Choices updated dynamically
    submit_button = gr.Button("✅ Submit Answer")
    score_display = gr.Textbox(label="Score", interactive=False, visible=False)  # Initially hidden
    
    restart_button = gr.Button("🔄 Restart Quiz")
    exit_button = gr.Button("🚪 Exit")
    
    # Event Bindings
    start_button.click(
        start_quiz,
        inputs=[num_questions_slider],
        outputs=[question_display, answer_options, answer_options, score_display, num_questions_slider]
    ).then(
        lambda: session_state.update({"start_time": time.time()}),  # Start timer after question is displayed
        inputs=None,
        outputs=None
    )
    
    submit_button.click(
        submit_answer,
        inputs=[answer_options],
        outputs=[question_display, answer_options, answer_options, score_display, score_display]
    ).then(
        lambda: session_state.update({"start_time": time.time()}),  # Start timer for the next question
        inputs=None,
        outputs=None
    )
    
    restart_button.click(
        start_quiz,
        inputs=[num_questions_slider],
        outputs=[question_display, answer_options, answer_options, score_display, num_questions_slider]
    ).then(
        lambda: session_state.update({"start_time": time.time()}),  # Start timer after restart
        inputs=None,
        outputs=None
    )
    
    exit_button.click(
        exit_quiz,
        inputs=[],
        outputs=[question_display, answer_options, answer_options, score_display, num_questions_slider]
    )

# Run Gradio App
if __name__ == "__main__":
    quiz_app.launch()