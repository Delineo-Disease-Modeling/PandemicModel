// meeting place
import { combineReducers } from 'redux';
import countyReducer from "./countyReducer";
import timeseriesReducer from "./timeseriesReducer";
import demographicsReducer from "./demographicsReducer";

export default combineReducers({
   county: countyReducer,
   demographics: demographicsReducer,
   timeseries: timeseriesReducer
});