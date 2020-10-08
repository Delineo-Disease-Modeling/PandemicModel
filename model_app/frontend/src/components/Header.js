import React, {Component} from 'react';
import { Navbar, NavbarBrand, Nav, NavbarToggler, Collapse, NavItem } from 'reactstrap';
import {NavLink} from 'react-router-dom';
import './Header.css';
import Logo from "./../images/delineo_vector_2.0.1.png"

class Header extends Component{

    constructor(props){
        super(props);
        this.state = {
            isNavOpen: false,
            isModalOpen: false
        };
        this.toggleNav = this.toggleNav.bind(this);
        this.toggleModal = this.toggleModal.bind(this);
    }

    toggleNav(){
        this.setState({
            isNavOpen: !this.state.isNavOpen
        });
    }

    toggleModal(){
        this.setState({
            isModalOpen: !this.state.isModalOpen,
        });
    }


    render(){

        const styleSheet = {
            color: "white"
        }

        const active={
            color:'#66FCF1', 
            borderBottom: '1px solid #66FCF1', 
            paddingBottom: '4px', 
        
        }

        return (
            <Navbar expand="md" className="color">
                <div className="container">
                <NavbarToggler onClick={this.toggleNav} />
                <NavbarBrand className="mr-auto" href="/">
                    <img src={Logo} alt="Logo" width="200" height="65"></img>
                </NavbarBrand>
                <Collapse isOpen={this.state.isNavOpen} navbar>
                    <Nav navbar className="ml-auto">
			<NavItem>                                                                               
                            <NavLink className="Nav-link"  to='/MapVisualization' activeClassName='active' activeStyle={active} style={styleSheet}>Map Visualization</NavLink>                                    
                        </NavItem>

                        <NavItem>
                            <NavLink className="Nav-link" to='/simulator' activeClassName='active' activeStyle={active} style={styleSheet}> Simulator</NavLink>
                        </NavItem>

                        <NavItem>
                            <NavLink className="Nav-link" to='/about' activeClassName='active' activeStyle={active} style={styleSheet}>About</NavLink>
                        </NavItem>

                        <NavItem>
                            <NavLink className="Nav-link" to='/team' activeClassName='active' activeStyle={active} style={styleSheet}>Team</NavLink>
                        </NavItem>

                        <NavItem>
                            <NavLink className="Nav-link"  to='/developmentblog' activeClassName='active' activeStyle={active} style={styleSheet}> Development Blog</NavLink>
                        </NavItem>
                    </Nav>
                </Collapse>
                </div>
            </Navbar>
            
        );
    }
}

export default Header;
