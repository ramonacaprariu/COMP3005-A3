import psycopg2
from dotenv import load_dotenv
import os
from datetime import date, datetime

#want to use the .env file variables set
load_dotenv()

connection = psycopg2.connect(user = os.getenv("db_user"),
                              password = os.getenv("db_password"),
                              host = os.getenv("db_host"),
                              port = os.getenv("db_port"),
                              database = os.getenv("db_name"))
 
cursor = connection.cursor()

def get_all_students():
    cursor.execute('SELECT * FROM students ORDER BY student_id;')
    rows = cursor.fetchall()
    for row in rows:
        #f-string so formatted string literal here
        print(f"Student ID: {row[0]}, Name: {row[1]} {row[2]}, E-mail: {row[3]}, Enrollment Date: {row[4]}")

def add_student():
    f_name = input("Provide the student's first name: ")
    l_name = input("Provide the student's last name: ")
    email = input("Provide the student's email: ")
    e_date = input("Provide the student's enrollment date, formatted YYYY-MM-DD: ")
    # result = True
    try:
        result = bool(datetime.strptime(e_date, "%Y-%m-%d"))
    except ValueError:
        # res = False
        print("Invalid date. Student not added to system.")
        return
    e_date = e_date.split("-")
    year, month, day = [int(item) for item in e_date]
    e_date = date(year, month, day)

    try:
        #using the psycopg2 %s placeholders to pass in variables
        cursor.execute('INSERT into students(first_name, last_name, email, enrollment_date)' \
        'VALUES (%s, %s, %s, %s);', (f_name, l_name, email, e_date))
    except psycopg2.errors.UniqueViolation:
       print("Email already in use. Student not added to system.")
       return
    
    #committing the changes to database
    connection.commit()


def update_email():
    id = int(input("Provide the student's id: "))
    #checking for id validity
    cursor.execute('SELECT COUNT(*) FROM students WHERE student_id = %s;', (id,))
    row = cursor.fetchone()
    count = row[0]
    #notifying no student was deleted
    if count == 0:
        print("No student with matching id.")
        return
    
    email = input("Provide the updated email address: ")
    #checking uniqueness of email
    try:
        #for id, even though numeric, %s still used
        cursor.execute('UPDATE students SET email = %s WHERE student_id = %s;', (email, id))
        connection.commit()
    except psycopg2.errors.UniqueViolation:
       print("Email already in use. Student email not updated.")

def delete_student():
    id = int(input("Provide the student's id: "))

    cursor.execute('SELECT COUNT(*) FROM students WHERE student_id = %s;', (id,))
    row = cursor.fetchone()
    count = row[0]
    #notifying no student was deleted
    if count == 0:
        print("No student with matching id.")
        return
    cursor.execute('DELETE FROM students WHERE student_id = %s;', (id,))
    connection.commit()

#hard-coding values, just to match up to the spec-provided values
def reset():
    #deleting all additionally added students
    cursor.execute('DELETE FROM students WHERE student_id > 3')
    #resetting the auto-incrementing student_id
    cursor.execute('ALTER SEQUENCE students_student_id_seq RESTART WITH 4')
    print("Program successfully reset.")
    connection.commit()

def display_menu():
    print("Choose one of the following options:")
    print("1. Get all students")
    print("2. Add a student")
    print("3. Update a student's email")
    print("4. Delete a student")
    print("5: Reset program")
    print("6: Quit")

def user_choice():
    choice = input("Enter: ")
    return choice

while True:
    display_menu()
    choice = user_choice()
    while not choice.isdigit() or int(choice) < 1 or int(choice) > 6:
        choice = input("Enter a valid menu option: ")
    if int(choice) == 1:
        get_all_students()
        print()
    elif int(choice) == 2:
        add_student()
        print()
    elif int(choice) == 3:
        update_email()
        print()
    elif int(choice) == 4:
        delete_student()
        print()
    elif int(choice) == 5:
        reset()
        print()
    else:
        print("Goodbye!")
        break

connection.close()
cursor.close()