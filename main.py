#!/usr/bin/python3

import os
import smtplib

EMAIL_ADDRESS='thivankanimshan@gmail.com'
EMAIL_PASSWORD='cefrqvpfymzmogii'

with smtplib.SMTP('smtp.gmail.com',587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)

    subject='Grab dinner this weekend'
    body='How about dinner at 6pm this Saturday'

    msg=f'Subject: {subject}\n\n{body}'

    smtp.sendmail(EMAIL_ADDRESS,'thivankanimesh@hotmail.com',msg)