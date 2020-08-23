import React, {Component} from 'react';

// SearchBox is a stateless component that handles search box operations like
// clicking on the box, typing/autocomplete, and most importantly saving the
// searched location in our redux store
class SearchBox extends Component {
  constructor(props) {
    super(props);
    this.clearSearchBox = this.clearSearchBox.bind(this);
  }

  componentDidMount({ map, mapApi } = this.props) {
    this.searchBox = new mapApi.places.SearchBox(this.searchInput);
    this.searchBox.addListener('places_changed', this.onPlacesChanged);
    this.searchBox.bindTo('bounds', map);
  }

  componentWillUnmount({ mapApi } = this.props) {
    mapApi.event.clearInstanceListeners(this.searchInput);
  }

  // change map view and save the place in redux store (this is addplace method passed from props)
  onPlacesChanged = ({ map, addplace } = this.props) => {
  	// if we already searched for a place, clear that polygon overlay
  	if (this.feature) {
  		map.data.remove(this.feature[0]);
  	}

  	// update with new searched place
    const selected = this.searchBox.getPlaces();
    const { 0: place } = selected;

    // add to redux store
    addplace(place);

    if (!place.geometry) return;
    if (place.geometry.viewport) {
      map.fitBounds(place.geometry.viewport);
    } else {
      map.setCenter(place.geometry.location);
      map.setZoom(17);
    }

    this.searchInput.blur();
  };

  polygonOverlay(geojson) {
  	let formattedGeojson = geojson;
  	if (geojson['type'] !== "Feature" && geojson['type']!== "FeatureCollection") {
  		formattedGeojson = { "type": "Feature", "geometry": geojson, "properties": {} };
  	}
  	this.feature = this.props.map.data.addGeoJson(formattedGeojson);
  }

  clearSearchBox() {
    this.searchInput.value = '';
  }

  render() {
    return (
      <div style={{marginTop:'30px', marginBottom:'15px'}}>
        <input
          ref={(ref) => {
            this.searchInput = ref;
          }}
          type="text"
          onFocus={this.clearSearchBox}
          placeholder="Enter a location"
        />
      </div>
    );
  }
}

export default SearchBox;