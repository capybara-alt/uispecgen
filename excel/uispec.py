import os
import uuid
import xlsxwriter
from typing import Tuple, List
from .componentInfo import ComponentInfo
from .iuispec import IUispec

class UiSpec(IUispec):
    header_common: xlsxwriter.format
    header_bg: xlsxwriter.format

    def __init__(self, filepath: str):
        super().__init__(filepath)
        self.image_insert_cell = 'A12'
        self.sheet.set_column('A:I', 15)
        self.header_common = self.workbook.add_format({'border_color': '000000', 'border': 1})
        self.header_bg = self.workbook.add_format({ 'locked': True, 'bg_color': '999999', 'border_color': '000000', 'border': 1})

    def set_header(self):
        self.sheet.merge_range('A1:I1', '画面レイアウト定義', self.header_bg)
        self.sheet.merge_range('A2:A6', '共通情報', self.header_bg)
        self.sheet.merge_range('A7:A9', '書誌情報', self.header_bg)
        self.sheet.merge_range('A10:I10', 'レイアウト図', self.header_bg)
        self.sheet.write('B2', 'プロジェクト名', self.header_bg)
        self.sheet.write('B3', 'システム名', self.header_bg)
        self.sheet.write('B4', '工程名', self.header_bg)
        self.sheet.write('B5', 'ドキュメントID', self.header_bg)
        self.sheet.write('B6', 'ドキュメント名', self.header_bg)
        self.sheet.merge_range('C2:E2', '', self.header_common)
        self.sheet.merge_range('C3:E3', '', self.header_common)
        self.sheet.merge_range('C4:E4', '', self.header_common)
        self.sheet.merge_range('C5:E5', '', self.header_common)
        self.sheet.merge_range('C6:E6', '', self.header_common)
        self.sheet.write('F2', '作成者', self.header_bg)
        self.sheet.write('F3', '作成日付', self.header_bg)
        self.sheet.write('F4', 'バージョン', self.header_bg)
        self.sheet.write('F5', '更新者', self.header_bg)
        self.sheet.write('F6', '更新日付', self.header_bg)
        self.sheet.merge_range('G2:I2', '', self.header_common)
        self.sheet.merge_range('G3:I3', '', self.header_common)
        self.sheet.merge_range('G4:I4', '', self.header_common)
        self.sheet.merge_range('G5:I5', '', self.header_common)
        self.sheet.merge_range('G6:I6', '', self.header_common)
        self.sheet.write('B7', '画面ID', self.header_bg)
        self.sheet.write('B8', '画面名称', self.header_bg)
        self.sheet.write('B9', '概要', self.header_bg)
        self.sheet.merge_range('C7:I7', '', self.header_common)
        self.sheet.merge_range('C8:I8', '', self.header_common)
        self.sheet.merge_range('C9:I9', '', self.header_common)

    def insert_image(self, dio_filepath: str):
        filename = os.path.basename(dio_filepath)
        filename = filename.replace('.drawio', '.png', 1)
        drawio_exacutable = os.environ['DRAW_IO_PATH']
        os.system('{}/draw.io -x -f jpg -o /tmp/{} {}'.format(drawio_exacutable, filename, dio_filepath))
        self.sheet.insert_image('A12', '/tmp/{}'.format(filename), {'x_scale': 0.5, 'y_scale': 0.5})

    def set_footer(self, component_info_list: List[ComponentInfo]):
        self.sheet.merge_range('A45:I45', '使用する部品', self.header_bg)
        self.sheet.merge_range('A46:I46', '', self.header_common)
        self.sheet.write('A47', '識別ID', self.header_bg)
        self.sheet.merge_range('B47:C47', 'ラベル', self.header_bg)
        self.sheet.merge_range('D47:E47', '画面部品の種類', self.header_bg)
        self.sheet.write('F47', '表示範囲', self.header_bg)
        self.sheet.merge_range('G47:I47', '画面部品の説明', self.header_bg)
        for index, component_info in enumerate(component_info_list):
            offset = index + 48
            self.sheet.write('A{}'.format(offset), index + 1)
            self.sheet.merge_range('B{0}:C{0}'.format(offset), component_info.name)
            self.sheet.merge_range('D{0}:E{0}'.format(offset), component_info.component_type)
            self.sheet.write('F{}'.format(offset), component_info.display_range)
            self.sheet.merge_range('G{0}:I{0}'.format(offset), component_info.description)

    def close_workbook(self):
        self.workbook.close()
