/* Use these sites to get icons and place types
icons 				https://sites.google.com/site/gmapsdevelopment/
google maps 		https://developers.google.com/places/web-service/supported_types
osm overpass		https://wiki.openstreetmap.org/wiki/Key:amenity
*/

export const options = ['food', 'transportation'];

export const markerIcons = {};
let baseUrl = 'http://maps.google.com/mapfiles/ms/micons/';
let ext = '.png';
markerIcons['food'] = baseUrl + 'restaurant' + ext;
markerIcons['transportation'] = baseUrl + 'rail' + ext;

export const queries = {};
queries['food'] = (areaId) => {
	return `[out:json];
	(
	  node(${areaId})[amenity~"bar|restaurant|fast_food|pub|cafe|food_court"];
	  way(${areaId})[amenity~"bar|restaurant|fast_food|pub|cafe|food_court"];
	  rel(${areaId})[amenity~"bar|restaurant|fast_food|pub|cafe|food_court"];
	)->.amenities;
	(
	  node(${areaId})[shop~"bakery|convenience"];
	  way(${areaId})[shop~"bakery|convenience"];
	  rel(${areaId})[shop~"bakery|convenience"];
	)->.shops;
	(
	  .amenities;
	  .shops;
	);
	out;`
}
queries['transportation'] = (areaId) => {
	return `[out:json];
	(
	  node(${areaId})[amenity~"bicycle_parking|bicycle_repair_station|bicycle_rental|boat_rental|boat_sharing|bus_station|car_rental|car_sharing|car_wash|vehicle_inspection|charging_station|ferry_terminal|fuel|grit_bin|motorcycle_parking|parking|parking_entrance|parking_space|taxi"];
	  way(${areaId})[amenity~"bicycle_parking|bicycle_repair_station|bicycle_rental|boat_rental|boat_sharing|bus_station|car_rental|car_sharing|car_wash|vehicle_inspection|charging_station|ferry_terminal|fuel|grit_bin|motorcycle_parking|parking|parking_entrance|parking_space|taxi"];
	  rel(${areaId})[amenity~"bicycle_parking|bicycle_repair_station|bicycle_rental|boat_rental|boat_sharing|bus_station|car_rental|car_sharing|car_wash|vehicle_inspection|charging_station|ferry_terminal|fuel|grit_bin|motorcycle_parking|parking|parking_entrance|parking_space|taxi"];
	);
	out;`
}

export default {options, markerIcons, queries};