# 🎯 Quiz App with Score Tracker

A Python-based quiz application with multiple interface options: Command Line Interface (CLI), and Tkinter GUI. Features include score tracking, timer, question shuffling, and result history.

## 📁 Project Structure

```
quiz-app/
│
├── main.py                  # CLI version of the quiz app
├── gui_quiz.py             # Tkinter GUI version
├── questions.json          # Quiz questions database
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── assets/                # Optional: images or media
└── results.txt            # Quiz results history (auto-generated)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project files**

2. **Install dependencies** (for Streamlit version):
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 How to Run

### Option 1: Command Line Interface (CLI)
```bash
python main.py
```

**Features:**
- ✅ Simple text-based interface
- ✅ Score tracking
- ✅ Timer functionality
- ✅ Question shuffling
- ✅ Result saving
- ✅ Play again option

### Option 2: Tkinter GUI (Desktop App)
```bash
python gui_quiz.py
```

**Features:**
- ✅ Modern desktop GUI
- ✅ Interactive buttons
- ✅ Real-time progress bar
- ✅ Timer display
- ✅ Visual feedback for answers
- ✅ Save results functionality
- ✅ Play again option

### Option 3: Streamlit Web App
```bash
streamlit run streamlit_quiz.py
```

**Features:**
- ✅ Web-based interface
- ✅ Responsive design
- ✅ Progress tracking
- ✅ Quiz history
- ✅ Statistics dashboard
- ✅ Modern UI with custom CSS
- ✅ Sidebar with additional info

## 📊 Features

### Core Features
- **Multiple Choice Questions**: 4 options per question
- **Score Tracking**: Real-time score updates
- **Timer**: Track time taken for the quiz
- **Question Shuffling**: Random question order for variety
- **Result History**: Save and view past quiz results
- **Performance Feedback**: Get feedback based on your score

### Advanced Features
- **Progress Tracking**: Visual progress indicators
- **Statistics**: View average scores and performance trends
- **Responsive Design**: Works on different screen sizes
- **Error Handling**: Graceful handling of file errors
- **Data Persistence**: Results saved to JSON format

## 📝 Customizing Questions

Edit `questions.json` to add your own questions:

```json
[
  {
    "question": "Your question here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Correct Option"
  }
]
```

### Question Format
- **question**: The question text
- **options**: Array of 4 possible answers
- **answer**: The correct answer (must match one of the options exactly)

## 🎯 Sample Questions Included

The app comes with 10 sample questions covering:
- Geography (capitals, countries)
- Science (planets, chemistry)
- Literature (authors)
- History (dates)
- Mathematics (geometry)

## 📈 Understanding Results

### Score Categories
- **90%+**: 🏆 Excellent! Outstanding performance!
- **80-89%**: 🎯 Great job! Well done!
- **70-79%**: 👍 Good work! Keep it up!
- **60-69%**: 📚 Not bad! Room for improvement.
- **<60%**: 📖 Keep studying! Practice makes perfect!

### Results File Format
Results are saved in `results.txt` as JSON:
```json
[
  {
    "timestamp": "2024-01-15 14:30:25",
    "score": 8,
    "total": 10,
    "percentage": 80.0,
    "time_taken": "2m 15s"
  }
]
```

## 🔧 Technical Details

### Dependencies
- **Python Standard Library**: `json`, `random`, `time`, `datetime`
- **Tkinter**: Built-in GUI library (no installation needed)
- **Streamlit**: Web app framework (`pip install streamlit`)
- **Pandas**: Data manipulation (optional, for advanced features)

### File Descriptions
- `main.py`: CLI version with full feature set
- `gui_quiz.py`: Tkinter GUI with modern interface
- `streamlit_quiz.py`: Web app with interactive dashboard
- `questions.json`: Question database in JSON format
- `results.txt`: Auto-generated results history

## 🚀 Deployment

### Local Development
All versions work locally without additional setup beyond Python installation.

### Desktop Distribution (Tkinter)
The Tkinter version can be packaged into standalone executables using tools like:
- PyInstaller: `pip install pyinstaller && pyinstaller --onefile gui_quiz.py`
- cx_Freeze: For cross-platform distribution

## 🐛 Troubleshooting

### Common Issues

**"questions.json file not found"**
- Ensure `questions.json` is in the same directory as the Python files
- Check file permissions

**"Invalid JSON format"**
- Validate your JSON syntax using online tools
- Ensure proper comma placement and quote usage

**Streamlit not working**
- Install with: `pip install streamlit`
- Check Python version compatibility

**Tkinter errors**
- Tkinter is included with Python by default
- On Linux, you might need: `sudo apt-get install python3-tk`

## 🤝 Contributing

Feel free to enhance the quiz app by:
- Adding more questions to `questions.json`
- Implementing new features
- Improving the UI/UX
- Adding new question types
- Creating additional themes

## 📄 License

This project is open source and available under the MIT License.

## 🎉 Enjoy Your Quiz!

Choose the interface that works best for you and start testing your knowledge! The app is designed to be educational, engaging, and easy to use.

---

**Happy Quizzing! 🎯** 
