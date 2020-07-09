import React, {Component} from 'react';
import { County, Timeseries, GoogleMap } from '../components';
import { Dropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap';
import './Simulator.css'
import axios from 'axios';



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
        this.deleteItem = this.deleteItem.bind(this);
    }

    handleAdd = ()=>{
        this.setState({hidden: !this.state.hidden})
        console.log("Add Was clicked:"+ this.state.hidden)
    }

    toggle = () => this.setState({dropdownOpen: !this.state.dropdownOpen});

    deleteItem = (pos, policy)=>{
        
        this.setState({policyComponent: this.state.policyComponent.filter((item)=> item.policy!= policy)});

        let list = this.state.policyList;
        list.push(policy);
        this.setState({policyList:list});
        console.log("Item has been removed: "+this.state.policyComponent.length);
    }

    save = ()=>{
<<<<<<< HEAD
        if(this.state.duration != '' && this.state.selectedPolicy != 'Policy'){
            let newPolicy = {
                policy: this.state.selectedPolicy,
                duration:this.state.duration,
            }
            this.setState({policyComponent:[...this.state.policyComponent, newPolicy]})
=======
        if(this.state.duration !== '' && this.state.selectedPolicy !== 'Policy'){
            this.setState({policyComponent:[...this.state.policyComponent, <Intervention policy={this.state.selectedPolicy} days={this.state.duration}/>]})
>>>>>>> 2381b4ab1beab676d96ef4afbfadb5e4028d9f8d
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
                {this.state.policyComponent.map((item)=>{
                    return(<Intervention policy={item.policy} days={item.duration} remove={this.deleteItem.bind(this)}/>);
                })}
                <div align='left' className={this.state.hidden? 'hidden':''}>
                    <div className='row'>

                        <div className='col4'>
                        <Dropdown isOpen={this.state.dropdownOpen} toggle={this.toggle} style={{marginLeft:'10px'}}> 
                            <DropdownToggle caret> {this.state.selectedPolicy} </DropdownToggle>
                            <DropdownMenu>
                                {this.state.policyList.map((item)=>{
                                    return(
                                    <DropdownItem key={item} onClick={()=>{this.setState({selectedPolicy:item})}}>{item}</DropdownItem>
                                    );
                                })}
                            </DropdownMenu>
                        </Dropdown>
                        </div>

                        <div align='left' className='col4'>
                            <p style={{color:'white'}}>Duration (in days): </p>
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


class Intervention extends Component{

    constructor(){
        super(); 
    }

    remove = ()=>{
        this.props.remove(this.props.position, this.props.policy);
    }
    render(){
        return(
            <div align='left' className='row'>

                <div className='col'>
                <text style={{color:'white', marginRight:'10px', textAlign:'left'}}>{this.props.policy}</text>
                </div>
                
                <div className='col'>
                    <text style={{color:'white', marginRight:'20px'}} >Duration :</text>
                    <text className='durationText' style={{backgroundColor:'#1b4441ad', padding:'5px', textAlign:'center', border:'2px solid #66FCF1', borderRadius:'40px', minWidth:'90px'}}>{this.props.days} days</text>
                </div>
                
                <div className='col2'>
                    <i align='right' onClick={this.remove} class="fa fa-close" style={{fontSize:'30px', color:'#66FCF1'}}></i>
                </div>
                
                <hr align='left' className='dotted'></hr>

            </div>
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

    constructor(){
        super();
        this.state={
            hidden:false,
            policy:'',
            loading: false,
            data: '',
            jobId: null
        }
    }

    handleOnClick = () => {
        // if user had an existing job request, delete that 
        if (this.state.jobId) {
            axios.delete(`./simulations/${this.state.jobId}`)
                .catch(err => console.log(err) );
        }

        // configure post body with specific model params
        let body = {};

        // send post request
        axios.post('./simulations', body)
            .then(res => {
                // only upon successful post request, update state with in progress state and 
                if (res.status === 200) {
                    this.setState({jobId: `${res.data}`, loading: true});
                    console.log('post sent with job id ' + res.data);

                    axios.get(`./simulations/${res.data}`)
                        .then(result => {
                            this.setState({
                                loading: false,
                                data: [...result.data],
                            });

                            console.log('simulation finished running');
                        })
                        .catch(err => {
                            console.log(err);
                        });

                    // should probably save data to redux store
                    // maybe also save jobId? idk yet
                }
            })
            .catch(err => {
                console.log(err);
                throw err;
            });
    }


    render(){
        const {data, loading} = this.state;

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
                    <button className='button' onClick={this.handleOnClick}>Run Simulation</button>

                </div>
                
                {loading ? <p>loading...</p> :
                <div className='GreenBackground'>
                    <h3>Analysis</h3>
                    <p>{data}</p>
                    <Timeseries/>
                </div>
                }
                
            </div>
        );

    }

}

export default Simulator;