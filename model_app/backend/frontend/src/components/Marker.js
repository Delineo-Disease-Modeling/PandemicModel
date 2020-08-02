import {Component} from 'react';
import { connect } from 'react-redux';
import {options, markerIcons} from '../const/placeTypes.js';

class Marker extends Component {
    constructor(props) {
        super(props);
        // markers looks like {'lodging': [marker1, marker2, ...], 'restaurant': [marker1, ...], ...}
        this.markers = options.reduce((options, option) => ({
                ...options,
                [option]: []
            }), {})
    }

    // Initialize once
    componentDidMount({map, mapApi} = this.props) {
        this.infowindow = new mapApi.InfoWindow();
        this.service = new mapApi.places.PlacesService(map);
    }

    // Only re-render if a new search occurs or if one of the checkboxes change.
    componentDidUpdate(prevProps) {
        if(this.props.place !== prevProps.place) {
            var boundary = this.props.place.geometry.viewport;
            this.nearbySearch(this.props, boundary);
        }
        else if (this.props.filter !== prevProps.filter) {
            options.forEach(option => {
                if (this.props.filter[option] !== prevProps.filter[option]) {
                    this.props.filter[option] ? this.setVisible(this.props, option) :
                                            this.setInvisible(option);
                }
            });
        }
    }

    // Conduct a search of the area and initialize the map with all markers + markerIcons.
    // Show only the markers that correspond to selected checkboxes.
    nearbySearch({ map, mapApi} = this.props, boundary) {
        this.clearMarkers();

        // TODO: fix commmunication with redux store + polygon shape. for osm search if we're doing this?
        // if it's smth with defined borders like a county then this is easy
        // if it's some rando shape then this will kind of be a mess lol
        //let areaId = (place['osmType'] === "relation") ? place['osmId']+3600000000 : place['osmId']+2400000000; 
        //console.log(areaId);

        options.forEach(option => {
            // initialize search param
            let search = {
                bounds: boundary,
                types: [`${option}`]
            };
            this.service.nearbySearch(search, (places, status) => {
                if (status === mapApi.places.PlacesServiceStatus.OK) {
                    // create marker and add to array
                    places.forEach(place => {
                    let marker = new mapApi.Marker({ map:
                        this.props.filter[option] ? map : null,
                                position: place.geometry.location,
                                icon: markerIcons[option]
                    });
                    this.markers[option].push(marker);

                    // open info window when clicked
                    mapApi.event.addListener(marker, 'click', () => {
                        this.infowindow.setContent('<div><strong>' + place.name + '</strong><br>' +
                                    'Type: ' + place.types + '</div>');
                        this.infowindow.open(map, marker);
                        });
                    });
                }
            });
        })
    }

    // set all markers of type 'option' to visible
    setVisible({map} = this.props, option) {
        this.markers[option].forEach(m => { m.setMap(map); });
    }

    // set all markers of type 'option' to invisible
    setInvisible(option) {
        this.markers[option].forEach(m => { m.setMap(null); });
    }

    // delete markers by setting marker visibility to null and removing from markers array
    clearMarkers() {
        options.forEach(option => this.setInvisible(option));
        this.markers = options.reduce((options, option) => ({
                ...options,
                [option]: []
            }), {});
    }

    // because we use google map api markers and info windows, we don't render
    // anything ourselves. just make sure to use componentWillUpdate() for all
    // relevant state changes
    render() {
        return null;
    }
}

const mapStateToProps = (state) => ({
    place: state.place
});

export default connect(mapStateToProps, null)(Marker);