minu README
==================

Getting Started
---------------

- cd <directory containing this file>

- $VENV/bin/python setup.py develop

- $VENV/bin/initialize_minu_db development.ini

- $VENV/bin/pserve development.ini


Testing & Code coverage
----------------

- cd <Project folder directory>

- nosetests

- nosetests --with-coverage --cover-package=minu
