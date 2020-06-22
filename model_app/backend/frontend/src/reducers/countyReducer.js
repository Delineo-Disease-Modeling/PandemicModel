// check action and dispatch to reducer
import { GET_COUNTY } from "../actions/types";

const initialState = {
    county : []
}

export default function (state=initialState, action) {
    switch (action.type) {
        case GET_COUNTY:
            return {
                county: action.payload
            };
        default:
            return state;
    }
}