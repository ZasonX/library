
# TODO GUI 介面
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

#TODO: badge
# alg:
# 建立 global badge 圖庫
# 使用前維護圖庫
# 圖庫另存
# 建立 實況主 頻道圖庫
# 同上
# 建立 markdown 時可將 data:image/png;改為讀取圖庫
# https://badges.twitch.tv/v1/badges/global/display
# "https://badges.twitch.tv/v1/badges/channels/{streamerId}/display"
# import base64
# import requests
# def get_as_base64(url):
#     return base64.b64encode(requests.get(url).content)

'''
    Configs
'''
# target folder (workspace)


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
DICT_yaml_files = {}

'''
    Functions
'''


def dump_into_yaml_file(folder_path, file_name):
    """
    Convert a python object into yaml

    Args:
        folder_path (string): base folder path
        file_name (string): name of file with the path

    """
    json_file = folder_path / (file_name + ".json")

    with open(json_file, "r", encoding="utf-8") as f:
        # load json file into a python object
        data = json.load(f)

    yaml_file_path = folder_path / "out"
    yaml_file = yaml_file_path / (file_name + ".yaml")
    with open(yaml_file, 'w') as f:
        yaml.dump(data, f)


def translate_to_markdown(folder_path, file_name):
    """
    translate chat json file into a markdown file for human to read

    Args:
        folder_path (string): base folder path
        file_name (string): name of file with the path

    """
    json_file = folder_path / (file_name + ".json")
    with open(json_file, "r", encoding="utf-8") as f:
        # load json file into a python object
        data = json.load(f)

    # 準備寫入
    markdown_file_path = folder_path / "out"
    markdown_file = markdown_file_path / (file_name + ".md")
    with open(markdown_file, "w", encoding="utf-8") as f:
        # data['emotes']
        # Iterating through the json
        # list
        for row in data['comments']:
            """
                一行一行的聊天訊息
            """
            # 時間戳記
            offset_seconds = row['content_offset_seconds']
            timeStamp = time.strftime('%H:%M:%S', time.gmtime(offset_seconds))
            f.write(f' {timeStamp} ')

            # 使用者名稱
            name = row['commenter']['display_name']
            user_color = row['message']['user_color']
            f.write(f'<span style="color:{user_color}">{name}</span>: ')

            # since 1.51.1
            # embeddedData instead of emotes
            if data['embeddedData']:
                emotes = data['embeddedData']
            elif data['emotes']:
                emotes = data['emotes']
            else:
                emotes = None

            if emotes:
                if row['message']['fragments']:
                    for fragment in row['message']['fragments']:
                        if fragment['emoticon']:
                            emoticon_id = fragment['emoticon']['emoticon_id']

                            img_data_in_firstParty = [img["data"] for img in emotes
                                                      ['firstParty'] if img["id"] == emoticon_id]
                            img_data_in_thirdParty = [img["data"] for img in emotes
                                                      ['thirdParty'] if img["id"] == emoticon_id]

                            image_data = img_data_in_firstParty[0] if img_data_in_firstParty[
                                0] else img_data_in_thirdParty[0]

                            message = "![](data:image/png;base64,%s)" % image_data
                            f.write(message)
                        else:
                            message = fragment['text']
                            message = message.replace("*", "\*")
                            message = message.replace("~", "\~")
                            message = message.replace("_", "\_")
                            f.write(message)
                else:
                    message = row['message']['body']
                    message = message.replace("*", "\*")
                    message = message.replace("~", "\~")
                    message = message.replace("_", "\_")
                    f.write(message)
            else:
                message = row['message']['body']
                message = message.replace("*", "\*")
                message = message.replace("~", "\~")
                message = message.replace("_", "\_")
                f.write(message)

            f.write('  \n')


'''
    Main Code
'''
print('program start ...\n')
# src
# JSON files
for file_name in listdir(consts.FOLDER_PATH):
    file = consts.FOLDER_PATH / file_name
    if isfile(file):
        if file_name[-5:] == ".json":
            DICT_json_files[file_name[:-5]] = True

# dst
src_folder = consts.FOLDER_PATH / "out"
for file_name in listdir(src_folder):
    file = src_folder / file_name
    if isfile(file):
        # print(f'checking for {file_name} ...\n')
        # markdown outputs
        # print('markdown file ...')
        if file_name[-3:] == ".md":
            # print('check!')
            DICT_markdown_files[file_name[:-3]] = True
        # else:
            # print('missing :(')
        # print(f'\n')

        # yaml outputs
        # print('yaml file ...')
        if file_name[-5:] == ".yaml":
            # print('check!')
            DICT_yaml_files[file_name[:-5]] = True
        # else:
            # print('missing :(')
        # print(f'\n')

# generate output files
for file_name in DICT_json_files:
    if file_name not in DICT_markdown_files:
        print(f'generating markdown files: {file_name} ....')
        translate_to_markdown(consts.FOLDER_PATH, file_name)
        print(f'done\n')
    if file_name not in DICT_yaml_files:
        print(f'generating yaml files: {file_name} ....')
        dump_into_yaml_file(consts.FOLDER_PATH, file_name)
        print(f'done\n')

print('finish\n')
input("Press Enter to continue...")
