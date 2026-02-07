# Student Records Management System

A simple command-line application for managing student records using Python and SQLite.

## Overview

This Student Records Management System provides a user-friendly interface for performing CRUD (Create, Read, Update, Delete) operations on student data. The application stores student information including names, grades, and email addresses in a local SQLite database.

## Features

- **Add Student Records**: Create new student entries with validated input
- **View All Records**: Display all students in the database
- **Update Records**: Modify existing student information (name, grade, or email)
- **Delete Records**: Remove student records with confirmation
- **Input Validation**: Built-in regex validation for names, grades, and email addresses
- **Persistent Storage**: All data is stored in a SQLite database (`students.db`)

## Requirements

- Python 3.10 or higher (uses `match` statement)
- SQLite3 (included with Python standard library)

## Installation

1. Clone this repository:

```bash
git clone https://github.com/willdelorm/student-records-system.git
cd student-records-system
```

2. No additional dependencies required - uses Python standard library only!

## Usage

Run the program:

```bash
python main.py
```

### Main Menu Options

```
1. Add a new student record
2. View all existing student records
3. Update an existing student's information
4. Delete a student record
5. Exit the program
```

### Example Workflow

**Adding a Student:**

```
Student Name: John Doe
Current grade (0-100): 85
Email address: john.doe@example.com
```

**Updating a Student:**

```
Enter Student ID: 1
What would you like to update?
[name, grade, email]: grade
Please enter new value: 90
```

**Deleting a Student:**

```
Enter Student ID: 1
Are you sure you want to delete student John Doe?
[yes/No]: yes
```

## Database Schema

The application automatically creates a `students.db` SQLite database with the following schema:

| Column | Type         | Constraints                |
| ------ | ------------ | -------------------------- |
| id     | INTEGER      | PRIMARY KEY, AUTOINCREMENT |
| name   | VARCHAR(100) | NOT NULL                   |
| grade  | VARCHAR(3)   | DEFAULT '0'                |
| email  | VARCHAR(100) | NOT NULL                   |

## Input Validation

The application validates all user input:

- **Name**: 1-100 characters, letters and spaces only
- **Grade**: Integer between 0-100 (inclusive)
- **Email**: Valid email format (user@domain.tld)

## Error Handling

- Graceful handling of SQLite errors
- User-friendly error messages
- Input validation with retry prompts
- Confirmation prompts for destructive operations

## Project Structure

```
student-records-system/
├── main.py          # Main application file
├── students.db      # SQLite database (created on first run)
└── README.md        # This file
```

## Functions

- `validate_input()`: Validates user input against regex patterns
- `find_student_by_id()`: Searches for a student by ID
- `add_record()`: Adds a new student to the database
- `view_records()`: Displays all student records
- `update_record()`: Updates existing student information
- `delete_record()`: Removes a student record
- `main()`: Main program loop and menu system

## Future Enhancements

- [ ] Search functionality (by name or email)
- [ ] Export records to CSV
- [ ] Bulk import from file
- [ ] Grade statistics and analytics
- [ ] Data backup and restore
- [ ] GUI interface

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

Will Delorm - [will@willdelorm.com](mailto:will@willdelorm.com)

## Acknowledgments

- Built with Python's standard library
- Uses SQLite for lightweight data persistence
