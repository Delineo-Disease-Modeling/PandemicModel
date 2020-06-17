// meeting place
import { combineReducers } from 'redux';
import countyReducer from "./countyReducer";
import timeseriesReducer from "./timeseriesReducer";

export default combineReducers({
   county: countyReducer,
   timeseries: timeseriesReducer
});