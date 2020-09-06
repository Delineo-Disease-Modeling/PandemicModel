import { GET_TIMESERIES } from "./types";
import axios from 'axios';


export const getTimeseries = (id, start, end) => dispatch => {
    axios
        .get(`./timeseries/${id}?start=${start}&end=${end}`)
        .then(res =>
            dispatch({
                type: GET_TIMESERIES,
                // data returned from backend routers
                payload: res.data
            })
        )
};