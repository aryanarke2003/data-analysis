import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, jsonify
import matplotlib.pyplot as plt
import io
from werkzeug.utils import secure_filename
import os
import base64

app = Flask(__name__, template_folder='templates')
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@34.72>
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Household(db.Model):
    __tablename__ = 'households'
    HSHD_NUM = db.Column(db.Integer, primary_key=True)
    L = db.Column(db.String(100))
    AGE_RANGE = db.Column(db.String(200))
    MARITAL = db.Column(db.String(200))
    INCOME_RANGE = db.Column(db.String(200))

if __name__ == '__main__':
    app.run(debug=True)

# Dictionary to store user information (simulating a database)
users = {}

# Read data from CSV file
households_data = pd.read_csv("home/arya_narke20/flaskapp/400_households.csv")
transactions_data = pd.read_csv("home/arya_narke20/flaskapp/400_transactions.csv")
products_data = pd.read_csv("home/arya_narke20/flaskapp/400_products.csv")

# Strip leading and trailing spaces from column names
households_data.columns = households_data.columns.str.strip()
transactions_data.columns = transactions_data.columns.str.strip()
products_data.columns = products_data.columns.str.strip()

# Convert 'HSHD_NUM' column to integer
households_data['HSHD_NUM'] = households_data['HSHD_NUM'].astype(int)

# Rename the 'PURCHASE_' column to 'PURCHASE_DATE' in transactions_data
transactions_data.rename(columns={'PURCHASE_': 'PURCHASE_DATE'}, inplace=True)

# Join transactions_data with products_data using 'PRODUCT_NUM'
joined_df = pd.merge(transactions_data, products_data, on='PRODUCT_NUM', how='inner')

# Join the result with households_data using 'HSHD_NUM'
final_df = pd.merge(joined_df, households_data, on='HSHD_NUM', how='inner')

# Remove leading and trailing whitespace, replace "null" with 0
final_df['HH_SIZE'] = final_df['HH_SIZE'].str.strip().replace("null", 0)

# Replace values ending with "+" with the corresponding integer
final_df['HH_SIZE'] = final_df['HH_SIZE'].str.strip().replace("5+", "5")

# Replace NaN values with 0
final_df['HH_SIZE'] = final_df['HH_SIZE'].fillna(0)

# Convert the entire column to integers
final_df['HH_SIZE'] = final_df['HH_SIZE'].astype(int)

