import datetime
import json
from pprint import pprint

import pytz
import upwork
from upwork.routers import workdiary

from config import CLIENT_ID, CLIENT_SECRET, TOKEN, CONTRACT_ID


class Upwork:
    def __init__(self):

        if TOKEN:
            config_dict = {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": 'https://localhost',
                'token': TOKEN
            }
        else:
            config_dict = {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": 'https://localhost',
            }

        config = upwork.Config(config_dict)
        self.client = upwork.Client(config)

        # For the first time, we need to get the token manually
        try:
            token = self.client.get_actual_config().token
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

        # update the refreshed token
        with open('config.py', 'r') as f:
            lines = f.readlines()
        with open('config.py', 'w') as f:
            lines[[i for i, line in enumerate(lines) if 'TOKEN' in line][0]] = f'TOKEN = {repr(token)}\n'
            f.writelines(lines)

    def create_time_blocks(self, data):
        end_times = []
        timeblocks = []
        zep_ids = []
        for i in data:
            zep_id = i['zep_id']
            start_time = i['start_time']
            end_time = i['end_time']
            if not end_times or end_times[-1] != start_time or zep_ids[-1] != zep_id:
                end_times.append(end_time)
                zep_ids.append(zep_id)
                timeblocks.append(i)
            else:
                index = len(end_times) - 1
                timeblocks[index]['end_time'] = i['end_time']
                end_times[index] = end_time
        
        for i in timeblocks:
            st = datetime.datetime.strptime(i['start_time'], '%H:%M')
            et = datetime.datetime.strptime(i['end_time'], '%H:%M')
            duration = et - st
            i['duration'] = ':'.join(str(duration).split(':')[:2])
        return timeblocks
            

        


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
        timeblocks = self.create_time_blocks(data=diary_data)
        print(timeblocks)
        return timeblocks


if __name__ == "__main__":
    api = Upwork()
    data = api.get_work_diary(datetime.datetime.now(), CONTRACT_ID)
    print(data)
