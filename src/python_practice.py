"""Beginner-friendly examples of core Python fundamentals. Run: python src/python_practice.py"""
from pathlib import Path

def main() -> None:
    # Variables and data types
    learner, lessons, score = "Alex", 3, 87.5
    print("Types:", type(learner).__name__, type(lessons).__name__, type(score).__name__)
    # Arithmetic, comparison, and logical operators
    print("Arithmetic:", 7 + 2, 7 / 2, 7 // 2, 7 % 2, 2 ** 3)
    print("Comparisons/logical:", score >= 50, lessons > 0 and score < 100)
    # Conditional statements
    if score >= 80:
        result = "strong pass"
    elif score >= 50:
        result = "pass"
    else:
        result = "review needed"
    print("Conditional:", result)
    # For and while loops
    for number in range(1, 4):
        print("For loop:", number)
    countdown = 2
    while countdown > 0:
        print("While loop:", countdown)
        countdown -= 1
    # Functions and return values
    def average(values: list[float]) -> float:
        return sum(values) / len(values) if values else 0.0
    print("Function result:", average([80, 90, 100]))
    # Lists and common list operations
    topics = ["Python", "Pandas"]
    topics.append("Charts")
    topics.sort()
    print("List:", topics, "first:", topics[0])
    # Tuples are ordered and immutable
    coordinate = (4, 7)
    print("Tuple:", coordinate)
    # Dictionaries store key/value pairs
    learner_record = {"name": learner, "lessons": lessons}
    print("Dictionary:", learner_record)
    # Sets contain unique values
    unique_topics = set(topics + ["Python"])
    print("Set:", sorted(unique_topics))
    # File handling: write and read a small text file beside this script
    note_path = Path(__file__).resolve().parent / "practice_note.txt"
    try:
        note_path.write_text("Python file handling works.\n", encoding="utf-8")
        print("File contents:", note_path.read_text(encoding="utf-8").strip())
    except OSError as exc:
        print(f"Could not read/write practice note at {note_path}: {exc}")
    # Basic error handling
    try:
        converted = int("not a number")
    except ValueError as exc:
        print("Handled conversion error:", exc)

if __name__ == "__main__":
    main()
