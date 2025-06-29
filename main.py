import json
import random
import time
from datetime import datetime

class QuizApp:
    def __init__(self):
        self.questions = []
        self.score = 0
        self.total_questions = 0
        self.start_time = None
        self.end_time = None
        
    def load_questions(self):
        """Load questions from JSON file"""
        try:
            with open("questions.json", "r") as f:
                self.questions = json.load(f)
            self.total_questions = len(self.questions)
            print(f"✅ Loaded {self.total_questions} questions successfully!")
        except FileNotFoundError:
            print("❌ Error: questions.json file not found!")
            return False
        except json.JSONDecodeError:
            print("❌ Error: Invalid JSON format in questions.json!")
            return False
        return True
    
    def shuffle_questions(self):
        """Randomly shuffle the questions"""
        random.shuffle(self.questions)
        print("🔄 Questions shuffled!")
    
    def display_welcome(self):
        """Display welcome message and instructions"""
        print("=" * 60)
        print("🎯 WELCOME TO THE QUIZ APP! 🎯")
        print("=" * 60)
        print("📝 Instructions:")
        print("• You will be shown one question at a time")
        print("• Choose the correct answer from the options (1-4)")
        print("• Your score will be tracked throughout the quiz")
        print("• At the end, you'll see your final score and time taken")
        print("=" * 60)
        input("Press Enter to start the quiz...")
    
    def display_question(self, question_data, question_num):
        """Display a single question with options"""
        print(f"\n{'='*50}")
        print(f"Question {question_num}/{self.total_questions}")
        print(f"{'='*50}")
        print(f"❓ {question_data['question']}")
        print()
        
        for idx, option in enumerate(question_data['options'], 1):
            print(f"   {idx}. {option}")
        print()
    
    def get_user_answer(self):
        """Get and validate user input"""
        while True:
            try:
                user_input = input("Your choice (1-4): ").strip()
                choice = int(user_input)
                if 1 <= choice <= 4:
                    return choice
                else:
                    print("❌ Please enter a number between 1 and 4!")
            except ValueError:
                print("❌ Please enter a valid number!")
    
    def check_answer(self, question_data, user_choice):
        """Check if the user's answer is correct"""
        correct_answer = question_data['answer']
        user_answer = question_data['options'][user_choice - 1]
        
        if user_answer == correct_answer:
            print("✅ Correct! Well done!")
            self.score += 1
            return True
        else:
            print(f"❌ Wrong! The correct answer is: {correct_answer}")
            return False
    
    def display_progress(self):
        """Display current progress"""
        percentage = (self.score / self.total_questions) * 100
        print(f"\n📊 Progress: {self.score}/{self.total_questions} ({percentage:.1f}%)")
    
    def calculate_time_taken(self):
        """Calculate time taken for the quiz"""
        if self.start_time and self.end_time:
            time_taken = self.end_time - self.start_time
            minutes = int(time_taken // 60)
            seconds = int(time_taken % 60)
            return f"{minutes}m {seconds}s"
        return "Unknown"
    
    def display_final_results(self):
        """Display final results"""
        print("\n" + "="*60)
        print("🎉 QUIZ COMPLETED! 🎉")
        print("="*60)
        
        percentage = (self.score / self.total_questions) * 100
        time_taken = self.calculate_time_taken()
        
        print(f"📊 Final Score: {self.score}/{self.total_questions}")
        print(f"📈 Percentage: {percentage:.1f}%")
        print(f"⏱️  Time Taken: {time_taken}")
        
        # Performance feedback
        if percentage >= 90:
            print("🏆 Excellent! Outstanding performance!")
        elif percentage >= 80:
            print("🎯 Great job! Well done!")
        elif percentage >= 70:
            print("👍 Good work! Keep it up!")
        elif percentage >= 60:
            print("📚 Not bad! Room for improvement.")
        else:
            print("📖 Keep studying! Practice makes perfect!")
        
        print("="*60)
    
    def save_results(self):
        """Save quiz results to file"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            percentage = (self.score / self.total_questions) * 100
            time_taken = self.calculate_time_taken()
            
            result_entry = {
                "timestamp": timestamp,
                "score": self.score,
                "total": self.total_questions,
                "percentage": round(percentage, 1),
                "time_taken": time_taken
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
            
            print("💾 Results saved to results.txt")
            
        except Exception as e:
            print(f"⚠️  Could not save results: {e}")
    
    def run_quiz(self):
        """Main quiz execution"""
        # Load questions
        if not self.load_questions():
            return
        
        # Display welcome
        self.display_welcome()
        
        # Shuffle questions for variety
        self.shuffle_questions()
        
        # Start timer
        self.start_time = time.time()
        
        # Run through questions
        for idx, question in enumerate(self.questions, 1):
            self.display_question(question, idx)
            user_choice = self.get_user_answer()
            self.check_answer(question, user_choice)
            self.display_progress()
            
            # Small pause between questions
            time.sleep(1)
        
        # End timer
        self.end_time = time.time()
        
        # Display final results
        self.display_final_results()
        
        # Save results
        self.save_results()
        
        # Ask if user wants to play again
        play_again = input("\n🔄 Would you like to take the quiz again? (y/n): ").lower()
        if play_again in ['y', 'yes']:
            print("\n" + "="*50)
            self.__init__()  # Reset the quiz
            self.run_quiz()
        else:
            print("👋 Thanks for playing! Goodbye!")

def main():
    """Main function to start the quiz app"""
    quiz = QuizApp()
    quiz.run_quiz()

if __name__ == "__main__":
    main() 