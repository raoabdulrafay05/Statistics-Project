import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import seaborn as sns

# DataFrame to hold marks
data_frame = pd.DataFrame()

# verify email and password
def verify_credentials(user_email, user_password):
    return user_email == "u2023017@giki.edu.pk" and user_password == "1234"

# get user input
def process_login():
    entered_username = username_input.get()
    entered_password = password_input.get()

    if verify_credentials(entered_username, entered_password):
        messagebox.showinfo("Login Successful", "Welcome to the Grading System!")
        login_frame.pack_forget()  # Hide login frame
        main_menu_frame.pack(fill="both", expand=True)  # Show main menu frame
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# handle file dialog
def handle_file_action(action_type):
    global data_frame
    file_selection_frame.pack(fill="both", expand=True)

    if action_type == "open":
        load_existing_file()
    elif action_type == "create":
        create_new_file()

def load_existing_file():
    global data_frame
    file_selection_frame.pack_forget()
    loading_frame.pack(fill="both", expand=True)

    file_path = filedialog.askopenfilename(
        title="Open File",
        filetypes=(("CSV Files", "*.csv"), ("Excel Files", "*.xlsx"), ("All Files", "*.*")),
    )

    try:
        if file_path.endswith(".csv"):
            data_frame = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            data_frame = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please select a .csv or .xlsx file.")

        if data_frame.empty:
            raise ValueError("The selected file is empty.")

        loading_frame.pack_forget()
        messagebox.showinfo("File Loaded", "File loaded successfully!")
        grading_screen.pack(fill="both", expand=True)

    except Exception as error:
        loading_frame.pack_forget()
        messagebox.showerror("Error", f"Failed to open file: {error}")
        file_selection_frame.pack(fill="both", expand=True)

def create_new_file():
    global data_frame
    new_file_name = file_name_input.get()
    column_headers = columns_input.get().split(",")
    data_frame = pd.DataFrame(columns=column_headers)
    try:
        data_frame.to_csv(new_file_name + ".csv", index=False)
        messagebox.showinfo("File Created", f"New file '{new_file_name}.csv' created!")
        file_options_frame.pack_forget()
        grading_screen.pack(fill="both", expand=True)
    except Exception as error:
        messagebox.showerror("Error", f"Failed to create file: {error}")

# input fields
def add_student_details():
    global data_frame
    if data_frame.empty:
        messagebox.showerror("Error", "No dataset found. Please create or load a dataset.")
        return
    try:
        student_name = student_name_input.get()
        student_marks = float(student_marks_input.get())
        new_record = {"Name": student_name, "Marks": student_marks}
        data_frame = pd.concat([data_frame, pd.DataFrame([new_record])], ignore_index=True)
        
        # Ensure the columns are in the correct order
        data_frame = data_frame[["Name", "Marks"]]
        
        messagebox.showinfo("Success", "Student details added successfully!")
        student_name_input.delete(0, tk.END)
        student_marks_input.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Invalid marks. Please enter a numeric value.")




# absolute grading function 0-50(F), 50-60(D), 70-80(C), 80-90(B), 90-100(A)
def apply_absolute_grading():
    global data_frame
    if data_frame.empty:
        messagebox.showerror("Error", "The dataset is empty. Please load or create a dataset first.")
        return
    try:
        data_frame = data_frame .reset_index(drop=True)
        data_frame["Grade"] = pd.cut(
            data_frame["Marks"],
            bins=[0, 50, 60, 70, 80, 100],
            labels=["F", "D", "C", "B", "A"],
            right=False,
            include_lowest=True,
        )
        messagebox.showinfo("Grading Successful", "Absolute grading applied!")
    except KeyError:
        messagebox.showerror("Error", "Marks column not found in the dataset.")
    except Exception as error:
        messagebox.showerror("Error", f"An error occurred: {error}")

