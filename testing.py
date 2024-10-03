import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from email.mime.image import MIMEImage
import random


smtp_server = 'smtp.mail.yahoo.com'
smtp_port = 587  # or 465 for SSL
yahoo_email = st.secrets["yahoo_email"]
yahoo_password = st.secrets["yahoo_pass"]
# yahoo_email = "amsterlog_za@yahoo.com"
# yahoo_password = "anywglrypagcdhuk"


st.markdown("<h1 style='text-align: center;'>TikTok Studio Bot</h1>", unsafe_allow_html=True)
st.write("<br>", unsafe_allow_html=True)


def send_email(subject, message, to_email):
    # Create message container
    msg = MIMEMultipart()
    msg['From'] = yahoo_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach message
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Establish a secure session with the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        # Login using your Yahoo email and password
        server.login(yahoo_email, yahoo_password)

        # Send the email
        server.sendmail(yahoo_email, to_email, msg.as_string())
        print("Email sent successfully!")

    except smtplib.SMTPException as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        # Quit the server
        try:
            if server:
                server.quit()
        except Exception as e:
            print(f"Error while quitting server: {e}")
    
def tries_left(username, password):
    users = sheet
    for user in users:
        if user['Username'] == username and user['Password'] == password and user['Count'] >= 1 and user['Status'] == 'trial':
            return 1 - user['Count']        
        if user['Username'] == username and user['Password'] == password and user['Count'] >= 1 and user['Status'] == 'trial':
            return 1 - user['Count']
        if user['Username'] == username and user['Password'] == password and user['Count'] <= 3 and user['Status'] == 'trial':
            return 3 - user['Count']        
        if user['Username'] == username and user['Password'] == password and user['Count'] <= 1 and user['Status'] == 'trial':
            return 1 - user['Count']         
        elif user['Username'] == username and user['Password'] == password and user['Status'] == 'verified':
            return 10 - user['Count'] 
        elif user['Username'] == username and user['Password'] == password and user['Count'] <= 12 and user['Status'] == 'verified':
            return 12 - user['Count']
        elif user['Username'] == username and user['Password'] == password and user['Status'] == 'pending':
            return 0
    return False

def account_status(username,password):
    users = sheet
    for user in users:
        if user['Username'] == username and user['Password'] == password and user['Status'] == 'trial':
            return 'trial'
        elif user['Username'] == username and user['Password'] == password  and user['Status'] == 'verified':
            return 'verified'   
        
def main(username,password):

    remaining_captions = tries_left(username,password)
    st.markdown(f"API calls Remaining : {remaining_captions}")
    # account_state = account_status(username, password)
    # if account_state == 'trial':
    #     st.markdown("Account : Trial")
    # elif account_state == 'verified':
    #     st.markdown("Account : Paid")

    col1, col2, col3, col4= st.columns([1, 2, 3, 4])

    with col4:
        if st.button("Logout"):
                st.session_state.logged_in = False
                st.rerun()  # Rerun to reflect logout

