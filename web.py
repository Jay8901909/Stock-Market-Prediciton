from re import template
from flask import jsonify
import subprocess
import mysql.connector
import secrets
from flask import Flask, request, render_template, redirect, url_for, make_response,flash,Response
from flask_mail import Mail, Message
from flask import session
from datetime import datetime, timedelta
from flask import render_template_string
import hashlib
import secrets
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from jinja2 import Environment
 


app = Flask(__name__, static_url_path='/static', static_folder='static')


# # Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stock_pro"
)


# # Establish a connection to the MySQL server
connection = mysql.connector.connect(host='localhost', user='root', password='', database='stock_pro')
cursor = connection.cursor()



# Generate a secret key
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = ''  # Update with your email
app.config['MAIL_PASSWORD'] = ''  # Update with your password

mail = Mail(app)

# Simulated database to store tokens
tokens = {}

@app.route('/forgot_password', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form['f_e-id']
        
        try:
            # Check if email exists in the database
            cursor.execute("SELECT e_id FROM registration WHERE e_id = %s", (email,))
            row = cursor.fetchone()
            if row:
                # Generate and store a unique token
                token = generate_unique_token()
                # Store the token with the email and current timestamp
                tokens[token] = {'email': email, 'timestamp': datetime.now()}
                send_reset_email(email, token)
                print('Password reset link sent to your email.')
                return render_template('fk.html', valid_message="Check your email (including spam) for the password reset link.")
            else:
                print('Email ID does not exist.')
                return render_template('fk.html', error_message="Invalid email,Please confirm your email and try again.")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            print('An error occurred. Please try again later.')

        return redirect(url_for('index'))
    
    return render_template('fk.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    error_message = None
    if request.method == 'POST':
        token = request.form.get('token')  # Use .get() to avoid KeyError
        # Verify token and handle password reset
        if token in tokens:
            token_data = tokens[token]
            email = token_data['email']
            timestamp = token_data['timestamp']
            # Check if the token is still valid (e.g., not expired)
            if datetime.now() - timestamp > timedelta(minutes=5):  # Token expires after 5 minutes
                error_message = 'Password reset link has expired. Please request a new one.'
            else:
                # Update user's password
                new_password = request.form['password']
                update_password(email, new_password)
                del tokens[token]  # Invalidate the token after use
                flash('Password successfully reset.')
                return redirect(url_for('index'))
        else:
            error_message = 'Password reset link expired. Please request a new one'
    
    # If the request method is GET or there's an error, render the password reset form
    token = request.args.get('token')  # Get the token from the query string
    return render_template('reset_page.html', token=token, error_message=error_message if request.method == 'POST' else None)

def generate_unique_token():
    return secrets.token_urlsafe(16)

def send_reset_email(email, token):
    msg = Message('Password Reset Request', sender='', recipients=[email])
    msg.body = f"Remember, to reset your password for FK stock prediction, make sure it's secure with at least one uppercase letter, one lowercase letter, one special symbol,and one number, example 'Aa$1796', and never share your passwords with anyone. Thank you for choosing us!,visit the following link and reset your password: {request.url_root}reset_password?token={token}"

    try:
        mail.send(msg)
        print("Password reset email sent successfully.")
    except Exception as e:
        print(f'Error sending email: {str(e)}')

def update_password(email, new_password):
    try:
        update_query = "UPDATE registration SET password = %s, c_password = %s WHERE e_id = %s"
        cursor.execute(update_query, (new_password, new_password, email))
        connection.commit()
        print(f'Password for {email} successfully updated.')
    except mysql.connector.Error as err:
        print(f"Error updating password: {err}")

@app.route('/')
def index():
    return render_template('fk.html')

@app.route('/terms')
def terms_and_conditions():
    return render_template('terms.html')

@app.route('/fk_page')
def fk_page():
    # Get the value of the 'cookie_name' cookie
    cookie_value = request.cookies.get('cookie_name')

    # Check if the 'success' parameter is present in the URL
    success = request.args.get('success', False)

    return render_template('fk.html', cookie_value=cookie_value, success=success)

# @app.route('/submit', methods=['POST'])
# def submit():
#     if request.method == 'POST':
#         first_name = request.form['First_Name']
#         last_name = request.form['Last_Name']
#         e_mail = request.form['Email_Id']
#         m_no = request.form['Mobile_Number']
#         passw = request.form['Password']
#         c_passw = request.form['Confirm_Password']

#         try:
#             # Use parameterized queries to prevent SQL injection
#             select_query = "SELECT e_id, mo_num FROM registration WHERE e_id = %s AND mo_num = %s"
#             cursor.execute(select_query, (e_mail, m_no))
#             row = cursor.fetchone()

#             if row:
#                 print("User already exists")
#                 return render_template('fk.html', error_message="User already exists")

#             # Insert data into the table
#             insert_query = "INSERT INTO registration (f_name, l_name, e_id, mo_num, password, c_password) VALUES (%s, %s, %s, %s, %s, %s)"
#             cursor.execute(insert_query, (first_name, last_name, e_mail, m_no, passw, c_passw))

#             # Commit the changes
#             connection.commit()

#             # Set a cookie
#             response = make_response(redirect(url_for('fk_page', success=True)))
#             response.set_cookie('cookie_name', 'cookie_value')

#             return response

#         except mysql.connector.Error as err:
#             print(f"Error: {err}")
#             return render_template('fk.html', error_message="User already exists")

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        first_name = request.form['First_Name']
        last_name = request.form['Last_Name']
        e_mail = request.form['Email_Id']
        m_no = request.form['Mobile_Number']
        passw = request.form['Password']
        c_passw = request.form['Confirm_Password']

        try:
            # Check if the email is verified
            if not is_email_verified(e_mail):
                return render_template('fk.html', error_message="Please verify your email before registering.")
            
            # Use parameterized queries to prevent SQL injection
            select_query = "SELECT e_id, mo_num FROM registration WHERE e_id = %s AND mo_num = %s"
            cursor.execute(select_query, (e_mail, m_no))
            row = cursor.fetchone()

            if row:
                print("User already exists")
                return render_template('fk.html', error_message="User already exists")

            # Insert data into the table
            insert_query = "INSERT INTO registration (f_name, l_name, e_id, mo_num, password, c_password) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (first_name, last_name, e_mail, m_no, passw, c_passw))

            # Commit the changes
            connection.commit()

            # Remove the verification token associated with the registered email
            cleanup_verification_token(e_mail)

            # Set a cookie or perform any other necessary actions upon successful registration
            flash('Registration successful. Please log in.')
            return redirect(url_for('fk'))

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return render_template('fk.html', error_message="An error occurred during registration. Please try again later.")

# Function to remove the verification token associated with the registered email
def cleanup_verification_token(email):
    # Remove the verification token associated with the registered email
    for token, token_data in verification_tokens.items():
        if token_data['email'] == email:
            del verification_tokens[token]
            break  # Exit loop after removing the token

lol_active = False  # Initial state is inactive




# @app.route('/login', methods=['POST'])
# def login():
#     if request.method == 'POST':
#         e_mail = request.form['l_e_id']
#         password = request.form['psw']
#         try:
#             select_query = "SELECT e_id, password FROM registration WHERE e_id = %s AND password = %s"
#             cursor.execute(select_query, (e_mail, password))
#             row = cursor.fetchone()
#             if row:
#                 flash("Successfully logged in!")
#                 #session['e_id'] = e_mail  # Storing e_id in session
#                 session['e_id'] = row[0]
#                 return redirect(url_for('stock_predict'))  # Redirect to the streamlit page upon successful login
#             else:
#                 print("Email ID or password is incorrect.")
#                 error_message = "Email ID or password is incorrect"
#                 return render_template('fk.html', error_message=error_message)
#         except mysql.connector.Error as err:
#             return f"Database error: {err}"
#     return render_template('fk.html')
        
# @app.route('/login', methods=['POST'])
# def login():
#     if request.method == 'POST':
#         e_mail = request.form['l_e_id']
#         password = request.form['psw']
#         cursor.execute("SELECT f_name, e_id FROM registration WHERE e_id = %s AND password = %s", (e_mail, password))
#         user = cursor.fetchone()
#         if user:
#             flash("Successfully logged in!")
#             first_name = user[0]
#             session['firstname'] = first_name  # Storing first name in session
#             session['e_id'] = user[1]  # Storing e_id in session
#             print("First name:", first_name)  # Debugging statement
#             print("Session contents:", session)  # Debugging statement
#             return redirect(url_for('stock_predict'))  # Redirect to the Streamlit page upon successful login
#         else:
#             return "Invalid email or password"
#     return render_template('fk.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        e_mail = request.form['l_e_id']
        password = request.form['psw']
        cursor.execute("SELECT f_name, l_name, e_id, mo_num, password, c_password FROM registration WHERE e_id = %s", (e_mail,))
        user = cursor.fetchone()
        if user:
            stored_password = user[4]  # Index 4 is the stored password
            if stored_password == password:
                flash("Successfully logged in!")
                first_name = user[0]
                last_name = user[1]
                email = user[2]
                mobile_number = user[3]
                login_time = datetime.now()
                cursor.execute("INSERT INTO login_history (f_name, l_name, e_id, mo_num, login_time) VALUES (%s, %s, %s, %s, %s)", (first_name, last_name, email, mobile_number, login_time))
                connection.commit()
                session['firstname'] = first_name  # Storing first name in session
                session['e_id'] = email  # Storing e_id in session
                print("First name:", first_name)  # Debugging statement
                print("Session contents:", session)  # Debugging statement
                return redirect(url_for('stock_predict'))  # Redirect to the Streamlit page upon successful login
            else:
                error_message = "Invalid email or password"
        else:
            error_message = "Invalid email or password"
    return render_template('fk.html', error_message=error_message)


# @app.route('/login', methods=['POST'])
# def login():
#     if request.method == 'POST':
#         e_mail = request.form['l_e_id']
#         password = request.form['psw']
#         cursor.execute("SELECT f_name, e_id, password FROM registration WHERE e_id = %s", (e_mail,))
#         user = cursor.fetchone()
#         if user:
#             stored_password = user[2]
#             if stored_password == password:
#                 flash("Successfully logged in!")
#                 first_name = user[0]
#                 email = user[2]
#                 cursor.execute("INSERT INTO login_history (email) VALUES (%s)", (email,))
#                 connection.commit()
#                 session['firstname'] = first_name  # Storing first name in session
#                 session['e_id'] = user[1]  # Storing e_id in session
#                 print("First name:", first_name)  # Debugging statement
#                 print("Session contents:", session)  # Debugging statement
#                 return redirect(url_for('stock_predict'))  # Redirect to the Streamlit page upon successful login
#             else:
#                 error_message = "Invalid email or password"
#                 return render_template('fk.html', error_message=error_message)
#         else:
#             error_message = "Invalid email or password"
#             return render_template('fk.html', error_message=error_message)
#     return render_template('fk.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        mo_num = request.form['mo_num']
        message = request.form['message']
        
        try:
            # Insert data into the database
            insert_query = "INSERT INTO contact_us (name, email, mo_num, message) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (name, email, mo_num, message))
            connection.commit()  # Commit the transaction

            # Redirect after successful submission
            return redirect(url_for('contact'))

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            # Handle database error
            
    return render_template('contact.html')

# @app.route('/stock_predict')
# def stock_predict():
#     if 'e_id' in session:
#         # Check if the user is logged in
#         return redirect('http://192.168.92.126:8501/lol')
#     else:
#         # Redirect to login if not logged in
#         return redirect(url_for('fk'))

# @app.route('/stock_predict')
# def stock_predict():
#     if 'e_id' in session:
#         # Check if the user is logged in
#         return redirect('http://192.168.92.126:8501/lol')
#     else:
#         # Redirect to login if not logged in
#         return redirect(url_for('fk'))

@app.route('/stock_predict')
def stock_predict():
    if 'e_id' in session:
        # User is logged in
        # Pass session information to Streamlit page
        e_id = session['e_id']
        first_name = session['firstname']
        # base_url = 'http://192.168.92.126:8501/lol'
        base_url = ' http://192.168.92.126:8503/lol'
        # Redirect to the Streamlit page with session information
        #return redirect(f'http://192.168.92.126:8501/lol?e_id={e_id}&first_name={first_name}')
        # Hashing the email ID
        hashed_e_id = hashlib.sha1(e_id.encode()).hexdigest()
        
        
        
        # Redirect to the Streamlit page with session information
        #return redirect(f'http://192.168.92.126:8501/lol?e_id={hashed_e_id}&first_name={first_name}')
        return redirect(f'{base_url}?e_id={hashed_e_id}&first_name={first_name}')
    else:
        # Redirect to login if not logged in
        return redirect(url_for('fk'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('fk'))  # Redirect to your main page (e.g., 'fk.html')

@app.route('/fk')
def fk():
    return render_template('fk.html')

# Dictionary to store email verification tokens temporarily
verification_tokens = {}

# Function to generate a verification token
def generate_verification_token(email):
    token = secrets.token_urlsafe(16)
    verification_tokens[token] = {'email': email, 'code': generate_verification_code(), 'timestamp': datetime.now()}
    return token

# Function to generate a verification code
def generate_verification_code():
    return str(secrets.randbelow(1000000)).zfill(6)

# Route to send verification email
@app.route('/send_verification_email', methods=['POST'])
def send_verification_email():
    email = request.json.get('email')
    token = generate_verification_token(email)
    verification_code = verification_tokens[token]['code']  # Retrieve the verification code
    
    # Call the function to send verification email
    send_verification_email(email, token, verification_code)
    
    return jsonify({"message": "Verification email sent successfully."})


# # Function to send verification email
# def send_verification_email(email, token, verification_code):
#     msg = Message('Verify Your Email', sender='', recipients=[email])
#     verification_link = f"{request.url_root}verify_email/{token}"  # Verification link without email as a query parameter
#     # msg.body = f"Please click the following link to verify your email: {verification_link}\nVerification Code: {verification_code}"
#     msg.body = f"Please click the following link to verify your email: {verification_link}\nVerification Code: {verification_code}\nEmail: {email}"
#     mail.send(msg)

# Function to send verification email
def send_verification_email(email, token, verification_code):
    msg = Message('Verify Your Email', sender='', recipients=[email])
    verification_link = f"{request.url_root}verify_email/{token}?email={email}"  # Include email as a query parameter
    msg.body = f"Please click the following link to verify your email: {verification_link}\nVerification Code: {verification_code}"
    mail.send(msg)


# # Route to render the verification form
# @app.route('/verify_email/<token>')
# def verify_email(token):
#     # Check if the token exists in the verification_tokens dictionary
#     if token in verification_tokens:
#         # Render the verification HTML page with the token
#         return render_template('verify.html', token=token)
#     else:
#         return "Invalid or expired verification link."

# Route to render the verification form
@app.route('/verify_email/<token>')
def verify_email(token):
    email = request.args.get('email')  # Retrieve the email from the query parameters
    # Check if the token exists in the verification_tokens dictionary
    if token in verification_tokens:
        # Render the verification HTML page with the token and email
        return render_template('verify.html', token=token, email=email)
    else:
        return "Invalid or expired verification link."
    
# Route to handle the verification process
@app.route('/verify_email_process', methods=['POST'])
def verify_email_process():
    token = request.form['token']
    email = request.form['email']
    verification_code = request.form['verificationCode']
    
    # Check if the token exists and is valid
    if token in verification_tokens:
        token_data = verification_tokens[token]
        # Compare the verification code with the one stored in the dictionary
        if token_data['email'] == email and token_data['code'] == verification_code:
            # Mark the email as verified
            token_data['verified'] = True
            # Optionally, you can also remove the token after successful verification
            #del verification_tokens[token]
            return jsonify({"message": "Email verified successfully.", "alert": "success"})
        else:
            return jsonify({"error": "Invalid verification code or email.", "alert": "error"}), 400
    else:
        return jsonify({"error": "Invalid or expired verification link.", "alert": "error"}), 400

    

# Function to check if email is verified
def is_email_verified(email):
    # Check if the email exists in the verification_tokens dictionary
    for token_data in verification_tokens.values():
        if token_data['email'] == email and token_data.get('verified', False):
            return True
    return False

#new admin panal code date 8-3-2024
# Function to authenticate admin login
# def authenticate_admin(username, password):
#     if username == 'admin' and password == '@Dm|n':
#         return True
#     return False

# # Route for admin login
# @app.route('/moderator', methods=['GET', 'POST'])
# def admin_login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if authenticate_admin(username, password):
#             session['is_admin'] = True
#             return redirect(url_for('admin_dashboard'))
#         else:
#             return render_template('admin_login.html', error='Invalid credentials')
#     return render_template('admin_login.html')

# # Route for admin dashboard
# @app.route('/admin/dashboard')
# def admin_dashboard():
#     if session.get('is_admin'):
#         return render_template('admin_dashboard.html')
#     else:
#         return redirect(url_for('admin_login'))

# Function to retrieve admin credentials from the database
def get_admin_credentials(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admin')
    row = cursor.fetchone()
    if row:
        return {'username': row[1], 'password': row[2]}
    return None

# Function to authenticate admin login
def authenticate_admin(username, password, conn):
    admin_credentials = get_admin_credentials(conn)
    if admin_credentials and username == admin_credentials['username'] and password == admin_credentials['password']:
        return True
    return False

# Route for admin login
# @app.route('/admin', methods=['GET', 'POST'])
# def admin_login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if authenticate_admin(username, password, connection):
#             session['is_admin'] = True
#             return redirect(url_for('admin_dashboard'))
#         else:
#             return render_template('admin_login.html', error='Invalid credentials')
#     return render_template('admin_login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_admin(username, password, connection):
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    elif request.method == 'GET' and 'logout' in request.args:
        session.pop('is_admin', None)  # Clear the 'is_admin' session variable
        return redirect(url_for('admin_login'))
    return render_template('admin_login.html')

# Route for displaying admin dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))  # Redirect if not logged in as admin
    return render_template('admin_dashboard.html')

# Route for changing password
@app.route('/admin/change_password', methods=['POST'])
def change_password():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))  # Redirect if not logged in as admin
    new_password = request.form['new_password']
    cursor = connection.cursor()
    cursor.execute('UPDATE admin SET password = %s', (new_password,))
    connection.commit()
    return redirect(url_for('admin_login'))

# Route for viewing users
@app.route('/admin/users')
def view_users():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if start_date and end_date:
            cursor.execute("SELECT `f_name`, `l_name`, `e_id`, `mo_num`, `password`, `c_password`, `registration_timestamp` FROM `registration` WHERE `registration_timestamp` BETWEEN %s AND %s", (start_date, end_date))
        else:
            cursor.execute("SELECT `f_name`, `l_name`, `e_id`, `mo_num`, `password`, `c_password`, `registration_timestamp` FROM `registration`")

        users = cursor.fetchall()
        return render_template('admin_users.html', users=users)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template('error.html', error_message="An error occurred while fetching users.")

# Route for adding a new user
@app.route('/admin/users/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Retrieve user data from the form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        mobile_number = request.form['mobile_number']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            return render_template('add_user.html', error_message="Password and confirm password do not match.")

        try:
            # Insert the new user into the database
            insert_query = "INSERT INTO registration (f_name, l_name, e_id, mo_num, password, c_password) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (first_name, last_name, email, mobile_number, password, confirm_password))
            connection.commit()
            return redirect(url_for('view_users'))
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return render_template('add_user.html', error_message="An error occurred while adding the user.")
    return render_template('add_user.html')

# Route for editing user information
@app.route('/admin/users/edit', methods=['GET', 'POST'])
def edit_user():
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        # Fetch user data from the database based on user_id
        try:
            cursor.execute("SELECT `f_name`, `l_name`, `e_id`, `mo_num`, `password`, `c_password` FROM `registration` WHERE `e_id` = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                return render_template('edit_user.html', user=user)
            else:
                return "User not found"
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return render_template('error.html', error_message="An error occurred while fetching user details.")

    elif request.method == 'POST':
        # Update user information in the database
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        mobile_number = request.form['mobile_number']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        try:
            update_query = "UPDATE registration SET f_name = %s, l_name = %s, mo_num = %s, password = %s, c_password = %s WHERE e_id = %s"
            cursor.execute(update_query, (first_name, last_name, mobile_number, password, confirm_password, email))
            connection.commit()
            return redirect(url_for('view_users'))
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return render_template('edit_user.html', error_message="An error occurred while updating the user.")
    return redirect(url_for('admin_dashboard'))

# Route for deleting a user
@app.route('/admin/delete_user', methods=['POST'])
def delete_user():
    if 'is_admin' not in session or not session['is_admin']:
        return redirect(url_for('admin_login'))  # Redirect if not logged in as admin
    try:
        email = request.form['email']
        delete_query = "DELETE FROM registration WHERE e_id = %s"
        cursor.execute(delete_query, (email,))
        connection.commit()  # Commit changes to the database
        return redirect(url_for('view_users'))
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template('error.html', error_message="An error occurred while deleting the user.")
    

# admin login history 9-3-2024
from datetime import datetime

# @app.route('/admin/login_history')
# def login_history():
#     if session.get('is_admin'):
#         try:
#             # Execute SQL query to fetch login history records
#             cursor.execute("SELECT id, f_name, l_name, e_id, mo_num, login_time FROM login_history")
#             login_records = cursor.fetchall()

#             # Render template with login history records
#             return render_template('login_history.html', login_records=login_records)
#         except mysql.connector.Error as err:
#             # Handle database errors
#             print(f"Database error: {err}")
#             return render_template('error.html', error_message="An error occurred while fetching login history.")
#     else:
#         # Redirect unauthorized users to admin login page
#         return redirect(url_for('admin_login'))





@app.route('/admin/login_history', methods=['GET', 'POST'])
def login_history():
    if session.get('is_admin'):
        try:
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            cursor = connection.cursor()
            sql_query = "SELECT id, f_name, l_name, e_id, mo_num, login_time FROM login_history"
            
            if start_date and end_date:
                sql_query += " WHERE login_time BETWEEN %s AND %s"
                cursor.execute(sql_query, (start_date, end_date))
            else:
                cursor.execute(sql_query)

            login_records = cursor.fetchall()
            cursor.close()

            return render_template('login_history.html', login_records=login_records)
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return render_template('error.html', error_message="An error occurred while fetching login history.")
    else:
        return redirect(url_for('admin_login'))


# @app.route('/admin/login_history', methods=['GET', 'POST'])
# def login_history():
#     if session.get('is_admin'):
#         try:
#             start_date = request.args.get('start_date')
#             end_date = request.args.get('end_date')
#             # Assuming you already have a connection established elsewhere in your code
#             cursor = connection.cursor()
#             sql_query = "SELECT id, f_name, l_name, e_id, mo_num, login_time FROM login_history"
#             cursor.execute(sql_query)
#             login_records = cursor.fetchall()
#             # Construct SQL query with date filtering
#             sql_query = "SELECT id, f_name, l_name, e_id, mo_num, login_time FROM login_history WHERE login_time BETWEEN %s AND %s"
#             cursor.execute(sql_query, (start_date, end_date))
#             login_records = cursor.fetchall()

#             # Close the cursor after fetching data
#             cursor.close()

#             # Render template with filtered login history records
#             return render_template('login_history.html', login_records=login_records)
#         except mysql.connector.Error as err:
#             # Handle database errors
#             print(f"Database error: {err}")
#             return render_template('error.html', error_message="An error occurred while fetching login history.")
#     else:
#         # Redirect unauthorized users to admin login page
#         return redirect(url_for('admin_login'))
    
# feedback get from contactus (admin)
@app.route('/feedback')
def feedback():
    # Retrieve contact data from the database
    cursor.execute("SELECT name, email, mo_num, message FROM contact_us")
    contact_data = cursor.fetchall()
    
    return render_template('feedback.html', contact_data=contact_data)

    



if __name__ == '__main__':
    subprocess.Popen(["streamlit", "run", r"C:\Users\APMS\Desktop\Project\templates\lol.py", "--server.headless", "true"])
    # app.run(debug=True,host='127.0.0.1')
    app.run(debug=True, host='192.168.15.126')

connection.close()