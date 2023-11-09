import psycopg2
import requests
import urllib3
import configparser
import sys


def handle_notify(conn):
    conn.poll()
    for notify in conn.notifies:
        print(notify.payload)
        splits = notify.payload.strip("()").split(",")
        send_to_alamos(splits[0], splits[1])
    conn.notifies.clear()

def send_to_alamos(issi, status):
    print(f"Issi: {issi}, Status: {status}")
    data = {}
    data['type'] = 'STATUS'
    data['sender'] = __sender
    data['authorization'] = __auth
    data['data'] = {}
    data['data']['status'] = status
    data['data']['address'] = issi
    requests.post(__url, json=data, verify=False)

def main_listener():
    global __url
    global __auth
    global __sender

    print(f"Starting status listener on DB ...")
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    config = configparser.ConfigParser()
    config.read('fireboard.ini')

    try:
        conn = psycopg2.connect(database=config['Postgres']['db'],
                                host=config['Postgres']['host'],
                                user=config['Postgres']['user'],
                                password=config['Postgres']['password'],
                                port=config['Postgres']['port'],
                                connect_timeout=5)
        
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = conn.cursor()
        cursor.execute("LISTEN status_notification")
    except psycopg2.Error as e:
        print(f"DB Error, Code: {e.pgcode} Error: {e.pgerror}")
        return -1

    __url = config['Alamos']['stats_endpoint']
    __auth = config['Alamos']['auth']
    __sender = config['Alamos']['sender']

    try:
        while True:
            handle_notify(conn)
    except KeyboardInterrupt:
        print(f"Keyboard Interrupt, exiting")
        cursor.close()
        conn.close()
        return 0

if __name__ == "__main__":
    sys.exit(main_listener())