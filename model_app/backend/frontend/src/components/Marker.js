import {Component} from 'react';
import { connect } from 'react-redux';
import {options, markerIcons} from '../const/placeTypes.js';

class Marker extends Component {
    constructor(props) {
        super(props);
        this.markers = options.reduce((options, option) => ({
                ...options,
                [option]: []
            }), {})
    }

    componentDidMount({map, mapApi} = this.props) {
        this.infowindow = new mapApi.InfoWindow();
        this.service = new mapApi.places.PlacesService(map);
    }

    componentDidUpdate(prevProps) {
        if(this.props.place !== prevProps.place) {
            this.nearbySearch(this.props);
        }
    }

    nearbySearch({ map, mapApi, place } = this.props) {
        this.clearMarkers();

        options.forEach(option => {
            let search = {
                bounds: place.geometry.viewport,
                types: [`${option}`]
            };
            this.service.nearbySearch(search, (places, status) => {
                if (status === mapApi.places.PlacesServiceStatus.OK) {
                    places.forEach(place => {
                    let marker = new mapApi.Marker({ map: map,
                                position: place.geometry.location,
                                icon: markerIcons[option]
                    });
                    this.markers[option].push(marker);
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

    setVisible({map} = this.props) {
        options.forEach(option => {
            this.markers[option].forEach(m => { m.setMap(map); });
        })
    }

    setInvisible() {
        options.forEach(option => {
            this.markers[option].forEach(m => { m.setMap(null); });
        })
    }

    clearMarkers() {
        console.log(this.markers);
        this.setInvisible();
        this.markers = options.reduce((options, option) => ({
                ...options,
                [option]: []
            }), {});
    }

    render() {
        return null;
    }
}

const mapStateToProps = (state) => ({
    place: state.county
});

export default connect(mapStateToProps, null)(Marker);