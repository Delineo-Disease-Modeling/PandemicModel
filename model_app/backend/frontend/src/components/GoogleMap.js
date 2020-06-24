import React, { Fragment, Component } from 'react';
import { connect } from 'react-redux';
import GoogleMapReact from 'google-map-react';
import SearchBox from './SearchBox.js';
import { getCounty } from '../actions/countyActions';
import Marker from './Marker.js';

class GoogleMap extends Component {
    // for autauga county
    static defaultProps = {
        center: {
            lat: 32,
            lng: -86
        },
        zoom: 10
    };

    constructor(props) {
        super(props);

        this.state = {
            mapApiLoaded: false,
            mapInstance: null,
            mapApi: null
        };
    }

    apiHasLoaded = (map, maps) => {
        this.setState({
            mapApiLoaded: true,
            mapInstance: map,
            mapApi: maps,
        });
    };

    addPlace = (place) => {
        this.props.getCounty(place);
    };

    render() {
        const { mapApiLoaded, mapInstance, mapApi } = this.state;

        return (
        <Fragment>
            {mapApiLoaded && <SearchBox map={mapInstance} mapApi={mapApi} addplace={this.addPlace} />}
            <div style={{ height: '100vh', width: '100%' }}>
                <GoogleMapReact
                    bootstrapURLKeys={{ key: 'AIzaSyBgND2XyCZrz8L5RbrZObu7i-zgrY688pQ',
                                        libraries: ['places'] }}
                    defaultCenter={this.props.center}
                    defaultZoom={this.props.zoom}
                    yesIWantToUseGoogleMapApiInternals
                    onGoogleApiLoaded={({ map, maps }) => this.apiHasLoaded(map, maps)}
                >
                    {mapApiLoaded && <Marker map={mapInstance} mapApi={mapApi} />}
                </GoogleMapReact>
            </div>
        </Fragment>
        );
    }
}

const mapStateToProps = (state) => ({
    county: state.county
});

export default connect(mapStateToProps, {getCounty})(GoogleMap);