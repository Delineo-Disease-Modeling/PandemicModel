// meeting place
import { combineReducers } from 'redux';
import placeReducer from "./placeReducer";
import timeseriesReducer from "./timeseriesReducer";
import demographicsReducer from "./demographicsReducer";

export default combineReducers({
   place: placeReducer,
   demographics: demographicsReducer,
   timeseries: timeseriesReducer
});