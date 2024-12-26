# Statistics-Project
This Python script is a student grading and visualization system implemented using the Tkinter library for GUI and libraries like Pandas, NumPy, Matplotlib, Seaborn, and SciPy for data handling and visualization.
Key Functionalities:
1. Login System:
The program starts with a login interface where users must enter an email and password.
Hardcoded credentials:
Email: u2023017@giki.edu.pk
Password: 1234
If verified, it transitions to the main menu.
2. File Handling:
Users can either load an existing dataset (CSV or Excel file) or create a new dataset.
For new files:
Users input a file name and column names.
A new CSV file is created with the specified column headers.
3. Adding Student Details:
Allows users to enter a student's name and marks.
These details are appended to the loaded or newly created dataset.
4. Grading System:
Absolute Grading: Grades students based on predefined boundaries:
F: 0-50, D: 50-60, C: 60-70, B: 70-80, A: 80-100.
Relative Grading: Grades students based on statistical analysis:
Uses mean and standard deviation to create grading bins (D to A+).
5. Data Visualization:
The system provides various visualization options:

Histogram: Displays the distribution of marks.
Normal Distribution Curve: Fits a Gaussian curve to the marks.
Pie Chart: Shows the grade distribution as a percentage.
Bar Chart: Displays the count of students for each grade.
6. Saving Grades:
Allows users to save the updated dataset (with grades) to a new file or overwrite an existing one.
7. GUI Navigation:
Uses multiple frames to switch between login, file management, grading, and visualization screens.
The layout ensures a smooth transition between different functionalities.
Libraries Used:
Tkinter: For creating the graphical user interface.
Pandas: For data manipulation and storage.
NumPy: For numerical calculations (e.g., mean, standard deviation).
Matplotlib & Seaborn: For generating visualizations like histograms, pie charts, and bar charts.
SciPy: For generating normal distribution curves.
Code Structure:
Login and Verification:
Validates user credentials.
File Operations:
Handles loading and creation of datasets.
Grading:
Two types of grading methods (absolute and relative).
Visualization:
Provides multiple ways to visualize marks and grades.
GUI Setup:
Contains frames for login, file management, grading, and visualization, with smooth navigation.
User Interaction Flow:
Login with the email and password.
Choose to load or create a dataset.
Add student details and apply grading (absolute or relative).
Save grades or visualize the data.
Exit or switch between functionalities as needed.
Advantages:
User-friendly GUI: Simplifies data management for users unfamiliar with programming.
Flexible Grading: Provides both absolute and relative grading options.
Visual Insights: Includes various data visualization tools for better analysis.
Scalability: Can handle datasets of various sizes.
This script is well-suited for educators or administrators to manage student performance data effectively.
