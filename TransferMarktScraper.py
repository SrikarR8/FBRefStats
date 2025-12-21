# ⚠️⚠️⚠️ Disclaimer & Ethics
# This project is for **educational purposes only**. 
# **Usage:** I do not encourage or condone the mass scraping of Transfermarkt. Please respect their `robots.txt` and Terms of Service. (https://www.transfermarkt.us/intern/anb)
# **Responsibility:** The author is not responsible for any misuse of this software or any bans incurred by the user. 
# **Throttling:** This script includes built-in `time.sleep()` delays to avoid over-burdening the Transfermarkt servers.

import requests
from bs4 import BeautifulSoup
import time
import random

def enterData(start, end):
    url = ""
    #Use as necessary
    headers = {} 
    start_year = start
    end_year = end
    players = []
    
    for year in range(start_year, end_year):

        print(f"Scraping year: {year}") 
        #Make request for Premier League Transfers
        url = f"https://www.transfermarkt.us/premier-league/transfers/wettbewerb/GB1/plus/?saison_id={year}&s_w=&leihe=1&intern=0&intern=1"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        #Code for scraping
        #Club: show which club has bought or sold (to be used with direction): trFrom
        #Direction: has value of either "Left" or "Joined", used in conjunction with Club
        mydivs = soup.find_all("div", {"class": "box"})
        for div in mydivs:
            table = (div.find_all('table'))

            for t in table:
                direction = "Transfer"
                header_th = t.find('th', {"class": "verein-transfer-cell"})
                if header_th:
                    direction = header_th.text.strip()
                
                if not t.tbody:
                    continue
                    
                tb = (t.tbody)

                for tr in tb.find_all('tr'):

                    trFrom = "Unknown"
                    trVal = "0"
                    trFee = "0"
                    
                    td = (tr.find_all('td', {"class": "rechts"}))
                    tdClub = tr.find_all('td', {"class": "no-border-links verein-flagge-transfer-cell"})
                    
                    if(len(tdClub) > 0):
                        trFrom = (tdClub[0].text)
                    if (len(td) > 0):
                        trVal = (td[0].text)
                        trFee = (td[1].text)

                        for td_cell in tr.find_all('td'):
                            if(td_cell.div):
                                trDiv = (td_cell.div)

                                row_string = f'"{trDiv.text.strip()}","{trVal.strip()}","{trFee.strip()}","{trFrom.strip()}","{direction}"'
                                players.append(row_string)

        time.sleep(random.uniform(2, 5)) 

    return players


#Use start year of starting season and end date of ending season
#Example for 2017-18 to 2025-26
playersArr = enterData(2017, 2026)

file_name = 'data_output.csv'


with open(file_name, 'w', encoding='utf-8') as f:
    f.write('Name,Value,Fee,Club,Direction\n')
    for player in playersArr:
        f.write(player + '\n')

print(f"Successfully saved {len(playersArr)} rows to {file_name}")
