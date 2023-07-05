import requests
from datetime import datetime
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_LAT = 9.081999 
MY_LONG = 8.675277
EMAIL_PASS = "vyqupkpworxumhbt"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now().hour

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.


def position_checker():
    if (abs(iss_latitude - MY_LAT) <= 5) and (abs(iss_longitude - MY_LONG) <= 5):
        return True
    else:
        return False
    
def time_checker():
    if (abs(time_now - sunrise) <=5) or (abs(time_now - sunset) <= 5):
        return True
    else:
        return False
    

def mail_sender(sender='husseinkhidr3@gmail.com', receiver='daqmedia@gmail.com', subject='ISS SPOTTING', message='LOOK UP!!!!'):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Enable secure connection
        server.login(sender, EMAIL_PASS)  # Replace with your email password
        server.send_message(msg)  # Send the email


while True:
    if position_checker() and time_checker():
        mail_sender()
    time.sleep(60)
