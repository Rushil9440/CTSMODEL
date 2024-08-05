import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

from dotenv import load_dotenv

#load env variables
current_dir = Path.cwd()
env_vars = current_dir / ".env"
load_dotenv(env_vars)

sender_email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
print(sender_email,password,'fsfse')
def send_email(user_record):
    msg = EmailMessage()
    msg['Subject'] = "Health report"
    msg['From'] = formataddr(("Health Partner", f"{sender_email}"))
    msg['To'] = user_record['email']

    msg.set_content(
        f"""\
        Hi {user_record['name']},
        I hope you are well.
        I just wanted to drop a quick note to remind you.

        Health Report

        Predicted disease: {user_record['disease']}
        Description: {user_record['description']}
        Precautions: {user_record['precautions']}
        Medication: {user_record['medications']}
        Diet: {user_record['diet']}
        Workout: {user_record['workout']},
        'Personalized Advice':{user_record['Personalized Advice']}

        Best regards,
        Your Health Partner
        """
    )

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, user_record['email'], msg.as_string())

'''if __name__ == "__main__":
    send_email({
        "email": "john.doe@example.com",
        "name": "John Doe", 
        "disease": "fever",
        "description": "xyz",x
        "precautions": "don't go out",
        "medications": "paracitamol",
        "diet": "rice",
        "workout": "jogging"
    })
'''