# relative grading function based on mean and standard deviation
def apply_relative_grading():
    global data_frame
    if data_frame.empty:
        messagebox.showerror("Error", "The dataset is empty. Please load or create a dataset first.")
        return

    try:
        # Ensure the 'Marks' column exists and is numeric
        if "Marks" not in data_frame.columns:
            raise KeyError("Marks column not found in the dataset.")
        if not pd.api.types.is_numeric_dtype(data_frame["Marks"]):
            raise ValueError("Marks column must contain numeric values.")

        # Calculate mean and standard deviation
        mean_marks = data_frame["Marks"].mean()
        std_dev_marks = data_frame["Marks"].std()

        # Handle edge case: standard deviation is zero
        if std_dev_marks == 0:
            raise ValueError("Standard deviation of Marks is zero. Grading cannot be applied.")

        # Define the grading boundaries
        bins = [
            -np.inf,  # Below x - 2sigma (D and Fail)
            mean_marks - 2 * std_dev_marks,
            mean_marks - (5/3) * std_dev_marks,
            mean_marks - (4/3) * std_dev_marks,
            mean_marks - std_dev_marks,
            mean_marks - std_dev_marks / 2,
            mean_marks + std_dev_marks / 2,
            mean_marks + std_dev_marks,
            mean_marks + (3/2) * std_dev_marks,
            mean_marks + 2 * std_dev_marks,
            np.inf  # Above x + 2sigma
        ]

        # Use unique labels
        labels = [
            "D",   # Below x - 2sigma
            "C-",  # Between x - 2sigma and x - (5/3)sigma
            "C",   # Between x - (5/3)sigma and x - (4/3)sigma
            "C+",  # Between x - (4/3)sigma and x - sigma
            "B-",  # Between x - sigma and x - sigma/2
            "B",   # Between x - sigma/2 and x + sigma/2
            "B+",  # Between x + sigma/2 and x + sigma
            "A-",  # Between x + sigma and x + (3/2)sigma
            "A",   # Between x + (3/2)sigma and x + 2sigma
            "A+"   # Above x + 2sigma
        ]

        # Apply grading
        data_frame["Grade"] = pd.cut(data_frame["Marks"], bins=bins, labels=labels, right=False)

        messagebox.showinfo("Grading Successful", "Relative grading applied!")
    except KeyError as e:
        messagebox.showerror("Error", str(e))
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as error:
        messagebox.showerror("Error", f"An unexpected error occurred: {error}")

# Saving grades into other file or existing one
def save_grades_to_file():
    global data_frame
    if data_frame.empty:
        messagebox.showerror("Error", "The dataset is empty. Please load or create a dataset first.")
        return
    save_file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")),
    )
    try:
        data_frame.to_csv(save_file_path, index=False)
        messagebox.showinfo("Success", f"Data saved to '{save_file_path}' successfully!")
    except Exception as error:
        messagebox.showerror("Error", f"Failed to save file: {error}")

