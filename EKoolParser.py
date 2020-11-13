import requests
import hashlib
from datetime import datetime
import json
from AssignmentTimeframe import AssignmentTimeframe
from Feed import Feed
from Absences import Absences

# EKooli Endpointid
API_URL = 'https://postikana.ekool.eu/rest/json'
SERVER_ROOT_URL = 'https://ekool.eu/'
REACTIONS_API_URL = 'https://api.ekool.eu/v1'
MESSAGING_API_URL = 'https://messaging.ekool.eu'
MESSAGING_WEB_SOCKET = 'wss://messaging.ekool.eu/messaging_websocket:8020/'


# EKooli API't kasutav class, mille kaudu saab võtta näiteks tunniplaani jne.
class EKoolParser:
    # Konstruktoris on vaja eKooli kasutaja kasutajanime ja parooli
    def __init__(self, username, password):
        self.logged_in = False
        self.access_token = None
        self.refresh_token = None
        self.person_info = None
        self.student_id = None
        self.parents = None
        # Logime eKooli sisse
        self.login(username, password)
        # Võtame inimese kohta info
        self.get_person_data()

    # returnib {"start": startStr, "end":endStr}
    # format 05.01.2020 from datetime object
    @staticmethod
    def format_date_for_ekool(date):
        # formaat saab olema 
        # 05.01.2020
        date_str = str(date.day).zfill(2) + "." + str(date.month).zfill(2) + "." + str(date.year)
        return date_str

    # Puudumiste võtmine
    def get_absences(self):
        return Absences(self.data_miner_with_cache(['absences90Days', self.student_id]))

    # Voo kindla elemendi võtmine
    def get_feed_item(self, event_id):
        return self.data_miner_with_cache(['feeditem',self.student_id, event_id])

    # Terve voo saamine
    def get_feed(self):
        return Feed(self.data_miner_with_cache(['feed', self.student_id]))

    '''
    Näide kodutoode võtmisel saadud response'ist 
        {
      "startDate": "06.01",
      "endDate": "10.01",
      "weekNo": 1,
      "eventList": [
        {
          "authorName": "Mare Uritam",
          "title": "\\u00f5pik(suur) \\u00fcl. 355 ( 5;6;8)nendest \\u00fclesannetest vali 5 \\u00fclesannet, lahenda, 357 (1;4), 358( 1;2;4;7;9), 359(1;3) -",
          "orderTimestampLong": 1578265200000,
          "content": "",
          "comments": null,
          "url": null,
          "id": 15159286778,
          "isHot": null,
          "subjectName": "Matemaatika",
          "deadLine": "06.01.2020",
          "added": "13.12.2019 13:33",
          "isDone": null,
          "isTest": false,
          "isGraded": false,
          "typeId": 1
        },
        {
          "authorName": "Siiri Vallim\\u00e4e",
          "title": "Esitlustega j\\u00e4tkamine",
          "orderTimestampLong": 1578610800000,
          "content": "Palun valmistuda esitlusteks need grupid, kes detsembris j\\u00e4id kuulmata.",
          "comments": null,
          "url": null,
          "id": 15168778836,
          "isHot": null,
          "subjectName": "Inimese\\u00f5petus",
          "deadLine": "10.01.2020",
          "added": "03.01.2020 12:45",
          "isDone": null,
          "isTest": false,
          "isGraded": false,
          "typeId": 1
        },
        {
          "authorName": "Kaisa L\\u00f5hmus",
          "title": "Vocabulary test",
          "orderTimestampLong": 1578265200000,
          "content": "<a href=\"https://quizlet.com/458731052/academic-english-year-10-success-21-flash-cards/?new\" target=\"_blank\">https://quizlet.com/458731052/academic-english-year-10-success-21-flash-cards/?new</a>",
          "comments": null,
          "url": null,
          "id": 15141161663,
          "isHot": null,
          "subjectName": "A-v\\u00f5\\u00f5rkeel (inglise keel)",
          "deadLine": "06.01.2020",
          "added": "26.11.2019 13:00",
          "isDone": null,
          "isTest": true,
          "isGraded": true,
          "typeId": 1
        }
      ],
      "orderTimestampLong": 1578261600000
    }
    '''
    # Võtame kodutööd ajavahemikus
    def get_assignments_for_timeframe(self, startingDate, endDate):
        starting_str = self.format_date_for_ekool(startingDate)
        end_str = self.format_date_for_ekool(endDate)

        raw_data = self.data_miner_with_cache(
            ['todolist', str(self.student_id), starting_str, end_str], API_URL)
        return AssignmentTimeframe(raw_data)

    # Võtame sisse logitud inimese kohta infot.
    def get_person_data(self):
        self.person_info = self.data_miner_with_cache(['person'], API_URL)
        self.student_id = str(self.person_info["roles"][0]["studentId"])
        return self.person_info

    # Vanemate võtmine
    def get_parents(self):
        '''
         {'students': [{'name1': 'Robi', 'name2': 'Rohumaa', 'profileImgFn': 'REDACTED'}], 'parents': [{'name1': 'Priit', 'name2': 'Rohumaa', 'profileImgFn': None}, {'name1': 'Helen', 'name2': 'Rohumaa', 'profileImgFn': None}]}
        :return:
        '''
        self.parents = self.data_miner_with_cache(['family'], API_URL)["parents"]
        return self.parents

    # eKooli sisse logimine
    def login(self, username, password):
        # Ütleme eKoolile, et logime sisse parooliga ning et me tuleneme eKooli äpist
        query_base = {
            'grant_type': "password",
            'client_id': 'mKool',
            'username': username,
            'password': password
        }

        # eKool nõuab järnevaid headereid, et logida sisse
        headers = {
            'Authorization': 'Basic bUtvb2w6azZoOTdoYWZzcnZvbzNzZDEzZ21kdXE4YjZ0YnM1czE2anFtYTZydThmajN0dWVhdG5lOGE4amxtN2Jt',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        '''
        Sisselogimisel tagasi saadetud response
        {'access_token': 'bc24a0f1-8f28-4407-b7f0-3974dde3c04f', 'token_type': 'bearer', 'refresh_token': '6ed2e540-aa44-4802-81ff-0d6c8c6f1d56', 'scope': 'read'}
        '''
        # Teeme requesti, mis logib meid sisse
        r = requests.post(SERVER_ROOT_URL + 'auth/oauth/token', data=query_base, headers=headers)
        login_state = r.json()
        if r.status_code is 200:
            # logisime sisse 
            self.logged_in = True
            self.access_token = login_state["access_token"]
            self.refresh_token = login_state["refresh_token"]

    # eKoolist data't võttev meetod, mille kaudu saame võtta näiteks voogu, tunniplaani jne 
    def data_miner_with_cache(self, pathElements, apiUrl=API_URL):
        key = ''
        # Lisame api endpointile pathElemente. Näiteks /family
        for element in pathElements:
            key += '/' + str(element)
        
        # Lisame MD5 Checksumi saadetavale datale
        query_base = self.stampTheBase(self.get_query_base())

        # Peame kaasa saatma oma sisselogimisel saadud access_tokeni. Seetõttu lisame selle siin headerites
        headers = {
            "Authorization": "Bearer " + self.access_token,
            'Content-Type': 'application/json;charset=UTF-8'
        }
        # Saadame data requesti
        r = requests.post(apiUrl + key, data=json.dumps(query_base), headers=headers)
        if r.status_code is 200:
            # Saime data
            return r.json()


    # Query_base on asi mis saadetakse iga requestiga kaasa. 
    @staticmethod
    def get_query_base():
        push_settings = [True, True, True, True, True]
        return {
            'langCode': 'et',
            'version': "4.6.6",
            'deviceId': "1234567",
            'userAgent': "Google Chrome",
            'checksum': None,
            'pushType': '1',
            'localTime': str(int(datetime.timestamp(datetime.now()))),
            'gradePush': push_settings[0],
            'absencePush': push_settings[1],
            'noticePush': push_settings[2],
            'todoPush': push_settings[3],
            'messagePush': push_settings[4]
        }

    # stampTheBase lisab meie query_base'ile md5sum'i iseendast. eKoolil on seda tarvis
    @staticmethod
    def stampTheBase(query_base):
        str = ''
        str += query_base['langCode'] or ''
        str += query_base['version'][::-1] or ''
        str += query_base['deviceId'] or ''
        str += query_base['userAgent'] or ''
        str += query_base['pushType'] or ''
        str += query_base['version'] or ''
        str += query_base['localTime'] or ''
        query_base["checksum"] = hashlib.md5(str.encode('utf-8')).hexdigest()
        return query_base
