import json
import requests
import urllib.parse
from pathlib import Path
from jinja2 import Template

def get_change_by_id(id, changes):
    change = list(filter(lambda d: d['id'] == id, changes))
    if len(change) > 0:
        return change[0]
    else:
        return None

def diff_changes(new_json, local_json):
    new_json = json.loads(new_json)
    local_json = json.loads(local_json)
    diffs = {}
    for change in new_json:
        change_found = get_change_by_id(change['id'], local_json)
        if not change_found:
            if change['project'] not in diffs:
                diffs[change["project"]] = {}
            if change["branch"] not in diffs.get(change["project"]):
                diffs[change["project"]][change["branch"]] = []
            diffs[change["project"]][change["branch"]].append(change)
            print('Found change: ' + change['project'] + ' (' + change['branch'] + ' branch) - ' + change['subject'])
    return diffs

def get_changes(gerrit_url, status):
    max_changes = 5000
    url = '{0}/changes/?q=status:{1}&n={2}'.format(gerrit_url, status, max_changes)
    return requests.get(url).text.lstrip(')]}\'')

def get_account_info(gerrit_url, account_id):
    url = '{0}/accounts/{1}'.format(gerrit_url, account_id)
    return json.loads(requests.get(url).text.lstrip(')]}\''))

def parse_diffs(gerrit_url, status, diffs):
    project_url = "{0}/q/project:{1}+branch:{2}+status:{3}"
    max_changes = 10
    texts = []
    if diffs:
        template_data = {}
        template_data["max_changes"] = max_changes
        template_data["status"] = status
        template_data["gerrit_url"] = gerrit_url
        for project, branch_dict in diffs.items():
            for branch_name, branch_changes in branch_dict.items():
                template_data["changes_length"] = len(branch_changes)
                branch_changes = branch_changes[:max_changes]
                template_data["project"] = project
                template_data["project_url"] = project_url.format(gerrit_url, urllib.parse.quote_plus(project), urllib.parse.quote_plus(branch_name), status)
                template_data["branch"] = branch_name
                template_data["changes"] = branch_changes
                for change in branch_changes:
                    change["subject_sanitized"] = change["subject"].replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
                    account_info = get_account_info(gerrit_url, change["owner"]["_account_id"])
                    if account_info["username"] != account_info["name"]:
                        change["account_name"] = '{0} ({1})'.format(account_info["name"], account_info["username"])
                    else:
                        change["account_name"] = account_info["username"]
                texts.append(Template(Path("templates/event.html").read_text(), trim_blocks=True).render(template_data))
    else:
        print("No diffs for status: " + status)
    return texts
