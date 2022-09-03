# # First things, first. Import the wxPython package.
# import wx

# # Next, create an application object.
# app = wx.App()

# # Then a frame.
# frm = wx.Frame(None, title="Hello World")

# # Show it.
# frm.Show()

# # Start the event loop.
# app.MainLoop()

# # import wx; a=wx.App(); wx.Frame(None, title="Hello World").Show(); a.MainLoop()
# Python program to read
# json file


from pathlib import Path
import yaml
import json
import time
from os import listdir
from os.path import isfile

'''
    Configs
'''
# target folder (workspace)
import sys


class Const(object):
    """
        Manually reconstruct an usage of constant variables
    """
    def ConstError(TypeException, text):
        print(text)
        pass

    def __setattr__(self, key, value):
        if self.__dict__.has_key(key):
            raise self.ConstError("Changing const.%s", key)
        else:
            self.__dict__[key] = value

    def __getattr__(self, key):
        if self.__dict__.has_key(key):
            return self.key
        else:
            return None

    # constant variables
    # You can use os.path.abspath() to convert it:
    FOLDER_PATH = Path(r"C:\Users\Jason\Downloads\TwitchDownloader\chat")


consts = Const()


'''
    Global Variables
'''
DICT_json_files = {}
DICT_markdown_files = {}

'''
    Functions
'''


def dump_into_yaml_file(data, file):
    """
    Convert a python object into yaml

    Args:
        data (any): python objected data
        file (string): file name with full path

    """
    # bonus, convert json into yaml
    with open(file, 'w') as f:
        yaml.dump(data, f)


def translate_to_markdown(folder_path, file_name):
    json_file = folder_path / (file_name + ".json")
    print(json_file)
    f = open(json_file, "r", encoding="utf-8")

    # returns JSON object as a dictionary
    data = json.load(f)

    # Close reading file
    f.close()
    markdown_file_path = folder_path / "out"
    markdown_file = markdown_file_path / (file_name + ".md")
    f = open(markdown_file, "w", encoding="utf-8")

    # Iterating through the json
    # list
    for row in data['comments']:
        offset_seconds = row['content_offset_seconds']
        timeStamp = time.strftime('%H:%M:%S', time.gmtime(offset_seconds))

        name = row['commenter']['display_name']
        msg = row['message']['body'].replace("*", "\*")
        user_color = row['message']['user_color']
        # f.write(f'[{timeStamp}][{name}]: {msg}')
        f.write(f' {timeStamp} ')
        f.write(f'<span style="color:{user_color}">{name}</span>: {msg}')
        f.write('  \n')

    f.close()

    # bonus, dump into a yaml file
    yaml_file_path = folder_path / "out"
    yaml_file = yaml_file_path / (file_name + ".yaml")
    dump_into_yaml_file(data, yaml_file)


'''
    Main Code
'''
# src
# JSON files
for file_name in listdir(consts.FOLDER_PATH):
    file = consts.FOLDER_PATH / file_name
    if isfile(file):
        if file_name[-5:] == ".json":
            print(file)
            DICT_json_files[file_name[:-5]] = True

# dst
# markdown outputs
src_folder = consts.FOLDER_PATH / "out"
for file_name in listdir(src_folder):
    file = consts.FOLDER_PATH / file_name
    if isfile(file):
        if file_name[-3:] == ".md":
            DICT_markdown_files[file_name[:-3]] = True

# generate output files
for file_name in DICT_json_files:
    if file_name not in DICT_markdown_files:
        print(f'generating files: {file_name} ....')
        translate_to_markdown(consts.FOLDER_PATH, file_name)
        print(f'done\n')

print('finish\n')
input("Press Enter to continue...")
