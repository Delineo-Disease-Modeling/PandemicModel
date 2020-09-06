import React, { Component } from 'react';
import { Media } from 'reactstrap';
import { AboutImg, DevelopmentBlogImg, SimulatorImg, TeamImg } from '../images'

class Home extends Component{

    constructor(props) {
        super(props);

        this.links = [
            {
                id: 0,
                name:'About',
                image: AboutImg,
                description:'Overview of our Covid-19 Modeling project'
            },
            {
                id: 1,
                name:'Team',
                image: TeamImg,
                description:'Our team composition and leadership'
            },
            {
                id: 2,
                name:'Simulator',
                image: SimulatorImg,
                description:'Use this page to run the simulator we create for Covid-19 Modeling'
            },
            {
                id: 3,
                name:'Development Blog',
                image: DevelopmentBlogImg,
                description:'The page displaying our process of simulator development and expectation on future update'
            },
        ];
    }

    render() {

        const menu = this.links.map((link) => {
            let imagStyle = {maxHeight: 128,
                maxWidth: 128};
            return (
                <div key={link.id} className="col-12 mt-5">
                    <Media tag="li">
                        <Media left middle>
                            <Media object src={link.image} style={imagStyle} alt={link.name} />
                        </Media>
                        <Media body className="ml-5">
                            <Media heading>{link.name}</Media>
                            <p>{link.description}</p>
                        </Media>
                    </Media>
                </div>
            );
        });

        return (
            <div className="container">
                <div className="row">
                    <Media list>
                        {menu}
                    </Media>
                </div>
            </div>
        );
    }
}

export default Home;