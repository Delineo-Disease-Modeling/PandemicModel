import setuptools
from pathlib import Path
with open(r"README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Delineo",
    version="0.2.26",
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
                 'delineo.synthpops': 'src/simulation/synthpops'},
    package_data={'delineo': [
        'data/*', 'data/diseasedata/*'], 'delineo.synthpops': ['data/*', 'synthpops/*', 'data/demographics/*',
                                                               'data/demographics/contact_matrices_152_countries/*', 'data/demographics/contact_matrices_152_countries/usa/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/disease distributions/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/household living arrangements/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/New_York/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/New_York/age distributions/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/New_York/age distributions/NYRegion/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/New_York/household living arrangements/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/Washington/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/Washington/age distributions/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/Washington/contact_networks/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/Washington/employment/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/Washington/enrollment/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/Washington/household living arrangements/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/Washington/household size distributions/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/Washington/schools/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/Washington/seattle_metro/schools/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/Washington/seattle_metro/schools/county_school_enrollment_by_age/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/Washington/workplaces/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/Oregon/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/Oregon/age distributions/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/Oregon/household living arrangements/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/Oklahoma/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/Oklahoma/household living arrangements/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/Oklahoma/household size distributions/*',
                                                               'data/demographics/contact_matrices_152_countries/usa/Oklahoma/age_distributions/*',
                                                               ]},
    python_requires="==3.8",
    install_requires=[
    ],  # external packages as dependencies
)
