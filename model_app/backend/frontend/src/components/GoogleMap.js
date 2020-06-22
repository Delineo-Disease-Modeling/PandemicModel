import React, { Fragment, Component } from 'react';
import GoogleMapReact from 'google-map-react';
import SearchBox from './SearchBox.js';

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
            mapApi: null,
            places: [],
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
        this.setState({ places: place });
    };

    render() {
        const { places, mapApiLoaded, mapInstance, mapApi } = this.state;
        return (
        <Fragment>
            {mapApiLoaded && <SearchBox map={mapInstance} mapApi={mapApi} addplace={this.addPlace} />}
            <div style={{ height: '100vh', width: '100%' }}>
                <GoogleMapReact
                    bootstrapURLKeys={{ key: 'AIzaSyBkeKK8GaNumlCxgPf1-DtbB4bAo2Sqrwg',
                                        libraries: ['places'] }}
                    defaultCenter={this.props.center}
                    defaultZoom={this.props.zoom}
                    yesIWantToUseGoogleMapApiInternals
                    onGoogleApiLoaded={({ map, maps }) => this.apiHasLoaded(map, maps)}
                >
                </GoogleMapReact>
            </div>
        </Fragment>
        );
    }
}

export default GoogleMap;