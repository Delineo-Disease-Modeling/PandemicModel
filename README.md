# PandemicModel
Repository for Delineo Disease Modeling at the Johns Hopkins University. 

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
## `Architecture Branch General`

The architecture group is responsible for deploying the web application that will make Delineo's simulation available to the end users. This application is being built using the MERN stack. In addition, the architecture group is responsible for implementing the interface between the backend/database and the module & control group, and the interface between the backend/database and the visualizations group. 

## `Installation`
[Node.js](https://nodejs.org/en/download) and [Python >=3.6](https://www.python.org/downloads/) are required.

1. Install all dependencies: Navigate to **model_app**. In Terminal or CMD, enter
	```
	npm install
	npm run server-install
	npm run client-install
	```

## `Important Folders/Files`
All important files for running are in the /simulation folder
**simulation/diseasedata**: contains comorbidity data  
**simulation/synthpops**: DO NOT TOUCH unless you really know what you're doing  
**simulation/master.py**: runs the simulation- call this file on command line to get a result  
