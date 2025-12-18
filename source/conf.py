# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Abby Jane\'s Knowledge Base'
copyright = '2025, abby jane morton'
author = 'abby jane morton'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        "myst_parser",
        "sphinx.ext.todo",
]

source_suffix = {
        ".rst": "restructuredtext",
        ".md": "markdown",
}

templates_path = ['_templates']
exclude_patterns = []
todo_include_todos = True


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_title = 'Abby Jane\'s Knowledge Base'
html_static_path = ['_static']
html_css_files = ["style.css"]
html_favicon = "_static/favicon.png"
html_show_sourcelink = False

html_sidebars = {
    "**": [
        "sidebar/brand.html",
        "sidebar/about.html",
        "sidebar/search.html",
        "sidebar/navigation.html",
    ]
}


html_theme_options = {
    # Text at the very top of the sidebar under the project name
    "sidebar_hide_name": False,

    # Little banner at the top of the page (nice for your tagline)
    #"announcement": "Tech, blog notes, errata, and what 3 AM Abby keeps forgetting.",

    # Keyboard nav between pages
    "navigation_with_keys": True,

    # Brand colors (roughly your old link colors)
    "light_css_variables": {
        "color-brand-primary": "#c2185b",
        "color-brand-content": "#7b1fa2",
    },
    "dark_css_variables": {
        "color-brand-primary": "#ff80ab",
        "color-brand-content": "#ce93d8",
    },
}


html_use_modindex = False

html_last_updated_fmt = ""
html_show_sphinx = False