// check action and dispatch to reducer
import { GET_COUNTY } from "../actions/types";

export default function (state=[], action) {
    switch (action.type) {
        case GET_COUNTY:
            return action.payload['address_components'];
        default:
            return state;
    }
}