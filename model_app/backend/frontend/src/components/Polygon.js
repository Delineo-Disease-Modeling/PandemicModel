import { Component } from 'react';
import { connect } from 'react-redux';
import { addPolygon, deletePolygon, resetPolygon } from '../actions/polygonActions';
import axios from 'axios';

class Polygon extends Component {

  componentDidMount() {
    this.drawPolygon();
  }

  drawPolygon({map,mapApi} = this.props) {
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
        //draggable: true
      },
      polygonOptions: {
        clickable: true,
        editable: true,
        //draggable: true
      },
      rectangleOptions : {
        clickable: true,
        editable: true,
        //draggable: true
      }
    });

<<<<<<< HEAD
    mapApi.event.addListener(this.drawingManager, 'circlecomplete', function(circle) {
      console.log("drawing circle");
      var radius = circle.getRadius();
      console.log(radius.toString());
      mapApi.event.addListener(circle,'radius_changed', function() {
        console.log("editing");
        radius = circle.getRadius();
        console.log(radius.toString());
      });
    });

    mapApi.event.addListener(this.drawingManager, 'rectanglecomplete', function(rectangle) {
      console.log("drawing rectangle");
      var bounds = rectangle.getBounds();
      console.log(bounds.toString());
      //this.polygonInfo(bounds.toString());
      mapApi.event.addListener(rectangle,'bounds_changed', function() {
        console.log("editing");
        bounds = rectangle.getBounds();
        console.log(bounds.toString());
        //this.polygonInfo(bounds.toString());
      });
=======
    mapApi.event.addListener(this.drawingManager, 'overlaycomplete', function(event) {
      console.log(event.overlay)
      //var lon_lat_array = event.overlay.getPath().getArray();
      //console.log(lon_lat_array.toString());

      // TODO: for each user-drawn polygon, create osm polygon and save to redux store with
      // this.props.addPolygon(whatever)

      // TODO: delete polygon with id from store using
      // this.props.deletePolygon(id)
>>>>>>> c8b22659575b36d543b098ad7663c2ee012bdd0e
    });

    mapApi.event.addListener(this.drawingManager, 'polygoncomplete', function(polygon) {
      console.log("drawing polygon");
      var path = polygon.getPath();
      console.log(path.getArray().toString());
      //this.polygonInfo(path.getArray().toString());
      mapApi.event.addListener(path,'insert_at', function() {
        console.log("editing");
        path = polygon.getPath();
        console.log(path.getArray().toString());
        //this.polygonInfo(path.getArray().toString());
      });
      mapApi.event.addListener(path,'set_at', function() {
        console.log("editing");
        path = polygon.getPath();
        console.log(path.getArray().toString());
        //this.polygonInfo(path.getArray().toString());
      });
    });


    this.props.editable ? this.drawingManager.setMap(this.props.map) : this.drawingManager.setMap(null);

  }

  componentDidUpdate(prevProps) {
    this.props.editable ? this.drawingManager.setMap(this.props.map) : this.drawingManager.setMap(null);

    if (this.props.place !== prevProps.place) {
      const {map, place} = this.props;

      // if we already searched for a place, clear that polygon overlay
      // clear redux store completely
      if (this.feature) {
        map.data.remove(this.feature[0]);
        this.props.resetPolygon();
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

          // add osm relation id to redux store so we have access to it for nearby search
          this.props.addPolygon(data['osm_id'], data['osm_type']);
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
    place: state.place,
    polygons: state.polygons // unsure if we need this, currently unused
});

<<<<<<< HEAD


export default connect(mapStateToProps, null)(Polygon);
=======
export default connect(mapStateToProps, { addPolygon, deletePolygon, resetPolygon } )(Polygon);
>>>>>>> c8b22659575b36d543b098ad7663c2ee012bdd0e
