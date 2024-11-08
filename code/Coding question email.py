import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def send_email(sender_email, sender_password, recipients, job_role, google_form_link):
    subject_template = 'Job Offer - {recipient_name}'
    body_template = """
        Hi {recipient_name},

        We are pleased to provide you with the Google Colab link for the coding questions for the role of {job_role}.

        Please access the link below to complete the coding questions:
        {google_form_link}

        If you have any questions, feel free to reach out to us.

        Best regards,
        Hiring Team
        """

    for recipient_email, recipient_name in recipients:
        msg = MIMEMultipart()
        msg['From'] = sender_email

        subject = subject_template.format(recipient_name=recipient_name)
        msg['Subject'] = subject

        body = body_template.format(recipient_name=recipient_name, job_role=job_role, google_form_link=google_form_link)
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        #server.starttls()  # Secure the connection

        server.login(sender_email, sender_password)

        # Send the email
        msg['To'] = recipient_email
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
    ('Vedanth.balakrishna2001@gmail.com', 'Vedanth Balakrishna')
]
job_role = "Software Engineer"
colab_link = "https://colab.research.google.com/drive/1zg8SHj68WO0LdCI1xCWkyOjSvDkPmMKA?usp=sharing"

send_email(sender_email, sender_password, recipients, job_role, colab_link)
