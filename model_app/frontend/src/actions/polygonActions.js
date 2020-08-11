import { ADD_POLYGON, DELETE_POLYGON, RESET_POLYGON } from "./types";

export const addPolygon = (osmId, osmType) => ({
    type: ADD_POLYGON,
    id: osmId,
    osmType: osmType
});

export const deletePolygon = id => ({
	type: DELETE_POLYGON,
	id: id
});

export const resetPolygon = () => ({
	type: RESET_POLYGON
});