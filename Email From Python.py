import smtplib
from email.mime.text import MIMEText

email_address = 'username@email.com'
password = 'password'

#Without CC
def simple_email (from_email, recipients_CC, subject, message):  

  msg = MIMEText(message,'html')
  msg['To'] = ", ".join(recipients_CC)
  msg['Subject'] = subject
  msg['From'] = from_email
  header  = 'From: %s\n' % from_email
  header += 'To: %s\n' % msg.get('To')
  header += 'Subject: %s\n' % subject
  message = header + message

  try:
      smtpObj = smtplib.SMTP('smtp.office365.com', 587)
  except Exception as e:
      print(e)
      smtpObj = smtplib.SMTP_SSL('smtp.office365.com', 465)
  smtpObj.ehlo()
  smtpObj.starttls()
  smtpObj.login(email_address, password)
  smtpObj.sendmail(from_email, recipients_CC, msg.as_string())
  smtpObj.quit()

#With CC
def simple_email_cc (from_email, recipients, recipients_CC, subject, message):  

  msg = MIMEText(message,'html')
  msg['To'] = ", ".join(recipients)
  msg['CC'] = ", ".join(recipients_CC)
  msg['Subject'] = subject
  msg['From'] = from_email
  header  = 'From: %s\n' % from_email
  header += 'To: %s\n' % msg.get('To')
  header += 'CC: %s\n' % msg.get('CC')
  header += 'Subject: %s\n' % subject
  message = header + message

  to_email_all = recipients + recipients_CC

  try:
      smtpObj = smtplib.SMTP('smtp.office365.com', 587)
  except Exception as e:
      print(e)
      smtpObj = smtplib.SMTP_SSL('smtp.office365.com', 465)
  smtpObj.ehlo()
  smtpObj.starttls()
  smtpObj.login(email_address, password)
  smtpObj.sendmail(from_email, to_email_all, msg.as_string())
  smtpObj.quit()
