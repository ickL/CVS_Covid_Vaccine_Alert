import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import winsound
address = "https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status.MD.json?vaccineinfo?" ##change state to select appropriate file, or remove state to get all states. CVS could change access to this/file structure at any time.
URL = address

fullLog = pd.DataFrame()
i = True
while i == True:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    dictSoup = eval(soup.text.replace('true',"True").replace('false',"False"))
    Table = dictSoup['responsePayloadData']['data']['MD']
    df = pd.DataFrame(Table)
    df['DateTime'] = dictSoup['responsePayloadData']['currentTime']
    if len(df[df['status'] != "Fully Booked"]) > 0:
        print(df)
        winsound.Beep(400, 5000)
    else:
        print("Fully Booked - Last Updated - " + str(dictSoup['responsePayloadData']['currentTime']))
    fullLog = fullLog.append(df).drop_duplicates(subset=["city","DateTime"]).reset_index(drop=True)
    #fullLog.to_csv("C:\VaccineOpening.csv", index=False) ##if you want to see how it evolves over time (in 15 min increments)
    time.sleep(120) ##while CVS updates their site every 15 minutes, having this at a higher sampling rate will make sure you don't miss any change in updates
