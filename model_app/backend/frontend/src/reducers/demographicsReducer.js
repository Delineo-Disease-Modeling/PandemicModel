// check action and dispatch to reducer
import { GET_DEMOGRAPHICS } from "../actions/types";

const initialState = {
    demographics : []
}

export default function (state=initialState, action) {
    switch (action.type) {
        case GET_DEMOGRAPHICS:
            return {
                ...state,
                // change the state using backend feedback
                demographics: action.payload
            };
        default:
            return state;

    }
}