#######  SETUP   ############

# Import required modules
import requests
import csv
from bs4 import BeautifulSoup

## URLs
urlSA = 'http://www.hcscc.sa.gov.au/orders-issued-code-conduct-unregistered-health-practitioners/'
urlNSW = ['http://www.hccc.nsw.gov.au/Hearings---decisions/Register-of-Prohibition-Orders-in-Force/List-of-Prohibition-Orders-in-Force', 'http://www.hccc.nsw.gov.au/Hearings---decisions/Register-of-Prohibition-Orders-in-Force/List-of-Prohibition-Orders-in-Force?retain=true&PagingModule=2615&Pg=2', 'http://www.hccc.nsw.gov.au/Hearings---decisions/Register-of-Prohibition-Orders-in-Force/List-of-Prohibition-Orders-in-Force?retain=true&PagingModule=2615&Pg=3']
urlQLD = 'https://www.oho.qld.gov.au/news-updates/immediate-actions/prohibition-orders/'
urlVIC = 'https://hcc.vic.gov.au/prohibition-orders-warnings/prohibition-orders?page={}'


# Initialise lists
output = []


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



########### START OF VIC PROCESS #################

# Deal with pagination - increment page numbers
range_page_url = [urlVIC.format(i) for i in range(0,5)]

for range in range_page_url:
    r = requests.get(range)
    soup = BeautifulSoup(r.text, 'lxml')
    for tr in soup.table.find_all('tr')[1:-1]:
        date = [span.text for span in tr.find_all('span')]
        name = [strong.text for strong in tr.find_all('strong')]
        practitionerType = [strong.next_sibling for strong in tr.find_all('strong')]
        orderDetails = "view web page"
        orderType = "-"
        state = 'VIC'
        output.append([state, date, name, practitionerType, orderDetails, orderType])

# Test output
print('VIC - data gathered')

########### VIC complete #################

########### START OF NSW PROCESS #################
# Get website data
for link in urlNSW:
    dataNSW = requests.get(link)
    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(dataNSW.text, 'html.parser')
    # Identify table with data we want
    myTableNSW = soup.find('div', class_='widget')

# Iterate through each row
    for row in myTableNSW.find_all('dl'):
        date = row.find('dd').text.strip()
        name = row.find('span').text.strip()
        practitionerType = 'not listed'
        orderDetails = row.find('a').get('href')
        orderType = 'not listed'
        state = 'NSW'
        output.append([state, date, name, practitionerType, orderDetails, orderType])

# Test output
print('NSW - data gathered')

########### NSW complete #################






########### START OF SA PROCESS #################
# # Get website data
dataSA = requests.get(urlSA)
# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(dataSA.text, 'html.parser')
# Identify table with data we want
myTableSA = soup.find('div', class_='entry-content')

# Iterate through each row
for item in myTableSA('h2'):
    date = 'view order details'
    name = item.text
    practitionerType = 'not listed'
    orderDetails = 'to be fixed later'
    orderType = 'not listed'
    state = 'SA'
    output.append([state, date, name, practitionerType, orderDetails, orderType])


print('SA - data gathered')

########### SA complete #################



print("Here's an example of the output being written to CSV:")
print(output[0:2])

#########  Write all to CSV   ##########
print('writing to CSV...')

with open('prohibition_orders.csv', mode='w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(i for i in header)

    # Add scraped data to csv file
    for item in output:
        writer.writerow(item)

print('Writing to CSV complete')
