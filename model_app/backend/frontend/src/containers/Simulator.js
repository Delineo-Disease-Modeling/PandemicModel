import React, {Component} from 'react';
import { County, Timeseries, GoogleMap } from '../components';
import { Dropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap';
import './Simulator.css'




class OptionMenu extends Component{

    constructor() {
        super();
        this.state = {
            hidden: false,
            dropdownOpen:false,
            selectedPolicy:'Policy',
            duration:'0',
            policyComponent: [],
            policyList:["Schools", "Travel Ban", ">500 Gatherings","Restuarants", ">50 Gatherings"]
        };
    }

    handleAdd = ()=>{
        this.setState({hidden: !this.state.hidden})
        console.log("Add Was clicked:"+ this.state.hidden)
    }

    toggle = () => this.setState({dropdownOpen: !this.state.dropdownOpen});

    save = ()=>{
        if(this.state.duration != '' && this.state.selectedPolicy != 'Policy'){
            this.setState({policyComponent:[...this.state.policyComponent, <Intervention policy={this.state.selectedPolicy} days={this.state.duration}/>]})
            let array = this.state.policyList;
            let pos = array.indexOf(this.state.selectedPolicy); 
            if(pos>-1){
                array.splice(pos, 1);
            }
            this.setState({policyList:array, selectedPolicy:'Policy', hidden:!this.state.hidden});
        }
    }


    render(){
        return(
            <div>
                {this.state.policyComponent}
                <div align='left' className={this.state.hidden? 'hidden':''}>
                    <div className='row'>

                        <div className='col4'>
                        <Dropdown isOpen={this.state.dropdownOpen} toggle={this.toggle} style={{marginLeft:'10px'}}> 
                            <DropdownToggle caret> {this.state.selectedPolicy} </DropdownToggle>
                            <DropdownMenu>
                                {this.state.policyList.map((item)=>{
                                    return(
                                    <DropdownItem onClick={()=>{this.setState({selectedPolicy:item})}}>{item}</DropdownItem>
                                    );
                                })}
                            </DropdownMenu>
                        </Dropdown>
                        </div>

                        <div align='left' className='col4'>
                            <text style={{color:'white'}}>Duration (in days): </text>
                            <input required size='15' type='text' style={{marginRight:'10px'}} onChange={event=> this.setState({duration:event.target.value})}></input>
                            
                        </div>

                        <div align='left' className='col4'>
                            <button className='buttonSave' onClick={this.save}>Save</button>
                        </div>
                        
                    </div>
                    <hr align='left' className='dotted2'></hr>

                </div>

                <div style={{textAlign:'left', marginLeft:'55px'}}>
                        <button className='button'onClick={this.handleAdd}>Add+</button>
                </div>

            </div>

        );
        
    }

}


function Intervention(props){

    return(
        <div align='left' className='row'>

            <div className='col'>
            <text style={{color:'white', marginRight:'10px', textAlign:'left'}}>{props.policy}</text>
            </div>
            
            <div className='col'>
                <text style={{color:'white', marginRight:'20px'}} >Duration :</text>
                <text className='durationText' style={{backgroundColor:'#1b4441ad', padding:'5px', textAlign:'center', border:'2px solid #66FCF1', borderRadius:'40px', minWidth:'90px'}}>{props.days} days</text>
            </div>
            
            <div className='col2'>
                <i align='right' class="fa fa-close" style={{fontSize:'30px', color:'#66FCF1'}}></i>
            </div>
            

            <hr align='left' className='dotted'></hr>

        </div>
    );
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

    constructor(){
        super();
        this.state={
            hidden:false,
            policy:'',
        }
    }


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

                    <OptionMenu/>

                    
                    <br></br>
                    <button className='button' >Run Simulation</button>

                </div>
                
                <div className='GreenBackground'>
                    <h3>Analysis</h3>
                    <Timeseries/>
                </div>
                
                

                
            </div>
        );

    }

}

export default Simulator;