// check action and dispatch to reducer
import { GET_TIMESERIES } from "../actions/types";

export default function (state=[], action) {
    switch (action.type) {
        case GET_TIMESERIES:
            return action.payload;
        default:
            return state;

    }
}