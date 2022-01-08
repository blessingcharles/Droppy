import pandas as pd

from utils.utils import recursive_dir_search


class HtmlGenerator:
    def __init__(self,output : str , path="droppy_output/csv_output") -> None:
        self.output = output
        self.path = path

        self.html_output = f"{self.output}/output.html"
        
        self.html_template_path = "DroopyBrain/html_template.html"
        self.js_template_path = "DroopyBrain/js_template.js"

    def generate(self):

        self.files = recursive_dir_search(self.path , extension=".csv")

        html_doc = ''''''

        with open(self.html_template_path , "r") as f:
            for line in f.readlines():
                html_doc += line

        for file in self.files:
            
            heading : str = file.rsplit("/")[-1][:-4]
            heading.upper()

            html = f'''\n<h3 class="table-header table-header--expanded"><button class="header-button">{heading}</button></h3>'''
           
            table_start ='''<table class="table--expanded">'''
            
            df_table_start = '''<table border="1" class="dataframe">'''
            df_tr_html = '''<tr style="text-align: right;">'''


            df = pd.read_csv(file)


            df_html = df.to_html()

            df_html = df_html.replace(df_table_start , table_start)
            df_html = df_html.replace(df_tr_html , '''<tr>''')

            html += df_html

            html_doc += html

        with open(self.js_template_path , "r") as f:
            js_doc  = f.read()

        script_doc = "\n<script defer>" + js_doc + "</script>\n"
        html_doc += script_doc

        with open(self.html_output , "w") as f:
            f.write(html_doc)

            