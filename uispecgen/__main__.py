import os
import glob
import uuid
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from pydrawio.mxfile import Mxfile
from pydrawio.mxgraphmodel import decompress
from uilayout.uidiagram import UiDiagram
from excel.uispec import UiSpec

load_dotenv()
files = glob.glob('./input/*.drawio')

for file in files:
    mxfile = Mxfile()
    with open(file) as diofile:
        mxfile = Mxfile(diofile.read())
        # TODO: Multi Diagram support
        diagram = mxfile.diagram[0]
        uid = UiDiagram(diagram)
        mxfile.diagram[0].value = uid.set_numbering()

        fileid = uuid.uuid4()
        diofile_path = '{}/{}.drawio'.format(os.getenv('TMP_DIR'), fileid)
        mxfile.write(diofile_path)
        uispec = UiSpec('./output/{}.xlsx'.format(fileid))
        uispec.set_header()
        uispec.insert_image(diofile_path)

        component_info_list = uid.get_component_info()
        uispec.set_footer(component_info_list)
        uispec.close_workbook()
