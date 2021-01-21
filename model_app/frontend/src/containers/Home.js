import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import CssBaseline from '@material-ui/core/CssBaseline';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core';

const styles = {
    button: {
        borderColor: '#66FCF1',
        backgroundColor: '#66FCF1',
        border: '1px solid',
        "&:hover": {
            backgroundColor: '#222629',
            color: '#66FCF1',
            borderColor: '#66FCF1',
        },
    },

    buttonContainer: {
        width: '100%'
    },

    imageBox: {
        ///* Here's the trick */
        background: "linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5))",
        backgroundImage: "url('https://9to5mac.com/wp-content/uploads/sites/6/2020/01/Coronavirus.jpg?quality=82&strip=all')",
        backgroundSize: "cover",
        //backgroundImage: "url('https://images.pexels.com/photos/60597/dahlia-red-blossom-bloom-60597.jpeg?cs=srgb&dl=pexels-pixabay-60597.jpg&fm=jpg')",

        ///* Here's the same styles we applied to our content-div earlier */
        color: "white",
        height: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",

        "&:hover": {
            boxShadow: "inset 0 0 0 100vw rgba(0,0,0,0.5)",
        },
    },

    aboutSection: {
        padding: '100px 10px 100px 10px',
        backgroundColor: '#222D3C', /* Or #1C2531 ? */
        overflow: 'hidden',

        " p": {
            fontSize: '18px',
        }
    },

    whiteBackground: {
        backgroundColor: 'white',
        marginBottom: '50px',
        borderRadius: '30px 30px 30px 30px'
    },

    blogSection: {
        padding: '0px 30px 30px 30px',
        backgroundColor: '#badcf4',
        overflow: 'hidden',

        "> p": {
            fontSize: '18px',
            marginTop: '1rem',
            marginBottom: '2rem',
        }
    },

    blogImg: {
        backgroundColor: 'white',
        maxWidth: ' 100%',
        maxHeight: '100%',
        borderRadius: '30px 30px 30px 30px',
        overflow: 'hidden',
    },

    blogContainer: {
        paddingTop: '30px',
        textAlign: 'center',
        backgroundColor: '#444f56',
        borderRadius: '30px 30px 30px 30px',
        minHeight: '600px',
        overflow: 'hidden',
        margin: '25px'
    },

    blogText: {
        fontSize: '18px',
        marginTop: '1rem',
        marginBottom: '2rem',
    },

    blogContent: {
        padding: '20px'
    },

    imgContainer: {
        padding: '0px 20px 20px 20px'
    }

};

class Home extends Component {

