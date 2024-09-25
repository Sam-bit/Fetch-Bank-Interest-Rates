from icici import ICICIInterest
from postoffice import PostOfficeInterest
from rbl import RBLInterest
refresh = False
rates_file_name = "rates_list.csv"
if refresh:
    open(rates_file_name, 'w').close()
ICICIInterest(rates_file_name).start()
PostOfficeInterest(rates_file_name).start()
RBLInterest(rates_file_name).start()