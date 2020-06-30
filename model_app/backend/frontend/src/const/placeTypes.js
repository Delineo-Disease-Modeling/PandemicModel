/* Use these sites to get icons and place types
https://sites.google.com/site/gmapsdevelopment/
https://developers.google.com/places/web-service/supported_types
*/

export const options = ['lodging', 'restaurant', 'pharmacy', 'hospital', 'convenience_store'];

export const markerIcons = {};
let baseUrl = 'http://maps.google.com/mapfiles/ms/micons/';
let ext = '.png';

options.forEach(option => {
	markerIcons[option] = baseUrl + `${option}` + ext;
}
);
markerIcons['pharmacy'] = baseUrl + 'pharmacy-us' + ext;
markerIcons['hospital'] = baseUrl + 'hospitals' + ext;
markerIcons['convenience_store'] = baseUrl + 'convienancestore' + ext;

export default {options, markerIcons};