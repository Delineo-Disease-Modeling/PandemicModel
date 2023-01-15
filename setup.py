import setuptools
import os
with open(r"README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
    
for root, dirs, files in os.walk('src/simulation/synthpops/synthpops/data'):
    for file in files:
        if file.endswith('.csv'):
            print(file)
            print(os.path.join(root, file))
            print(os.path.join('delineo', 'synthpops', os.path.join(root, file)))
            print('----------------')

setuptools.setup(
    name="Delineo",
    version="0.2.4",
    author="Delineo",
    author_email="delineodiseasemodeling@gmail.com",
    description="short package description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://test.pypi.org/project/Delineo/",
    project_urls={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['disease modeling', 'epidemiology', 'disease spread'],
    packages=['delineo', 'delineo.synthpops'],
    package_dir={'delineo': 'src/simulation',
                 'delineo.synthpops': 'src/simulation/synthpops/synthpops'},
    package_data={'delineo': ['data/*', 'data/diseasedata/*'], 'delineo.synthpops': ['*']},
    python_requires="==3.8",
    install_requires=[
    ],  # external packages as dependencies
)