def load_google_sheets_credentials():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict({
        "type": "service_account",
        "project_id": st.secrets["google_sheets"]["project_id"],
        "private_key_id": st.secrets["google_sheets"]["private_key_id"],
        "private_key": st.secrets["google_sheets"]["private_key"],
        "client_email": st.secrets["google_sheets"]["client_email"],
        "client_id": st.secrets["google_sheets"]["client_id"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": st.secrets["google_sheets"]["client_x509_cert_url"]
    }, scope)
    client = gspread.authorize(creds)
    sheet_id = '1Bsv2n_12_wmWhNI5I5HgCmBWsVyAHFw3rfTGoIrT5ho'
    sheet = client.open_by_key(sheet_id).sheet1
    all_records = sheet.get_all_records()  # Use get_all_values instead
    return all_records
    
sheet = load_google_sheets_credentials()

# Define the expected headers explicitly
def check_user(username, password):
    users = sheet

    for user in users:
        if user['Username'] == username and user['Password'] == password and user['Count'] >= 1 and user['Status'] == 'trial':
            return 'limit'        
        if user['Username'] == username and user['Password'] == password and user['Count'] == 1 and user['Status'] == 'trial' and user['Promo Code Status'] == 'unverified':
            return 'limit'
        if user['Username'] == username and user['Password'] == password and user['Count'] == 3 and user['Status'] == 'trial' and user['Promo Code Status'] == 'verified':
            return 'limit3'        
        if user['Username'] == username and user['Password'] == password and user['Count'] <= 2 and user['Status'] == 'trial':
            return True        
        elif user['Username'] == username and user['Password'] == password and user['Count'] <= 10 and user['Status'] == 'verified':
            return True
        elif user['Username'] == username and user['Password'] == password and user['Count'] <= 12 and user['Status'] == 'verified' and user['Promo Code Status'] == 'verified':
            return True        
        elif user['Username'] == username and user['Password'] == password and user['Status'] == 'pending':
            return 'pending'
    return False


def feedback(email, text_feedback, ux, caption_quality):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict({
        "type": "service_account",
        "project_id": st.secrets["google_sheets"]["project_id"],
        "private_key_id": st.secrets["google_sheets"]["private_key_id"],
        "private_key": st.secrets["google_sheets"]["private_key"],
        "client_email": st.secrets["google_sheets"]["client_email"],
        "client_id": st.secrets["google_sheets"]["client_id"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": st.secrets["google_sheets"]["client_x509_cert_url"]
    }, scope)
    client = gspread.authorize(creds)
    sheet_id = '1Bsv2n_12_wmWhNI5I5HgCmBWsVyAHFw3rfTGoIrT5ho'
    sheet = client.open_by_key(sheet_id).get_worksheet(3)
    sheet.append_row([email,text_feedback,ux,caption_quality])
    return True

def signup_add_user(username, password, sender_email, status, email, promo_code_status):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict({
        "type": "service_account",
        "project_id": st.secrets["google_sheets"]["project_id"],
        "private_key_id": st.secrets["google_sheets"]["private_key_id"],
        "private_key": st.secrets["google_sheets"]["private_key"],
        "client_email": st.secrets["google_sheets"]["client_email"],
        "client_id": st.secrets["google_sheets"]["client_id"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": st.secrets["google_sheets"]["client_x509_cert_url"]
    }, scope)
    client = gspread.authorize(creds)
    sheet_id = '1Bsv2n_12_wmWhNI5I5HgCmBWsVyAHFw3rfTGoIrT5ho'
    sheet = client.open_by_key(sheet_id).sheet1
    sheet.append_row([username, password, 0, sender_email, status, 0, 0, email, promo_code_status]) 
    return True

def signup_user(username, password, sender_email, status, email, promo_code_status):
    users = sheet
    for user in users:
        if user['Username'] == username:
            return False  # Username already exists
    signup_add_user(username, password, sender_email, status, email, promo_code_status)
    # sheet.append_row([username, password, 0, sender_email])
    return True

def signup_user_check(email):
    users = sheet
    for user in users:
        if user['Email'] == email:
            return False  # Username already exists
    return True

def update_caption_count(i, user):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict({
        "type": "service_account",
        "project_id": st.secrets["google_sheets"]["project_id"],
        "private_key_id": st.secrets["google_sheets"]["private_key_id"],
        "private_key": st.secrets["google_sheets"]["private_key"],
        "client_email": st.secrets["google_sheets"]["client_email"],
        "client_id": st.secrets["google_sheets"]["client_id"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": st.secrets["google_sheets"]["client_x509_cert_url"]
    }, scope)
    client = gspread.authorize(creds)
    sheet_id = '1Bsv2n_12_wmWhNI5I5HgCmBWsVyAHFw3rfTGoIrT5ho'
    sheet = client.open_by_key(sheet_id).sheet1
    new_count = user['Count'] + 1
    sheet.update_cell(i + 2, 3, new_count)  # Update the count in the sheet (i + 2 to account for header)
    return True

def update_login_count(i, user):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict({
        "type": "service_account",
        "project_id": st.secrets["google_sheets"]["project_id"],
        "private_key_id": st.secrets["google_sheets"]["private_key_id"],
        "private_key": st.secrets["google_sheets"]["private_key"],
        "client_email": st.secrets["google_sheets"]["client_email"],
        "client_id": st.secrets["google_sheets"]["client_id"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": st.secrets["google_sheets"]["client_x509_cert_url"]
    }, scope)
    client = gspread.authorize(creds)
    sheet_id = '1Bsv2n_12_wmWhNI5I5HgCmBWsVyAHFw3rfTGoIrT5ho'
    sheet = client.open_by_key(sheet_id).sheet1
    new_count = user['Logins'] + 1
    sheet.update_cell(i + 2, 6, new_count)  # Update the count in the sheet (i + 2 to account for header)
    last_login = str(datetime.now())
    sheet.update_cell(i + 2, 7, last_login)  # Update the count in the sheet (i + 2 to account for header)

    return True

def load_google_sheets_credentials():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict({
        "type": "service_account",
        "project_id": st.secrets["google_sheets"]["project_id"],
        "private_key_id": st.secrets["google_sheets"]["private_key_id"],
        "private_key": st.secrets["google_sheets"]["private_key"],
        "client_email": st.secrets["google_sheets"]["client_email"],
        "client_id": st.secrets["google_sheets"]["client_id"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": st.secrets["google_sheets"]["client_x509_cert_url"]
    }, scope)
    client = gspread.authorize(creds)
    sheet_id = '1Bsv2n_12_wmWhNI5I5HgCmBWsVyAHFw3rfTGoIrT5ho'
    sheet = client.open_by_key(sheet_id).get_worksheet(1)
    all_records = sheet.get_all_records()  # Use get_all_values instead
    return all_records
    
promo_sheet = load_google_sheets_credentials()

def check_promo(promo_code, email_address_game):
    users = promo_sheet
    print(users)
    print(email_address_game)
    for user in users:
        if user['Promo'] == promo_code and user['Email'] == email_address_game:
            print("Promo Code Matched")
            return True
    print("Promo Code does not match")
    return False

def login_count(username, password):
    users = sheet
    for i, user in enumerate(users):
        if user['Username'] == username and user['Password'] == password:
            # Increment the login count
            update_login_count(i, user)
            
    return False  # Username or password incorrect

def captions_generated_count(username, password):
    users = sheet
    for i, user in enumerate(users):
        if user['Username'] == username and user['Password'] == password:
            # Increment the login count
            update_caption_count(i, user)
            
    return False  # Username or password incorrect

def generate_otp():
    otp = str(random.randint(1000, 9999))  # Generate a 4-digit OTP
    return otp

def validate_email(email):
    if "@" not in email or "." not in email.split('@')[-1]:
        return False
    return True

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'password' not in st.session_state:
    st.session_state.password = None

menu = ["Signup", "Login", "Support"]

# Use the index of the default choice in the options list
default_index = 1  # Index of "Login" in menu (starts from 0)
choice = st.sidebar.selectbox("Menu", menu, index=default_index)

promo_code_status = ''
status = 'pending'

if not st.session_state.logged_in:
    st.session_state.new_email = ''
    if choice == "Signup":
        st.subheader("Create a new account")
        st.session_state.new_email = st.text_input("Email Address")
        sender_email_1 = None  # Define sender_email_1 here

        # Initialize session state variables if they don't exist
        if 'otp_generated' not in st.session_state:
            st.session_state.otp_generated = None

        if st.button("Signup"):
            email = st.session_state.new_email

            if not email:
                print("No Email")
                st.error("Please enter your email address to sign up")
            else:
                if not validate_email(email):
                    st.error("Please enter a valid email address")
                else:
                    print("Email present in text: ", st.session_state.new_email)
                    if signup_user_check(email):
                        st.session_state.otp_generated = generate_otp()
                        send_email(
                            'OTP Verification',
                            f"Please use the following OTP to verify: {st.session_state.otp_generated}",
                            email,
                        )
                        st.success("Please check your email for the OTP")
                        time.sleep(2)
                        print(st.session_state.otp_generated)
                        st.session_state.signup_stage = 'otp_sent'
                    else:
                        st.error("Email address already registered")
                        st.rerun()

        if 'signup_stage' in st.session_state and st.session_state.signup_stage == 'otp_sent':
            enter_otp = st.text_input("Please enter the OTP received on your Email")
            print(enter_otp)
            if st.button("Verify OTP"):
                if enter_otp == st.session_state.otp_generated:
                    print("OTP Entered matched")
                    st.session_state.signup_stage = 'user_details'  # Move to the next stage
                else:
                    st.error("OTP entered is incorrect")

        if 'signup_stage' in st.session_state and st.session_state.signup_stage == 'user_details':
            new_username = st.text_input("Enter Username")  # Example input for username
            new_password = st.text_input("Enter Password", type="password")  # Example input for password
            sender_email_1 = ''  # Example sender email
            sender_email = sender_email_1

            if st.button("Proceed"):
                if not st.session_state.new_email:
                    st.error("Please enter your email address to sign up")
                elif new_username and new_password:
                    if signup_user(new_username, new_password, sender_email, status, st.session_state.new_email, promo_code_status):
                        st.success('Congratulations! You have signed up for the account.')
                        recipient_email = 'automatexpos@gmail.com'
                        email_subject = 'New user signup'
                        current_time = datetime.now()
                        print(current_time)
                        email_message = f'A new user has signed up\nUsername : {new_username}\nSubscription : {status}\nTime : {current_time}'
                        send_email(email_subject, email_message, recipient_email)

                        with st.spinner('Please wait while your payment is being processed...'):
                            time.sleep(5)
                        st.success('You can log in to continue once your payment is verified.')
                        time.sleep(5)
                        st.session_state.signup_stage = None

                        st.rerun()
                    else:
                        st.error("Username already exists. Please choose a different username.")
                else:
                    st.error("Please enter a username and password")

    elif choice == "Login":
        st.subheader("Login to your account")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            state = check_user(username, password)
            if state == True:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.password = password
                with st.spinner("Logging in..."):
                    time.sleep(5)
                st.success(f"Welcome back {username}!")
                login_count(username, password)
                time.sleep(3)
                st.rerun()
            elif state == 'limit':
                st.error("Sorry, Limit Exceeded. Please subscribe to use the tool")
                st.error("Contact Support to Subscribe")
            elif state == 'pending':
                st.error("Sorry, Your payment is still pending. Please wait..")
                st.error("Contact Support if payment is not verified within 5 minutes. Please share your username and payment confirmation screenshot")
            elif state == 'limit3':
                st.error("Sorry, Limit Exceeded. Please subscribe to use the tool")
                st.error("Contact Support to Subscribe")
            else:
                st.error("Invalid username or password")

    elif choice == "Support":
        st.subheader("Welcome to Support")
        ticket_type = st.radio("Select Ticket Type", ["Subscription Request", "Issue"])

        if 'button_pressed' not in st.session_state:
            st.session_state.button_pressed = False

        if ticket_type == "Issue":
            support_email_sender = st.text_input("Please enter your email address")
            email_text = st.text_input("Please enter your query")

            if st.session_state.button_pressed:
                st.warning("You have already submitted your request.")
            else:
                if st.button("Send", disabled=not (support_email_sender and email_text)):
                    with st.spinner("Creating ticket..."):
                        recipient_email = 'automatexpos@gmail.com'
                        email_subject = 'New Ticket'
                        current_time = datetime.now()
                        email_message = f'A new ticket has been opened\n\nTime : {current_time}\nEmail address : {support_email_sender}\nQuestion : {email_text}'
                        send_email(email_subject, email_message, recipient_email)

                    st.session_state.button_pressed = True
                    st.success("Your ticket has been received, a support agent will get back to you soon")
                elif st.session_state.button_pressed:
                    st.warning("You have already submitted your request.")

else:
    main(st.session_state.username, st.session_state.password)