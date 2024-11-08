import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def send_email(sender_email, sender_password, recipient_email, recipient_name, job_role, is_selected, subject, body_template):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # To determine the body of the email based on the selection status
    if is_selected:
        body = body_template.format(recipient_name=recipient_name, job_role=job_role)
    else:
        body = f"""
            Hi {recipient_name},

            Thank you for applying for the role of {job_role}. We appreciate your interest in our company.

            Unfortunately, we regret to inform you that you have not been selected for the position.

            Best regards,
            Hiring Team
            """

    # Attach the body of the email
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        #server.starttls()  # Secure the connection

        # Login to the server
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipient_email,msg.as_string())
        print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Failed to send email. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:

        server.quit()

sender_email = 'ts4235762@gmail.com'
sender_password = 'ypwz xwyj wufc eglc'
recipient_email = 'dhanshekardharshan@gmail.com'
recipient_name = 'Terry'
job_role = "Software Engineer"
subject = 'Job Application Update'

# Selected candidate
is_selected = False
body_template = """
    Hi {recipient_name},

    Congratulations! We are pleased to inform you that you have been selected for the role of {job_role}.


    If you have any questions, feel free to reach out to us.

    Best regards,
    Hiring Team
    """

send_email(sender_email, sender_password, recipient_email, recipient_name, job_role, is_selected, subject, body_template)

# Not selected candidate
is_selected = True
send_email(sender_email, sender_password, recipient_email, recipient_name, job_role, is_selected, subject, "")
