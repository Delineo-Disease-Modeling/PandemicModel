import React, { Fragment, Component } from 'react';
import { connect } from 'react-redux';
import GoogleMapReact from 'google-map-react';
import SearchBox from './SearchBox.js';
import { getCounty } from '../actions/countyActions';
import Marker from './Marker.js';
import {options} from '../const/placeTypes.js';
import Checkbox from './Checkbox.js'

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
            checkboxes: options.reduce((options, option) => ({
                ...options,
                [option]: true
            }), {})
        };
    }

    apiHasLoaded = (map, maps) => {
        this.setState({
            mapApiLoaded: true,
            mapInstance: map,
            mapApi: maps,
        });
    };

    // Save to redux store
    addPlace = (place) => {
        this.props.getCounty(place);
    };

    handleCheckboxChange = changeEvent => {
        const { name } = changeEvent.target;

        this.setState(prevState => ({
            checkboxes: {
                ...prevState.checkboxes,
                [name]: !prevState.checkboxes[name]
            }
        }));
    };

    // Contains SearchBox, Checkboxes, and Google Map with Marker
    render() {
        const { mapApiLoaded, mapInstance, mapApi, checkboxes } = this.state;

        return (
        <Fragment>
            {mapApiLoaded && <SearchBox map={mapInstance} mapApi={mapApi} addplace={this.addPlace} />}
            {options.map(option => ( <Checkbox key={option} isSelected={this.state.checkboxes[option]}
                onCheckboxChange={this.handleCheckboxChange} label = {option}/> ))}
            <div style={{ height: '100vh', width: '100%' }}>
                <GoogleMapReact
                    bootstrapURLKeys={{ key: 'AIzaSyBgND2XyCZrz8L5RbrZObu7i-zgrY688pQ',
                                        libraries: ['places'] }}
                    defaultCenter={this.props.center}
                    defaultZoom={this.props.zoom}
                    yesIWantToUseGoogleMapApiInternals
                    onGoogleApiLoaded={({ map, maps }) => this.apiHasLoaded(map, maps)}
                >
                    {mapApiLoaded && <Marker map={mapInstance} mapApi={mapApi} filter={checkboxes}/>}
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