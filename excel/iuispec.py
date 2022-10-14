import os
import xlsxwriter
from abc import ABCMeta
from typing import List
from .componentInfo import ComponentInfo

class IUispec(metaclass=ABCMeta):
    workbook: xlsxwriter.Workbook
    sheet: xlsxwriter.worksheet.Worksheet
    image_insert_cell: str

    def __init__(self, filepath: str):
        self.workbook = xlsxwriter.Workbook(filepath)
        self.sheet = self.workbook.add_worksheet()

    def insert_image(self, dio_filepath: str):
        filename = os.path.basename(dio_filepath)
        filename = filename.replace('.drawio', '.png', 1)
        drawio_exacutable = os.environ['DRAW_IO_PATH']
        os.system('{} -x -f jpg -o {}/{} {}'.format(os.getenv('DRAWIO_EXECUTABLE'), os.getenv('TMP_DIR'), filename, dio_filepath))
        self.sheet.insert_image(self.image_insert_cell, '/tmp/{}'.format(filename), {'x_scale': 0.5, 'y_scale': 0.5})
    
    def set_header(self):
        raise NotImplementedError

    def set_footer(self, component_info_list: List[ComponentInfo]):
        raise NotImplementedError

    def close_workbook(self):
        self.workbook.close()
