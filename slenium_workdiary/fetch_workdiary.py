import requests
import pickle
import datetime


class FetchWorkDiary:

    def __init__(self, date):
        with open('cookies.pkl', 'rb') as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                if cookie['name'] == 'workdiary_slave_token':
                    token = cookie['value']
                    break

        print(token)
        url = f'https://www.upwork.com/api/v3/wt/workdiaries/v2/contracts/31439064/{date}?offset=19800'
        headers = {'Authorization': f'Bearer {token}'}
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            self.work_diary = resp.json()
        else:
            print(resp.status_code, resp.json())