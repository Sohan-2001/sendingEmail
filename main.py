from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/', methods=['GET'])
def send_email():
    try:
        # Get parameters from query
        sender_email = request.args.get('sender_email')
        sender_password = request.args.get('sender_password')
        recipient_email = request.args.get('recipient_email')
        subject = request.args.get('subject')
        message_body = request.args.get('message')

        # Check if all required parameters are provided
        if not all([sender_email, sender_password, recipient_email, subject, message_body]):
            return jsonify({'success': 0, 'error': 'Missing required parameters'})

        # Initialize SMTP connection
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(sender_email, sender_password)

        # Build email message
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg.attach(MIMEText(message_body))

        # Send the email
        smtp.sendmail(from_addr=sender_email, to_addrs=[recipient_email], msg=msg.as_string())

        # Close the SMTP connection
        smtp.quit()

        # Return success response
        return jsonify({'success': 1, 'sent': 1})

    except Exception as e:
        # If any error occurs, return failure response
        return jsonify({'success': 0, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
