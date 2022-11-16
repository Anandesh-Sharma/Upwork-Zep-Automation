from datetime import datetime

from config import CONTRACT_ID
from post_time_zep import Zep
from upwork_api.workdiary import Upwork

if __name__ == "__main__":
    client = Zep()

    api = Upwork()
    data = api.get_work_diary(datetime.now(), CONTRACT_ID)
    for i in data:
        result = client.post_time(i)
        if not result:
            print(f'!! Failed : {i}')
