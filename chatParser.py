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


import json, time
from pkgutil import extend_path
# from time import strftime,gmtime
from os import listdir
from os.path import isfile, join

# Opening JSON file
folderPath = './'


def translateToMarkdown(folderPath, fileName):
    filePath = join(folderPath, fileName)
    f = open(filePath + ".json", "r", encoding="utf-8")

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Closing file
    f.close()

    f = open(filePath + ".md", "w", encoding="utf-8")

    # Iterating through the json
    # list
    for row in data['comments']:
        offsetSeconds = row['content_offset_seconds']
        timeStamp = time.strftime('%H:%M:%S', time.gmtime(offsetSeconds))

        name = row['commenter']['display_name']
        msg = row['message']['body'].replace("*", "\*")
        userColor = row['message']['user_color']
        # f.write(f'[{timeStamp}][{name}]: {msg}')
        f.write(f' {timeStamp} ')
        f.write(f'<span style="color:{userColor}">{name}</span>: {msg}')
        f.write('  \n')

    f.close()


jsonFiles = {}
markdownFiles = {}

for fileName in listdir(folderPath):
    fullPathFileName = join(folderPath, fileName)
    if isfile(fullPathFileName):
        if fileName[-5:] == ".json":
            jsonFiles[fileName[:-5]] = True
        elif fileName[-3:] == ".md":
            markdownFiles[fileName[:-3]] = True

for fileName in jsonFiles:
    if fileName not in markdownFiles:
        print(f'generating files: {fileName} ....')
        translateToMarkdown(folderPath, fileName)
        print(f'done\n')

print('finish\n')
input("Press Enter to continue...")