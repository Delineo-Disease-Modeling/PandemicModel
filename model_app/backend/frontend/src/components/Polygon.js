import { Component } from 'react';

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
        fillColor: '#ffff00',
        fillOpacity: 1,
        strokeWeight: 5,
        clickable: false,
        editable: true,
        zIndex: 1
      }
    });  
    this.drawingManager.setMap(map);
    mapApi.event.addListener(this.drawingManager, 'overlaycomplete', function(event) {
      console.log(event.overlay)
      var lon_lat_array = event.overlay.getPath().getArray();
      console.log(lon_lat_array);
    });
  }

  componentDidUpdate() {
    //this.props.editable ? this.drawingManager.setMap(this.props.map) : this.drawingManager.setMap(null)
  }

  render() {
    // Same deal with Marker?
    return null;
  }
}

export default Polygon;