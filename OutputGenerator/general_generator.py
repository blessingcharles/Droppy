import pandas as pd

from utils.utils import dir_create, recursive_dir_search

class GeneralOutputGenerator:
    def __init__(self, output , csv_dir)->None:
        self.output = output
        self.csv_dir = csv_dir

        self.json_output_path = f"{self.output}/json_output"
        self.xml_output_path = f"{self.output}/xml_output_path"

    def generate_json(self):
        self.files = recursive_dir_search(self.csv_dir , extension=".csv")
        dir_create(self.json_output_path)

        for file in self.files:
            
            file_name = file.rsplit("/")[-1][:-4]
            file_name += ".json"

            df = pd.read_csv(file)

            json_data = df.to_json()
            
            with open(f"{self.json_output_path}/{file_name}" , "w") as f:
                f.write(json_data)

    def generate_xml(self):
        self.files = recursive_dir_search(self.csv_dir , extension=".csv")
        dir_create(self.xml_output_path)

        for file in self.files:
            
            file_name = file.rsplit("/")[-1][:-4]
            file_name += ".xml"

            df = pd.read_csv(file)

            xml_data = df.to_xml()
            
            with open(f"{self.xml_output_path}/{file_name}" , "w") as f:
                f.write(xml_data)

    def generate_all(self):
        self.generate_json()
        self.generate_xml()
        