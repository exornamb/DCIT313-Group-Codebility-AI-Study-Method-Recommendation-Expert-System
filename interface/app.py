from pyswip import Prolog

STUDENT = "student1"

QUESTIONS = [
    ("Do you forget information quickly? (y/n): ", "forgets_quickly"),
    ("Are you preparing for exams now? (y/n): ", "preparing_for_exams"),

    ("Do you want long-term retention? (y/n): ", "wants_long_term_retention"),
    ("Are you studying a large amount of content? (y/n): ", "studying_large_content"),

    ("Do you learn best by explaining concepts to others? (y/n): ", "learns_by_explaining"),

    ("Do you prefer visual learning? (y/n): ", "prefers_visual_learning"),
    ("Do you like diagrams / structured notes? (y/n): ", "likes_diagrams"),

    ("Are you studying a practical course (math/programming/engineering)? (y/n): ", "studying_practical_course"),

    ("Do you prefer organized schedules? (y/n): ", "prefers_organized_schedule"),
    ("Do you mostly study alone? (y/n): ", "studies_alone"),

    ("Do you get bored reading textbooks? (y/n): ", "bored_reading_textbooks"),
    ("Do you prefer engaging methods? (y/n): ", "wants_engaging_methods"),

    ("Do you procrastinate often? (y/n): ", "procrastinates"),
    ("Are you easily distracted? (y/n): ", "easily_distracted"),

    ("Do you prefer discussion-based learning? (y/n): ", "prefers_discussion"),
    ("Do you like collaborative learning? (y/n): ", "collaborative_learner"),

    ("Do you struggle with complex topics deeply? (y/n): ", "difficulty_with_complex_topics"),
]

# Explanation dictionary
EXPLANATIONS = {
    "active_recall": "Active Recall is a method where you try to remember information without looking at your notes. This strengthens memory and helps you retain information for a longer time.",

    "spaced_repetition": "Spaced Repetition involves reviewing information at increasing time intervals to help move knowledge from short-term memory to long-term memory.",

    "feynman_technique": "The Feynman Technique involves explaining a concept in very simple language as if teaching someone else. This helps you identify gaps in your understanding.",

    "pomodoro_technique": "The Pomodoro Technique is a time-management method where you study for 25 minutes and take a 5-minute break. This helps maintain focus and prevents burnout.",

    "mind_mapping": "Mind Mapping is a visual way of organizing ideas by connecting related concepts around a central topic. It helps improve understanding and memory.",

    "practice_based_learning": "Practice-Based Learning focuses on learning by doing practical tasks instead of only reading or watching tutorials.",

    "distraction_free_environment": "A Distraction-Free Environment involves studying in a place with minimal interruptions to improve concentration.",

    "personal_study_timetable": "A Personal Study Timetable is a planned schedule that organizes what and when to study to help manage time effectively.",

    "practice_questions": "Practice Testing involves solving questions under real exam conditions without looking at notes to improve exam confidence.",

    "group_study": "Group Study involves studying with others to discuss ideas and solve problems together to improve understanding."
}

def yn(prompt: str) -> bool:
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please type y/n.")

def main():
    prolog = Prolog()

    prolog.consult("../knowledge_base/studyrules.pl")

    list(prolog.query(f"retractall(fact({STUDENT}, _))"))

    for question, trait in QUESTIONS:
        if yn(question):
            list(prolog.query(f"assertz(fact({STUDENT}, {trait}))"))

    results = list(prolog.query(f"recommendations({STUDENT}, List)"))

    print("\n=== Recommended Study Techniques ===\n")

    if not results:
        print("No recommendation matched. Try different answers.")
        return

    recs = results[0]["List"]

    if not recs:
        print("No recommendation matched. Try different answers.")
        return

    for r in recs:
        name = r.replace("_", " ").title()
        print(f"{name}")
        print(EXPLANATIONS.get(r, "No explanation available."))
        print()

if __name__ == "__main__":
    main()