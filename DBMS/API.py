import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Function to fetch data from SQLite database
def get_data():
    conn = sqlite3.connect('db.db')  # Ensure the correct database file is used
    cursor = conn.cursor()
    
    # Fetch all data from the 'students' table (excluding the Grade column)
    cursor.execute("SELECT id, name, age FROM students")
    data = cursor.fetchall()
    
    conn.close()
    return data

# Function to populate the Treeview table with data
def populate_table():
    # Clear existing data in the table
    for row in tree.get_children():
        tree.delete(row)
    
    # Fetch data from the database
    data = get_data()

    # Insert fetched data into the Treeview
    for row in data:
        tree.insert("", "end", values=row)

# Function to insert new data into the SQLite database
def add_data():
    id = id_entry.get()
    name = name_entry.get()
    age = age_entry.get()

    # Ensure all fields are filled
    if id and name and age:
        try:
            # Insert new data into the 'students' table (without Grade)
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (id, name, age) VALUES (?, ?, ?)", (id, name, age))
            conn.commit()
            conn.close()

            # Clear input fields
            id_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            age_entry.delete(0, tk.END)

            # Repopulate table to show the new data
            populate_table()

            # Show success message
            messagebox.showinfo("Success", "Data inserted successfully")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Function to delete selected data from the database
def delete_data():
    selected_item = tree.selection()
    if selected_item:
        selected_id = tree.item(selected_item, "values")[0]
        
        try:
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id=?", (selected_id,))
            conn.commit()
            conn.close()
            
            # Refresh the table after deletion
            populate_table()
            
            messagebox.showinfo("Success", "Data deleted successfully")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error deleting data: {e}")
    else:
        messagebox.showwarning("Selection Error", "Please select a row to delete")

# Function to update the selected data
def update_data():
    selected_item = tree.selection()
    if selected_item:
        selected_id = tree.item(selected_item, "values")[0]
        new_name = name_entry.get()
        new_age = age_entry.get()
        
        if new_name and new_age:
            try:
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE students SET name=?, age=? WHERE id=?", (new_name, new_age, selected_id))
                conn.commit()
                conn.close()

                # Refresh the table after update
                populate_table()

                messagebox.showinfo("Success", "Data updated successfully")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error updating data: {e}")
        else:
            messagebox.showwarning("Input Error", "Please fill both Name and Age fields for update")
    else:
        messagebox.showwarning("Selection Error", "Please select a row to update")

# Function to fill the input fields with selected row data
def select_row(event):
    selected_item = tree.selection()
    if selected_item:
        selected_data = tree.item(selected_item, "values")
        id_entry.delete(0, tk.END)
        id_entry.insert(0, selected_data[0])
        name_entry.delete(0, tk.END)
        name_entry.insert(0, selected_data[1])
        age_entry.delete(0, tk.END)
        age_entry.insert(0, selected_data[2])

# Create the main window
root = tk.Tk()
root.title("Database Table Data")

# Define the columns for the Treeview table (ID, Name, Age) - removed 'Grade'
columns = ("ID", "Name", "Age")

# Create the Treeview widget
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

# Define the column headings
for col in columns:
    tree.heading(col, text=col)

# Set the width of the columns
tree.column("ID", width=50, anchor=tk.CENTER)
tree.column("Name", width=150, anchor=tk.W)
tree.column("Age", width=100, anchor=tk.CENTER)

# Pack the Treeview widget into the window
tree.pack(pady=20)

# Create input fields for adding new data (excluding 'Grade')
form_frame = tk.Frame(root)
form_frame.pack(pady=10)

tk.Label(form_frame, text="ID").grid(row=0, column=0)
tk.Label(form_frame, text="Name").grid(row=0, column=1)
tk.Label(form_frame, text="Age").grid(row=0, column=2)

id_entry = tk.Entry(form_frame, width=5)
id_entry.grid(row=1, column=0, padx=5)

name_entry = tk.Entry(form_frame, width=20)
name_entry.grid(row=1, column=1, padx=5)

age_entry = tk.Entry(form_frame, width=10)
age_entry.grid(row=1, column=2, padx=5)

# Add buttons to insert, update, and delete data
add_button = tk.Button(root, text="Add Data", command=add_data)
add_button.pack(pady=5)

update_button = tk.Button(root, text="Update Data", command=update_data)
update_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Data", command=delete_data)
delete_button.pack(pady=5)

# Add a button to refresh/reload the data from the database
refresh_button = tk.Button(root, text="Refresh Data", command=populate_table)
refresh_button.pack(pady=5)

# Bind the Treeview select event to fill the input fields
tree.bind("<<TreeviewSelect>>", select_row)

# Initial population of the table
populate_table()

# Start the Tkinter main loop
root.geometry("450x400")  # Set window size
root.mainloop()
