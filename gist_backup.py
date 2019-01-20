#!env python

# Note: if you are in China, you should make sure your shell can't visit
# foreign websites, otherwise you may fail to use git api

import argparse
import urllib
import json
import requests
import os
from datetime import datetime
from urllib.request import urlopen

parser = argparse.ArgumentParser(description='Pull gists from github')
parser.add_argument('git_account', type=str,
                    help="Specify the github account name you want pull gist")
parser.add_argument('-p', '--perpage', default=30, type=int,
                    help="Specify the number of entries per page")
parser.add_argument('-i', '--information_file', default='./gist_information.json',
                    type=str, help="The file of storing gist informations ")
opt = parser.parse_args()

user = opt.git_account
perpage = opt.perpage
information_file = opt.information_file

print('github user:', user)
root_url = 'https://api.github.com/users/'+user
userurl = urlopen(root_url)

public_gists = json.load(userurl)
gistcount = public_gists['public_gists']
print(f'Found gists : {gistcount}')
pages = (gistcount-1) // perpage + 1
print(f"Found pages : {pages}")

# dir '.' is the directory of running this script
# not the directory where script in
if os.path.exists(information_file):
    with open(information_file, 'r') as f:
        gist_information = json.load(f)
else:
    gist_information = dict()

update_information = dict()
files_counter = 0

for page in range(pages):
    print(f"Processing page number {page+1} ...")
    pageUrl = root_url + '/gists?page=' + str(page+1)
    gisturl = urlopen(pageUrl)
    gist_entries = json.load(gisturl)
    for gist_info in gist_entries:
        files_counter += 1

        gist_file = gist_info['files']
        gist_file_name = list(gist_file.keys())[0]
        gist_file_raw_url = gist_file[gist_file_name]['raw_url']

        gist_updated_time = gist_info['updated_at']
        gist_file_description = gist_info['description']

        update_information[gist_file_name] = {
                'updated_at': gist_updated_time,
                'description': gist_file_description
            }
        if (gist_file_name in gist_information and
                gist_information[gist_file_name]['updated_at'] == gist_updated_time):
            print(f'No.{files_counter} file {gist_file_name} is up to date')
            del gist_information[gist_file_name]
        else:
            if gist_file_name in gist_information:
                del gist_information[gist_file_name]
            print(f"No.{files_counter} file {gist_file_name} is updating...", end= ' ')
            gist_content = requests.get(gist_file_raw_url).text
            with open(gist_file_name, 'w') as f:
                f.write(gist_content)
            print('OK')

for gist_file_name in gist_information:
    if os.path.exists(os.path.join('.', gist_file_name)):
        os.remove(os.path.join('.', gist_file_name))
        print(f'File "{gist_file_name}" is deleted')

with open(information_file, 'w') as f:
    json.dump(update_information, f)

print('Complete backup')
