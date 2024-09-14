import requests
import csv
from bs4 import BeautifulSoup
import re,os
class RBLInterest:
	rates_file_name = "rates_list.csv"
	_BANK_NAME = 'RBL Bank'
	_BANK_URL = 'https://www.rblbank.com/interest-rates'
	def __init__(self,rates_file_name):
		self.rates_file_name = rates_file_name

	def appendtocsv(self,row):
		with open(self.rates_file_name, "r+") as file:
			for line in file:
				if ','.join([str(x) for x in row]) in line:
					break
			else: # not found, we are at the eof
				file.write(','.join([str(x) for x in row]))
	def start(self):
		r = requests.get(self._BANK_URL)
		soup = BeautifulSoup(r.text.encode('utf-8'),"html.parser")
		header = ['bank_name', 'old_or_new', 'deposit', 'deposit_name', 'from_year', 'from_period', 'from_period_d_m_y',
				  'from_period_operator',
				  'to_year', 'to_period', 'to_period_d_m_y', 'to_period_operator', 'min_amount', 'max_amount',
				  'premature_y_n',
				  'general_roi', 'senior_roi']
		self.appendtocsv(header)
