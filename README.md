# PandemicModel
Repository for Delineo Disease Modeling at Johns Hopkins University 

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

2. Set up environment variables: Create two .env files, one in **model_app/frontend** and one in **model_app/backend**.

The frontend .env file looks like
```
MAP_API=<your-map-api>
```

The backend .env file looks like
```
ATLAS_URI=<MongoDB-URI>
PYTHON_PATH=<path-where-to-locate-the-"python"-executable>
SCRIPT_PATH=<path-of-the-script-to-execute>
```

3. Activate the virtual environment for the synthpops simulation. Instructions for creating the virtual environment are found in **model_app/backend/synthpops**

4. Begin website development: In **model_app**, enter `npm run dev` to start the client and server connections. When you make changes to any file, the servers will restart. You should see a message

```
MongoDB database connection established successfully.
Development server is running on port: 5000
```

## `Structure`
**model_app/backend/models**: contains all database schemas   
**model_app/backend/routes**: contains all routing information for server  
**model_app/backend/synthpops**: contains all Python scripts needed for simulations  
**model_app/backend/server.js**: connects to the MongoDB database and links all routes to corresponding URI's

**model_app/backend/frontend/src**: All the folders for implementing the Redux architecture are here.

