import re
import xml.etree.ElementTree as ET
from pydrawio.mxgraphmodel import MxCell
from exception import numbering
from .contants import _NUMBERING_PARTS_GROUP_MX_CELL, _SURROUNDED_NUMBER_WITH_CIRCLE_MX_CELL, _LINE_MX_CELL
from typing import Tuple

class NumberingModel:
    ''' NumberingModel
    draw.io component for numbering target component
    '''

    __npg_mxcell: MxCell
    __snwc_mxcell: MxCell
    __l_mxcell: MxCell

    def __init__(self):
        self.__npg_mxcell = MxCell(ET.fromstring(_NUMBERING_PARTS_GROUP_MX_CELL))
        self.__snwc_mxcell = MxCell(ET.fromstring(_SURROUNDED_NUMBER_WITH_CIRCLE_MX_CELL))
        self.__l_mxcell = MxCell(ET.fromstring(_LINE_MX_CELL))

    def set_target_id(self, id: str):
        ''' set_target_id
        set numbering target component id
        Args:
            id (str): target component id
        '''

        self.__npg_mxcell.parent = id
        self.__l_mxcell.target = id

    def set_numbering_model_value(self, value: str):
        ''' set_numbering_model_value
        set numbering value displayed in circle
        Args:
            value (str): numbering value
        '''

        self.__snwc_mxcell.value = value

    def set_grouped_model_id(self, id: str):
        ''' set_grouped_model_id
        set numbering component id (cannot duplicate other draw.io component id)
        Args:
            id (str): numbering component id
        Raises:
            InvalidIdError: id is not int or format id not {str}-{int}
        '''

        self.__validate_id(id)

        seq_num = 0
        if len(id.split('-')) == 1:
            seq_num = int(id)
        else:
            seq_num = int(id.split('-')[1])

        self.__npg_mxcell.id = str(seq_num)
        self.__snwc_mxcell.id = str(seq_num + 1)
        self.__l_mxcell.id = str(seq_num + 2)

    def get_numbering_model(self) -> Tuple[MxCell]:
        ''' get_numbering_model
        after set id and value, get completed numbering model
        Returns:
            Tuple[MxCell]: numbering parts group MxCell, surrounded number with circle MxCell, line MxCell
        '''

        self.__snwc_mxcell.parent = self.__npg_mxcell.id
        self.__l_mxcell.source = self.__snwc_mxcell.id
        self.__l_mxcell.parent = self.__snwc_mxcell.id

        return self.__npg_mxcell, self.__snwc_mxcell, self.__l_mxcell

    def __validate_id(self, id: str):
        if re.match('[0-9]{1,}', id):
            return

        splitted = id.split('-')
        if len(splitted) > 1 or not re.match('[0-9]{1,}', splitted[1]):
            raise numbering.InvalidIdError()
