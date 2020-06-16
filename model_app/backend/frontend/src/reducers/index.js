// meeting place
import { combineReducers } from 'redux';
import countyReducer from "./countyReducer";

export default combineReducers({
   county: countyReducer
});