# PandemicModel
Repository for Delineo Disease Modeling at Johns Hopkins University 

## Developer Notes

### Setting up local dev environment
1. Ensure you have `python3.8` installed and set up.
2. Clone this repository.
3. Initialize a virtual environment: `python3.8 -m venv ~/.envs/PandemicModel`. (Consider using `virtualenvwrapper` for steps 3-4)
4. Activate the virtual environment: `source ~/.envs/PandemicModel/bin/activate`.
5. Install dependencies: `pip install -r requirements.txt`.

### Misc.
- Please do not commit `venv` stuff
- If you `pip install ` anything, remember to  `pip freeze > requirements.txt` before committing any changes.
