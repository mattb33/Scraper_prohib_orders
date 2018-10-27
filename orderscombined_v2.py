#######  SETUP   ############

# Import required modules
import requests
import pandas as pd
import csv
from bs4 import BeautifulSoup

## URLs
urlSA = 'http://www.hcscc.sa.gov.au/orders-issued-code-conduct-unregistered-health-practitioners/'
urlNSW = 'http://www.hccc.nsw.gov.au/Hearings---decisions/Register-of-Prohibition-Orders-in-Force/List-of-Prohibition-Orders-in-Force'
urlQLD = 'https://www.oho.qld.gov.au/news-updates/immediate-actions/prohibition-orders/'
urlVIC = 'https://hcc.vic.gov.au/prohibition-orders-warnings/prohibition-orders'

# Initialise lists
output = []
# outputSA = []
# outputNSW = []
# outputQLD = []
# outputVIC = []

#Define header for csv
header = ['state', 'date', 'name', 'practitionerType', 'orderDetails', 'orderType']

########## START OF QLD PROCESS #################

# Get website data
dataQLD = requests.get(urlQLD)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(dataQLD.text, 'html.parser')

# Identify table with data we want
myTableQLD = soup.find('tbody')

# Iterate through each row 
for tr in myTableQLD.find_all('tr'):
    date = tr.find_all('td')[0].text.strip()
    name = tr.find_all('td')[1].text.strip()
    practitionerType = tr.find_all('td')[2].text.strip()
    orderDetails = tr.find_all('td')[3].text.strip()
    orderType = tr.find_all('td')[4].text.strip()
    state = 'QLD'
    output.append([state, date, name, practitionerType, orderDetails, orderType])
    
# Test output
print('QLD - data gathered')

########### QLD complete #################

########### START OF SA PROCESS #################
# Get website data
dataSA = requests.get(urlSA)
# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(dataSA.text, 'html.parser')
# Identify table with data we want
myTableSA = soup.find('div', class_='entry-content')

# Iterate through each row 
for h2 in myTableSA.find_all('h2'):
    date = 'see order details'
    name = h2.text.strip()
    practitionerType = 'not listed'
    orderDetails = 'working on it'    #### Come back to this one   ####
    orderType = 'not listed'
    state = 'SA'
    output.append([state, date, name, practitionerType, orderDetails, orderType])
    
# Test output
print('SA - data gathered')

print(output)




#########  Write all to CSV   ##########
print('writing to CSV...')

with open('prohibition_orders.csv', mode='w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(i for i in header)
    
    # Add scraped data to csv file
    for item in output:
        writer.writerow(item)

print('Writing to CSV complete')



