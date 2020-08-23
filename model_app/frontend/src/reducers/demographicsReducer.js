// check action and dispatch to reducer
import { GET_DEMOGRAPHICS } from "../actions/types";

export default function (state={}, action) {
    switch (action.type) {
        case GET_DEMOGRAPHICS:
            return action.payload;
        default:
            return state;

    }
}