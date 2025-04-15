import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Constants
BLOOD_GROUPS = ("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-")

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="aaron912007",
    database="blood_bank"
)
cursor = conn.cursor()

# Main window
root = tk.Tk()
root.title("Blood Bank Donor Management")
root.geometry("550x750")
root.resizable(False, False)

# Banner Title
tk.Label(root, text="Blood Bank Donor Management", font=("Arial", 16, "bold")).pack(pady=10)

# Input Fields Frame
form_frame = tk.Frame(root, bg="white", padx=10, pady=10)
form_frame.pack(pady=10)

# Input fields
def add_labeled_entry(label, widget):
    tk.Label(form_frame, text=label, bg="white").pack(anchor='w')
    widget.pack(fill='x', pady=5)

name_entry = tk.Entry(form_frame)
add_labeled_entry("Donor Name", name_entry)

age_entry = tk.Entry(form_frame)
add_labeled_entry("Age", age_entry)

gender_entry = ttk.Combobox(form_frame, values=["Male", "Female", "Other"])
add_labeled_entry("Gender", gender_entry)

blood_group_entry = ttk.Combobox(form_frame, values=BLOOD_GROUPS)
add_labeled_entry("Blood Group", blood_group_entry)

hospital_name_entry = tk.Entry(form_frame)
add_labeled_entry("Hospital Name", hospital_name_entry)

hospital_address_entry = tk.Entry(form_frame)
add_labeled_entry("Hospital Address", hospital_address_entry)

contact_entry = tk.Entry(form_frame)
add_labeled_entry("Contact Number", contact_entry)

units_entry = tk.Entry(form_frame)
add_labeled_entry("Units of Blood Needed", units_entry)

# Functions
def add_donor():
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_entry.get()
    blood_group = blood_group_entry.get().upper()
    hospital_name = hospital_name_entry.get()
    hospital_address = hospital_address_entry.get()
    contact_no = contact_entry.get()
    units = units_entry.get()

    if blood_group not in BLOOD_GROUPS:
        messagebox.showerror("Error", "Invalid blood group.")
        return
    if not age.isdigit() or int(age) <= 0:
        messagebox.showerror("Error", "Please enter a valid age.")
        return
    if not contact_no.isdigit() or len(contact_no) < 10:
        messagebox.showerror("Error", "Please enter a valid contact number.")
        return
    if not units.isdigit() or int(units) <= 0:
        messagebox.showerror("Error", "Please enter a valid number of blood units.")
        return

    try:
        cursor.execute("""
            INSERT INTO donar (name, age, gender, blood_group, hospital_name, hospital_address, contact_no, units_needed)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, age, gender, blood_group, hospital_name, hospital_address, contact_no, units))
        conn.commit()
        messagebox.showinfo("Success", "Donor added successfully!")
        clear_entries()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def clear_entries():
    for entry in [name_entry, age_entry, hospital_name_entry, hospital_address_entry, contact_entry, units_entry]:
        entry.delete(0, tk.END)
    gender_entry.set("")
    blood_group_entry.set("")

def view_donors():
    cursor.execute("SELECT * FROM donar")
    data = cursor.fetchall()

    view_window = tk.Toplevel(root)
    view_window.title("All Donors")

    for d in data:
        tk.Label(view_window, text=f"ID: {d[0]}, Name: {d[1]}, Age: {d[2]}, Gender: {d[3]}, "
                                   f"Blood: {d[4]}, Hospital: {d[5]}, Address: {d[6]}, "
                                   f"Contact: {d[7]}, Units Needed: {d[8]}").pack()

def search_by_blood():
    bg = blood_group_entry.get().upper()

    if bg not in BLOOD_GROUPS:
        messagebox.showerror("Error", "Invalid blood group.")
        return

    cursor.execute("SELECT * FROM donar WHERE blood_group=%s", (bg,))
    data = cursor.fetchall()

    search_window = tk.Toplevel(root)
    search_window.title(f"Donors with Blood Group {bg}")

    if not data:
        tk.Label(search_window, text="No donors found.").pack()
    else:
        for d in data:
            tk.Label(search_window, text=f"ID: {d[0]}, Name: {d[1]}, Age: {d[2]}, Gender: {d[3]}, "
                                         f"Blood: {d[4]}, Hospital: {d[5]}, Address: {d[6]}, "
                                         f"Contact: {d[7]}, Units Needed: {d[8]}").pack()

# Buttons
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=15)

tk.Button(button_frame, text="Add Donor", command=add_donor, bg="green", fg="white", width=20).pack(pady=5)
tk.Button(button_frame, text="View All Donors", command=view_donors, width=20).pack(pady=5)
tk.Button(button_frame, text="Search by Blood Group", command=search_by_blood, width=20).pack(pady=5)

# Safe exit
def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()