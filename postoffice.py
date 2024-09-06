import requests
import csv
from bs4 import BeautifulSoup
import re, os

refresh = True


def get_roi(text_value):
    return text_value.split(" (")[0] if "(" in text_value else text_value


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


_BANK_NAME = 'Post Office'
_BANK_URL = 'https://www.indiapost.gov.in/Financial/pages/content/post-office-saving-schemes.aspx'
r = requests.get(_BANK_URL)
soup = BeautifulSoup(r.text.encode('utf-8'), "html.parser")
_senior_rate_inc = "0.25"
if refresh:
    open("rates_list.csv", 'w').close()
header = ['bank_name', 'old_or_new', 'deposit','deposit_name', 'from_year', 'from_period', 'from_period_d_m_y', 'from_period_operator',
          'to_year', 'to_period', 'to_period_d_m_y', 'to_period_operator', 'general_roi', 'senior_roi']
appendtocsv(header)
old_or_new = 'OLD'
all_tables = soup.find("div", attrs={"id": "tab6", "class": "tabContent"}).find_all("table")
table = all_tables[0]
for tr in table.find_all("tr")[1:]:
    from_year = tr.find_all('td')[0].text
    to_year = tr.find_all('td')[1].text
    general_roi = tr.find_all('td')[2].text
    each_row = [_BANK_NAME, old_or_new, 'SB','Post Office Savings Account', from_year, '', '', 'GE', to_year, '', '', 'LE', general_roi,
                float(general_roi) + float(_senior_rate_inc)]
    appendtocsv(each_row)
table = all_tables[1]
for tr in table.find_all("tr")[1:]:
    from_year = tr.find_all('td')[0].text
    to_year = tr.find_all('td')[1].text
    general_roi = get_roi(tr.find_all('td')[2].text)
    each_row = [_BANK_NAME, old_or_new, 'RD', 'National Savings Recurring Deposit Account',from_year, '', '', 'GE', to_year, '', '', 'LE', general_roi,
                float(general_roi) + float(_senior_rate_inc)]
    appendtocsv(each_row)
table = all_tables[2]
for tr in table.find_all("tr")[1:]:
    from_year = tr.find_all('td')[0].text
    to_year = tr.find_all('td')[1].text
    general_roi_1 = get_roi(tr.find_all('td')[2].text)
    general_roi_2 = get_roi(tr.find_all('td')[3].text)
    general_roi_3 = get_roi(tr.find_all('td')[4].text)
    general_roi_5 = get_roi(tr.find_all('td')[5].text)
    each_row = [_BANK_NAME, old_or_new, 'TD', 'National Savings Time Deposit Account',from_year, '', '', 'GE', to_year, '', '', 'LE', general_roi_1,
                float(general_roi_1) + float(_senior_rate_inc)]
    appendtocsv(each_row)
    each_row = [_BANK_NAME, old_or_new, 'TD', 'National Savings Time Deposit Account',from_year, '', '', 'GE', to_year, '', '', 'LE', general_roi_2,
                float(general_roi_2) + float(_senior_rate_inc)]
    appendtocsv(each_row)
    each_row = [_BANK_NAME, old_or_new, 'TD', 'National Savings Time Deposit Account',from_year, '', '', 'GE', to_year, '', '', 'LE', general_roi_3,
                float(general_roi_3) + float(_senior_rate_inc)]
    appendtocsv(each_row)
    each_row = [_BANK_NAME, old_or_new, 'TD', 'National Savings Time Deposit Account',from_year, '', '', 'GE', to_year, '', '', 'LE', general_roi_5,
                float(general_roi_5) + float(_senior_rate_inc)]
    appendtocsv(each_row)
table = all_tables[3]
for tr in table.find_all("tr")[1:]:
    from_year = tr.find_all('td')[0].text
    to_year = tr.find_all('td')[1].text
    general_roi = get_roi(tr.find_all('td')[2].text)
    each_row = [_BANK_NAME, old_or_new, 'MIS', 'National Savings Monthly Income Account',from_year, '', '', 'GE', to_year, '', '', 'LE', general_roi,
                float(general_roi) + float(_senior_rate_inc)]
    appendtocsv(each_row)
table = all_tables[4]
for tr in table.find_all("tr")[1:]:
    from_year = tr.find_all('td')[0].text
    to_year = tr.find_all('td')[1].text
    general_roi = get_roi(tr.find_all('td')[2].text)
    each_row = [_BANK_NAME, old_or_new, 'SCSS', 'Senior Citizens Savings Scheme Account',from_year, '', '', 'GE', to_year, '', '', 'LE', general_roi,
                float(general_roi) + float(_senior_rate_inc)]
    appendtocsv(each_row)