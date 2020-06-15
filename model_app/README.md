## `General`

The architecture group is responsible for deploying the web application that will make Delineo's simulation available to the end users. This application is being built using the MERN stack. In addition, the architecture group is responsible for implementing the interface between the backend/database and the module & control group, and the interface between the backend/database and the visualizations group.

## `Important Files/Folders`
**backend/models**: contains all database schemas   
**backend/routes**: contains all routing information for server   
**backend/server.js**: connects to the MongoDB database and links all routes to corresponding URI's   
**data_processing/pymongo/main.py**: Pymongo script to query demographics and timeseries database collections. Initial interface between architecture and mod & control

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
