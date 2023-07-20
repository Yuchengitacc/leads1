# retrieve data needs
#salesforce_username = 'yuchen.yao@micronetbd.org.litifydev'
#salesforce_password = 'Pwd123!!'
#salesforce_security_token = 'Xsu0h1rRnSXhL1mEPwTBPJGM'
#salesforce_consumer_key = '3MVG9gtDqcOkH4PJYgaVeRuF5ZnhfCBLnSIwNjFVpyv_YATEz41WrXTLznYtT.jis8sbwCVYM0UIdIss.LPuU'
#salesforce_consumer_secret = '295A0F7F50B7D6C5B42C7C0EEECCC95AFB53F4EE20FE1D2FDFF84DF5D95D3D04'

import pandas as pd
import requests

# Replace these with your Salesforce credentials and Connected App details
salesforce_username = 'yuchen.yao@micronetbd.org.litifydev'
salesforce_password = 'Pwd123!!'
salesforce_security_token = 'Xsu0h1rRnSXhL1mEPwTBPJGM'
salesforce_consumer_key = '3MVG9gtDqcOkH4PJYgaVeRuF5ZnhfCBLnSIwNjFVpyv_YATEz41WrXTLznYtT.jis8sbwCVYM0UIdIss.LPuU'
salesforce_consumer_secret = '295A0F7F50B7D6C5B42C7C0EEECCC95AFB53F4EE20FE1D2FDFF84DF5D95D3D04'

# using URL to log in
login_url = 'https://login.salesforce.com/services/oauth2/token'
data = {
    'grant_type': 'password',
    'client_id': salesforce_consumer_key,
    'client_secret': salesforce_consumer_secret,
    'username': salesforce_username,
    'password': salesforce_password + salesforce_security_token
}

response = requests.post(login_url, data=data)
response_data = response.json()

# error check 
if response.status_code == 200:
    print("Sucessful")
else:
    print("Fails, get status code:", response.status_code)

instance_url = response_data['instance_url']
access_token = response_data['access_token']

# SOQL_query the Leads object
soql_query = "SELECT Id, Name, Email, State, Status, CreatedDate FROM Lead"

# Retrieve all records using pagination
def fetch_all_records(url, headers):
    data = []
    while url:
        response = requests.get(url, headers=headers)
        records = response.json()
        data.extend(records['records'])
        url = records.get('nextRecordsUrl')
    return data

# URL initial request
leads_query_url = f"{instance_url}/services/data/v52.0/queryAll/?q={soql_query}"

# Make an HTTP GET request to Salesforce API to fetch data from the Lead object
headers = {'Authorization': f'Bearer {access_token}'}
all_records = fetch_all_records(leads_query_url, headers)

# Create a DataFrame 
df = pd.DataFrame(all_records)

# modify the time without 0
def extract_date(datetime_str):
    return datetime_str.split(".")[0]

df['CreatedDate/Time'] = df['CreatedDate'].apply(extract_date)

# Drop CreatedDate col
df.drop(columns=['CreatedDate'], inplace=True)

# Extract 'type' and 'url' attributes into separate columns
df['Type'] = df['attributes'].apply(lambda x: x['type'])
df['URL'] = df['attributes'].apply(lambda x: x['url'])

# Drop the 'attributes' col
df.drop(columns=['attributes'], inplace=True)

# Write the DataFrame to a CSV file
csv_filename = "salesforce_leads_data.csv"
df.to_csv(csv_filename, index=False)

print(f"CSV file '{csv_filename}' has been created.")