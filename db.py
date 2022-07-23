import psycopg2
import os
from pprint import pprint
import config
from loguru import logger
from datetime import datetime
import requests
import xmltodict

logger.add('test.log')


class DataBase:
    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        try:
            self.connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.connection.cursor()
            self.cursor.execute(config.create_table)
            self.connection.commit()
        except Exception as _e:
            logger.error('Something wrong with connection to DB\n' + str(_e))
            exit(-1)

    def _usd_to_rub(self, usd: int) -> float:
        try:
            r = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
            cbr_data = xmltodict.parse(r.content)
            for rate in cbr_data['ValCurs']['Valute']:
                if rate['CharCode'] == 'USD':
                    usd_rate = rate['Value'].replace(',', '.')
                    break
            if 'usd_rate' in locals():
                return round(usd * float(usd_rate), 2)
        except Exception as _e:
            logger.error('Something wrong with CBR\n' + str(_e))
            exit(-1)

    def add_item(self, item_data: list):
        if len(item_data) == 4:
            db_id, order_num, cost_usd, delivery_time = item_data
            try:
                db_id, order_num, cost_usd = map(
                    int, (db_id, order_num, cost_usd))
            except Exception as _e:
                logger.warning('Type casting failed')
                return
        else:
            logger.warning('Item data in the wrong format')
            return
        cost_rub = self._usd_to_rub(cost_usd)
        try:
            self.cursor.execute(
                config.add_item, (db_id, order_num, cost_usd, cost_rub, delivery_time))
            self.connection.commit()
        except Exception as _e:
            logger.warning(
                f'Something wrong when new item was add with id: {db_id}\n' + str(_e))

    def get_items(self):
        self.cursor.execute("""SELECT * FROM test_data""")
        pprint(self.cursor.fetchall())

    def drop_table(self):
        self.cursor.execute(config.drop_table)
        self.connection.commit()
