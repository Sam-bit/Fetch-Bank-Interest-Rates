import requests
from bs4 import BeautifulSoup

class PostOfficeInterest:
    rates_file_name = "rates_list.csv"
    _BANK_NAME = 'Post Office'
    _BANK_URL = 'https://www.indiapost.gov.in/Financial/pages/content/post-office-saving-schemes.aspx'
    _senior_rate_inc = "0.25"

    def __init__(self,rates_file_name):
        self.rates_file_name = rates_file_name

    def get_roi(self,text_value):
        return float((text_value.split(" (")[0] if "(" in text_value else text_value).replace('\u200b', ''))

    def appendtocsv(self,row=None):
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
        soup = BeautifulSoup(r.text.encode('utf-8'), "html.parser")
        # Insert Header
        header = ['bank_name', 'old_or_new', 'deposit', 'deposit_name', 'from_year', 'from_period', 'from_period_d_m_y',
                  'from_period_operator',
                  'to_year', 'to_period', 'to_period_d_m_y', 'to_period_operator', 'min_amount', 'max_amount', 'premature_y_n',
                  'general_roi', 'senior_roi']
        self.appendtocsv(header)
        # Fetch Old Interest Rates
        old_or_new = 'OLD'
        all_tables = soup.find("div", attrs={"id": "tab6", "class": "tabContent"}).find_all("table")
        table = all_tables[0]
        for tr in table.find_all("tr")[1:]:
            from_year = tr.find_all('td')[0].text
            to_year = tr.find_all('td')[1].text
            general_roi = self.get_roi(tr.find_all('td')[2].text)
            each_row = [self._BANK_NAME, old_or_new, 'SB', 'Post Office Savings Account', from_year, '', '', 'GE', to_year, '', '',
                        'LE', '', '', '', general_roi, float(general_roi) + float(self._senior_rate_inc)]
            self.appendtocsv(each_row)
        table = all_tables[1]
        for tr in table.find_all("tr")[1:]:
            from_year = tr.find_all('td')[0].text
            to_year = tr.find_all('td')[1].text
            general_roi = self.get_roi(tr.find_all('td')[2].text)
            each_row = [self._BANK_NAME, old_or_new, 'RD', 'National Savings Recurring Deposit Account', from_year, '', '', 'GE',
                        to_year, '', '', 'LE', '', '', '', general_roi,
                        float(general_roi) + float(self._senior_rate_inc)]
            self.appendtocsv(each_row)
        table = all_tables[2]
        for tr in table.find_all("tr")[1:]:
            from_year = tr.find_all('td')[0].text
            to_year = tr.find_all('td')[1].text
            general_roi_1 = self.get_roi(tr.find_all('td')[2].text)
            general_roi_2 = self.get_roi(tr.find_all('td')[3].text)
            general_roi_3 = self.get_roi(tr.find_all('td')[4].text)
            general_roi_5 = self.get_roi(tr.find_all('td')[5].text)
            each_row = [self._BANK_NAME, old_or_new, 'TD', 'National Savings Time Deposit Account', from_year, '1', 'Y', 'GE',
                        to_year, '1', 'Y', 'LE', '', '', '', general_roi_1,
                        float(general_roi_1) + float(self._senior_rate_inc)]
            self.appendtocsv(each_row)
            each_row = [self._BANK_NAME, old_or_new, 'TD', 'National Savings Time Deposit Account', from_year, '2', 'Y', 'GE',
                        to_year, '2', 'Y', 'LE', '', '', '', general_roi_2,
                        float(general_roi_2) + float(self._senior_rate_inc)]
            self.appendtocsv(each_row)
            each_row = [self._BANK_NAME, old_or_new, 'TD', 'National Savings Time Deposit Account', from_year, '3', 'Y', 'GE',
                        to_year, '3', 'Y', 'LE', '', '', '', general_roi_3,
                        float(general_roi_3) + float(self._senior_rate_inc)]
            self.appendtocsv(each_row)
            each_row = [self._BANK_NAME, old_or_new, 'TD', 'National Savings Time Deposit Account', from_year, '5', 'Y', 'GE',
                        to_year, '5', 'Y', 'LE', '', '', '', general_roi_5,
                        float(general_roi_5) + float(self._senior_rate_inc)]
            self.appendtocsv(each_row)
        table = all_tables[3]
        for tr in table.find_all("tr")[1:]:
            from_year = tr.find_all('td')[0].text
            to_year = tr.find_all('td')[1].text
            general_roi = self.get_roi(tr.find_all('td')[2].text)
            each_row = [self._BANK_NAME, old_or_new, 'MIS', 'National Savings Monthly Income Account', from_year, '', '', 'GE',
                        to_year, '', '', 'LE', '', '', '', general_roi,
                        float(general_roi) + float(self._senior_rate_inc)]
            self.appendtocsv(each_row)
        table = all_tables[4]
        for tr in table.find_all("tr")[1:]:
            from_year = tr.find_all('td')[0].text
            to_year = tr.find_all('td')[1].text
            general_roi = self.get_roi(tr.find_all('td')[2].text)
            each_row = [self._BANK_NAME, old_or_new, 'SCSS', 'Senior Citizens Savings Scheme Account', from_year, '', '', 'GE',
                        to_year, '', '', 'LE', '', '', '', general_roi,
                        float(general_roi) + float(self._senior_rate_inc)]
            self.appendtocsv(each_row)

        #Fetch New Interest Rates
        old_or_new = 'NEW'
        from_year = '01-04-2024'
        to_year = '31-03-2025'
        general_roi = 4.00
        each_row = [self._BANK_NAME, old_or_new, 'SB', 'Post Office Savings Account', from_year, '', '', 'GE', to_year, '', '', 'LE',
                    '', '', '', general_roi,
                    float(general_roi) + float(self._senior_rate_inc)]
        self.appendtocsv(each_row)
        from_year = '01-01-2024'
        to_year = '31-03-2025'
        general_roi = 6.70
        each_row = [self._BANK_NAME, old_or_new, 'RD', 'National Savings Recurring Deposit Account', from_year, '', '', 'GE',
                    to_year, '', '', 'LE', '', '', '', general_roi,
                    float(general_roi) + float(self._senior_rate_inc)]
        self.appendtocsv(each_row)
        from_year = '01-01-2024'
        to_year = '31-03-2024'
        general_roi_1 = 6.9
        general_roi_2 = 7.0
        general_roi_3 = 7.1
        general_roi_5 = 7.5
        each_row = [self._BANK_NAME, old_or_new, 'TD', 'National Savings Time Deposit Account', from_year, '1', 'Y', 'GE', to_year,
                    '1', 'Y', 'LE', '', '', '', general_roi_1,
                    float(general_roi_1) + float(self._senior_rate_inc)]
        self.appendtocsv(each_row)
        each_row = [self._BANK_NAME, old_or_new, 'TD', 'National Savings Time Deposit Account', from_year, '2', 'Y', 'GE', to_year,
                    '2', 'Y', 'LE', '', '', '', general_roi_2,
                    float(general_roi_2) + float(self._senior_rate_inc)]
        self.appendtocsv(each_row)
        each_row = [self._BANK_NAME, old_or_new, 'TD', 'National Savings Time Deposit Account', from_year, '3', 'Y', 'GE', to_year,
                    '3', 'Y', 'LE', '', '', '', general_roi_3,
                    float(general_roi_3) + float(self._senior_rate_inc)]
        self.appendtocsv(each_row)
        each_row = [self._BANK_NAME, old_or_new, 'TD', 'National Savings Time Deposit Account', from_year, '5', 'Y', 'GE', to_year,
                    '5', 'Y', 'LE', '', '', '', general_roi_5,
                    float(general_roi_5) + float(self._senior_rate_inc)]
        self.appendtocsv(each_row)
        from_year = '01-01-2024'
        to_year = '31-03-2025'
        general_roi = 7.4
        each_row = [self._BANK_NAME, old_or_new, 'MIS', 'National Savings Monthly Income Account', from_year, '', '', 'GE', to_year,
                    '', '', 'LE', '', '', '', general_roi,
                    float(general_roi) + float(self._senior_rate_inc)]
        self.appendtocsv(each_row)
        from_year = '01-01-2024'
        to_year = '31-03-2025'
        general_roi = 8.2
        each_row = [self._BANK_NAME, old_or_new, 'SCSS', 'Senior Citizens Savings Scheme Account', from_year, '', '', 'GE', to_year,
                    '', '', 'LE', '', '', '', general_roi,
                    float(general_roi) + float(self._senior_rate_inc)]
        self.appendtocsv(each_row)
