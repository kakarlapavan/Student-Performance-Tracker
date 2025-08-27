
from student_tracker.tracker import StudentTracker
import sys

def prompt_int(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Please enter a valid integer.")

def prompt_float(prompt):
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Please enter a valid number.")

def main():
    tracker = StudentTracker()

    while True:
        print("\n--- Student Performance Tracker (CLI) ---")
        print("1. Add Student")
        print("2. Add/Update Grades")
        print("3. View Student Details")
        print("4. Calculate Student Average")
        print("5. Subject-wise Topper")
        print("6. Class Average for a Subject")
        print("7. Backup to Text File")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Enter student name: ").strip()
            roll = prompt_int("Enter roll number: ")
            if tracker.add_student(name, roll):
                print("Student added.")
            else:
                print("Roll number already exists.")
        elif choice == "2":
            roll = prompt_int("Enter roll number: ")
            grades = {}
            while True:
                subject = input("Subject name (or blank to stop): ").strip()
                if not subject:
                    break
                score = prompt_float(f"Score for {subject} (0-100): ")
                if 0 <= score <= 100:
                    grades[subject] = score
                else:
                    print("Invalid score range.")
            ok = tracker.add_grades(roll, grades)
            print("Grades saved." if ok else "Student not found.")
        elif choice == "3":
            roll = prompt_int("Enter roll number: ")
            s = tracker.get_student(roll)
            if s:
                print(s.info())
            else:
                print("Student not found.")
        elif choice == "4":
            roll = prompt_int("Enter roll number: ")
            avg = tracker.calculate_average(roll)
            print(f"Average: {avg:.2f}" if avg is not None else "No grades or student not found.")
        elif choice == "5":
            subject = input("Enter subject: ").strip()
            topper = tracker.subject_topper(subject)
            if topper:
                r, n, sc = topper
                print(f"Topper in {subject}: {n} (Roll {r}) with {sc}")
            else:
                print("No data for this subject yet.")
        elif choice == "6":
            subject = input("Enter subject: ").strip()
            avg = tracker.class_average(subject)
            print(f"Class average in {subject}: {avg:.2f}" if avg is not None else "No data for this subject yet.")
        elif choice == "7":
            path = tracker.backup_to_text("backup.txt")
            print(f"Backup saved to {path}")
        elif choice == "0":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
