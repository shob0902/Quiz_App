import tkinter as tk
from tkinter import messagebox, ttk
import json
import random
import time
from datetime import datetime
from tkinter import font as tkfont

class QuizGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz")
        self.master.configure(bg="#000000")
        self.master.geometry("900x650")
        self.master.resizable(False, False)

        # Custom fonts
        self.title_font = tkfont.Font(family="Arial", size=44, weight="bold")
        self.stats_font = tkfont.Font(family="Arial", size=20, weight="bold")
        self.feedback_font = tkfont.Font(family="Arial", size=18, weight="bold")
        self.button_font = tkfont.Font(family="Arial", size=16, weight="bold")
        self.option_font = tkfont.Font(family="Arial", size=16, weight="bold")
        self.question_font = tkfont.Font(family="Arial", size=20, weight="bold")

        # Quiz state
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.total_questions = 0
        self.start_time = None
        self.end_time = None
        self.timer_label = None
        self.timer_running = False
        self.answered = False

        self.load_questions()
        self.start_quiz()

    def load_questions(self):
        """Load questions from JSON file"""
        try:
            with open("questions.json", "r") as f:
                self.questions = json.load(f)
            self.total_questions = len(self.questions)
            random.shuffle(self.questions)  # Shuffle questions
        except FileNotFoundError:
            messagebox.showerror("Error", "questions.json file not found!")
            self.master.destroy()
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format in questions.json!")
            self.master.destroy()

    def start_quiz(self):
        """Start the quiz"""
        self.current_question = 0
        self.score = 0
        self.start_time = time.time()
        self.show_question_ui()
        self.display_question()
        self.timer_running = True
        self.update_timer()

    def show_question_ui(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        # Title
        self.title_label = tk.Label(
            self.master,
            text="Quiz",
            font=self.title_font,
            fg="white",
            bg="#000000"
        )
        self.title_label.pack(pady=(30, 20))
        # Rounded question box using Canvas
        self.canvas = tk.Canvas(self.master, width=800, height=120, bg="#000000", highlightthickness=0)
        self.canvas.pack(pady=(0, 40))
        self.rounded_box = self._draw_rounded_rect(self.canvas, 0, 0, 800, 120, radius=40, fill="#151515")
        # Question text in the center
        self.question_text = self.canvas.create_text(
            400, 60,
            text="",
            font=self.question_font,
            fill="white",
            justify="center",
            width=700
        )
        # Option canvases (2x2 grid)
        self.options_frame = tk.Frame(self.master, bg="#000000")
        self.options_frame.pack(pady=(0, 0))
        self.option_canvases = []
        for row in range(2):
            for col in range(2):
                c = tk.Canvas(self.options_frame, width=340, height=70, bg="#000000", highlightthickness=0, bd=0)
                c.grid(row=row, column=col, padx=30, pady=15)
                # Draw rounded rectangle and text
                rect = self._draw_rounded_rect(c, 0, 0, 340, 70, radius=35, fill="#222222")
                text = c.create_text(170, 35, text="choose", font=self.option_font, fill="white", width=300)
                self.option_canvases.append((c, rect, text))
        for i in range(2):
            self.options_frame.grid_rowconfigure(i, weight=1)
            self.options_frame.grid_columnconfigure(i, weight=1)
        # Timer label at the bottom
        self.timer_label = tk.Label(self.master, text="Time: 00:00", font=self.button_font, fg="white", bg="#000000")
        self.timer_label.pack(side=tk.BOTTOM, pady=(0, 10))

    def _draw_rounded_rect(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, splinesteps=36, **kwargs)

    def update_timer(self):
        if self.timer_running and self.start_time is not None:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            if self.timer_label:
                self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
            self.master.after(1000, self.update_timer)

    def display_question(self):
        """Display the current question"""
        self.answered = False
        if self.current_question < self.total_questions:
            question = self.questions[self.current_question]
            
            # Display question
            self.canvas.itemconfig(self.question_text, text=question['question'])
            
            # Display options
            for i, (c, rect, text) in enumerate(self.option_canvases):
                c.itemconfig(rect, fill="#222222")
                c.itemconfig(text, text=question['options'][i] if i < len(question['options']) else "choose", fill="white")
                c.tag_bind(rect, '<Button-1>', lambda e, idx=i: self.check_answer(idx))
                c.tag_bind(text, '<Button-1>', lambda e, idx=i: self.check_answer(idx))
                c.tag_bind(rect, '<Enter>', lambda e, idx=i: self._on_option_hover(idx, True))
                c.tag_bind(text, '<Enter>', lambda e, idx=i: self._on_option_hover(idx, True))
                c.tag_bind(rect, '<Leave>', lambda e, idx=i: self._on_option_hover(idx, False))
                c.tag_bind(text, '<Leave>', lambda e, idx=i: self._on_option_hover(idx, False))
                c.config(cursor="hand2")
                c.bind('<Button-1>', lambda e, idx=i: self.check_answer(idx))
                c.bind('<Enter>', lambda e, idx=i: self._on_option_hover(idx, True))
                c.bind('<Leave>', lambda e, idx=i: self._on_option_hover(idx, False))
                c.state = "normal"
        else:
            self.show_result()

    def _on_option_hover(self, idx, entering):
        c, rect, text = self.option_canvases[idx]
        if c.state == "disabled":
            return
        if entering:
            c.itemconfig(rect, fill="#333333")
        else:
            c.itemconfig(rect, fill="#222222")

    def check_answer(self, idx):
        """Check if the selected answer is correct"""
        if self.answered:
            return
        self.answered = True
        question = self.questions[self.current_question]
        selected_answer = question['options'][idx]
        correct_answer = question['answer']
        
        # Disable all buttons temporarily
        for c, rect, text in self.option_canvases:
            c.state = "disabled"
        
        if selected_answer == correct_answer:
            self.score += 1
            # Show correct feedback
            for c, rect, text in self.option_canvases:
                c.itemconfig(rect, fill="#27ae60")
            messagebox.showinfo("Correct!", "✅ Well done! That's correct!")
        else:
            # Show incorrect feedback
            for c, rect, text in self.option_canvases:
                c.itemconfig(rect, fill="#e74c3c")
            messagebox.showinfo("Incorrect", f"❌ Wrong! The correct answer is: {correct_answer}")
        
        # Reset button colors and enable them
        for c, rect, text in self.option_canvases:
            c.itemconfig(rect, fill="#222222")
            c.state = "normal"
        
        self.master.after(900, self._after_feedback)

    def _after_feedback(self):
        self.current_question += 1
        if self.current_question < self.total_questions:
            self.display_question()
        else:
            self.end_time = time.time()
            self.timer_running = False
            self.show_result()

    def show_result(self):
        """Display final results"""
        self.end_time = time.time()
        time_taken = int(self.end_time - self.start_time)
        minutes = time_taken // 60
        seconds = time_taken % 60
        
        percentage = (self.score / self.total_questions) * 100
        
        # Clear the main frame
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Create results display
        results_frame = tk.Frame(self.master, bg='#000000')
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Results title
        tk.Label(
            results_frame,
            text="🎉 Quiz Completed! 🎉",
            font=self.title_font,
            fg="white",
            bg='#000000'
        ).pack(pady=(50, 30))
        
        # Results details
        results_text = f"""
🗂️  Final Score: {self.score}/{self.total_questions}
📋 Percentage: {percentage:.1f}%
⏰ Time Taken: {minutes}m {seconds}s
        """
        
        tk.Label(
            results_frame,
            text=results_text,
            font=self.stats_font,
            fg='white',
            bg='#000000',
            justify=tk.CENTER
        ).pack(pady=(0, 30))
        
        # Performance feedback
        if percentage >= 90:
            feedback = ("🏆 Excellent! Outstanding performance!", "#27ae60")
        elif percentage >= 80:
            feedback = ("🎯 Great job! Well done!", "#27ae60")
        elif percentage >= 70:
            feedback = ("👍 Good work! Keep it up!", "#27ae60")
        elif percentage >= 60:
            feedback = ("📚 Not bad! Room for improvement.", "#27ae60")
        else:
            feedback = ("📖 Keep studying! Practice makes perfect!", "#e67e22")
        
        feedback_label = tk.Label(
            results_frame,
            text=feedback[0],
            font=self.feedback_font,
            fg=feedback[1],
            bg='#000000'
        )
        feedback_label.pack(pady=(0, 30))
        
        # Buttons frame
        buttons_frame = tk.Frame(results_frame, bg='#000000')
        buttons_frame.pack()
        
        # Play again button
        play_btn = tk.Button(
            buttons_frame,
            text="🗂️ Play Again",
            font=self.button_font,
            fg="white",
            bg="#2196f3",
            activebackground="#1976d2",
            width=14,
            height=2,
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.start_quiz
        )
        play_btn.pack(side=tk.LEFT, padx=10)
        
        # Save results button
        save_btn = tk.Button(
            buttons_frame,
            text="💾 Save Results",
            font=self.button_font,
            fg="white",
            bg="#27ae60",
            activebackground="#219150",
            width=14,
            height=2,
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.save_results
        )
        save_btn.pack(side=tk.LEFT, padx=10)
        
        # Exit button
        exit_btn = tk.Button(
            buttons_frame,
            text="🛑 Exit",
            font=self.button_font,
            fg="white",
            bg="#e74c3c",
            activebackground="#c0392b",
            width=14,
            height=2,
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.master.destroy
        )
        exit_btn.pack(side=tk.LEFT, padx=10)

    def save_results(self):
        """Save quiz results to file"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            percentage = (self.score / self.total_questions) * 100
            time_taken = int(self.end_time - self.start_time)
            minutes = time_taken // 60
            seconds = time_taken % 60
            
            result_entry = {
                "timestamp": timestamp,
                "score": self.score,
                "total": self.total_questions,
                "percentage": round(percentage, 1),
                "time_taken": f"{minutes}m {seconds}s"
            }
            
            # Load existing results or create new list
            try:
                with open("results.txt", "r") as f:
                    results = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                results = []
            
            results.append(result_entry)
            
            # Save updated results
            with open("results.txt", "w") as f:
                json.dump(results, f, indent=2)
            
            messagebox.showinfo("Success", "💾 Results saved to results.txt!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not save results: {e}")

def main():
    """Main function to start the GUI quiz app"""
    root = tk.Tk()
    app = QuizGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 