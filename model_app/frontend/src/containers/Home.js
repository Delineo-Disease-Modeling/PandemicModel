import React, { Component } from 'react';
import { Media } from 'reactstrap';
import { AboutImg, DevelopmentBlogImg, SimulatorImg, TeamImg } from '../images'

import CssBaseline from '@material-ui/core/CssBaseline';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';

class Home extends Component {
    constructor(props) {
        super(props);
        this.links = [
            {
                id: 0,
                name: 'About',
                image: AboutImg,
                description: 'Overview of our Covid-19 Modeling project'
            },
            {
                id: 1,
                name: 'Team',
                image: TeamImg,
                description: 'Our team composition and leadership'
            },
            {
                id: 2,
                name: 'Simulator',
                image: SimulatorImg,
                description: 'Use this page to run the simulator we create for Covid-19 Modeling'
            },
            {
                id: 3,
                name: 'Development Blog',
                image: DevelopmentBlogImg,
                description: 'The page displaying our process of simulator development and expectation on future update'
            },
        ];
    }

    render() {

        const menu = this.links.map((link) => {
            let imagStyle = {
                maxHeight: 128,
                maxWidth: 128
            };
            return (
                <div key={link.id} className="col-12 mt-5">
                    <Media tag="li">
                        <Media left middle>
                            <Media object src={link.image} style={imagStyle} alt={link.name} />
                        </Media>
                        <Media body className="ml-5">
                            <Media heading style={{color: "#66FCF1"}}>{link.name}</Media>
                            <p>{link.description}</p>
                        </Media>
                    </Media>
                </div>
            );
        });

        return (
            <React.Fragment>
                <CssBaseline />
                <Container maxWidth="xl">
                    <Typography component="div" style={{ margin: '-30px', backgroundColor: 'black', backgroundImage: "url('https://9to5mac.com/wp-content/uploads/sites/6/2020/01/Coronavirus.jpg?quality=82&strip=all')", backgroundRepeat: "no-repeat", height: '100vh' }} />

                    <div className="row" style={{position: "absolute", top: '13%', left: "10%", backgroundColor: "rgba(0, 0, 0, 0.70)"}}>
                            <Media list>
                                {menu}
                            </Media>
                        </div>
                </Container>
            </React.Fragment>
        );
    }
}

export default Home;