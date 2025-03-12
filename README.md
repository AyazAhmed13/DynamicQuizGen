# Dynamic Quiz Generator

This project is a **dynamic quiz generator** that extracts text from a PDF, generates questions dynamically using the Mistral model via Ollama, and adjusts question difficulty based on user responses. It includes a **Gradio-based UI** for an interactive quiz experience.

## Features
- 📄 **Upload PDF**: Extract text from any uploaded PDF.
- 🤖 **AI-Generated Questions**: Uses Mistral (via Ollama) to generate questions dynamically.
- 📊 **Adaptive Difficulty**: Adjusts question difficulty based on response time and correctness.
- 📊 Score Tracking – Keeps track of user performance.
- 📂 **Persistent Storage**: Stores user responses using ChromaDB.
- 🎭 **Interactive UI**: Built with Gradio for easy interaction.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/dynamic-quiz-generator.git
   cd dynamic-quiz-generator
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the application:**
  
📌 Option 1: Run CLI-Based Quiz

python main.py

🌐 Option 2: Run Web App with Gradio

python app.py

This will launch a local Gradio interface where you can upload PDFs and start quizzes interactively.

## Usage

1. Upload a PDF containing relevant content.
2. Select the number of questions you want.
3. Start the quiz and answer the dynamically generated questions.
4. View your final score at the end of the quiz.

## File Structure
```
├── app.py              # Main Gradio application
├── main.py             # Core quiz logic
├── utils/
│   ├── pdf_parser.py   # Extracts text from PDF
│   ├── qg_pipeline.py  # Generates questions using Ollama
│   ├── evaluator.py    # Evaluates user answers
│   ├── db_utils.py     # Stores responses in ChromaDB
├── requirements.txt    # Required dependencies
├── README.md           # Project documentation
```

## Dependencies
- `gradio`
- `pdfplumber`
- `ollama`
- `chromadb`

Install them using:
```sh
pip install -r requirements.txt
```

## Contributing
Feel free to fork and submit pull requests!



