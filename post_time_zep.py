import datetime
import re
import urllib.parse
from io import StringIO

import requests
from lxml import etree

from config import *
from decorators import *
from upwork_api.workdiary import Upwork


class Zep:
    def __init__(self):
        self.session = requests.Session()
        self.client_session_id = ''
        self.php_session_id = ''
        self.request_token = ''
        self.is_subticket = False

        # preparing the zep session
        if self.login() and self.change_timezone():
            print(f'>>> Session : {self.session} is ready to post time')
        else:
            exit()

    @handle_login_failures
    def login(self):
        response = self.session.get('https://zep-online.de/zeppstag/view/index.php')
        self.php_session_id = response.cookies['PHPSESSID']

        #login headers
        headers = {
             'Host': 'www.zep-online.de',
             'Origin': 'https://www.zep-online.de',
             'Content-Type': 'application/x-www-form-urlencoded',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.63 Safari/537.36',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
             'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
             'Cookie': f'PHPSESSID={self.php_session_id}',
        }

        payload = f'menu=ProjektzeitVerwaltungMgr&userid={USERNAME}&password={PASSWORD}&login='
        response = self.session.post(LOGIN_URL, headers=headers, data=payload)

        return response.url

    @handle_timezone_failures
    def change_timezone(self):
        response = self.session.get(TIMEZONE_URL)

        # finding client session id
        matches = re.findall(REGEX_CLIENT_SESSION_ID, response.text)
        if matches:
            self.client_session_id = matches[0][1]

        # finding request token
        matches_rt = re.findall(REGEX_REQUEST_TOKEN, response.text)
        if matches_rt:
            self.request_token = matches_rt[0][1]

        if self.client_session_id and self.request_token:
            return True
        else:
            return False

    @handle_payload_id_extraction
    def extract_project_id_and_occurrence_id(self, ticket_id: str):
        if '.' in ticket_id:
            self.is_subticket = True
            sub_ticket_id = ticket_id
            ticket_id = sub_ticket_id.split('.')[0]
        else:
            self.is_subticket = False

        url = TICKET_ID_URL.format(client_session_id=self.client_session_id, ticket_id=ticket_id)

        response = self.session.get(url)

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(response.text), parser)
        # extract occurrence id
        occurrence_id = tree.xpath(XPATH_OCCURRENCE_ID)
        if occurrence_id:
            occurrence_id = occurrence_id[0].strip()
            if self.is_subticket:
                occurrence_id = self.extract_occurrence_id_of_subticket(sub_ticket_id, occurrence_id)

        # extract project id
        project_id = tree.xpath(XPATH_PROJECT_ID)
        if project_id:
            project_id = project_id[0].strip()

        if occurrence_id and project_id:
            return True, (occurrence_id, project_id)
        else:
            return False, ()

    @handle_subticketid_failures
    def extract_occurrence_id_of_subticket(self, sub_ticket_id: str, occurrence_id: str):
        ticket_id = sub_ticket_id.split('.')[0]
        url = SUBTICKET_ID_URL.format(client_session_id=self.client_session_id, ticket_id=ticket_id, ticket_entity_id=ticket_id)
        response = self.session.get(url)
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(response.text), parser)
        sub_ticket_url = tree.xpath(XPATH_SUBTICKET_OCCURRENCE_ID.format(sub_ticket_id=sub_ticket_id))
        if sub_ticket_url:
            model_id = sub_ticket_url[0].split('&')[-1].split('=')[-1]
            return occurrence_id.replace('NULL', model_id)
        else:
            return occurrence_id

    @handle_post_time_failures
    def post_time(self, cell_data):

        # get the occurrence id and project id
        occurrence_id, project_id = self.extract_project_id_and_occurrence_id(str(cell_data['zep_id']))

        url = POST_TIME_URL.format(self.client_session_id)
        self.session.headers.update()
        headers = {
            'authority': 'www.zep-online.de',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': f'PHPSESSID={self.php_session_id}',
            'origin': 'https://www.zep-online.de',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-requesttoken': f'{self.request_token}'
        }
        payload = POST_TIME_PAYLOAD.format(
            date=cell_data['date'],
            start_time=cell_data['start_time'],
            end_time=cell_data['end_time'],
            duration=cell_data['duration'],
            project_id=project_id,
            occurrence_id=occurrence_id,
            memo=cell_data['memo']
        )

        quoted_payload = urllib.parse.quote(payload, safe='=&')

        response = self.session.post(url, headers=headers, data=quoted_payload)
        return response


if __name__ == "__main__":
    client = Zep()
    # api = Upwork()
    # data = api.get_work_diary(datetime.datetime.now(), '31439064')
    # print(data)
    # for i in data:
    #     print(i)
    #     result = client.post_time(i)
    #     if not result:
    #         print(f'!! Failed : {i}')

    result = client.post_time({'start_time': '11:40', 'end_time': '11:50', 'date': '2023-01-01', 'duration': '00:10', 'memo': 'RCR 2', 'zep_id': '2759'})
