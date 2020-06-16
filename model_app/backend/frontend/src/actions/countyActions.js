import { GET_COUNTIES } from "./types";
import axios from 'axios';


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