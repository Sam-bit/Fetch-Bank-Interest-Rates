import datetime
import re

import requests
from bs4 import BeautifulSoup
class RBLInterest:
	rates_file_name = "rates_list.csv"
	_BANK_NAME = 'RBL Bank'
	_BANK_URL = 'https://www.rblbank.com/interest-rates'
	def __init__(self,rates_file_name):
		self.rates_file_name = rates_file_name
	def get_date(self,string):
		A = re.search(r'(\S+\s\d{2}[,]\s\d{4})', string)
		if A:
			a = A.group(1)
			return datetime.datetime.strptime(a, "%B %d, %Y").strftime("%d-%m-%Y")
	def parse_amount(self,amountText):
		amountText = amountText.replace('*','').replace('\xa0',' ').replace('  ',' ')
		A = re.search(r'Upto INR (\d+\.*\d+) lakh', amountText) or re.search(r'Upto INR (\d+) lakh', amountText)
		if A:
			b = float(A.group(1)) * 100000
			return 1,b
		B = re.search(r'Above INR (\d+\.*\d+) lakh upto INR (\d+\.*\d+) lakh', amountText) or re.search(r'Above INR (\d+) lakh upto INR (\d+) lakh', amountText)
		if B:
			a = float(B.group(1)) * 100000 + 1
			b = float(B.group(2)) * 100000
			return a,b
		C = re.search(r'Above INR (\d+\.*\d+) lakh upto INR (\d+\.*\d+) Crore', amountText) or re.search(r'Above INR (\d+) lakh upto INR (\d+) Crore', amountText)
		if C:
			a = float(C.group(1)) * 100000 + 1
			b = float(C.group(2)) * 10000000
			return a, b
		D = re.search(r'Above INR (\d+\.*\d+) Crore and upto INR (\d+\.*\d+) Crore', amountText) or re.search(r'Above INR (\d+) Crore and upto INR (\d+) Crore', amountText)
		if D:
			a = float(D.group(1)) * 10000000 + 1
			b = float(D.group(2)) * 10000000
			return a, b
		E = re.search(r'Above INR (\d+\.*\d+) Crore', amountText) or re.search(r'Above INR (\d+) Crore', amountText)
		if E:
			a = float(E.group(1)) * 10000000 + 1
			b = 999999999999999
			return a, b
		F = re.search(r'Above INR (\d+\.*\d+) lakh and upto INR (\d+\.*\d+) Crore', amountText) or re.search(r'Above INR (\d+) lakh and upto INR (\d+) Crore', amountText)
		if F:
			a = float(F.group(1)) * 100000 + 1
			b = float(F.group(2)) * 10000000
			return a, b

	def appendtocsv(self, row=None):
		if row is None:
			row = []
		open(self.rates_file_name, 'a').close()
		with open(self.rates_file_name, "r+", newline='\n') as file:
			for line in file:
				if ','.join([str(x) for x in row]) in line:
					break
			else:  # not found, we are at the eof
				file.write(','.join([str(x).replace('\u200b', '') for x in row]))
				file.write('\n')
	def start(self):
		r = requests.get(self._BANK_URL)
		soup = BeautifulSoup(r.text.encode('utf-8'),"html.parser")
		header = ['bank_name', 'old_or_new', 'deposit', 'deposit_name', 'from_year', 'from_period', 'from_period_d_m_y',
				  'from_period_operator',
				  'to_year', 'to_period', 'to_period_d_m_y', 'to_period_operator', 'min_amount', 'max_amount',
				  'premature_y_n',
				  'general_roi', 'senior_roi']
		self.appendtocsv(header)
		num_tables = 1
		deposit_type = {
			1: 'SB',
			2: 'FD',
			3: 'FD',
			4: 'RD',
			5: 'FCNR(B) / RFC',
			6: 'MCLR',
		}
		premature_y_n = {
			1:'Y',
			2:'Y',
			3:'N',
			4:'N'
		}
		tables = soup.find_all('div',class_='i-rate-outer-card')
		deposit_type_name= 'SB'
		premature_y_n_name = 'N'
		from_year = self.get_date(tables[0].find_all('div')[0].text)
		print(from_year)
		sb_table = tables[0].find_all('div')[1]
		all_trs = sb_table.find('table').find('tbody').find_all('tr')
		old_end_date = self.get_date(all_trs[0].find_all('th')[1].text)
		print(old_end_date)
		for tr in all_trs[1:]:
			min_amount,max_amount = self.parse_amount(tr.find_all('td')[0].text)
			old_roi = tr.find_all('td')[1].text.replace('%','')
			new_roi =tr.find_all('td')[2].text.replace('%','')
			each_row = [self._BANK_NAME, 'OLD', deposit_type_name, 'Savings Account', '', '',
						'',
						'', old_end_date,
						'', '',
						'LE', min_amount, max_amount, premature_y_n_name, old_roi, old_roi]
			self.appendtocsv(each_row)
			each_row = [self._BANK_NAME, 'NEW', 'RD', 'Regular Recurring Deposit', from_year, '',
						'',
						'GE', '',
						'', '',
						'', min_amount, max_amount, premature_y_n_name, new_roi, new_roi]
			self.appendtocsv(each_row)