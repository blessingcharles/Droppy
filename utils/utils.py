import os , glob

def recursive_dir_search(directory_path : str , extension : str = ".js"):
    result = []

    for x in os.walk(directory_path):
        for y in glob.glob(os.path.join(x[0], f'*{extension}')):
            result.append(y)

    return result
