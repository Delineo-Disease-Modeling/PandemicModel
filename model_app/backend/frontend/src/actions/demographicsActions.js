import { GET_DEMOGRAPHICS } from "./types";
import axios from 'axios';

/*
export const getCounties = () => dispatch => {
    axios
        .get('./demographics')
        .then(res =>
            dispatch({
                type: GET_COUNTIES,
                // data returned from backend routers
                payload: res.data
            })
        )
};
*/

export const getDemographics = (id) => dispatch => {
    axios
        .get(`./demographics/${id}`)
        .then(res =>
            dispatch({
                type: GET_DEMOGRAPHICS,
                // data returned from backend routers
                payload: res.data
            })
        )
};