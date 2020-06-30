import React from 'react';
import './App.css';
import { AppNavbar } from './components';
import { Home, About, Simulator, DevelopmentBlog, Team, Contact } from './containers';
import { Provider } from 'react-redux';
import store from './store';
import leaders from './const/leader';

// routers
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Redirect
} from "react-router-dom";

function App() {
  return (
      <Provider store={store}>
          <div className={"App"}>
              <Router>
                  <AppNavbar />
                  <Switch>
                      <Route exact path="/" component={Home} />
                      <Route exact path="/about" component={()=> <About leaders={leaders} />} />
                      <Route exact path="/simulator" component={Simulator} />
                      <Route exact path="/team" component={Team} />
                      <Route exact path="/developmentblog" component={DevelopmentBlog} />
                      <Route exact path="/contact" component={Contact} />
                      <Redirect to="/" />
                  </Switch>
              </Router>
          </div>
      </Provider>
  );
}

export default App;
