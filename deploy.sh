#!/bin/bash

# This script is used to deploy a new package. Please run it from the root of the project.
git pull
cd src
pip install -r requirements.txt
cd ../
py -m pip install --upgrade build
py -m build
py -m pip install --upgrade twine
py -m twine upload -u 'Delineo' -p 'Bluejay123*' --repository-url https://test.pypi.org/legacy/ --verbose --skip-existing dist/* dist/* 
echo "https://test.pypi.org/project/Delineo/"
echo "Upload successful!"
read -p "Press enter to continue"
