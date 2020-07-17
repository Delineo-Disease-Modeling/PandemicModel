# PandemicModel
Repository for Delineo Disease Modeling at Johns Hopkins University 

## `Architecture Branch General`

The architecture group is responsible for deploying the web application that will make Delineo's simulation available to the end users. This application is being built using the MERN stack. In addition, the architecture group is responsible for implementing the interface between the backend/database and the module & control group, and the interface between the backend/database and the visualizations group.

## `Important Files/Folders`
**model_app/backend/models**: contains all database schemas   
**model_app/backend/routes**: contains all routing information for server   
**model_app/backend/server.js**: connects to the MongoDB database and links all routes to corresponding URI's   
**model_app/data_processing/pymongo/main.py**: Pymongo script to query demographics and timeseries database collections. Initial interface between architecture and mod & control    
**model_all/backend/frontend/src**: All the folders for implementing the Redux architecture are here. 

## `To Run`
After pulling from this branch, navigate to the backend folder and enter npm run dev, which starts both the client and server connection. Make sure you have the right .env file in the backend folder (not in repository) and another copy in the frontend folder, so that you have all the keys necessary to connect with MongoDB and the GoogleMaps API. 

