import re
import sqlite3

RE_NAME = "^[a-zA-z ]{1,100}$"
RE_GRADE = "^(100|[1-9]?[0-9])$"
RE_EMAIL = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"


def validate_input(str_prompt, pattern, str_invalid="Invalid value. Try again.\n"):
    while True:
        val = input(str_prompt).strip()

        is_valid = re.match(pattern, val)
        if is_valid is not None:
            break
        else:
            print("\n" + str_invalid)
    return val


def wait_for_user(str="Press Enter to return to Main Menu..."):
    print()
    input(str)


def find_student_by_id(c):
    # Create parameterized query
    query = "SELECT * FROM student WHERE id = ?"

    # Loop until student row found or return to Main Menu
    while True:
        # Get student ID
        u_id = input("Enter Student ID (0 to exit): ").strip()

        # Stop early if 0
        if u_id == "0":
            print("\nReturning to Main Menu...")
            return None

        # Skip to next loop if bad data
        if re.match("^[0-9]+$", u_id) is None:
            print("Please enter a valid ID.")
            continue

        # Check db for student row
        try:
            res = c.execute(query, u_id)
            data = res.fetchall()
        except sqlite3.Error as e:
            print(f"\nUnable to retrieve student data: {e}")
            return None

        # Skip to next loop if no data
        if len(data) == 0:
            print("\nStudent ID does not exist.\n")
            continue

        return data[0]


def add_record(c):
    print("\nAdd a new student. Please provide student information:\n")

    # Get student data
    s_name = validate_input(
        "Student Name: ",
        RE_NAME,
        "Invalid name. Please use letters and spaces only.\n",
    )

    # Get student grade
    s_grade = validate_input(
        "Current grade (0-100): ",
        RE_GRADE,
        "Invalid grade. Please enter value between 0 and 100, inclusive.\n",
    )

    # Get student email
    s_email = validate_input(
        "Email address: ",
        RE_EMAIL,
        "Invalid email. Please follow format '<user>@<domain>.<tld> Try again.\n",
    )

    # Create parameterized query data
    query = "INSERT INTO student (name, grade, email) VALUES (?, ?, ?)"
    s_data = (s_name, s_grade, s_email)

    # Write student data to db
    try:
        c.execute(query, s_data)
        print("\nStudent successfully entered.\n")

        wait_for_user("Press Enter to return to Main Menu...")
    except sqlite3.Error as e:
        print(f"\nUnable to add student: {e}")
        return


def view_records(c):
    print("\nStudent Records\n")

    # Get records from db
    try:
        res = c.execute("SELECT * FROM student")
        data = res.fetchall()
    except sqlite3.Error as e:
        print(f"Unable to retrieve student data: {e}")
        return

    # Print records
    if len(data) == 0:
        print("No student records found.\n")
    else:
        for row in data:
            s_id, s_name, s_grade, s_email = row
            print(f"{s_id}. {s_name} -- Grade: {s_grade} -- Email: {s_email}")

    wait_for_user("Press Enter to return to Main Menu...")


def update_record(c):
    print("\nUpdate Student Record\n")

    s_data = find_student_by_id(c)
    if s_data is None:
        return

    # Get new student information
    print("\nWhat would you like to update?")

    # Validate column name
    while True:
        col = input("[name, grade, email]: ").strip()
        if col not in ["name", "grade", "email"]:
            print("\nInvalid response. Try again.\n")
        else:
            break

    # Set up references for validation and query
    col_refs = {
        "name": (RE_NAME, "UPDATE student SET name = ? WHERE id = ?"),
        "grade": (RE_GRADE, "UPDATE student SET grade = ? WHERE id = ?"),
        "email": (RE_EMAIL, "UPDATE student SET email = ? WHERE id = ?"),
    }
    pattern, u_query = col_refs[col]

    # Validate value and construct query string
    val = validate_input("\nPlease enter new value: ", pattern)

    # Update student row
    data = (val, s_data[0])
    try:
        c.execute(u_query, data)
        print("\nStudent successfully updated.")

        wait_for_user("Press Enter to return to Main Menu...")
    except sqlite3.Error as e:
        print(f"Unable to update student: {e}")


# Remove student row from db
def delete_record(c):
    print("\nRemove Student Record\n")

    s_data = find_student_by_id(c)
    if s_data is None:
        return

    # If student found, confirm deletion
    s_id, s_name, s_grade, s_email = s_data
    print(f"\n{s_id}. Student: {s_name} -- Grade: {s_grade} -- Email: {s_email}\n")
    print(f"Are you sure you want to delete student {s_name}?")
    res = input("[yes/No]: ").strip()
    if res in ["yes", "Yes", "y", "Y"]:
        d_query = "DELETE FROM student WHERE id = ?"
        d_id = s_id

        try:
            c.execute(d_query, (d_id,))
            print("\nStudent record successfully deleted")

            wait_for_user()
        except sqlite3.Error as e:
            print(f"Unable to delete row: {e}")
    else:
        print("\nDeletion aborted. Returning to Main Menu...")


def main():
    # Connect to db if it exists, or create it
    con = sqlite3.connect("students.db")
    # Create cursor to execute SQL statements
    cur = con.cursor()
    # Create student table unless it exists
    cur.execute(
        "CREATE TABLE IF NOT EXISTS student("
        "   id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "   name VARCHAR(100) NOT NULL, "
        "   grade VARCHAR(3) DEFAULT '0', "
        "   email VARCHAR(100) NOT NULL"
        ")"
    )

    print("Welcome to the Student Records Management System.")

    # Main Menu, loops indefinitely
    while True:
        print("\nMain Menu\n")
        print(
            "Please select from the following options:\n"
            "1. Add a new student record\n"
            "2. View all existing student records\n"
            "3. Update an existing student's information\n"
            "4. Delete a student record\n"
            "5. Exit the program\n"
        )

        # Loops until valid input
        while True:
            response = input("Command: ")
            match response:
                case "1":
                    add_record(cur)
                    con.commit()
                    break
                case "2":
                    view_records(cur)
                    break
                case "3":
                    update_record(cur)
                    con.commit()
                    break
                case "4":
                    delete_record(cur)
                    con.commit()
                    break
                case "5":
                    break
                case _:
                    print("Invalid response. Try again.")

        # Exit gracefully
        if response == "5":
            print(
                "\nThank you for using the Student Records Management System. Goodbye."
            )
            break

    # Shut down db connection
    con.close()


if __name__ == "__main__":
    main()
