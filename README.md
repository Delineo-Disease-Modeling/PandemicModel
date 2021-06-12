# PandemicModel
Repository for Delineo Disease Modeling at the Johns Hopkins University. 

## Developer Notes
Choose one of the below, either a local dev environment or a Conda environment.
### Setting up local dev environment
1. Ensure you have `python3.8` installed and set up.
2. Clone this repository.
3. Initialize a virtual environment: `python3.8 -m venv ~/.envs/PandemicModel`. (Consider using `virtualenvwrapper` for steps 3-4)
4. Activate the virtual environment: `source ~/.envs/PandemicModel/bin/activate`.
5. Install dependencies: `pip install -r requirements.txt`.

### Setting up Conda environment
1. In the Anaconda CMD.exe Prompt, create a new environment with `conda create -n myenv python=3.9.1`, where `myenv` is the name of the environment. Python version 3.9.1 is what's up and running on the covidmod server so it's a good choice to use for your conda environment.
2. Activate the conda environment with `conda activate myenv`.
3. Clone this repository.
4. Navigate into the PandemicModel folder and run `pip install -r requirements.txt`. 

For both, the best way to verify everything is working is to navigate into the `simulation` folder and try running `python master.py`. If you get a bunch of numbers spit out to your terminal, then you're all set. 

### Troubleshooting
- Most likely, you will run into issues due to some dependency not being installed in your conda environment/virtual env. Check ClickUp and/or Slack for a full list of working dependencies.
- If you get an error along the lines of `synthpops has no attribute 'validate'` in `population.py`, open up an editor and uncomment the first synthpops import, and comment the second one out. 

### Misc.
- Please do not commit `venv` stuff.
- If you `pip install ` anything, remember to  `pip freeze > requirements.txt` before committing any changes.
- You cannot commit to the `master` branch, remember to commit all changes to a new branch and open a PR when you're ready to merge.

## `Important Folders/Files`
All important files for running are in the /simulation folder

**simulation/diseasedata**: contains comorbidity data  
**simulation/synthpops**: DO NOT TOUCH unless you really know what you're doing  
**simulation/master.py**: runs the simulation- call this file on command line to get a result  