final_df['SPEND'] = final_df['SPEND'].astype(float)
final_df = final_df.sort_values(by=['HSHD_NUM', 'BASKET_NUM', 'PURCHASE_DATE', 'PRODUCT_NUM', 'DEPARTMENT', 'COMMODITY'])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error_message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        # Check if username is already taken
        if username in users:
            error_message = "Username already exists. Choose a different one."
        else:
            # Store user information in the dictionary
            users[username] = {
                'password': password,
                'firstname': firstname,
                'lastname': lastname,
                'email': email
            }

            # Redirect to login page
            return redirect(url_for('login'))
    return render_template('register.html', error_message=error_message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username and password match
        user_info = users.get(username, None)
        if user_info and user_info['password'] == password:
            # Redirect to success page upon successful login
            return redirect(url_for('success', username=username))
        else:
            error_message = "Username or password incorrect."

    return render_template('login.html', error_message=error_message)

# Function to generate line graph and return it as base64 encoded image
def generate_plot():
    # Grouping by household size and collecting all spend values
   # grouped_df = final_df.groupby('HH_SIZE')['SPEND'].apply(list).reset_index()

    # Filter out HH_SIZE of 0
   # grouped_df = grouped_df[grouped_df['HH_SIZE'] != 0]

    # Line graph
   # plt.figure(figsize=(10, 6))
   # for index, row in grouped_df.iterrows():
    #    plt.plot([row['HH_SIZE']] * len(row['SPEND']), row['SPEND'], marker='o', linestyle='', label=f'HH_SIZE {row["HH_SIZE"]}')
   # plt.title('Household Size vs. Spend')
   # plt.xlabel('Household Size')
   # plt.ylabel('Spend')
   # plt.grid(True)
    #plt.legend()
    basket_agg = final_df.groupby(['HSHD_NUM', 'BASKET_NUM']).agg({'HH_SIZE': 'first', 'SPEND': 'sum'}).reset_index()

# Further aggregate by household number and sum the spend of each basket
    household_agg = basket_agg.groupby('HSHD_NUM').agg({'HH_SIZE': 'first', 'SPEND': 'sum'}).reset_index()


# Filter out rows where household size is 0 and basket number is not 0
    household_agg = household_agg[household_agg['HH_SIZE'] > 0]
# Plot the aggregated spend for each household
    plt.figure(figsize=(10, 6))
    plt.scatter(household_agg['HH_SIZE'], household_agg['SPEND'], alpha=0.5)
    plt.title('Household Size vs Total Spend (Aggregated by Basket)')
    plt.xlabel('Household Size')
    plt.ylabel('Total Spend')
    plt.grid(True)
    # Save plot to memory buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode plot image to base64
    plot_data = base64.b64encode(buffer.getvalue()).decode()

    return plot_data

# Function to calculate correlation coefficient
def calculate_correlation():
    # Filter out rows with null values in HH_SIZE or SPEND columns
#    filtered_df = final_df.dropna(subset=['HH_SIZE', 'SPEND'])
    
    # Exclude data for HH_SIZE of 0
 #   filtered_df = filtered_df[filtered_df['HH_SIZE'] != 0]
    
    # Calculate correlation coefficient
    #correlation = filtered_df['HH_SIZE'].corr(filtered_df['SPEND'])
    basket_agg = final_df.groupby(['HSHD_NUM', 'BASKET_NUM']).agg({'HH_SIZE': 'first', 'SPEND': 'sum'}).reset_index()

# Further aggregate by household number and sum the spend of each basket
    household_agg = basket_agg.groupby('HSHD_NUM').agg({'HH_SIZE': 'first', 'SPEND': 'sum'}).reset_index()

# Filter out rows where household size is 0 and basket number is not 0
    household_agg = household_agg[household_agg['HH_SIZE'] > 0]
    correlation_coefficient = household_agg['HH_SIZE'].corr(household_agg['SPEND'])

   # print("Correlation coefficient:", correlation_coefficient)

  
    return correlation_coefficient

@app.route('/success/<username>', methods=['GET', 'POST'])
def success(username):
    user_info = users.get(username, None)
    plot_data = generate_plot()
    # Filter final_df for HSHD_NUM 10
    hshd_10_df = final_df[final_df['HSHD_NUM'] == 10]
    correlation = calculate_correlation()
    hshd_num = request.form.get('hshd_num', default=1)  # Set default value to 1 if hshd_num is not provided
    filtered_df = final_df[final_df['HSHD_NUM'] == hshd_num]

    # Check if the POST request has the file part
    # if 'transactions_file' not in request.files:
    #     return 'No transactions file provided', 400
    # if 'households_file' not in request.files:
    #     return 'No households file provided', 400
    # if 'products_file' not in request.files:
    #     return 'No products file provided', 400
    
    # Get the files from the request
    # transactions_file = request.files['transactions_file']
    # households_file = request.files['households_file']
    # products_file = request.files['products_file']

   # Check if the file is selected
    # if transactions_file.filename == '':
    #     return 'No transactions file selected', 400
    # if households_file.filename == '':
    #     return 'No households file selected', 400
    # if products_file.filename == '':
    #     return 'No products file selected', 400

    # Save the files to the upload folder
    # transactions_filename = secure_filename(transactions_file.filename)
    # transactions_file_path = os.path.join(app.config['UPLOAD_FOLDER'], transactions_filename)
    # transactions_file.save(transactions_file_path)

    # households_filename = secure_filename(households_file.filename)
    # households_file_path = os.path.join(app.config['UPLOAD_FOLDER'], households_filename)
    # households_file.save(households_file_path)

    # products_filename = secure_filename(products_file.filename)
    # products_file_path = os.path.join(app.config['UPLOAD_FOLDER'], products_filename)
    # products_file.save(products_file_path)

    # Render template with existing data
    return render_template('success.html', filtered_df = filtered_df,  user_info=user_info, hshd_10_df=hshd_10_df, plot_data=plot_data, correlation=correlation)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
