import React from 'react';
import logo from './logo.svg';
import './App.css';
import { County, AppNavbar, Timeseries } from './components';
import { Provider } from 'react-redux';
import store from './store';

// routers
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from "react-router-dom";

function App() {
  return (
      <Provider store={store}>
          <div className={"App"}>
              <AppNavbar />
              <Router>
                  <Switch>
                      <Route exact path="/">
                          <Home />
                      </Route>
                      <Route exact path="/counties">
                          <County/>
                          <Timeseries/>
                      </Route>
                  </Switch>
              </Router>
          </div>
      </Provider>
  );
}

function Home() {
    return <h2>Home Page</h2>
}

export default App;
