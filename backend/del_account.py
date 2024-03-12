import requests
import json

url = 'https://tobiichi3227.eu.org/'
# url = 'http://localhost:8000/'

with open('./config.json', 'r') as f:
    token = json.load(f)['token']


account = input('Enter the account you want to delete: ')
password = input('Enter the password: ')

payload = {
    'token': token,
    'type': 'del account',
    'account': account,
    'password': password,
}
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    response = response.json()
    if response['message'] == 'Account deleted successfully':
        print('Account deleted successfully')
    else:
        print(response['message'])
except requests.exceptions.RequestException as e:
    print('Failed to post data:', e)
