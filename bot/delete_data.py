import shutil
import os

def delete_file(fpath):
    print(f'Deleting file {fpath}')
    try:
        os.remove(fpath)
        print(f"{fpath} removed successfully")
    except OSError as error:
        print(error)
        print("File path can not be removed")

def delete_folder(folder_path):
    print(f'Deleting Folder {folder_path}')
    try:
        shutil.rmtree(folder_path)
        print(f"{folder_path} removed successfully")
    except OSError as error:
        print(error)
        print("File path can not be removed")

def delete(fpath, folder_path):
    print(f'Deleting...')
    delete_folder(folder_path=folder_path)
    delete_file(fpath=fpath)