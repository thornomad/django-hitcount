import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import hitcount
extensions = []
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'django-hitcount'
copyright = u'2009-2015 Damon Timm'
author = u'Damon Timm'
version = hitcount.__version__
release = hitcount.__version__
language = None
exclude_patterns = ['_build']
pygments_style = 'sphinx'
todo_include_todos = False
html_static_path = ['_static']
htmlhelp_basename = 'django-hitcountdoc'
latex_elements = {}
latex_documents = [(master_doc, 'django-hitcount.tex',
    u'django-hitcount Documentation', u'Damon Timm', 'manual')]
man_pages = [(master_doc, 'django-hitcount',
    u'django-hitcount Documentation', [author], 1)]
texinfo_documents = [(master_doc, 'django-hitcount',
    u'django-hitcount Documentation', author, 'django-hitcount',
    'One line description of project.', 'Miscellaneous')]
import os
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
