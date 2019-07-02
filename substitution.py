import re
import os

f = open('original.py','r+')
g = open('temp.py','w')

for i in f:
    i=re.sub('thivankanimesh@hotmail.com','abc',i)
    g.write(i)

os.remove('original.py')
os.rename('temp.py','original.py')

f = open('original.py','r+')
g = open('temp.py','w')

for i in f:
    i=re.sub('mouse_click_events=False','mouse_click_events=True',i)
    g.write(i)

os.remove('original.py')
os.rename('temp.py','original.py')
