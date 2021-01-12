import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import GridListTile from '@material-ui/core/GridListTile';
import Grid from '@material-ui/core/Grid';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center',
    overflow: 'hidden',
    backgroundColor: '#1b4441c2',
    padding: theme.spacing(6),
    textAlign: 'center',

  },
  icon: {
    color: 'rgba(255, 255, 255, 0.54)',
  },

  displayUnder: {
    font: "Brush Script MT",
    fontSize: 14,
    border: 0,
    borderRadius: 3,
    color: 'white',
    height: 10,
    padding: '0 30px',
    padding: theme.spacing(1),

  },

  displayUnderTitle: {
    font: "Lucida Console",
    fontSize: 20,
    border: 0,
    borderRadius: 3,
    color: 'white',
    height: 10,
    padding: '0 30px',
    padding: theme.spacing(1),

  },


  displayOver: {
    height: "100%",
    left: "0",
    position: "absolute",
    top: "0",
    width: "100%",
    zIndex: 2,
    transition: "background-color 350ms ease",
    backgroundColor: "rgba(0,0,0,.5)",
    padding: "20px 20px 0 20px",
    boxSizing: "border-box",
    opacity: 0,
  },
  hover: {
    opacity: 1,
    transition: "opacity 350ms ease",
  },
  hoverTitle: {
    transform: "translate3d(0,50px,0)",
    transition: "transform 350ms ease",
    fontSize: '20px'
  },
  hoverSubtitle: {
    transform: "translate3d(0,50px,0)",
    transition: "transform 350ms ease",
    fontSize: '16px'
  },
  hoverP: {
    transform: "translate3d(0,50px,0)",
    transition: "transform 350ms ease",
  },
  gridList: {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',

  },
  GridListTile: {
    '&:hover p, &:hover h3, &:hover h4': {
      transform: "translate3d(0,0,0)",
    },
    '&:hover div': {
      opacity: 1,
    },
    width: '200px',
    height:'200px',



  },
}));

export default function TitlebarGridList(tileData) {
  const classes = useStyles();


  return (
    <Container className={classes.root} maxWidth="md">
      <Grid container spacing={4}>
        {tileData.map((tile) => (
          
          <Grid item key={tile.name}  xs={12} sm={6} md={3}>
            <GridListTile className={classes.GridListTile} key={tile.img}>
              

              <img src={tile.img} alt={tile.name} class="center" />
              <h3 className={classes.displayUnder}>{tile.name}</h3>
            

              <div className={classes.displayUnder}>
                <div className={classes.displayUnder}>
                  <h8 className={classes.displayUnder}>{tile.name}</h8>
                  <h4 className={classes.displayUnder}>{tile.role}</h4>
                  <p className={classes.displayUnder}>{tile.description}</p>
                </div>
              </div>

              <div className={classes.displayUnder}>
              <div className={classes.root}>
              


              </div>
              </div>

 
            </GridListTile>

            <br></br>
            <Typography variant="h4" component="h4" color="red" >
                  <h4 className={classes.displayUnderTitle} >{tile.name}</h4>
                  <h4 className={classes.displayUnder}>{tile.role}</h4>
            </Typography>
          </Grid>
        ))}

      </Grid>
    </Container>
  );
}
