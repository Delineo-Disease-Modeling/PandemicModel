import { GET_COUNTY } from "./types";

export const getCounty = place => ({
    type: GET_COUNTY,
    payload: { place }
});