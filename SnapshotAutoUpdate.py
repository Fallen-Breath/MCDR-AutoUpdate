# -*- coding: utf-8 -*-
import os
import urllib
import filecmp
import shutil
import json

version_check_path = './plugins/AutoUpdate/Current_Version.json'
empty_list = {}

def on_server_startup(server):
    urllib.request.urlretrieve('https://launchermeta.mojang.com/mc/game/version_manifest.json', 'versions_new.json')
    if not os.path.exists(version_check_path):
        os.mkdir('./plugins/AutoUpdate')
        with open(version_check_path, 'w') as f:
            json.dump(empty_list, f, indent=4)
        server.stop()
        server_update(server)
        server.start()
        if os.path.exists('versions_new.json'):
            os.remove('versions_new.json')
    elif not filecmp.cmp('versions_new.json', version_check_path):
        server.stop()
        server_update(server)
        server.start()
        if os.path.exists('versions_new.json'):
            os.remove('versions_new.json')
    else:
        os.remove('versions_new.json')
        server.logger.info('[AutoUpdate] Update Check Success, No New Version Exists')

def server_update(server):
    shutil.copy2('versions_new.json', version_check_path)
    with open(version_check_path) as versions_file:
            versions = json.load(versions_file)
    version = versions["latest"]["snapshot"]
    server.logger.info('[AutoUpdate] Current Version is {}, Updating...'.format(version))
    version_json = ''
    with open(version_check_path) as versions_file:
        versions = json.load(versions_file)

    for version_entry in versions["versions"]:
        if version_entry["id"] == version and version_entry["type"] == "snapshot":
            version_json = version_entry["url"]
            break

    if version_json is not '':
        urllib.request.urlretrieve(version_json, 'server.json')
        with open('server.json') as version_file:
            version_json_file = json.load(version_file)
            server_url = version_json_file["downloads"]["server"]["url"]
    urllib.request.urlretrieve(server_url, 'server/server.jar')
    os.remove('server.json')