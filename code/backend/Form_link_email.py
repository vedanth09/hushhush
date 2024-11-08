import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
 
def send_email(sender_email, sender_password, recipient_email, recipient_name, job_role, google_form_link, image_path):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    subject = f'Job Offer at Doodle'
    msg['Subject'] = subject
 
    # Create the body of the email with HTML
    html_body = f"""
<html>
<body>
<p>Dear Candidate,</p>
<p>We are excited to inform you that you have been selected for the next phase of the recruitment process at Doodle. Congratulations on reaching this milestone!</p>
<p>The next steps of the recruitment process will be attempting a coding challenge for the time you have specified in the google form.</p>
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
 
    # Setting up the server
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
    finally:
        server.quit()