import { GET_PLACE } from "./types";

export const getPlace = place => ({
    type: GET_PLACE,
    payload: place[0]
});