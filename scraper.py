import requests
import psycopg2
import pprint as pp
import time
import configparser
import sys
from bs4 import BeautifulSoup
from datetime import datetime
from Settings import settings

def main_scraper():
    conf = settings.get_settings()
    config = configparser.ConfigParser()
    config.read('fireboard.ini')

    format = "%d.%m.%Y %H:%M:%S"
    url = conf.fb_url
    cookies = dict(PHPSESSID=conf.fb_phpsessid)

    conn = psycopg2.connect(database=conf.db_name,
                            host=conf.db_host,
                            user=conf.db_user,
                            password=conf.db_password,
                            port=conf.db_port)

    try:
        while True:
            print("########## Refresh status", datetime.now())
            try:
                html_text = requests.get(url, cookies=cookies).text
            except (requests.Timeout, requests.ConnectionError) as error:
                pp.pprint(error)
                # TODO send telemetry along
                time.sleep(15)
                continue
            try:
                soup = BeautifulSoup(html_text, 'html.parser')
                table_body = soup.find('tbody')
                table_rows = table_body.find_all('tr')
            except (AttributeError):
                print("PHP Session invalid")
                break
            for row in table_rows:
                table_cols = row.find_all('td')
                table_cols = [ele.text.strip() for ele in table_cols]
                dtime = datetime.strptime(table_cols[6], format)

                sql = """INSERT INTO fahrzeug_status(id, issi, status, timestamp)
                        VALUES(%s, %s, %s, %s)
                """
                with conn:
                    with conn.cursor() as cursor:
                        try:
                            record = (row['data-key'], table_cols[0], table_cols[4], dtime)
                            print("Trying to insert: ")
                            pp.pprint(record)
                            cursor.execute(sql, record)
                            conn.commit()
                        except (Exception, psycopg2.DatabaseError) as error:
                            pass
            time.sleep(15)
    except KeyboardInterrupt:
        print(f"Keyboard Interrupt, exiting")
        cursor.close()
        conn.close()
        return 0
    

if __name__ == "__main__":
    sys.exit(main_scraper())