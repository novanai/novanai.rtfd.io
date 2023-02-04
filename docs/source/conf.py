# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "NovaNAI"
copyright = "2022, Nova"
author = "Nova"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser", "sphinxext.opengraph"]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]

html_favicon = "_static/favicon.png"
html_title = "NovaNAI"

myst_heading_anchors = 1

# -- OpenGraph ---------------------------------------------------------------

ogp_image = "https://novanai.readthedocs.io/en/latest/_static/banner.png"
ogp_description_length = 66

ogp_custom_meta_tags = [
    '<meta property="theme-color" content="#fe7c9e">',
]
