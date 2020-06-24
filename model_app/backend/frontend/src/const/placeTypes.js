/* Use these sites to get icons and place types
https://sites.google.com/site/gmapsdevelopment/
https://developers.google.com/places/web-service/supported_types
*/

export const options = ['lodging', 'restaurant'];

export const markerIcons = {};

options.forEach(option => {
	markerIcons[option] = `http://maps.google.com/mapfiles/ms/micons/${option}.png`
}
);

export default {options, markerIcons};