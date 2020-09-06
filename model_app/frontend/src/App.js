import React from 'react';
import './App.css';
import { Header, Footer } from './components';
import { Home, About, Simulator, DevelopmentBlog, Team } from './containers';
import { Provider } from 'react-redux';
import store from './store';

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
                  <Header />
                  <Switch>
                      <Route exact path="/" component={Home} />
                      <Route exact path="/about" component={About} />
                      <Route exact path="/simulator" component={Simulator} />
                      <Route exact path="/team" component={Team} />
                      <Route exact path="/developmentblog" component={DevelopmentBlog} />
                      <Redirect to="/" />
                  </Switch>
                  <Footer />
              </Router>
          </div>
      </Provider>
  );
}

export default App;
