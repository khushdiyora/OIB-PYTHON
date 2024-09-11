import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt

# Data storage setup
data_file = 'bmi_data.csv'

def save_data(age, gender, weight, height, bmi, health_status, health_percentage):
    try:
        data = pd.read_csv(data_file)
    except FileNotFoundError:
        data = pd.DataFrame(columns=['Age', 'Gender', 'Weight', 'Height', 'BMI', 'Health Status', 'Health Percentage'])
    
    new_entry = pd.DataFrame([{
        'Age': age,
        'Gender': gender,
        'Weight': weight,
        'Height': height,
        'BMI': bmi,
        'Health Status': health_status,
        'Health Percentage': health_percentage
    }])
    
    data = pd.concat([data, new_entry], ignore_index=True)
    data.to_csv(data_file, index=False)

def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return round(bmi, 2)

def get_health_status_and_percentage(bmi):
    if bmi < 18.5:
        return "Underweight", round((bmi / 18.5) * 100, 1)
    elif 18.5 <= bmi < 24.9:
        return "Healthy weight", 100
    else:
        return "Overweight", round((24.9 / bmi) * 100, 1)

def show_statistics():
    try:
        data = pd.read_csv(data_file)
        plt.figure(figsize=(10, 6))
        for status in data['Health Status'].unique():
            subset = data[data['Health Status'] == status]
            plt.hist(subset['BMI'], bins=10, alpha=0.5, label=status)
        plt.xlabel('BMI')
        plt.ylabel('Frequency')
        plt.title('BMI Distribution by Health Status')
        plt.legend()
        plt.show()
    except FileNotFoundError:
        messagebox.showerror("Error", "No data file found.")

def submit_form():
    try:
        age = int(age_entry.get())
        gender = gender_var.get()
        weight = float(weight_entry.get())
        height = float(height_entry.get()) / 100  # Convert cm to meters
        
        bmi = calculate_bmi(weight, height)
        health_status, health_percentage = get_health_status_and_percentage(bmi)
        
        # Save the data
        save_data(age, gender, weight, height, bmi, health_status, health_percentage)
        
        # Show result
        result_label.config(text=f'BMI: {bmi}\nHealth Status: {health_status}\nHealth Percentage: {health_percentage}%', fg=color_map[health_status])
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid data.")

# Tkinter GUI setup
root = tk.Tk()
root.title("BMI Calculator")

tk.Label(root, text="Age:").grid(row=0, column=0, padx=10, pady=10)
age_entry = tk.Entry(root)
age_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Gender:").grid(row=1, column=0, padx=10, pady=10)
gender_var = tk.StringVar(value="male")
tk.Radiobutton(root, text="Male", variable=gender_var, value="male").grid(row=1, column=1, padx=10, pady=10)
tk.Radiobutton(root, text="Female", variable=gender_var, value="female").grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="Height (cm):").grid(row=2, column=0, padx=10, pady=10)
height_entry = tk.Entry(root)
height_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Weight (kg):").grid(row=3, column=0, padx=10, pady=10)
weight_entry = tk.Entry(root)
weight_entry.grid(row=3, column=1, padx=10, pady=10)

tk.Button(root, text="Calculate", command=submit_form).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

result_label = tk.Label(root, text="", font=("Helvetica", 14))
result_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

tk.Button(root, text="Show Statistics", command=show_statistics).grid(row=6, column=0, columnspan=3, padx=10, pady=10)

color_map = {
    "Underweight": "yellow",
    "Healthy weight": "green",
    "Overweight": "red"
}

root.mainloop()
