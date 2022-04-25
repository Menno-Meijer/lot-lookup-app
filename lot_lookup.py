from bs4 import BeautifulSoup
import requests
from datetime import datetime

lot = ""

def singlelot_lookup(lot):
    url = "https://www.biolegend.com/Default.aspx?ID=18921&action=Detail"
    post_params = {"Coa.LotId": lot}
    response = requests.post(url, data=post_params)
    soup = BeautifulSoup(response.text, "html.parser")
    soup_tr = soup.find_all("tr")
    exp_date = ""
    for i in soup_tr:
        if "Expiration Date:" in i.get_text():
            exp_date = i.find_all("td")[1].get_text().strip()
    try:
        exp_date = datetime.strptime(exp_date, "%B %d, %Y").date()
    except:
        exp_date = ""
    return exp_date
