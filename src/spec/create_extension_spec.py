# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec
# TODO: import other spec classes as needed
# from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""An example extension to demonstrate the TAB proposal for enhancements to optical physiology neurodata types.""",
        name="""ndx-microscopy""",
        version="""0.1.0""",
        author=list(map(str.strip, """Cody Baker and Alessandra Trapani""".split(','))),
        contact=list(map(str.strip, """cody.baker@catalystneuro.com""".split(',')))
    )

    # TODO: specify the neurodata_types that are used by the extension as well
    # as in which namespace they are found.
    # this is similar to specifying the Python modules that need to be imported
    # to use your new data types.
    # all types included or used by the types specified here will also be
    # included.
    ns_builder.include_type('ElectricalSeries', namespace='core')

    # TODO: define your new data types
    # see https://pynwb.readthedocs.io/en/latest/extensions.html#extending-nwb
    # for more information
    tetrode_series = NWBGroupSpec(
        neurodata_type_def='TetrodeSeries',
        neurodata_type_inc='ElectricalSeries',
        doc=('An extension of ElectricalSeries to include the tetrode ID for '
             'each time series.'),
        attributes=[
            NWBAttributeSpec(
                name='trode_id',
                doc='The tetrode ID.',
                dtype='int32'
            )
        ],
    )

    # TODO: add all of your new data types to this list
    new_data_types = [tetrode_series]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)
    print('Spec files generated. Please make sure to rerun `pip install .` to load the changes.')


if __name__ == '__main__':
    # usage: python create_extension_spec.py
    main()
