import requests
import json
import time
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def findavailability(centers):
    centerswithavailability={}
    i=0
    for center in centers:
        for sessions in center["sessions"]:
            if sessions["available_capacity"] != 0:
                centerswithavailability[i]=center
                i+=1
    return centerswithavailability

def alertuser():
    pass


def getData():
    apiurl="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
    parameters={"district_id":308,"date":"7-05-2021"}
    header={"Accept-Language": "hi_IN", 'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    
    response = requests.get(url=apiurl,params=parameters,headers=header)
    return response

if __name__=="__main__":
    while True:
        response = getData()
        if response.status_code==200:
            print("good")
            centers=response.json()["centers"]
            print("---")
            availableCenters=findavailability(centers)
            if availableCenters:
                jprint(availableCenters)
                print("tadaa!!")
                alertuser()
            else:
                print("no available centers")
        time.sleep(10)