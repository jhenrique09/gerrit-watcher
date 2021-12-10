import os
import traceback
import sys
from gerrit_utils import *
from file_utils import *
from json_utils import *
from telegram_utils import *
from time import sleep

def main():
    global gerrit_url, status_to_listen
    if not os.path.exists('data'):
        os.mkdir('data')
    gerrit_url = os.getenv('GERRIT_URL').rstrip('/')
    if os.getenv('GERRIT_STATUS_TO_LISTEN'):
        status_to_listen = os.getenv('GERRIT_STATUS_TO_LISTEN').split(";")
    else:
        status_to_listen = ['open', 'merged', 'abandoned']
    while True:
        loop()
        sleep(60)


def loop():
    for status in status_to_listen:
        path = get_file_path(status, gerrit_url)
        print('Obtaining changes with \'' + status + '\' status from ' + gerrit_url)
        try:
            json_data = get_changes(gerrit_url, status)
            if not validate_json(json_data):
                raise Exception('Failed to parse json')
            if os.path.exists(path):
                print('Checking diffs')
                for text in parse_diffs(gerrit_url, status, diff_changes(json_data, load_file(path))):
                    print('Sending telegram message')
                    send_tg_message(text)
                write_file(json_data, path)
            else:
                print('Creating new file...')
                write_file(json_data, path)
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            traceback.print_exc()


if __name__ == "__main__":
    main()