    render() {
        const { classes } = this.props;

        return (
            <React.Fragment>
                <CssBaseline />
                <div className={classes.imageBox}>
                    <div className="header-text">
                        <h1>Interactive Disease Simulation</h1>
                        <Button className={classes.button} variant="contained" color="inherit" href="/simulator">
                            Explore Simulation
                        </Button>
                    </div>
                </div>

                <div className={classes.aboutSection}>
                    <Grid container spacing={3}>
                        <Grid item xs={6}>
                            <img className={classes.whiteBackground} src='https://icon-library.com/images/simulator-icon/simulator-icon-2.jpg' alt="Simulator" title="Simulator" />

                        </Grid>
                        <Grid item xs={6}>
                            <Typography variant="h5" component="h3" gutterBottom>
                                Description of ML
                                </Typography>
                            <p style={{ fontSize: '18px' }}>
                                Lorem ipsum dolor sit amet, consectetur adipiscing elit. In arcu ligula, auctor ut dictum ac, malesuada et arcu. Vestibulum ut commodo enim, in pulvinar magna. Mauris est enim, pretium id porta ut, maximus at felis. Donec aliquam, velit a tempus accumsan, lorem metus viverra augue, ac convallis quam enim quis lacus. Aliquam ipsum orci, ullamcorper vel erat in, semper posuere tortor. Vestibulum consequat ante nec mauris iaculis ultrices. Vivamus non sagittis sem. Duis a laoreet ante, in facilisis nisl. Quisque tempor non orci id accumsan. Ut nulla augue, ultricies vel odio sed, porta finibus massa. Nunc auctor ante sit amet mi fermentum accumsan. Phasellus fermentum sed lacus id ornare. Curabitur congue, neque sed porta faucibus, risus orci aliquet ex, id fermentum nisl sapien vel sem. Nunc sodales, elit et hendrerit consectetur, sem mauris tempus ligula, sed faucibus quam libero a nibh. Sed orci ex, imperdiet dignissim urna ac, egestas bibendum tortor.
                                </p>
                            <div className={classes.buttonContainer}>

                                <Button className={classes.button} variant="contained" color="inherit" href="#top">
                                    Learn More
                                    </Button>
                            </div>
                        </Grid>
                        <Grid item xs={6}>
                            <Typography variant="h5" component="h3" gutterBottom>
                                Description of Simulator
                            </Typography>
                            <p style={{ fontSize: '18px' }}>
                                Lorem ipsum dolor sit amet, consectetur adipiscing elit. In arcu ligula, auctor ut dictum ac, malesuada et arcu. Vestibulum ut commodo enim, in pulvinar magna. Mauris est enim, pretium id porta ut, maximus at felis. Donec aliquam, velit a tempus accumsan, lorem metus viverra augue, ac convallis quam enim quis lacus. Aliquam ipsum orci, ullamcorper vel erat in, semper posuere tortor. Vestibulum consequat ante nec mauris iaculis ultrices. Vivamus non sagittis sem. Duis a laoreet ante, in facilisis nisl. Quisque tempor non orci id accumsan. Ut nulla augue, ultricies vel odio sed, porta finibus massa. Nunc auctor ante sit amet mi fermentum accumsan. Phasellus fermentum sed lacus id ornare. Curabitur congue, neque sed porta faucibus, risus orci aliquet ex, id fermentum nisl sapien vel sem. Nunc sodales, elit et hendrerit consectetur, sem mauris tempus ligula, sed faucibus quam libero a nibh. Sed orci ex, imperdiet dignissim urna ac, egestas bibendum tortor.
                            </p>
                            <div className={classes.buttonContainer}>
                                <Button className={classes.button} variant="contained" color="inherit" href="#top" style={styles.buttonStyle}>
                                    Learn More
                            </Button>
                            </div>
                        </Grid>
                        <Grid item xs={6}>
                            <img className={classes.whiteBackground} src='https://icon-library.com/images/simulator-icon/simulator-icon-2.jpg' alt="Simulator" title="Simulator" />
                        </Grid>
                    </Grid>
                </div>

                <div className={classes.blogSection}>
                    <Typography variant="h4" component="h2" gutterBottom>
                        Recent Blog Posts
                    </Typography>

                    <Grid container spacing={2}>
                        <Grid item xs={4}>
                            <div className={classes.blogContainer}>
                                <div className={classes.blogContent}>
                                    <div className={classes.imgContainer}>
                                        <img className={classes.blogImg}  src='https://icon-library.com/images/009_070_checkpoint_geo_location_geolocation_target_here-512.png' />
                                    </div>
                                    <Grid container spacing={4}>
                                        <Grid item xs={6}>
                                            <Typography variant="h5" component="h3" gutterBottom>
                                                Title
                                            </Typography>
                                        </Grid>
                                        <Grid item xs={6}>
                                            <Typography variant="h5" component="h3" gutterBottom>
                                                Date
                                            </Typography>
                                        </Grid>
                                    </Grid>
                                    <p className={classes.blogText}>
                                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. In arcu ligula, auctor ut dictum ac, malesuada et arcu. Vestibulum ut commodo enim, in pulvinar magna. Mauris est enim, pretium id porta ut, maximus at felis. Donec aliquam, velit a tempus accumsan, lorem metus viverra augue, ac convallis quam enim quis lacus.
                                    </p>
                                    <div className={classes.buttonContainer}>
                                        <Button className={classes.button} variant="contained" color="inherit" href="#top" style={styles.buttonStyle}>
                                            Read More
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </Grid>
                        <Grid item xs={4}>
                            <div className={classes.blogContainer}>
                                <div className={classes.blogContent}>
                                    <div className={classes.imgContainer}>
                                        <img className={classes.blogImg} src='https://icon-library.com/images/1276.svg.svg' />
                                    </div>
                                    <Grid container spacing={4}>
                                        <Grid item xs={6}>
                                            <Typography variant="h5" component="h3" gutterBottom>
                                                Title
                                            </Typography>
                                        </Grid>
                                        <Grid item xs={6}>
                                            <Typography variant="h5" component="h3" gutterBottom>
                                                Date
                                            </Typography>
                                        </Grid>
                                    </Grid>
                                    <p className={classes.blogText}>
                                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. In arcu ligula, auctor ut dictum ac, malesuada et arcu. Vestibulum ut commodo enim, in pulvinar magna. Mauris est enim, pretium id porta ut, maximus at felis. Donec aliquam, velit a tempus accumsan, lorem metus viverra augue, ac convallis quam enim quis lacus.
                                    </p>
                                    <div className={classes.buttonContainer}>
                                        <Button className={classes.button} variant="contained" color="inherit" href="#top" style={styles.buttonStyle}>
                                            Read More
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </Grid>
                        <Grid item xs={4}>
                            <div className={classes.blogContainer}>
                                <div className={classes.blogContent}>
                                    <div className={classes.imgContainer}>
                                        <img className={classes.blogImg} src='https://icon-library.com/images/072_chocolatebar-512_4905.png' />
                                    </div>
                                    <Grid container spacing={4}>
                                        <Grid item xs={6}>
                                            <Typography variant="h5" component="h3" gutterBottom>
                                                Title
                                            </Typography>
                                        </Grid>
                                        <Grid item xs={6}>
                                            <Typography variant="h5" component="h3" gutterBottom>
                                                Date
                                            </Typography>
                                        </Grid>
                                    </Grid>
                                    <p className={classes.blogText}>
                                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. In arcu ligula, auctor ut dictum ac, malesuada et arcu. Vestibulum ut commodo enim, in pulvinar magna. Mauris est enim, pretium id porta ut, maximus at felis. Donec aliquam, velit a tempus accumsan, lorem metus viverra augue, ac convallis quam enim quis lacus.
                                    </p>
                                    <div className={classes.buttonContainer}>
                                        <Button className={classes.button} variant="contained" color="inherit" href="#top">
                                            Read More
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </Grid>
                    </Grid>
                </div>
            </React.Fragment>
        );
    }
}

export default withStyles(styles)(Home);