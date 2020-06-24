export const options = ['lodging', 'restaurant'];

export const markerIcons = {};

options.forEach(option => {
	markerIcons[option] = `http://maps.google.com/mapfiles/ms/micons/${option}.png`
}
);


export default {options, markerIcons};