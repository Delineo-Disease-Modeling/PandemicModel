import setuptools

with open(r"README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Delineo",
    version="0.1.0",
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
    packages=['delineo'],
    package_dir={'delineo': 'src/simulation'},
    package_data={'delineo': ['data/*']},
    python_requires="==3.8"
)
