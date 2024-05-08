import smtplib
# SMTP server configuration
smtp_server = 'smtp.office365.com'
smtp_port = 587
sender_email = 'notreplystockpredict@outlook.com'
password = 'Noreplypmpatel1@'  # Use your Gmail password or App Password

# Create a SMTP connection
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()  # Enable TLS encryption
server.login(sender_email, password)

# Test sending an email
recipient_email = 'dakij50927@mcuma.com'
message = 'Subject: Test Email\n\nThis is a test email from Python.'
server.sendmail(sender_email, recipient_email, message)

# Close the SMTP connection
server.quit()