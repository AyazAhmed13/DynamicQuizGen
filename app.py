
import traceback
import gradio as gr
from main import extract_text_from_pdf, generate_questions_ollama, evaluate_answer
import time  # Import time module for timing functionality

print('started')

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

# Function to exit quiz
def exit_quiz():
    session_state["quiz_started"] = False
    session_state["quiz_ended"] = True  # Mark quiz as ended
    return "🎉 Thank you for participating! The quiz has ended.", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

# Gradio Interface
with gr.Blocks() as quiz_app:
    gr.Markdown("# 📝 Dynamic Quiz Generator")

    pdf_uploader = gr.File(label="Upload PDF", type="filepath")
    upload_button = gr.Button("📤 Upload PDF")
    upload_status = gr.Textbox(interactive=False, label="Upload Status")
    num_questions_slider = gr.Slider(1, 10, value=5, step=1, label="Select Number of Questions", visible=True)
    start_button = gr.Button("▶️ Start Quiz")
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
