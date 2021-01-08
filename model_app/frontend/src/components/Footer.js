import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(1),
  },
}));

function TypographyTheme() {
    const classes = useStyles();
  
    return <div className={classes.root}>{"Sample footer."}</div>;
  }

function Footer(props) {
    return(
    <div className="footer" style={{backgroundColor:'#222629', padding:'-10%'}}>
	<p style={{color:'white'}}>JHU.edu Copyright © 2020 by Johns Hopkins University & Medicine. All rights reserved.</p>
	<p style={{color:'white'}}> <a href="https://it.johnshopkins.edu/policies/privacystatement" target="_blank" rel="noopener noreferrer">Privacy Statement</a> </p>
    </div>
    )
}

export default Footer;
