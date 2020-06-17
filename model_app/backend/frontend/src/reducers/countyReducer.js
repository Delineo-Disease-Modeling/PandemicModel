// check action and dispatch to reducer
import { GET_COUNTIES, GET_COUNTY } from "../actions/types";

const initialState = {
    counties : []
}

export default function (state=initialState, action) {
    switch (action.type) {
        case GET_COUNTIES:
            return {
                ...state,
                // change the state using backend feedback
                counties: action.payload
            };
        case GET_COUNTY:
            return {
                ...state,
                // change the state using backend feedback
                counties: action.payload
            };
        default:
            return state;

    }
}