# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from importlib.metadata import version as get_version

project = "ndx-microscopy"
copyright = "2024, Alessandra Trapani, Cody Baker"
author = "Alessandra Trapani, Cody Baker"

release = get_version(project)
version = release

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.ifconfig",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "myst_nb",
]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for the example notebooks ----------------------------------------
# The notebooks in ../../examples are copied into ./examples when the build starts and executed during the build.
nb_execution_mode = "force"
nb_execution_timeout = 300
nb_execution_raise_on_error = True
nb_output_stderr = "remove"

language = "en"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]

# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}


############################################################################
#  CUSTOM CONFIGURATIONS ADDED BY THE NWB TOOL FOR GENERATING FORMAT DOCS
###########################################################################

import sphinx_rtd_theme  # noqa: E402
import textwrap  # noqa: E402

# -- Options for intersphinx  ---------------------------------------------
intersphinx_mapping.update(
    {
        "core": ("https://nwb-schema.readthedocs.io/en/latest/", None),
        "hdmf-common": ("https://hdmf-common-schema.readthedocs.io/en/latest/", None),
        "ndx-ophys-devices": ("https://ndx-ophys-devices.readthedocs.io/en/latest/", None),
    }
)

# -- Generate sources from YAML---------------------------------------------------
# Always rebuild the source docs from YAML even if the folder with the source files already exists
spec_doc_rebuild_always = True


def register_custom_namespace(_):
    """Register the ndx-ophys-devices namespace for documentation generation"""
    try:
        import ndx_ophys_devices
    except ImportError:
        print("Warning: Could not import ndx-ophys-devices")


def run_doc_autogen(_):
    # Execute the autogeneration of Sphinx format docs from the YAML sources
    import sys
    import os

    conf_file_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(conf_file_dir)  # Need so that generate format docs can find the conf_doc_autogen file
    from conf_doc_autogen import spec_output_dir

    if spec_doc_rebuild_always or not os.path.exists(spec_output_dir):
        sys.path.append("./docs")  # needed to enable import of generate_format docs
        from hdmf_docutils.generate_format_docs import main as generate_docs

        generate_docs()


def copy_example_notebooks(_):
    # The notebooks in examples/ are the only copy of the examples; copy them into the docs source tree
    import shutil
    from pathlib import Path

    conf_file_dir = Path(__file__).resolve().parent
    target_dir = conf_file_dir / "examples"
    target_dir.mkdir(exist_ok=True)
    for notebook in (conf_file_dir.parent.parent / "examples").glob("*.ipynb"):
        shutil.copy(notebook, target_dir / notebook.name)


def setup(app):
    app.connect("builder-inited", register_custom_namespace)
    app.connect("builder-inited", run_doc_autogen)
    app.connect("builder-inited", copy_example_notebooks)
    # overrides for wide tables in RTD theme
    try:
        app.add_css_file("theme_overrides.css")  # Used by newer Sphinx versions
    except AttributeError:
        app.add_stylesheet("theme_overrides.css")  # Used by older version of Sphinx


# -- Customize sphinx settings
numfig = True
autoclass_content = "both"
autodoc_docstring_signature = True
autodoc_member_order = "bysource"
add_function_parentheses = False


# -- HTML sphinx options
html_theme = "sphinx_rtd_theme"

# LaTeX Sphinx options
latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    "papersize": "letterpaper",
    # The font size ('10pt', '11pt' or '12pt').
    "pointsize": "10pt",
    # Additional stuff for the LaTeX preamble.
    "preamble": textwrap.dedent(
        """
        \\setcounter{tocdepth}{3}
        \\setcounter{secnumdepth}{6}
        \\usepackage{enumitem}
        \\setlistdepth{100}
        """
    ),
}
