from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

app = Flask(__name__)

@app.route('/', methods=['GET'])
def send_email():
    try:
        email = request.args.get('email')
        message = request.args.get('message')

        if not email or not message:
            return jsonify({'success': 0, 'error': 'Email or message not provided'})

        sender_email = '<email>'
        sender_password = '<forwarding_password>'

        subject = "<subject>"
        to_email = email
        body = message

        # Initialize SMTP connection
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(sender_email, sender_password)

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to_email
        msg.attach(MIMEText(body))

        smtp.sendmail(from_addr=sender_email, to_addrs=[to_email], msg=msg.as_string())

        smtp.quit()

        return jsonify({'success': 1, 'sent': 1})

    except Exception as e:
        return jsonify({'success': 0, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
