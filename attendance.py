import csv, os
from datetime import date

STUDENTS = "students.csv"
RECORDS = "attendance.csv"

def init_files():
    for f, header in [(STUDENTS, ["id", "name"]), (RECORDS, ["date", "id", "status"])]:
        if not os.path.exists(f):
            with open(f, "w", newline="") as fh:
                csv.writer(fh).writerow(header)

def load_students():
    with open(STUDENTS) as f:
        return list(csv.DictReader(f))

def add_student():
    sid = input("Student ID: ").strip()
    name = input("Name: ").strip()
    if any(s["id"] == sid for s in load_students()):
        print("ID already exists.")
        return
    with open(STUDENTS, "a", newline="") as f:
        csv.writer(f).writerow([sid, name])
    print("Student added.")

def mark_attendance():
    students = load_students()
    if not students:
        print("No students yet. Add students first.")
        return
    today = str(date.today())
    with open(RECORDS, "a", newline="") as f:
        w = csv.writer(f)
        for s in students:
            status = ""
            while status not in ("P", "A"):
                status = input(f"{s['id']} {s['name']} (P/A): ").strip().upper()
            w.writerow([today, s["id"], status])
    print("Attendance saved.")

def percentages():
    stats = {}
    with open(RECORDS) as f:
        for r in csv.DictReader(f):
            total, present = stats.get(r["id"], (0, 0))
            stats[r["id"]] = (total + 1, present + (r["status"] == "P"))
    return {k: round(p * 100 / t, 1) for k, (t, p) in stats.items()}

def view_report():
    names = {s["id"]: s["name"] for s in load_students()}
    data = percentages()
    if not data:
        print("No attendance recorded yet.")
        return
    for sid, pct in data.items():
        print(f"{sid} {names.get(sid, '?')}: {pct}%")

def defaulters():
    names = {s["id"]: s["name"] for s in load_students()}
    found = False
    for sid, pct in percentages().items():
        if pct < 75:
            print(f"{sid} {names.get(sid, '?')}: {pct}% (below 75%)")
            found = True
    if not found:
        print("No defaulters.")

def menu():
    print("\n1. Add student\n2. Mark attendance\n3. View report\n4. Defaulters (<75%)\n5. Exit")
    return input("Choose: ").strip()

def main():
    init_files()
    while True:
        choice = menu()
        if choice == "1":
            add_student()
        elif choice == "2":
            mark_attendance()
        elif choice == "3":
            view_report()
        elif choice == "4":
            defaulters()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
