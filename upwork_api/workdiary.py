import datetime
import json
from pprint import pprint

import pytz
import upwork
from upwork.routers import workdiary

from config import CLIENT_ID, CLIENT_SECRET, TOKEN


class Upwork:
    def __init__(self):
        # if running for the first time
        # comment the TOKEN in config and get
        # the token manually and store it.
        config = upwork.Config({
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": 'https://localhost',
            'token': TOKEN
        })

        self.client = upwork.Client(config)
        actual_token = self.client.get_actual_config().token

        # update the refreshed token
        with open('config.py', 'r') as f:
            lines = f.readlines()
        with open('config.py', 'w') as f:
            lines[[i for i, line in enumerate(lines) if 'TOKEN' in line][0]] = f'TOKEN = {repr(actual_token)}'
            f.writelines(lines)
        # For the first time, we need to get the token manually
        # and then update it in the config.py
        try:
            config.token
        except AttributeError:
            authorization_url, state = self.client.get_authorization_url()
            # cover "state" flow if needed
            authz_code = input(
                "Please enter the full callback URL you get "
                "following this link:\n{0}\n\n> ".format(authorization_url)
            )

            print("Retrieving access and refresh tokens.... ")
            token = self.client.get_access_token(authz_code)
            # WARNING: the access token will be refreshed automatically for you
            # in case it's expired, i.e. expires_at < time(). Make sure you replace the
            # old token accordingly in your security storage. Call client.get_actual_config
            # periodically to sync-up the data
            pprint(token)
            print("OK")

    def get_work_diary(self, date: datetime, contract_id: str):
        str_date = date.strftime('%Y%m%d')
        diary = workdiary.Api(self.client).get_by_contract(contract=contract_id, date=str_date)
        diary_data = []
        tz = pytz.timezone('Asia/Kolkata')
        for cell in diary['data']['cells']:
            unixtime = int(cell['cell_time'])
            start_time = datetime.datetime.fromtimestamp(unixtime, tz)
            end_time = start_time + datetime.timedelta(minutes=10)
            memo_data = json.loads(cell['memo'])
            cell_data = {
                'start_time': start_time.strftime('%H:%M'),
                'end_time': end_time.strftime('%H:%M'),
                'date': date.strftime('%Y-%m-%d'),
                'duration': '00:10'  # in minutes
            }
            # add memo data to cell data
            cell_data.update(memo_data)
            diary_data.append(cell_data)

        return diary_data


if __name__ == "__main__":
    api = Upwork()
    data = api.get_work_diary(datetime.datetime.now(), '31439064')
    print(data)
