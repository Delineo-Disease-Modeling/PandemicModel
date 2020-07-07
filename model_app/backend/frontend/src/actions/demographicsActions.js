import { GET_DEMOGRAPHICS } from "./types";
import axios from 'axios';

export const getDemographics = (stateId, countyId) => dispatch => {
    axios
        .get(`./demographics/${stateId}/${countyId}`)
        .then(res =>
            dispatch({
                type: GET_DEMOGRAPHICS,
                // data returned from backend routers
                payload: res.data
            })
        )
};