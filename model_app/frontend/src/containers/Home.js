import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import CssBaseline from '@material-ui/core/CssBaseline';
import Typography from '@material-ui/core/Typography';
import './Home.css';

class Home extends Component {

    render() {

        return (
            <React.Fragment>
                <CssBaseline />
                <div className="image-box">
                    <div className="header-text">
                        <h1>Interactive Disease Simulation</h1>
                        <Button className="Button" variant="contained" color="primary" href="/simulator">
                            Explore Simulation
                        </Button>
                    </div>
                </div>

                <div className="about-section">
                    <Grid container spacing={3}>
                        <Grid item xs={6}>
                            <img src='https://icon-library.com/images/simulator-icon/simulator-icon-2.jpg' alt="Simulator" title="Simulator" />
                            <Typography variant="h5" component="h3" gutterBottom>
                                Description of ML
                        </Typography>
                            <p>
                                Lorem ipsum dolor sit amet, consectetur adipiscing elit. In arcu ligula, auctor ut dictum ac, malesuada et arcu. Vestibulum ut commodo enim, in pulvinar magna. Mauris est enim, pretium id porta ut, maximus at felis. Donec aliquam, velit a tempus accumsan, lorem metus viverra augue, ac convallis quam enim quis lacus. Aliquam ipsum orci, ullamcorper vel erat in, semper posuere tortor. Vestibulum consequat ante nec mauris iaculis ultrices. Vivamus non sagittis sem. Duis a laoreet ante, in facilisis nisl. Quisque tempor non orci id accumsan. Ut nulla augue, ultricies vel odio sed, porta finibus massa. Nunc auctor ante sit amet mi fermentum accumsan. Phasellus fermentum sed lacus id ornare. Curabitur congue, neque sed porta faucibus, risus orci aliquet ex, id fermentum nisl sapien vel sem. Nunc sodales, elit et hendrerit consectetur, sem mauris tempus ligula, sed faucibus quam libero a nibh. Sed orci ex, imperdiet dignissim urna ac, egestas bibendum tortor.
                        </p>
                            <div className='button-container'>

                                <Button className="Button" variant="contained" color="inherit" href="#top">
                                    Learn More
                        </Button>
                            </div>
                        </Grid>
                        <Grid item xs={6}>
                            <Typography variant="h5" component="h3" gutterBottom>
                                Description of Simulator
                            </Typography>
                            <p>
                                Lorem ipsum dolor sit amet, consectetur adipiscing elit. In arcu ligula, auctor ut dictum ac, malesuada et arcu. Vestibulum ut commodo enim, in pulvinar magna. Mauris est enim, pretium id porta ut, maximus at felis. Donec aliquam, velit a tempus accumsan, lorem metus viverra augue, ac convallis quam enim quis lacus. Aliquam ipsum orci, ullamcorper vel erat in, semper posuere tortor. Vestibulum consequat ante nec mauris iaculis ultrices. Vivamus non sagittis sem. Duis a laoreet ante, in facilisis nisl. Quisque tempor non orci id accumsan. Ut nulla augue, ultricies vel odio sed, porta finibus massa. Nunc auctor ante sit amet mi fermentum accumsan. Phasellus fermentum sed lacus id ornare. Curabitur congue, neque sed porta faucibus, risus orci aliquet ex, id fermentum nisl sapien vel sem. Nunc sodales, elit et hendrerit consectetur, sem mauris tempus ligula, sed faucibus quam libero a nibh. Sed orci ex, imperdiet dignissim urna ac, egestas bibendum tortor.
                            </p>
                            <div className='button-container'>
                                <Button className="Button" variant="contained" color="inherit" href="#top">
                                    Learn More
                            </Button>
                            </div>
                            <img src='https://icon-library.com/images/simulator-icon/simulator-icon-2.jpg' alt="Simulator" title="Simulator" />
                        </Grid>
                    </Grid>
                </div>

                <div className='blog-section'>

                </div>
            </React.Fragment>
        );
    }
}

export default Home;