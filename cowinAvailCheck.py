import requests
import json
import time
import os
import smtplib, ssl
from email.mime.text import MIMEText
from datetime import date, datetime
from playsound import playsound

today = date.today()
todaysdate = today.strftime("%d-%m-%Y")
# district_id=308 #palakkad 308
# district_id=202 #palakkad 308
district_id=int(input("enter district id - ")) #palakkad 308



intervalTime=20
sender_email=os.environ.get("temp_email_address")
password=os.environ.get("temp_email_password")
receiver_email = os.environ.get("my_email_address")


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def findavailability(centers):
    centerswithavailability=[]
    # i=0
    for center in centers:
        for sessions in center["sessions"]:
            if sessions["available_capacity"] != 0:
                centerswithavailability.append(center)
    return centerswithavailability

def messagetosent(centers):
    
    subject="vaccination slot available"
    message=""
    for center in centers:
        message+="\n "+ center["name"]+ " has::   \n"
        for session in center["sessions"]:
            message+="           ---"+ session["date"] + "(" + str(session["available_capacity"]) + " doses)  \n"
        message+="--------------------------------------\n"
    message+="\n\n this message was sent by anoop through a python script\n"
    return subject,message


def getData(district_id,todaysdate):
    apiurl="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
    parameters={"district_id":district_id,"date":todaysdate}
    header={"Accept-Language": "hi_IN", 'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    
    response = requests.get(url=apiurl,params=parameters,headers=header)
    return response

def sentMail(sender_email, password, receiver_email, subject,message):
    
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"

    msg = MIMEText(message)

    msg['Subject'] = subject
    msg['From'] = "Anoop " + sender_email
    msg['To'] = receiver_email

    



    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("mail sent!")


# sentMail("hello")

if __name__=="__main__":

    while True:
        response = getData(district_id,todaysdate)
        if response.status_code==200:
            print("status code=",response.status_code)
            centers=response.json()["centers"]
            # print("---")
            availableCenters=findavailability(centers)
            if len(availableCenters):
                # jprint(availableCenters)
                print("tadaa!!")
                print(availableCenters)
                subject ,msg = messagetosent(availableCenters)
                sentMail(sender_email, password, receiver_email,subject,msg)
                playsound('sound.mp3')
                quit()

            else:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                # print("Current Time =", current_time)
                print("no available centers at district id = ",district_id," (",current_time,")")
        else:
            print("error: response code= ",response.status_code)
        time.sleep(intervalTime)
