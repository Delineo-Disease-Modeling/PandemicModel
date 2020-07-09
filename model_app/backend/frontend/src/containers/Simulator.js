import React, {Component} from 'react';
import { County, Timeseries, GoogleMap } from '../components';
import { Dropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap';
import './Simulator.css'


function intervention(props){

    return(
        <div align='left' className='row'>

            <div className='col'>
                <text style={{color:'white', marginRight:'10px', textAlign:'left'}}>Policy Intervention</text>
            </div>
            
            <div className='col'>
                <text style={{color:'white', marginRight:'20px'}} >Duration :</text>
                <text className='durationText' style={{backgroundColor:'#1b4441ad', padding:'5px', textAlign:'center', border:'2px solid #66FCF1', borderRadius:'40px', minWidth:'90px'}}>90-days</text>
            </div>
            
            <div className='col2'>
                <i align='right' class="fa fa-close" style={{fontSize:'30px', color:'#66FCF1'}}></i>
            </div>
            

            <hr align='left' className='dotted'></hr>

        </div>
    );
}

class OptionMenu extends Component{

    constructor() {
        super();
        this.state = {
            dropdownOpen:false,
            selectedPolicy:'Policy'
        };
    }

    handleSelectedPolicy = (item)=>{this.setState({selectedPolicy:item})}

    toggle = () => this.setState({dropdownOpen: !this.state.dropdownOpen});


    render(){
        return(
            <Dropdown isOpen={this.state.dropdownOpen} toggle={this.toggle}>
                <DropdownToggle caret> {this.state.selectedPolicy} </DropdownToggle>
                <DropdownMenu>
                    {this.props.list.map((item)=>{
                        return(
                        <DropdownItem onClick={()=>{this.setState({selectedPolicy:item})}}>{item}</DropdownItem>
                        );
                    })}
                </DropdownMenu>
            </Dropdown>
        );
        
    }

}

function Parameters(){
    return(

    <div>

        <div className='row'>
            <div className='col'>
                <table>
                    <tbody>

                        <tr>
                            <td>
                                <label className='label'>Simulation duration (days):</label>
                            </td>
                            <td>
                                <input required minLength='6' type='text' size='15'></input>
                            </td>
                        </tr>

                        <tr>
                            <td>
                                <label className='label'>Other Parameters:</label>
                            </td>
                            <td>
                                <input required minLength='6' type='text' size='15'></input>
                            </td>
                        </tr>

                    </tbody>
                </table>
                
            </div>

            <div className='col'> 

                <table>
                    <tbody>

                        <tr>
                            <td>
                                <label className='label'>Infection duration (days):</label>
                            </td>
                            <td>
                                <input required minLength='6' type='text' size='15'></input>
                            </td>
                        </tr>

                        <tr>
                            <td>
                                <label className='label'>Other Parameters:</label>
                            </td>
                            <td>
                                <input required minLength='6' type='text' size='15'></input>
                            </td>
                        </tr>

                    </tbody>
                </table>

            </div>
        </div>

    </div> 
    );
}

class Simulator extends Component{


    render(){

        return(
            <div className='CardBackground'>

                <div className='GreenBackground'>
                    <h3>Map</h3>
                    <County/>
                    <GoogleMap/> 
                </div>

                <div className='GreenBackground'>
                    <h3>Configurations</h3>
                    <p style={{textAlign:'left', fontSize:'20px', color:'#66FCF1'}}>Model Parameters</p>
                    <Parameters/>
                    <p style={{textAlign:'left', fontSize:'20px', color:'#66FCF1', marginTop:'20px'}}>Intervention Policy</p>
                    <div style={{textAlign:'left', marginLeft:'55px'}}>
                        <button className='button'>Add+</button>
                        
                    </div>
                
                    <br></br>
                    <button className='button' >Run Simulation</button>
                </div>
                
                <div className='GreenBackground'>
                    <h3>Analysis</h3>
                    <Timeseries/>
                </div>
                
                <OptionMenu list={["hello", "hi"]}></OptionMenu>

                
            </div>
        );

    }

}

export default Simulator;