from hdmf.utils import docval, popargs

from pynwb import get_class

MicroscopyTable = get_class("MicroscopyTable", "ndx-microscopy")


@docval(
    {"name": "region", "type": list, "doc": "the indices of the MicroscopyTable"},
    {"name": "description", "type": str, "doc": "a brief description of what these table entries represent"},
)
def create_microscopy_table_region(self, **kwargs):
    region, description = popargs("region", "description", kwargs)
    name = "microscopy_table_region"
    return super(MicroscopyTable, self).create_region(name=name, region=region, description=description)


MicroscopyTable.create_microscopy_table_region = create_microscopy_table_region
