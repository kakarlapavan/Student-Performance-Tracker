
import sqlite3
from typing import Dict, Optional, List, Tuple

DB_FILE = "student_tracker.db"

def _ensure_db(db_path: str = DB_FILE):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            roll_number INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_number INTEGER NOT NULL,
            subject TEXT NOT NULL,
            score REAL NOT NULL CHECK(score >= 0 AND score <= 100),
            FOREIGN KEY (roll_number) REFERENCES students(roll_number)
        );
    ''')
    con.commit()
    con.close()

class Student:
    def __init__(self, name: str, roll_number: int, grades: Optional[Dict[str, float]] = None):
        self.name = name
        self.roll_number = roll_number
        self.grades: Dict[str, float] = grades or {}

    def add_grade(self, subject: str, score: float):
        if not (0 <= score <= 100):
            raise ValueError("Score must be between 0 and 100.")
        self.grades[subject] = score

    def average_grade(self) -> Optional[float]:
        if not self.grades:
            return None
        return sum(self.grades.values()) / len(self.grades)

    def info(self) -> str:
        avg = self.average_grade()
        avg_str = f"{avg:.2f}" if avg is not None else "N/A"
        lines = [f"Student: {self.name} (Roll: {self.roll_number})", f"Average: {avg_str}", "Grades:"]
        for subj, score in self.grades.items():
            lines.append(f"  - {subj}: {score}")
        return "\n".join(lines)

class StudentTracker:
    def __init__(self, db_path: str = DB_FILE):
        self.db_path = db_path
        _ensure_db(self.db_path)

    # ---------- Helper methods ----------
    def _connect(self):
        return sqlite3.connect(self.db_path)

    def is_roll_unique(self, roll_number: int) -> bool:
        con = self._connect()
        cur = con.cursor()
        cur.execute("SELECT 1 FROM students WHERE roll_number = ?", (roll_number,))
        exists = cur.fetchone() is None
        con.close()
        return exists

    def add_student(self, name: str, roll_number: int) -> bool:
        if not self.is_roll_unique(roll_number):
            return False
        con = self._connect()
        cur = con.cursor()
        cur.execute("INSERT INTO students (roll_number, name) VALUES (?, ?)", (roll_number, name))
        con.commit()
        con.close()
        return True

    def add_grades(self, roll_number: int, grades: Dict[str, float]) -> bool:
        if not self.get_student(roll_number):
            return False
        # validate
        for subject, score in grades.items():
            if not (0 <= float(score) <= 100):
                raise ValueError("Scores must be between 0 and 100. Invalid: %s=%s" % (subject, score))
        con = self._connect()
        cur = con.cursor()
        # upsert behavior: delete existing subjects for this roll and re-insert provided ones
        for subject, score in grades.items():
            cur.execute("DELETE FROM grades WHERE roll_number=? AND subject=?", (roll_number, subject))
            cur.execute("INSERT INTO grades (roll_number, subject, score) VALUES (?, ?, ?)", (roll_number, subject, float(score)))
        con.commit()
        con.close()
        return True

    def get_student(self, roll_number: int) -> Optional[Student]:
        con = self._connect()
        cur = con.cursor()
        cur.execute("SELECT name FROM students WHERE roll_number = ?", (roll_number,))
        row = cur.fetchone()
        if not row:
            con.close()
            return None
        name = row[0]
        cur.execute("SELECT subject, score FROM grades WHERE roll_number = ?", (roll_number,))
        grades = dict(cur.fetchall())
        con.close()
        return Student(name=name, roll_number=roll_number, grades=grades)

    def calculate_average(self, roll_number: int) -> Optional[float]:
        student = self.get_student(roll_number)
        return student.average_grade() if student else None

    def all_students(self) -> List[Student]:
        con = self._connect()
        cur = con.cursor()
        cur.execute("SELECT roll_number, name FROM students ORDER BY roll_number ASC")
        students_rows = cur.fetchall()
        students = []
        for roll, name in students_rows:
            cur.execute("SELECT subject, score FROM grades WHERE roll_number = ?", (roll,))
            grades = dict(cur.fetchall())
            students.append(Student(name=name, roll_number=roll, grades=grades))
        con.close()
        return students

    # ---------- Bonus Features ----------
    def subject_topper(self, subject: str) -> Optional[Tuple[int, str, float]]:
        \"\"\"Return (roll_number, name, score) for the top-performing student in a subject.\"\"\"
        con = self._connect()
        cur = con.cursor()
        cur.execute(\"\"\"
            SELECT s.roll_number, s.name, g.score
            FROM grades g
            JOIN students s ON s.roll_number = g.roll_number
            WHERE g.subject = ?
            ORDER BY g.score DESC, s.roll_number ASC
            LIMIT 1
        \"\"\", (subject,))
        row = cur.fetchone()
        con.close()
        return row if row else None

    def class_average(self, subject: str) -> Optional[float]:
        con = self._connect()
        cur = con.cursor()
        cur.execute("SELECT AVG(score) FROM grades WHERE subject = ?", (subject,))
        row = cur.fetchone()
        con.close()
        return float(row[0]) if row and row[0] is not None else None

    def backup_to_text(self, file_path: str) -> str:
        \"\"\"Save student data to a simple text file for backup.\"\"\"
        students = self.all_students()
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("Student Performance Backup\n")
            f.write("==========================\n\n")
            for s in students:
                f.write(s.info() + "\n\n")
        return file_path
