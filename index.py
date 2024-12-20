import sqlite3

try:
    from tkinter import *
    from tkinter import messagebox, ttk
except ImportError:
    print("Error: Tkinter is not available in your environment. Please ensure you have Tkinter installed.")
    exit(1)

# Database setup
def connect_database():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            grade TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Add a student to the database
def add_student(name, age, grade):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", (name, age, grade))
    conn.commit()
    conn.close()

# View all students from the database
def view_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Update a student in the database
def update_student(student_id, name, age, grade):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE students
        SET name = ?, age = ?, grade = ?
        WHERE id = ?
    """, (name, age, grade, student_id))
    conn.commit()
    conn.close()

# Delete a student from the database
def delete_student(student_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

# GUI setup
def student_management_system():
    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        for row in view_students():
            tree.insert("", END, values=row)

    def add():
        if name_var.get() == "" or age_var.get() == "" or grade_var.get() == "":
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            age = int(age_var.get())
            add_student(name_var.get(), age, grade_var.get())
            refresh_table()
            name_var.set("")
            age_var.set("")
            grade_var.set("")
        except ValueError:
            messagebox.showerror("Error", "Age must be an integer")

    def update():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a student to update")
            return
        student_id = tree.item(selected_item, "values")[0]
        try:
            age = int(age_var.get())
            update_student(student_id, name_var.get(), age, grade_var.get())
            refresh_table()
            name_var.set("")
            age_var.set("")
            grade_var.set("")
        except ValueError:
            messagebox.showerror("Error", "Age must be an integer")

    def delete():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a student to delete")
            return
        student_id = tree.item(selected_item, "values")[0]
        delete_student(student_id)
        refresh_table()

    def select(event):
        selected_item = tree.selection()
        if not selected_item:
            return
        student = tree.item(selected_item, "values")
        name_var.set(student[1])
        age_var.set(student[2])
        grade_var.set(student[3])

    # Main window
    root = Tk()
    root.title("Student Management System")
    root.geometry("800x500")
    root.configure(bg="#f2f2f2")

    # Style configurations
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 10), rowheight=25)
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    style.configure("TButton", font=("Arial", 10))

    # Variables
    name_var = StringVar()
    age_var = StringVar()
    grade_var = StringVar()

    # Input fields
    Label(root, text="Name:", bg="#f2f2f2", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=W)
    Entry(root, textvariable=name_var, font=("Arial", 12), width=20).grid(row=0, column=1, padx=10, pady=10)

    Label(root, text="Age:", bg="#f2f2f2", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky=W)
    Entry(root, textvariable=age_var, font=("Arial", 12), width=20).grid(row=1, column=1, padx=10, pady=10)

    Label(root, text="Grade:", bg="#f2f2f2", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky=W)
    Entry(root, textvariable=grade_var, font=("Arial", 12), width=20).grid(row=2, column=1, padx=10, pady=10)

    # Buttons
    Button(root, text="Add", command=add, font=("Arial", 12), bg="#4CAF50", fg="white", width=10).grid(row=0, column=2, padx=10, pady=10)
    Button(root, text="Update", command=update, font=("Arial", 12), bg="#2196F3", fg="white", width=10).grid(row=1, column=2, padx=10, pady=10)
    Button(root, text="Delete", command=delete, font=("Arial", 12), bg="#f44336", fg="white", width=10).grid(row=2, column=2, padx=10, pady=10)

    # Table
    columns = ("ID", "Name", "Age", "Grade")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("Grade", text="Grade")
    tree.column("ID", width=50, anchor=CENTER)
    tree.column("Name", width=200, anchor=W)
    tree.column("Age", width=100, anchor=CENTER)
    tree.column("Grade", width=150, anchor=W)
    tree.grid(row=3, column=0, columnspan=3, padx=10, pady=20)

    # Bind select event
    tree.bind("<ButtonRelease-1>", select)

    refresh_table()
    root.mainloop()

# Initialize database and start GUI
if __name__ == "__main__":
    connect_database()
    try:
        student_management_system()
    except Exception as e:
        print("An error occurred while running the application:", e)
        exit(1)


# import sqlite3
# import bcrypt
# from tkinter import *
# from tkinter import messagebox, ttk


# # Database setup
# def connect_database():
#     conn = sqlite3.connect("students.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS students (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT NOT NULL,
#             name TEXT NOT NULL,
#             age INTEGER NOT NULL,
#             grade TEXT NOT NULL,
#             marks INTEGER
#         )
#     """)
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT NOT NULL UNIQUE,
#             password TEXT NOT NULL,
#             role TEXT NOT NULL
#         )
#     """)
#     conn.commit()
#     conn.close()


# # Add user to the database
# def add_user(username, password, role):
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#     conn = sqlite3.connect("students.db")
#     cursor = conn.cursor()
#     try:
#         cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, role))
#         conn.commit()
#     except sqlite3.IntegrityError:
#         messagebox.showerror("Error", "Username already exists")
#     conn.close()


# # Authenticate user
# def authenticate_user(username, password):
#     conn = sqlite3.connect("students.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
#     result = cursor.fetchone()
#     conn.close()
#     if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
#         return result[1]  # Return role
#     return None


# # Fetch all students for the admin panel
# def fetch_all_students():
#     conn = sqlite3.connect("students.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, name, age, grade, marks FROM students")
#     rows = cursor.fetchall()
#     conn.close()
#     return rows


