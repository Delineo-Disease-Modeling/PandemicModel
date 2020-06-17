// check action and dispatch to reducer
import { GET_TIMESERIES } from "../actions/types";

const initialState = {
    timeseries: []
}

export default function (state=initialState, action) {
    switch (action.type) {
        case GET_TIMESERIES:
            return {
                ...state,
                // change the state using backend feedback
                timeseries: action.payload
            };
        default:
            return state;

    }
}