import os

import process
import splitter

path = os.getcwd()
file_names = os.listdir(path)
data = {}

for name in file_names:
    file_type = splitter.filetype(name)
    if file_type != 5:
        data[name.split(".")[0]] = file_type
        process.process(file_type, name)

print(data)