# # Add a student to the database
# def add_student(username, name, age, grade, marks):
#     conn = sqlite3.connect("students.db")
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO students (username, name, age, grade, marks) VALUES (?, ?, ?, ?, ?)",
#                    (username, name, age, grade, marks))
#     conn.commit()
#     conn.close()


# # Delete a student from the database
# def delete_student(student_id):
#     conn = sqlite3.connect("students.db")
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
#     conn.commit()
#     conn.close()


# # Fetch data for the logged-in student
# def fetch_student_data(username):
#     conn = sqlite3.connect("students.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT name, grade, marks FROM students WHERE username = ?", (username,))
#     data = cursor.fetchone()
#     conn.close()
#     return data


# # GUI for the login page
# def login_page():
#     def login():
#         role = authenticate_user(username_var.get(), password_var.get())
#         if role:
#             if role == "admin":
#                 root.destroy()
#                 admin_panel()
#             elif role == "student":
#                 root.destroy()
#                 student_panel(username_var.get())
#         else:
#             messagebox.showerror("Error", "Invalid username or password")

#     root = Tk()
#     root.title("Login")
#     root.geometry("400x300")

#     Label(root, text="Username:", font=("Arial", 12)).pack(pady=10)
#     username_var = StringVar()
#     Entry(root, textvariable=username_var, font=("Arial", 12)).pack(pady=10)

#     Label(root, text="Password:", font=("Arial", 12)).pack(pady=10)
#     password_var = StringVar()
#     Entry(root, textvariable=password_var, show="*", font=("Arial", 12)).pack(pady=10)

#     Button(root, text="Login", command=login, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=20)

#     root.mainloop()


# # GUI for the admin panel
# def admin_panel():
#     def refresh_table():
#         for row in tree.get_children():
#             tree.delete(row)
#         for row in fetch_all_students():
#             tree.insert("", END, values=row)

#     def add():
#         if not name_var.get() or not age_var.get() or not grade_var.get() or not marks_var.get():
#             messagebox.showerror("Error", "All fields are required")
#             return
#         try:
#             age = int(age_var.get())
#             marks = int(marks_var.get())
#             add_student(username_var.get(), name_var.get(), age, grade_var.get(), marks)
#             refresh_table()
#             name_var.set("")
#             age_var.set("")
#             grade_var.set("")
#             marks_var.set("")
#         except ValueError:
#             messagebox.showerror("Error", "Age and Marks must be integers")

#     def delete():
#         selected_item = tree.selection()
#         if not selected_item:
#             messagebox.showerror("Error", "No student selected")
#             return
#         student_id = tree.item(selected_item)["values"][0]
#         delete_student(student_id)
#         refresh_table()

#     root = Tk()
#     root.title("Admin Panel")
#     root.geometry("800x600")

#     username_var = StringVar()
#     name_var = StringVar()
#     age_var = StringVar()
#     grade_var = StringVar()
#     marks_var = StringVar()

#     Label(root, text="Username:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
#     Entry(root, textvariable=username_var, font=("Arial", 12)).grid(row=0, column=1, padx=10, pady=10)

#     Label(root, text="Name:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
#     Entry(root, textvariable=name_var, font=("Arial", 12)).grid(row=1, column=1, padx=10, pady=10)

#     Label(root, text="Age:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
#     Entry(root, textvariable=age_var, font=("Arial", 12)).grid(row=2, column=1, padx=10, pady=10)

#     Label(root, text="Grade:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10)
#     Entry(root, textvariable=grade_var, font=("Arial", 12)).grid(row=3, column=1, padx=10, pady=10)

#     Label(root, text="Marks:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=10)
#     Entry(root, textvariable=marks_var, font=("Arial", 12)).grid(row=4, column=1, padx=10, pady=10)

#     Button(root, text="Add", command=add, font=("Arial", 12), bg="#4CAF50", fg="white").grid(row=5, column=0, pady=10)
#     Button(root, text="Delete", command=delete, font=("Arial", 12), bg="#F44336", fg="white").grid(row=5, column=1, pady=10)

#     columns = ("ID", "Name", "Age", "Grade", "Marks")
#     tree = ttk.Treeview(root, columns=columns, show="headings")
#     for col in columns:
#         tree.heading(col, text=col)
#         tree.column(col, width=100)
#     tree.grid(row=6, column=0, columnspan=2, pady=20)

#     refresh_table()
#     root.mainloop()


# # GUI for the student panel
# def student_panel(username):
#     root = Tk()
#     root.title("Student Panel")
#     root.geometry("400x300")

#     data = fetch_student_data(username)
#     if data:
#         Label(root, text=f"Name: {data[0]}", font=("Arial", 12)).pack(pady=10)
#         Label(root, text=f"Grade: {data[1]}", font=("Arial", 12)).pack(pady=10)
#         Label(root, text=f"Marks: {data[2]}", font=("Arial", 12)).pack(pady=10)
#     else:
#         Label(root, text="No data found", font=("Arial", 12)).pack(pady=10)

#     root.mainloop()


# if __name__ == "__main__":
#     connect_database()
#     # Uncomment the line below to add an initial admin user for testing
#     # add_user("admin", "admin123", "admin")
#     login_page()
