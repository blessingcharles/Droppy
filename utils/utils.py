from logging import error
import os , glob , csv
import signal
import sys

def recursive_dir_search(directory_path : str , extension : str = ".js"):
    result = []

    for x in os.walk(directory_path):
        for y in glob.glob(os.path.join(x[0], f'*{extension}')):
            result.append(y)

    return result

def dir_create(dirname):

    pwd = os.getcwd()

    new_dir_path = os.path.join(pwd,dirname)
    print(new_dir_path)
    if not os.path.exists(new_dir_path):
        try:
            os.mkdir(new_dir_path)
            return new_dir_path
        except error as e:
            print(e)
            pass

    return new_dir_path

def dict_to_csv_writer(dictionary : dict , file_path : str):
    headers = ["name" , "count"]

    with open(file_path , "w") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for key , value in dictionary.items():
            writer.writerow([key,value])


def signal_handler(sig, frame):
    print('You pressed [Ctrl+C] : ( ')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

