import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database import setup_database, connect_db

# Tạo database
setup_database()

# Hàm xử lý
def login(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def search_students(keyword):
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM students WHERE name LIKE ?"
    cursor.execute(query, ('%' + keyword + '%',))
    results = cursor.fetchall()
    conn.close()
    return results

def add_student(name, age, email):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO students (name, age, email) VALUES (?, ?, ?)"
        cursor.execute(query, (name, age, email))
        conn.commit()
        conn.close()
        return "Thêm sinh viên thành công!"
    except Exception as e:
        return str(e)

# Giao diện GUI
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý sinh viên")

        # Tạo giao diện đăng nhập
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Username").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Password").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2)

        # Tạo giao diện chính
        self.main_frame = tk.Frame(self.root)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if login(username, password):
            messagebox.showinfo("Success", "Đăng nhập thành công!")
            self.login_frame.pack_forget()
            self.main_menu()
        else:
            messagebox.showerror("Error", "Sai tài khoản hoặc mật khẩu!")

    def main_menu(self):
        self.main_frame.pack(pady=20)

        tk.Button(self.main_frame, text="Tìm kiếm sinh viên", command=self.search_students).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self.main_frame, text="Thêm sinh viên mới", command=self.add_student).grid(row=0, column=1, padx=10, pady=10)

    def search_students(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Tìm kiếm sinh viên")

        tk.Label(search_window, text="Từ khóa").grid(row=0, column=0)
        keyword_entry = tk.Entry(search_window)
        keyword_entry.grid(row=0, column=1)

        result_tree = ttk.Treeview(search_window, columns=("ID", "Name", "Age", "Email"), show="headings")
        result_tree.grid(row=1, column=0, columnspan=2)

        result_tree.heading("ID", text="ID")
        result_tree.heading("Name", text="Name")
        result_tree.heading("Age", text="Age")
        result_tree.heading("Email", text="Email")

        def search_action():
            keyword = keyword_entry.get()
            results = search_students(keyword)
            for row in result_tree.get_children():
                result_tree.delete(row)
            for student in results:
                result_tree.insert("", "end", values=student)

        tk.Button(search_window, text="Tìm kiếm", command=search_action).grid(row=0, column=2, padx=10)

    def add_student(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Thêm sinh viên")

        tk.Label(add_window, text="Tên").grid(row=0, column=0)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1)

        tk.Label(add_window, text="Tuổi").grid(row=1, column=0)
        age_entry = tk.Entry(add_window)
        age_entry.grid(row=1, column=1)

        tk.Label(add_window, text="Email").grid(row=2, column=0)
        email_entry = tk.Entry(add_window)
        email_entry.grid(row=2, column=1)

        def add_action():
            name = name_entry.get()
            age = age_entry.get()
            email = email_entry.get()
            message = add_student(name, int(age), email)
            messagebox.showinfo("Result", message)

        tk.Button(add_window, text="Thêm", command=add_action).grid(row=3, column=0, columnspan=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
