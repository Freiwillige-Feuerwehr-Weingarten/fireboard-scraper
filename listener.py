import psycopg2
import requests
import urllib3
import sys
import select
from Settings import settings


def handle_notify(conn):
    if select.select([conn],[],[]) == ([],[],[]):
        pass
    else:
        conn.poll()
        for notify in conn.notifies:
            print(notify.payload)
            splits = notify.payload.strip("()").split(",")
            send_to_alamos(splits[0], splits[1])
        conn.notifies.clear()

def send_to_alamos(issi, status):
    sconf = settings.get_settings()
    print(f"Issi: {issi}, Status: {status}")
    data = {}
    data['type'] = 'STATUS'
    data['sender'] = sconf.alamos_sender
    data['authorization'] = sconf.alamos_auth
    data['data'] = {}
    data['data']['status'] = status
    data['data']['address'] = issi
    print(f"Sending to Weingarten")
    try:
        requests.post(sconf.alamos_stats_endpoint, json=data, verify=False)
    except requests.exceptions.RequestException as err:
        print(f'Error sending to Weingarten: {err}')
    print(f"Sending to Wangen")
    data['sender'] = sconf.alamos_remote_sender
    data['authorization'] = sconf.alamos_remote_auth
    try:
        requests.post(sconf.alamos_remote_stats_endpoint, json=data, verify=False)
    except requests.exceptions.RequestException as err:
        print(f'Error sending to Wangen: {err}')
    
    print(f"Sending to Wangen DRK")
    data['sender'] = sconf.alamos_remote_secondary_sender
    data['authorization'] = sconf.alamos_remote_secondary_auth
    try:
        requests.post(sconf.alamos_remote_secondary_stats_endpoint, json=data, verify=False)
    except requests.exceptions.RequestException as err:
        print(f'Error sending to Wangen DRK: {err}')

def main_listener():
    conf = settings.get_settings()

    print(f"Starting status listener on DB ...")
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        conn = psycopg2.connect(database=conf.db_name,
                                host=conf.db_host,
                                user=conf.db_user,
                                password=conf.db_password,
                                port=conf.db_port,
                                connect_timeout=5)
        
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = conn.cursor()
        cursor.execute("LISTEN status_notification")
    except psycopg2.Error as e:
        print(f"DB Error, Code: {e.pgcode} Error: {e.pgerror}")
        return -1
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