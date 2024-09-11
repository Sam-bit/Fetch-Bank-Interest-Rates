import json

import requests
import csv
from bs4 import BeautifulSoup
import re, os
import datetime


refresh = True
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0'}

def parse_tenure(tenureText=None):
    print(tenureText)
    A = re.search(r'(\d+) to (\d+) Days', tenureText)
    if A:
        a = A.group(1)
        b = A.group(2)
        return a, 'D', 'GE', b, 'D', 'LE'
    B = re.search(r'(\d+) Days to < (\d+) Year', tenureText)
    if B:
        a =B.group(1)
        b = B.group(2)
        return a, 'D', 'GE', b, 'Y', 'LT'
    C =  re.search(r'(\d+) Year to < (\d+) Months', tenureText)
    if C:
        a =C.group(1)
        b = C.group(2)
        return a, 'Y', 'GE', b, 'M', 'LT'
    D = re.search(r'(\d+) Months to < (\d+) Months', tenureText)
    if D:
        a = D.group(1)
        b = D.group(2)
        return a, 'M', 'GE', b, 'M', 'LT'
    E = re.search(r'(\d+) Months to (\d+) Years', tenureText)
    if E:
        a = E.group(1)
        b = E.group(2)
        return a, 'M', 'GE', b, 'Y', 'LE'
    F = re.search(r'(\d+) Years 1 Day to (\d+) Years', tenureText)
    if F:
        a = F.group(1)
        b = F.group(2)
        return a, 'Y', 'GT', b, 'Y', 'LE'
    G = re.search(r'(\d+)Y \(Tax Saver FD\)', tenureText)
    if G:
        a = G.group(1)
        return a, 'Y', 'GE', a, 'Y', 'LE'
    H = re.search(r'(\d+) Year to (\d+) Days', tenureText)
    if H:
        a = H.group(1)
        b = H.group(2)
        return a, 'Y', 'GE', b, 'D', 'LE'
    I = re.search(r'(\d+) Days to < (\d+) Months', tenureText)
    if I:
        a = I.group(1)
        b = I.group(2)
        return a, 'D', 'GE', b, 'M', 'LT'
    J = re.search(r'(\d+) Days to (\d+) Days', tenureText)
    if J:
        a = J.group(1)
        b = J.group(2)
        return a, 'D', 'GE', b, 'D', 'LE'
    K = re.search(r'(\d+) months', tenureText)
    if K:
        a = K.group(1)
        return a, 'M', 'GE', a, 'M', 'LE'
    L = re.search(r'Above (\d+) years upto (\d+) years', tenureText)
    if L:
        a = L.group(1)
        b = L.group(2)
        return a, 'Y', 'GE', b, 'Y', 'LT'
def get_roi(text_value):
    return float((text_value.split(" (")[0] if "(" in text_value else text_value).replace('\u200b', ''))

def removeComments(string):
    string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string) # remove all occurrences streamed comments (/*COMMENT */) from string
    string = re.sub(re.compile("//.*?\n" ) ,"" ,string) # remove all occurrence single-line comments (//COMMENT\n ) from string
    string = re.sub(r'(\w+):', r'"\1":', string) # Fix unquoted keys (convert them to quoted keys)
    return string
def appendtocsv(row=None):
    if row is None:
        row = []
    open("rates_list.csv", 'a').close()
    with open("rates_list.csv", "r+", newline='\n') as file:
        for line in file:
            if ','.join([str(x) for x in row]) in line:
                break
        else:  # not found, we are at the eof
            file.write(','.join([str(x).replace('\u200b', '') for x in row]))
            file.write('\n')

import ast
_BANK_NAME = 'ICICI'
if refresh:
    open("rates_list.csv", 'w').close()
header = ['bank_name', 'old_or_new', 'deposit', 'deposit_name', 'from_year', 'from_period', 'from_period_d_m_y',
          'from_period_operator',
          'to_year', 'to_period', 'to_period_d_m_y', 'to_period_operator', 'min_amount', 'max_amount', 'premature_y_n',
          'general_roi', 'senior_roi']
appendtocsv(header)

