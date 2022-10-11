#! /usr/bin/env python3

import os
import re
import requests

def get_files_in_dir(dir_path):
    """return target files in a list"""
    items_list = os.listdir(dir_path)
    item =""
    files_list = []
    for item in items_list:
        # check isfile txt
        if os.path.isfile(os.path.join(dir_path, item)):
            if re.search(r"\.txt", os.path.join(dir_path, item)) != None:
                files_list.append(item)

    # check  print(files_list)
    return files_list

def extact_content(file_path):
    """ create a dictionary by keeping title, name, date, and feedback as keys """
    content_dict = {}
    with open(file_path, 'r') as f:
        content_dict["title"] = f.readline().strip()
        content_dict["name"] = f.readline().strip()
        content_dict["date"] = f.readline().strip()
        content_dict["feedback"] = f.read().strip()

    return content_dict


def post_the_dict(content_list, ip):
    """ to the company's website through requests module """
    # http://<corpweb-external-IP>/feedback
    response = requests.post("http://"+ip+"/feedback/", json=content_list)
    print(response.ok)
    print(response.status_code)

def main():
    """ make sure an error message isn't returned """
    dir = ""
    while True:
        dir = os.path.abspath(input("please enter the directory: "))
        print(dir)
        if os.path.isdir(dir):
            print("directory valid")
            break
        else:
            print("directory invalid")

    files_list = get_files_in_dir(dir)

    content_list = []

    for file in files_list:
        print(os.path.join(dir, file))
        content_list.append(extact_content(os.path.join(dir, file)))

    # check print(content_list)

    ip = input("please enter the ip: ")
    response = requests.get("http://"+ip)
    if response.ok:
        for content in content_list:
            post_the_dict(content, ip)

if __name__ == "__main__":
    main()
