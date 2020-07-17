// check action and dispatch to reducer
import { GET_PLACE } from "../actions/types";

export default function (state={}, action) {
    switch (action.type) {
        case GET_PLACE:
            return action.payload;
        default:
            return state;
    }
}