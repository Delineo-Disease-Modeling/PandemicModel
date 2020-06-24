import React, {Component} from 'react';
import { connect } from 'react-redux';

class Marker extends Component {
    constructor(props) {
        super(props);
        this.markers = [];
    }

    componentDidMount({map, mapApi, place} = this.props) {
        this.infowindow = new mapApi.InfoWindow();
    }

    componentDidUpdate(prevProps) {
        if(this.props.place !== prevProps.place) {
            this.nearbySearch(this.props);
        }
    }

    nearbySearch({ map, mapApi, place } = this.props) {
        this.clearMarkers();

        let search = {
            bounds: place.geometry.viewport,
            types: ['lodging']
        };
        let service = new mapApi.places.PlacesService(map);
        service.nearbySearch(search, (places, status) => {
            if (status === mapApi.places.PlacesServiceStatus.OK) {
                places.forEach(place => {
                let marker = new mapApi.Marker({ map: map,
                                position: place.geometry.location
                });
                this.markers.push(marker);
                mapApi.event.addListener(marker, 'click', () => {
                        this.infowindow.setContent('<div><strong>' + place.name + '</strong><br>' +
                                    'Type: ' + place.types + '</div>');
                        this.infowindow.open(map, marker);
                        });
                });
            }
        });
    }

    clearMarkers() {
        this.markers.forEach(m => { m.setMap(null); });
        this.markers = [];
    }
    
    render() {
        return null;
    }
}

const mapStateToProps = (state) => ({
    place: state.county
});

export default connect(mapStateToProps, null)(Marker);