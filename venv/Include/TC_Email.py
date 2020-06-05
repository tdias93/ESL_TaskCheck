import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, msg):

    try:
        print('\n################################################## Connecting to Server')
        server = smtplib.SMTP('Outlook.office365.com:587')              # Realiza conexão ao servidor
        server.starttls()                                               # Modo de autenticação TLS
        server.login(email_user, password)                              # Passa parametros de login

        print('################################################## Writing Email')
        message = MIMEMultipart()
        message['Subject'] = subject                                    # Assunto do E-mail
        message['From'] = email_user                                    # E-mail Remetente
        message['To'] = email_send                                      # E-mail Destinatarios
        message.attach(MIMEText(msg, 'plain'))

        print('################################################## Send to Email')
        server.sendmail(email_user, email_send, message.as_string())    # Passa parametros do E-mail
        server.quit()                                                     # Fecha conexão
        
        email_status = 'Successful Email'
        email_error = ''
        return [email_status, email_error]

    except Exception as error:
        print(f'################################################## Error: {error}')

        email_status = 'Unsuccessful Email'
        email_error = error
        return [email_status, email_error]

email_user = 'thiago.dias@brsamor.com.br'
email_send = 'thiago.olimpio93@gmail.com'
password = ''   # Senha do E-mail
