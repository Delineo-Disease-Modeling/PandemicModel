import React, { Fragment, Component } from 'react';
import { connect } from 'react-redux';
import { Button } from 'reactstrap';
import GoogleMapReact from 'google-map-react';
import SearchBox from './SearchBox.js';
import { getPlace } from '../actions/placeActions';
import Marker from './Marker.js';
import {options} from '../const/placeTypes.js';
import Checkbox from './Checkbox.js'
import Polygon from './Polygon.js';

class GoogleMap extends Component {
    // initialize for autauga county
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
            }), {}),
            editPolygon: false
        };
    }

    // save Google Maps API in state
    apiHasLoaded = (map, maps) => {
        this.setState({
            mapApiLoaded: true,
            mapInstance: map,
            mapApi: maps,
        });
    };

    // Save to redux store
    addPlace = (place) => {
        this.props.getPlace(place);
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

    handleButtonChange = () => {
        this.setState({
            editPolygon: !this.state.editPolygon
        })
    }

    // Contains SearchBox, Checkboxes, and Google Map with Marker
    render() {
        const { mapApiLoaded, mapInstance, mapApi, checkboxes } = this.state;

        return (
        <Fragment>
            {mapApiLoaded && <SearchBox map={mapInstance} mapApi={mapApi} addplace={this.addPlace} />}
            {options.map(option => ( <Checkbox key={option} isSelected={this.state.checkboxes[option]}
                onCheckboxChange={this.handleCheckboxChange} label = {option}/> ))}
            <Button onClick={this.handleButtonChange}>Draw Polygon!</Button>
            {mapApiLoaded && <Polygon map={mapInstance} mapApi={mapApi} editable={this.state.editPolygon} />}
            <div style={{ height: '100vh', width: '100%' }}>
                <GoogleMapReact
                    bootstrapURLKeys={{ key: process.env.REACT_APP_MAP_API,
                                        libraries: ['places', 'drawing'] }}
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
    place: state.place
});

export default connect(mapStateToProps, {getPlace})(GoogleMap);