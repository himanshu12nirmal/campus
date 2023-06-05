"""import cv2
import xlsxwriter
import sqlite3
from sqlite3 import Error

wordbook = xlsxwriter.Workbook('Attendance.xlsx')

worksheet = wordbook.add_worksheet()
attendence = list()
names = list()
cap = cv2.VideoCapture(0)
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()
DB_PATH = r'/media/himanshu/My Passport/sem-5-project/campuscard/db.sqlite3'

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
    except Error as e:
        print(e)
    return conn

def select_all_task(conn,enroll):
    cur = conn.cursor()
    cur.execute("Select name from Student where enrollment="+str(enroll))
    rows = cur.fetchall()
    return rows
        
def select_all_course(conn):
    cur = conn.cursor()
    cur.execute("Select subject from Course")
    rows = cur.fetchall()
    return rows

conn =create_connection()

while True:
    _, img = cap.read()
    
        # detect and decode
    data, bbox, _ = detector.detectAndDecode(img)
    # check if there is a QRCode in the image
    if data:
        a=data
        rows = select_all_task(conn,str(a))
        if len(rows) != 0:
            attendence.append(str(a))
            names.append(rows[0][0])
        else:
            print("Student with that enrollment doesnt present")
    cv2.imshow("QRCODEscanner", img)
    if cv2.waitKey(1) == ord("q"):
        break

row = 0
column = 0
attendence = set(attendence)
names = set(names)
for item in attendence:
    worksheet.write(row,column,item)
    row +=1
    
row = 0
column = 1
for item in names:
    worksheet.write(row,column,item)
    row +=1
wordbook.close()
print("Data is written")
cap.release()
cv2.destroyAllWindows
"""

import urllib3, urllib
mydata=[('name','1'),('two','2')]    #The first is the var name the second is the value
mydata=urllib.urlencode(mydata)
path='https://mycampuscard.000webhostapp.com/phpFile.php'    #the url you want to POST to
req=urllib2.Request(path, mydata)
req.add_header("Content-type", "application/x-www-form-urlencoded")
page=urllib2.urlopen(req).read()
print (page)
