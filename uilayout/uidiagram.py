import re
import xml.etree.ElementTree as ET
from typing import List
from pydrawio.mxfile import Diagram
from pydrawio.mxgraphmodel import MxGraphModel, decompress, Object
from numbering.numbering_model import NumberingModel
from exception.numbering import InvalidIdError
from excel.componentInfo import ComponentInfo

class UiDiagram:
    __mxgraphmodel: MxGraphModel

    def __init__(self, diagram: Diagram):
        self.__mxgraphmodel = decompress(diagram.value)

    def get_seq_id(self) -> str:
        ids = self.__mxgraphmodel.get_ids()
        ids = filter(lambda id: id, ids)
        id_nums = []
        for id in ids:
            splitted = id.split('-')
            if len(splitted) == 2 and re.match('[0-9]{1,}', splitted[1]):
                id_nums.append(int(splitted[1]))
            elif len(splitted) == 1 and re.match('[0-9]{1,}', splitted[0]):
                id_nums.append(int(splitted[0]))
            else:
                raise InvalidIdError()

        return str(max(id_nums) + 1)

    def set_numbering(self) -> str:
        objects = filter(lambda item: isinstance(item, Object), self.__mxgraphmodel.content.items)
        for index, item in enumerate(objects):
            nmodel = NumberingModel()
            nmodel.set_target_id(item.id)
            nmodel.set_numbering_model_value(str(index + 1))
            nmodel.set_grouped_model_id(self.get_seq_id())
            group, number, line = nmodel.get_numbering_model()
            self.__mxgraphmodel.content.items.append(group)
            self.__mxgraphmodel.content.items.append(number)
            self.__mxgraphmodel.content.items.append(line)

        return self.__mxgraphmodel.compress()

    def get_component_info(self) -> List[ComponentInfo]:
        objects = filter(lambda item: isinstance(item, Object), self.__mxgraphmodel.content.items)
        return [ ComponentInfo(item) for item in objects ]
