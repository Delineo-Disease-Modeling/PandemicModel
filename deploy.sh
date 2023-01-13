#!/bin/bash

# This script is used to deploy a new package. Please run it from the root of the project.
git pull
cd src
pip install -r requirements.txt
cd ../
python setup.py sdist
py -m pip install --upgrade twine
py -m twine upload -u 'Delineo' -p 'Bluejay123*' --repository-url https://test.pypi.org/legacy/ --verbose --skip-existing dist/*
echo "https://test.pypi.org/project/Delineo/"
read -p "Press enter to continue"
rm -rf dist