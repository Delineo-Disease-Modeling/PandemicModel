// check action and dispatch to reducer
import { ADD_POLYGON, DELETE_POLYGON, RESET_POLYGON } from "../actions/types";

export default function (state=[], action) {
    switch (action.type) {
        case ADD_POLYGON:
            return [
            	...state,
            	{
            		id: action.id,
            		type: action.osmType
            	}
            ];
        case DELETE_POLYGON:
        	return state.filter(id => id !== action.id);
        case RESET_POLYGON:
        	return [];
        default:
            return state;
    }
}