_senior_rate_inc =0
_BANK_FD_URL ='https://www.icicibank.com/personal-banking/deposits/fixed-deposit/fd-interest-rates'
r = requests.get(_BANK_FD_URL,headers=headers)
soup = BeautifulSoup(r.text.encode('utf-8'), "html.parser")
effectDate = soup.find("div",class_ = "interest-rates").find('h2').text.replace('FD Interest Rate for General and Senior Citizens(w.e.f. from ','').replace(')','')
from_year = datetime.datetime.strptime(effectDate, "%b %d, %Y").strftime("%d-%m-%Y")
_INTEREST_FD_URL = 'https://www.icicibank.com/content/dam/icicibank/india/managed-assets/revamp-pages/fixed-deposits-all-pages/script/retail-new-data.js'
r = requests.get(_INTEREST_FD_URL,headers=headers)
filetext = removeComments(r.text).replace('\t','').replace('  ','').replace('\n','').replace('\r','').replace("'", '"')
interestre = re.findall(r'interestData = .*];', filetext,flags=re.MULTILINE)
interestData = interestre[0].replace('interestData = ','').replace(';','')
numList = 1
interestDataDict = None
try:
    interestDataDict = ast.literal_eval(interestData)
except Exception as e:
    print(f"Error during conversion: {e}")
if interestDataDict is not None:
    for inner_list in interestDataDict:
        for entry in inner_list:
            values = list(entry.values())
            amount_ranges = {
                1: (10000, 30000000),
                2: (30000000, 50000000),
                3: (50000000, 51000000),
                4: (51000000, 249000000),
                5: (249000000, 250000000),
                6: (250000000, 1000000000),
                7: (1000000000, 2500000000),
                8: (2500000000, 5000000000),
                9: (5000000000, 9999999999999)
            }

            if numList in amount_ranges:
                min_amount, max_amount = amount_ranges[numList]
            else:
                min_amount,max_amount = 0,0
            from_period, from_period_d_m_y,from_period_operator,to_period, to_period_d_m_y,to_period_operator = parse_tenure(values[0])
            if max_amount == 30000000 and from_period == 15 and to_period == 18 and from_period_d_m_y == 'M' and to_period_d_m_y == 'M':
                _senior_rate_inc = 0.55
            each_row = [_BANK_NAME, 'NEW', 'FD', 'Regular Fixed Deposit', from_year, from_period, from_period_d_m_y, from_period_operator, '',
                        to_period, to_period_d_m_y,
                        to_period_operator, min_amount, max_amount, 'Y', values[1], float(values[1]) + float(_senior_rate_inc)]
            appendtocsv(each_row)
            each_row = [_BANK_NAME, 'NEW', 'FD', 'Regular Fixed Deposit', from_year, from_period, from_period_d_m_y, from_period_operator, '',
                        to_period, to_period_d_m_y,
                        to_period_operator, min_amount, max_amount, 'Y', values[2], float(values[2]) + float(_senior_rate_inc)]
            appendtocsv(each_row)
            each_row = [_BANK_NAME, 'NEW', 'FD', 'Regular Fixed Deposit', from_year, from_period, from_period_d_m_y, from_period_operator, '',
                        to_period, to_period_d_m_y,
                        to_period_operator, min_amount, max_amount, 'N', values[3], float(values[3]) + float(_senior_rate_inc)]
            appendtocsv(each_row)
            each_row = [_BANK_NAME, 'NEW', 'FD', 'Regular Fixed Deposit', from_year, from_period, from_period_d_m_y, from_period_operator, '',
                        to_period, to_period_d_m_y,
                        to_period_operator, min_amount, max_amount, 'N', values[4], float(values[4]) + float(_senior_rate_inc)]
            appendtocsv(each_row)
        numList+=1
_BANK_RD_URL = 'https://www.icicibank.com/personal-banking/deposits/recurring-deposits/rd-interest-rate'
r = requests.get(_BANK_RD_URL,headers=headers)
soup = BeautifulSoup(r.text.encode('utf-8'), "html.parser")
tablediv = soup.find('div',class_= 'accordion-content').find('table')
effectDate = tablediv.find('thead').find('tr').find_all('th')[1].find('b').text
from_year = datetime.datetime.strptime(effectDate, "%d %B, %Y").strftime("%d-%m-%Y")
all_trs = tablediv.find('tbody').find_all('tr')
for tr in all_trs:
    from_period, from_period_d_m_y,from_period_operator,to_period, to_period_d_m_y,to_period_operator = parse_tenure(tr.find_all('td')[0].text)
    generalroi = tr.find_all('td')[1].text.replace("%","")
    seniorroi = tr.find_all('td')[2].text.replace("%","")
    each_row = [_BANK_NAME, 'NEW', 'RD', 'Regular Recurring Deposit', from_year, from_period, from_period_d_m_y,
                from_period_operator, '',
                to_period, to_period_d_m_y,
                to_period_operator, 500, 1000000, 'N', generalroi, seniorroi]
    appendtocsv(each_row)