import tkinter as tk
from tkinter import ttk, messagebox
from pyswip import Prolog

STUDENT = "student1"

QUESTIONS = [
    ("Do you forget information quickly?", "forgets_quickly"),
    ("Are you preparing for exams now?", "preparing_for_exams"),
    ("Do you want long-term retention?", "wants_long_term_retention"),
    ("Are you studying a large amount of content?", "studying_large_content"),
    ("Do you learn best by explaining concepts to others?", "learns_by_explaining"),
    ("Do you prefer visual learning?", "prefers_visual_learning"),
    ("Do you like diagrams / structured notes?", "likes_diagrams"),
    ("Are you studying a practical course (math/programming/engineering)?", "studying_practical_course"),
    ("Do you prefer organized schedules?", "prefers_organized_schedule"),
    ("Do you mostly study alone?", "studies_alone"),
    ("Do you get bored reading textbooks?", "bored_reading_textbooks"),
    ("Do you prefer engaging methods?", "wants_engaging_methods"),
    ("Do you procrastinate often?", "procrastinates"),
    ("Are you easily distracted?", "easily_distracted"),
    ("Do you prefer discussion-based learning?", "prefers_discussion"),
    ("Do you like collaborative learning?", "collaborative_learner"),
    ("Do you struggle with complex topics deeply?", "difficulty_with_complex_topics"),
]

EXPLANATIONS = {
    "active_recall": "Active Recall is a method where you try to remember information without looking at your notes. This strengthens memory and helps you retain information for a longer time.",
    "spaced_repetition": "Spaced Repetition involves reviewing information at increasing time intervals to help move knowledge from short-term memory to long-term memory.",
    "feynman_technique": "The Feynman Technique involves explaining a concept in very simple language as if teaching someone else. This helps you identify gaps in your understanding.",
    "pomodoro_technique": "The Pomodoro Technique is a time-management method where you study for 25 minutes and take a 5-minute break. This helps maintain focus and prevents burnout.",
    "mind_mapping": "Mind Mapping is a visual way of organizing ideas by connecting related concepts around a central topic. It helps improve understanding and memory.",
    "practice_based_learning": "Practice-Based Learning focuses on learning by doing practical tasks instead of only reading or watching tutorials. It helps develop real skills through hands-on experience and problem solving.",
    "distraction_free_environment": "A Distraction-Free Environment involves studying in a place with minimal interruptions and distractions. This improves concentration and helps you study more effectively.",
    "personal_study_timetable": "A Personal Study Timetable is a planned schedule that organizes what and when to study. It helps manage time well and ensures all subjects are covered regularly.",
    "practice_questions": "Practice Testing involves solving questions under real exam conditions without looking at your notes. It helps improve exam confidence.",
    "group_study": "Group Study involves studying with others to discuss ideas and solve problems together to improve understanding.",
}

DISPLAY_NAMES = {
    "active_recall": "Active Recall",
    "spaced_repetition": "Spaced Repetition",
    "feynman_technique": "Feynman Technique",
    "pomodoro_technique": "Pomodoro Technique",
    "mind_mapping": "Mind Mapping",
    "practice_based_learning": "Practice-Based Learning",
    "distraction_free_environment": "Distraction-Free Environment",
    "personal_study_timetable": "Personal Study Timetable",
    "practice_questions": "Practice Testing",
    "group_study": "Group Study",
}


class StudyExpertSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Method Recommendation Expert System")
        self.root.geometry("980x720")
        self.root.minsize(900, 650)

        self.prolog = Prolog()
        self.prolog.consult("../knowledge_base/studyrules.pl")

        self.answers = {}
        self.build_gui()

    def build_gui(self):
        title = tk.Label(
            self.root,
            text="Study Method Recommendation Expert System",
            font=("Arial", 18, "bold"),
            pady=10
        )
        title.pack()

        subtitle = tk.Label(
            self.root,
            text="Select Yes or No for each statement, then click Generate Recommendation.",
            font=("Arial", 11)
        )
        subtitle.pack(pady=(0, 10))

        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True, padx=15, pady=10)

        # Left side: questions
        left_frame = tk.LabelFrame(container, text="Student Questions", padx=10, pady=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        canvas = tk.Canvas(left_frame)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for question, trait in QUESTIONS:
            frame = tk.Frame(self.scrollable_frame)
            frame.pack(fill="x", pady=5)

            # Question label (limit width so it doesn't push buttons)
            label = tk.Label(
                frame,
                text=question,
                anchor="w",
                justify="left",
                wraplength=380   # 👈 REDUCED from 500 → 380
            )
            label.pack(side="left", fill="x", expand=True)

            var = tk.StringVar(value="no")
            self.answers[trait] = var

            # Create a separate frame for buttons
            btn_frame = tk.Frame(frame)
            btn_frame.pack(side="right")

            yes_btn = tk.Radiobutton(btn_frame, text="Yes", variable=var, value="yes")
            no_btn = tk.Radiobutton(btn_frame, text="No", variable=var, value="no")

            # Add spacing
            yes_btn.pack(side="left", padx=5)
            no_btn.pack(side="left", padx=5)

        # Right side: results
        right_frame = tk.LabelFrame(container, text="Recommendations", padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True)

        self.result_box = tk.Text(right_frame, wrap="word", font=("Arial", 11))
        self.result_box.pack(fill="both", expand=True)

        button_frame = tk.Frame(self.root, pady=10)
        button_frame.pack()

        generate_btn = tk.Button(
            button_frame,
            text="Generate Recommendation",
            font=("Arial", 11, "bold"),
            width=24,
            command=self.generate_recommendations
        )
        generate_btn.pack(side="left", padx=10)

        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            font=("Arial", 11),
            width=12,
            command=self.clear_form
        )
        clear_btn.pack(side="left", padx=10)

    def generate_recommendations(self):
        try:
            self.result_box.delete("1.0", tk.END)

            # Clear previous facts for this student
            list(self.prolog.query(f"retractall(fact({STUDENT}, _))"))

            # Assert only the selected YES traits
            selected_traits = []
            for _, trait in QUESTIONS:
                if self.answers[trait].get() == "yes":
                    list(self.prolog.query(f"assertz(fact({STUDENT}, {trait}))"))
                    selected_traits.append(trait)

            results = list(self.prolog.query(f"recommendations({STUDENT}, List)"))

            self.result_box.insert(tk.END, "=== Recommended Study Techniques ===\n\n")

            if not results or not results[0]["List"]:
                self.result_box.insert(
                    tk.END,
                    "No recommendation matched based on the selected answers.\n"
                )
                return

            recs = results[0]["List"]

            for rec in recs:
                title = DISPLAY_NAMES.get(rec, rec.replace("_", " ").title())
                explanation = EXPLANATIONS.get(rec, "No explanation available.")

                self.result_box.insert(tk.END, f"{title}\n", "heading")
                self.result_box.insert(tk.END, f"{explanation}\n\n")

            self.result_box.tag_config("heading", font=("Arial", 12, "bold"))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

    def clear_form(self):
        for _, trait in QUESTIONS:
            self.answers[trait].set("no")
        self.result_box.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = StudyExpertSystemGUI(root)
    root.mainloop()