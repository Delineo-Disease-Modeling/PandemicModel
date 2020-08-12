import {Component} from 'react';
import { connect } from 'react-redux';
import {options, markerIcons, queries} from '../const/placeTypes.js';
import axios from 'axios';

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
        if (this.props.polygons !== prevProps.polygons) {
            this.clearMarkers();

            // TODO: loading stuff? so client doesn't get confused when searching takes forever
            // for every polygon, user-drawn or searched, get boundaries and query from overpass
            this.props.polygons.forEach(polygon => {
                this.nearbySearch(this.props, polygon);
            })
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
    nearbySearch({ map, mapApi } = this.props, polygon) {
        // TODO: check areaId for custom polyline for user-drawn polygons
        let areaId = (polygon['type'] === "relation") ? polygon['id']+3600000000 : polygon['id']+2400000000;

        // for every place type, make an osm overpass query
        options.forEach(option => {
            axios.get('https://overpass.kumi.systems/api/interpreter?data='+
                queries[option](`area:${areaId}`))
                // Overpass Kumi says we should include contact info but I think Chrome blocks us from setting User-Agent
                //{headers: {'User-Agent': 'Delineo Disease Modeling (email: delineodiseasemodeling-at-gmail.com)'}})
                .then(results => {
                    // get the results of the query
                    const {elements} = results.data;
                    
                    // create marker and add to array
                    elements.forEach(place => {
                    // TODO: plot ways and relations, not just nodes
                    if (place.type === 'node') {
                        let marker = new mapApi.Marker({ map:
                            this.props.filter[option] ? map : null,
                                    position: {lat: place.lat, lng: place.lon},
                                    icon: markerIcons[option]
                        });
                        this.markers[option].push(marker);

                        // open info window when clicked
                        mapApi.event.addListener(marker, 'click', () => {
                            this.infowindow.setContent('<div><strong>' + place.tags.name + '</strong><br>' +
                                        JSON.stringify(place.tags) + '</div>');
                            this.infowindow.open(map, marker);
                            });
                        }
                    });
                })
                .catch(err => console.log(err));
        });
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
    polygons: state.polygons
});

export default connect(mapStateToProps, null)(Marker);