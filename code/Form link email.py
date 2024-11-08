import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

def send_email(sender_email, sender_password, recipients, job_role, google_form_link, subject_template, body_template, image_path):
    for recipient_email, recipient_name in recipients:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        subject = subject_template.format(recipient_name=recipient_name)
        msg['Subject'] = subject

        # Create the body of the email with HTML
        body = body_template.format(recipient_name=recipient_name, job_role=job_role, google_form_link=google_form_link)
        html_body = f"""
        <html>
        <body>
            <p>Hi {recipient_name},</p>
            <p>Congratulations! We are pleased to inform you that you have been selected for the role of {job_role}.</p>
            <p>To proceed further, kindly fill out the following Google Form with your details and attempt the coding questions:</p>
            <a href="{google_form_link}">Google Form Link</a>
            <p>If you have any questions, feel free to reach out to us.</p>
            <p>Best regards,<br>Hiring Team</p>
            <img src="cid:image1">
        </body>
        </html>
        """
        msg.attach(MIMEText(html_body, 'html'))

        with open(image_path, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', '<image1>')  # this ID is used in the HTML part
            msg.attach(img)

        # Setting  up the server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

        # Login to the server
        server.login(sender_email, sender_password)

        # Send the email
        try:
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print(f"Email sent successfully to {recipient_email}!")
        except smtplib.SMTPException as e:
            print(f"Failed to send email to {recipient_email}. Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        server.quit()

sender_email = 'ts4235762@gmail.com'
sender_password = 'ypwz xwyj wufc eglc'
recipients = [
    ('dhanshekardharshan@gmail.com', 'Dharshan Dhanashekar'),
    ('Vedanth.balakrishna2001@gmail.com', 'Vedanth Balakrishna'),
    ('terrypoonacha2000@gmail.com', 'Terry')
]
job_role = "Software Engineer"
google_form_link = "https://docs.google.com/forms/d/e/1FAIpQLSdt-jRV3uf0hMh5tvlkdEKE1pTVztmLXfA4ezY-MIAco4CKSw/viewform?vc=0&c=0&w=1&flr=0"
subject_template = 'Job Offer - {recipient_name}'
body_template = """
    Hi {recipient_name},

    Congratulations! We are pleased to inform you that you have been selected for the role of {job_role}.

    To proceed further, kindly fill out the following Google Form with your details and attempt the coding questions:
    {google_form_link}

    If you have any questions, feel free to reach out to us.

    Best regards,
    Hiring Team
"""

image_path = "C:/Users/dhans/Downloads/WhatsApp Image 2024-09-19 at 23.02.58_4dc12f66.jpg"

send_email(sender_email, sender_password, recipients, job_role, google_form_link, subject_template, body_template,image_path)
