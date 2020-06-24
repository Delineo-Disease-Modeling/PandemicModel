import React, {Component} from 'react';
import { connect } from 'react-redux';

class Marker extends Component {
    constructor(props) {
        super(props);
        this.markers = [];
    }

  componentDidUpdate(prevProps) {
    if(this.props.place !== prevProps.place) {
        this.nearbySearch(this.props);
    }
  }

  nearbySearch({map, mapApi, place} = this.props) {
    this.clearMarkers();

    let search = {
        bounds: place.geometry.viewport,
        types: ['lodging']
      };
    let service = new mapApi.places.PlacesService(map);
    service.nearbySearch(search, (results, status) => {
        if (status == mapApi.places.PlacesServiceStatus.OK) {
            for (let i = 0; i < results.length; i++) {
                let marker = new mapApi.Marker({ map: map,
                            position: results[i].geometry.location});
                this.markers.push(marker);
            }
        }
    });
}

  clearMarkers() {
    for (let i = 0; i < this.markers.length; i++) {
        this.markers[i].setMap(null);
    }
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