# Function to display histogram
def display_marks_histogram():
    global data_frame
    if data_frame.empty:
        messagebox.showerror("Error", "The dataset is empty. Please load or create a dataset first.")
        return
    try:
        plt.figure(figsize=(8, 5))
        plt.hist(data_frame["Marks"], bins=10, edgecolor="black", color="lightgreen")
        plt.title("Marks Distribution", fontsize=16)
        plt.xlabel("Marks", fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.show()
    except KeyError:
        messagebox.showerror("Error", "Marks column not found in the dataset.")
    except Exception as error:
        messagebox.showerror("Error", f"An error occurred: {error}")

# Plot normal distribution curve
def display_normal_distribution_curve():
    global data_frame
    if data_frame.empty:
        messagebox.showerror("Error", "The dataset is empty. Please load or create a dataset first.")
        return
    try:
        mean_marks = data_frame["Marks"].mean()
        std_dev_marks = data_frame["Marks"].std()
        marks_min, marks_max = data_frame["Marks"].min(), data_frame["Marks"].max()
        x_values = np.linspace(marks_min, marks_max, 100)
        probability_density = norm.pdf(x_values, mean_marks, std_dev_marks)
        plt.figure(figsize=(8, 5))
        plt.plot(x_values, probability_density, "r", linewidth=2)
        plt.title("Normal Distribution Curve for Marks", fontsize=16)
        plt.xlabel("Marks", fontsize=12)
        plt.ylabel("Probability Density", fontsize=12)
        plt.grid(axis="both", linestyle="--", alpha=0.7)
        plt.show()
    except KeyError:
        messagebox.showerror("Error", "Marks column not found in the dataset.")

# Switch between frames
def switch_to_frame(target_frame):
    for widget in root_window.winfo_children():
        widget.pack_forget()
    target_frame.pack(fill="both", expand=True)

# Plot pie chart for grade distribution
def display_grade_pie_chart():
    global data_frame
    if data_frame.empty:
        messagebox.showerror("Error", "The dataset is empty. Please load or create a dataset first.")
        return
    try:
        # Get grade counts and filter out any grades with zero counts
        grade_counts = data_frame["Grade"].value_counts()
        grade_counts = grade_counts[grade_counts > 0]  # Remove grades with zero count
        
        if grade_counts.empty:
            messagebox.showinfo("Info", "No grades available for display.")
            return
        
        plt.figure(figsize=(6, 6))
        grade_counts.plot(
            kind="pie",
            autopct="%1.1f%%",
            startangle=90,
            colors=sns.color_palette("pastel"),
        )
        plt.title("Grade Distribution", fontsize=16)
        plt.ylabel("")  # Hide the y-label
        plt.show()
    except KeyError:
        messagebox.showerror("Error", "Grades column not found in the dataset.")
    except Exception as error:
        messagebox.showerror("Error", f"An error occurred: {error}")


# Plot bar chart for grade distribution
def display_grade_bar_chart():
    global data_frame
    if data_frame.empty:
        messagebox.showerror("Error", "The dataset is empty. Please load or create a dataset first.")
        return
    try:
        grade_counts = data_frame["Grade"].value_counts().sort_index()
        plt.figure(figsize=(8, 5))
        grade_counts.plot(kind="bar", color="lightblue", edgecolor="black")
        plt.title("Grade Distribution", fontsize=16)
        plt.xlabel("Grades", fontsize=12)
        plt.ylabel("Number of Students", fontsize=12)
        plt.xticks(rotation=0)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.show()
    except KeyError:
        messagebox.showerror("Error", "Grades column not found in the dataset.")
    except Exception as error:
        messagebox.showerror("Error", f"An error occurred: {error}")

# GUI Screen for entering
root_window = tk.Tk()
root_window.title("Grading System")
root_window.geometry("600x600")
root_window.configure(bg="light green")

# Login Frame
login_frame = tk.Frame(root_window, bg="light green")
login_frame.pack(pady=20)

tk.Label(login_frame, text="email:", bg="black", fg="white").pack(pady=5)
username_input = tk.Entry(login_frame)
username_input.pack(pady=5)

tk.Label(login_frame, text="Password:", bg="black", fg="white").pack(pady=5)
password_input = tk.Entry(login_frame, show="*")
password_input.pack(pady=5)

tk.Button(login_frame, text="Login", command=process_login, bg="#4CAF50", fg="red").pack(pady=20)

# Main Menu Frame
main_menu_frame = tk.Frame(root_window, bg="light blue")

tk.Label(main_menu_frame, text="Main Menu", font=("Helvetica", 20), bg="black", fg="white").pack(pady=20)
tk.Button(main_menu_frame, text="Open Existing File", command=lambda: switch_to_frame(file_selection_frame), bg="#2196F3", fg="white").pack(pady=10)
tk.Button(main_menu_frame, text="Create New File", command=lambda: switch_to_frame(file_options_frame), bg="#FF9800", fg="white").pack(pady=10)
tk.Button(main_menu_frame, text="Exit", command=root_window.quit, bg="#F44336", fg="white").pack(pady=10)
tk.Button(main_menu_frame, text="Go to Visualization", command=lambda: switch_to_frame(visualization_frame), bg="#4CAF50", fg="white").pack(pady=10)

# Select File Frame
file_selection_frame = tk.Frame(root_window, bg="light yellow")

tk.Label(file_selection_frame, text="Select a File to Open", font=("Helvetica", 20), bg="black", fg="white").pack(pady=20)

tk.Button(file_selection_frame, text="Choose File", command=load_existing_file, bg="#2196F3", fg="white").pack(pady=10)
tk.Button(file_selection_frame, text="Back to Main Menu", command=lambda: switch_to_frame(main_menu_frame), bg="#FF9800", fg="white").pack(pady=10)

# File Options Frame
file_options_frame = tk.Frame(root_window, bg="gray")

tk.Label(file_options_frame, text="Create New File", font=("Helvetica", 20), bg="black", fg="white").pack(pady=20)

tk.Label(file_options_frame, text="File Name:", bg="black", fg="white").pack(pady=5)
file_name_input = tk.Entry(file_options_frame)
file_name_input.pack(pady=5)

tk.Label(file_options_frame, text="Enter Columns (comma-separated):", bg="black", fg="white").pack(pady=5)
columns_input = tk.Entry(file_options_frame)
columns_input.pack(pady=5)

tk.Button(file_options_frame, text="Create File", command=create_new_file, bg="#4CAF50", fg="white").pack(pady=10)
tk.Button(file_options_frame, text="Back to Main Menu", command=lambda: switch_to_frame(main_menu_frame), bg="#FF9800", fg="white").pack(pady=10)

# Loading Frame ```python
loading_frame = tk.Frame(root_window, bg="black")

tk.Label(loading_frame, text="Loading File...", font=("Helvetica", 20), bg="black", fg="white").pack(pady=20)
tk.Label(loading_frame, text="Please wait while the file is being loaded.", font=("Helvetica", 12), bg="black", fg="white").pack(pady=5)

# Grading Screen
grading_screen = tk.Frame(root_window, bg="brown")

tk.Label(grading_screen, text="Enter Student Details", font=("Helvetica", 20), bg="black", fg="white").pack(pady=20)

tk.Label(grading_screen, text="Name:", bg="black", fg="white").pack(pady=5)
student_name_input = tk.Entry(grading_screen)
student_name_input.pack(pady=5)

tk.Label(grading_screen, text="Marks:", bg="black", fg="white").pack(pady=5)
student_marks_input = tk.Entry(grading_screen)  # Fixed the typo here
student_marks_input.pack(pady=5)

tk.Button(grading_screen, text="Add Student", command=add_student_details, bg="#4CAF50", fg="white").pack(pady=10)
tk.Button(grading_screen, text="Apply Absolute Grading", command=apply_absolute_grading, bg="#2196F3", fg="white").pack(pady=10)
tk.Button(grading_screen, text="Apply Relative Grading", command=apply_relative_grading, bg="#FF9800", fg="white").pack(pady=10)
tk.Button(grading_screen, text="Save Grades", command=save_grades_to_file, bg="#F44336", fg="white").pack(pady=10)
tk.Button(grading_screen, text="Go to Visualization", command=lambda: switch_to_frame(visualization_frame), bg="#4CAF50", fg="white").pack(pady=10)

# Visualization Frame
visualization_frame = tk.Frame(root_window, bg="red")

tk.Label(visualization_frame, text="Data Visualization", font=("Helvetica", 20), bg="black", fg="white").pack(pady=20)
tk.Button(visualization_frame, text="Show Histogram", command=display_marks_histogram, bg="#2196F3", fg="white").pack(pady=10)
tk.Button(visualization_frame, text="Show Normal Distribution Curve", command=display_normal_distribution_curve, bg="#FF9800", fg="white").pack(pady=10)
tk.Button(visualization_frame, text="Show Pie Chart", command=display_grade_pie_chart, bg="#4CAF50", fg="white").pack(pady=10)
tk.Button(visualization_frame, text="Show Bar Chart", command=display_grade_bar_chart, bg="#F44336", fg="white").pack(pady=10)
tk.Button(visualization_frame, text="Back to Grading", command=lambda: switch_to_frame(grading_screen), bg="#FF9800", fg="white").pack(pady=10)

# Start the GUI
root_window.mainloop()
