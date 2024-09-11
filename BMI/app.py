from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Data storage setup
data_file = 'bmi_data.csv'

color_map = {
    "Underweight": "yellow",
    "Healthy weight": "green",
    "Overweight": "red"
}

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
    return round(weight / (height ** 2), 2)

def get_health_status_and_percentage(bmi):
    if bmi < 18.5:
        return "Underweight", round((bmi / 18.5) * 100, 1)
    elif 18.5 <= bmi < 24.9:
        return "Healthy weight", 100
    else:
        return "Overweight", round((24.9 / bmi) * 100, 1)

def create_bmi_distribution_chart():
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
        
        # Save the plot to a BytesIO object and encode it to base64
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close()
        
        return img_base64
    except FileNotFoundError:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            age = int(request.form['age'])
            gender = request.form['gender']
            weight = float(request.form['weight'])
            height = float(request.form['height']) / 100  # Convert cm to meters

            bmi = calculate_bmi(weight, height)
            health_status, health_percentage = get_health_status_and_percentage(bmi)

            # Save the data
            save_data(age, gender, weight, height, bmi, health_status, health_percentage)

            return render_template('index.html', bmi=bmi, age=age, gender=gender,
                                   health_status=health_status, health_percentage=health_percentage,
                                   color_map=color_map)
        except ValueError:
            return render_template('index.html', error="Please enter valid data.", color_map=color_map)
    
    return render_template('index.html', color_map=color_map)

@app.route('/statistics')
def statistics():
    chart = create_bmi_distribution_chart()
    if chart:
        return render_template('statistics.html', chart=chart)
    else:
        return "No data available."

if __name__ == '__main__':
    app.run(debug=True, port=2496)
