from email.message import EmailMessage
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import os

class my_email:
    def __init__(self, receivers_txt="qqemail/receivers.txt", password_txt="qqemail/qq_email_password.txt"):
        self.sender = '939635003@qq.com'
        self.smtpSev = 'smtp.qq.com'
        self.password = self.__read_txt(password_txt)
        self.receivers = self.__read_txt(receivers_txt)

    def __read_txt(self, txt_path):
        assert os.path.exists(txt_path), "[ERROR] can not find {}".format(txt_path)
        with open(txt_path) as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
        if len(lines) == 1:
            return lines[0]
        else:
            return lines 

    def sendmail(self, theme, content, To="You", From="Qingren", image_path=None):
        messageRoot = MIMEMultipart('related')
        messageRoot['Subject'] = Header(theme, 'utf-8')
        messageRoot['From'] = Header(From, 'utf-8')
        messageRoot['To'] = Header(To, 'utf-8')

        messageAlternative = MIMEMultipart('alternative')
        messageRoot.attach(messageAlternative)
        
        suffix = """
        <p><img src="cid:image1" width=300></p>"""
        message = MIMEText(content + suffix, 'html', 'utf-8')
        messageAlternative.attach(message)

        if image_path != None:
            fp = open(image_path, 'rb')
            msgImg = MIMEImage(fp.read())
            fp.close()
        
            msgImg.add_header('Content-ID', '<image1>')
            messageRoot.attach(msgImg)

        try:
            smtpObj = smtplib.SMTP_SSL(self.smtpSev)
            smtpObj.connect(self.smtpSev, 465)
            smtpObj.login(self.sender, self.password)
            smtpObj.sendmail(from_addr=self.sender, to_addrs=self.receivers, msg=messageRoot.as_string())
            print("Successful sending ...")
        except smtplib.SMTPException as e:
            print(e)
        finally:
            smtpObj.quit()
