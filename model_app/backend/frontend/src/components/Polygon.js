import { Component } from 'react';
import { connect } from 'react-redux';
import axios from 'axios';

class Polygon extends Component {

  componentDidMount({map,mapApi} = this.props) {
    this.drawingManager = new mapApi.drawing.DrawingManager({
      drawingMode: mapApi.drawing.OverlayType.POLYGON,
      drawingControl: true,
      drawingControlOptions: {
        position: mapApi.ControlPosition.TOP_CENTER,
        drawingModes: [
          //	google.maps.drawing.OverlayType.MARKER,
          mapApi.drawing.OverlayType.CIRCLE,
          mapApi.drawing.OverlayType.POLYGON,
          //	google.maps.drawing.OverlayType.POLYLINE,
          mapApi.drawing.OverlayType.RECTANGLE
        ]
      },
      circleOptions: {
        clickable: true,
        editable: true,
        draggable: true
      },
      polygonOptions: {
        clickable: true,
        editable: true,
        draggable: true
      }
    });

    mapApi.event.addListener(this.drawingManager, 'overlaycomplete', function(event) {
      console.log(event.overlay)
      //var lon_lat_array = event.overlay.getPath().getArray();
      //console.log(lon_lat_array.toString());
    });

    this.props.editable ? this.drawingManager.setMap(this.props.map) : this.drawingManager.setMap(null);
  }

  componentDidUpdate(prevProps) {
    this.props.editable ? this.drawingManager.setMap(this.props.map) : this.drawingManager.setMap(null);

    if (this.props.place !== prevProps.place) {
      const {map, place} = this.props;
      // if we already searched for a place, clear that polygon overlay
      if (this.feature) {
        map.data.remove(this.feature[0]);
      }

      // get polygon boundaries from nominatim api if they exist
      // don't use place.name since there are multiple counties with same name
      axios.get(`https://nominatim.openstreetmap.org/search?q=${place.formatted_address}&format=json&addressdetails=1&limit=1&polygon_geojson=1`)
        .then(res => {
          const { 0: data } = res['data'];

          if (data['geojson']) {
            this.polygonOverlay(data['geojson']);
          }
          else {
            // another axios request, if polygon boundaries aren't included in nominatim
            // use osm id we got from nominatim
            axios.get(`http://polygons.openstreetmap.fr/get_geojson.py?id=${data['osm_id']}&params=0`)
              .then(results => {
                this.polygonOverlay(results);
              });
          }

          // TODO: add osm relation id to redux store so we have access to it for nearby search
          // probably need new variable
          place['osmId'] = data['osm_id'];
          place['osmType'] = data['osm_type'];
        })
        .catch(err => console.log(err));
    }
  }

  polygonOverlay(geojson) {
    let formattedGeojson = geojson;
    if (geojson['type'] !== "Feature" && geojson['type']!== "FeatureCollection") {
      formattedGeojson = { "type": "Feature", "geometry": geojson, "properties": {} };
    }
    this.feature = this.props.map.data.addGeoJson(formattedGeojson);
  }

  render() {
    // Same deal with Marker: No rendering necessary
    return null;
  }
}

const mapStateToProps = (state) => ({
    place: state.place
});

export default connect(mapStateToProps, null)(Polygon);