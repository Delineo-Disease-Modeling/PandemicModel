import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import GridListTileBar from '@material-ui/core/GridListTileBar';
import ListSubheader from '@material-ui/core/ListSubheader';
import IconButton from '@material-ui/core/IconButton';
import InfoIcon from '@material-ui/icons/Info';
import Grid from '@material-ui/core/Grid';
import Container from '@material-ui/core/Container';

import withWidth, { isWidthUp } from '@material-ui/core/withWidth';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center',
    overflow: 'hidden',
    backgroundColor: '#1b4441c2',
    paddingTop: theme.spacing(0),
    paddingBottom: theme.spacing(4),

  },
  icon: {
    color: 'rgba(255, 255, 255, 0.54)',
  },
  displayOver: {
    height: "100%",
    left: "0",
    position: "absolute",
    top: "0",
    width: "100%",
    zIndex: 2,
    transition: "background-color 350ms ease",
    backgroundColor: "transparent",
    padding: "20px 20px 0 20px",
    boxSizing: "border-box",
    opacity: 0,
    backgroundColor: "rgba(0,0,0,.5)"
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
          <Grid item key={classes.GridListTile}  xs={12} sm={6} md={3}>
            <GridListTile className={classes.GridListTile} key={tile.img}>
              <img src={tile.img} alt={tile.name} />

              <div className={classes.displayOver}>
                <div className={classes.hover}>
                  <h3 className={classes.hoverTitle}>{tile.name}</h3>
                  <h4 className={classes.hoverSubtitle}>{tile.role}</h4>
                  <p className={classes.hoverP}>{tile.description}</p>
                </div>
              </div>
            </GridListTile>
          </Grid>
        ))}

      </Grid>
    </Container>
  );
}
