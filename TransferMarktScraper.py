# ⚠️⚠️⚠️ Disclaimer & Ethics
# This project is for **educational purposes only**. 
# **Usage:** I do not encourage or condone the mass scraping of Transfermarkt. Please respect their `robots.txt` and Terms of Service. (https://www.transfermarkt.us/intern/anb)
# **Responsibility:** The author is not responsible for any misuse of this software or any bans incurred by the user. 
# **Throttling:** This script includes built-in `time.sleep()` delays to avoid over-burdening the Transfermarkt servers.
import requests
from bs4 import BeautifulSoup
import time
import random

def printDataByYear(start, end,inputUrl,LeagueName):
    url = ""
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"}
    start_year = start
    end_year = end
    players = []
    
    for year in range(start_year, end_year):

        print(f"Scraping year: {year} for {LeagueName}") 
        
        url = f"{inputUrl}{year}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
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

def enterDataByLeague(startYr,endYr,URL,LeagueName):

    playersArr = printDataByYear(startYr, endYr,URL,LeagueName)

    file_name = f"{LeagueName}.csv"

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write('Name,Value,Fee,From,Direction\n')
        for player in playersArr:
            f.write(player + '\n')

    print(f"Successfully saved {len(playersArr)} rows to {file_name}")


engTransfers = "https://www.transfermarkt.us/premier-league/transfers/wettbewerb/GB1/plus/?saison_id="
spnTransfers = "https://www.transfermarkt.us/laliga/transfers/wettbewerb/ES1/plus/?saison_id="
itlTransfers = "https://www.transfermarkt.us/serie-a/transfers/wettbewerb/IT1/saison_id/"
gerTransfers = "https://www.transfermarkt.us/bundesliga/transfers/wettbewerb/L1/plus/?saison_id="
fraTransfers = "https://www.transfermarkt.us/ligue-1/transfers/wettbewerb/FR1/plus/?saison_id="

# 2017-18 to 2025-26
enterDataByLeague(2017,2026,engTransfers,"England")
enterDataByLeague(2017,2026,spnTransfers,"Spain")
enterDataByLeague(2017,2026,itlTransfers,"Italy")
enterDataByLeague(2017,2026,gerTransfers,"Germany")
enterDataByLeague(2017,2026,fraTransfers,"France")


