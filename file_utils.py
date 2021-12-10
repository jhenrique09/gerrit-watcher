import re

def load_file(path):
    with open(path) as f:
        data = f.read()
    return data

def write_file(data, path):
    with open(path, 'w') as f:
        f.write(data)

def get_file_path(status, gerrit_url):
    file_name = re.sub('[^0-9a-zA-Z]', '', gerrit_url.replace('http://', '').replace('https://', ''))
    return 'data/' + status + '_' + file_name + '.json'