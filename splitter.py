import os


def filetype(file_name):
    split = os.path.splitext(file_name)
    extension = split[1]
    if extension == ".docx":
        return 0
    elif extension == ".pdf":
        return 1
    elif extension == ".doc":
        return 2
    elif extension == ".txt":
        return 3
    elif extension == ".html":
        return 4
    else:
        return 5
