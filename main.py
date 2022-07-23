import os
import httplib2
from loguru import logger
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from db import DataBase
from enum import Enum


class Status(Enum):
    first_start = 1
    standart_parsing = 2


class App:
    CRED_FILE = 'cred.json'
    SHEET_ID = '1Mef7rntsKANLNWsObqDhloQs6_4HZuq1dRRz3v5R49E'

    def __init__(self) -> None:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.CRED_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive']
        )
        http_auth = credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build(
            'sheets', 'v4', http=http_auth)
        self.db = DataBase('abul.db.elephantsql.com', 'aaneafdx',
                           'bknG2UQ4sliACNksrziUP7PUZcOME-sm', 'aaneafdx')

    def parse_items(self, first_start: bool = False) -> None:
        BATCH = 10
        step = 0
        while True:
            table_range = 'A' + str(2 + BATCH * step) + \
                ':D' + str(1 + BATCH * (step + 1))
            print(f'Table range: {table_range}')
            try:
                values = self.service.spreadsheets().values().batchGet(
                    spreadsheetId=self.SHEET_ID,
                    majorDimension='ROWS', ranges=[table_range]
                ).execute()
                print(values)
            except Exception as _e:
                logger.error(
                    'Something went wrong when get values from Google SpreadSheet')
                exit(-1)
            if 'values' not in values['valueRanges'][0]:
                break
            elif first_start:
                self.add_items(values['valueRanges'][0]['values'])
            step += 1

    def add_items(self, items: list) -> None:
        for item in items:
            print(item)
            self.db.add_item(item)


app = App()
app.parse_items(True)
