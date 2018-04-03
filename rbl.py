import requests
import csv
from bs4 import BeautifulSoup
import re,os

def appendtocsv(row = []):
   	with open("rates_list.csv", "r+") as file:
		for line in file:
			if ','.join([str(x) for x in row]) in line:
				break
		else: # not found, we are at the eof
			file.write(','.join([str(x) for x in row]))

_BANK_NAME = 'RBL Bank'
_BB_URL = 'https://www.bankbazaar.com/fixed-deposit/rbl-bank-fixed-deposit-rate.html'
r = requests.get(_BB_URL)
soup = BeautifulSoup(r.text.encode('utf-8'),"html.parser")
header = ['bank_name','from_period','from_period_d_m_y','from_period_operator','to_period','to_period_d_m_y','to_period_operator','general_roi','senior_roi']
appendtocsv(header)
#for table_row in soup.select("table table table-curved tr"):
for table_row in soup.find('table', attrs={'class':'table table-curved'}).find('tbody').find_all('tr'):
	cells = table_row.findAll('td')
	if len(cells) > 0:
		period_of_deposit = cells[0].text.strip()
		daysfromtore = re.search(r'(\d+) days to (\d+) days',period_of_deposit)
		if daysfromtore:
			each_row = []
			fromdays = daysfromtore.group(1)
			todays = daysfromtore.group(2)
			general_roi = float(cells[1].text.strip())
			senior_roi = float(cells[2].text.strip())
			each_row = [_BANK_NAME,fromdays,'D','GE',todays,'D','LE',general_roi,senior_roi]
			appendtocsv(each_row)
		monthsfromlessthantore = re.search(r'(\d+) months to less than (\d+) months',period_of_deposit)
		if monthsfromlessthantore:
			each_row = []
			frommonths = monthsfromlessthantore.group(1)
			lessthantomonths = monthsfromlessthantore.group(2)
			general_roi = float(cells[1].text.strip())
			senior_roi = float(cells[2].text.strip())
			each_row = [_BANK_NAME,frommonths,'M','GE',lessthantomonths,'M','L',general_roi,senior_roi]
			appendtocsv(each_row)
		monthsfromtore = re.search(r'(\d+) months to (\d+) months',period_of_deposit)
		if monthsfromtore:
			each_row = []
			monthsfrom = monthsfromtore.group(1)
			tomonths = monthsfromtore.group(2)
			general_roi = float(cells[1].text.strip())
			senior_roi = float(cells[2].text.strip())
			each_row = [_BANK_NAME,monthsfrom,'M','GE',tomonths,'M','LE',general_roi,senior_roi]
			appendtocsv(each_row)
