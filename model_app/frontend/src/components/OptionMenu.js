import React, { Component } from 'react';
import '../containers/Simulator.css'
import Intervention from './Intervention.js'
import { Dropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap';

class OptionMenu extends Component {

    constructor() {
        super();
        this.state = {
            hidden: false,
            dropdownOpen: false,
            selectedPolicy: 'Policy',
            duration: '0',
            policyComponent: [],
            policyList: ["Stay At Home Order", "Social Distancing Order", "Sanitation Order", "Mandatory Mask Order" ]
        };
        this.deleteItem = this.deleteItem.bind(this);
    }

    handleAdd = () => {
        this.setState({ hidden: !this.state.hidden })
        //console.log("Add Was clicked:"+ this.state.hidden)
    }

    toggle = () => this.setState({ dropdownOpen: !this.state.dropdownOpen });

    deleteItem = (pos, policy) => {

        this.setState({ policyComponent: this.state.policyComponent.filter((item) => item.policy !== policy) });

        let list = this.state.policyList;
        list.push(policy);
        this.setState({ policyList: list });
    }

    save = () => {
        if (this.state.duration !== '' && this.state.selectedPolicy !== 'Policy') {
            let newPolicy = {
                policy: this.state.selectedPolicy,
                duration: this.state.duration,
            }
            this.setState({ policyComponent: [...this.state.policyComponent, newPolicy] })
            let array = this.state.policyList;
            let pos = array.indexOf(this.state.selectedPolicy);
            if (pos > -1) {
                array.splice(pos, 1);
            }
            this.setState({ policyList: array, selectedPolicy: 'Policy', hidden: !this.state.hidden });
        }
    }



    render() {
        return (
            <div>
                {this.state.policyComponent.map((item) => {
                    return (<Intervention key={item.policy} policy={item.policy} days={item.duration} remove={this.deleteItem.bind(this)} />);
                })}
                <div align='left' className={this.state.hidden ? 'hidden' : ''}>
                    <div className='row'>

                        <div className='col'>
                            <Dropdown isOpen={this.state.dropdownOpen} toggle={this.toggle} style={{ marginLeft: '10px' }}>
                                <DropdownToggle caret> {this.state.selectedPolicy} </DropdownToggle>
                                <DropdownMenu>
                                    {this.state.policyList.map((item) => {
                                        return (
                                            <DropdownItem key={item} onClick={() => { this.setState({ selectedPolicy: item }) }}>{item}</DropdownItem>
                                        );
                                    })}
                                </DropdownMenu>
                            </Dropdown>

                          </div>
                          <div className ='col'>
                              <label htmlFor='usr' style={{color: 'white' }}>Duration (in days): </label>
                              &nbsp; &nbsp;
                              <input align='left' required size='15' type='text' style={{ marginRight: '30px', marginLeft: '0px' }} onChange={event => this.setState({ duration: event.target.value })}></input>
                          </div>
                          <div align='bottom' className='col4'>
                                <button className='buttonSave' onClick={this.save}>Save</button>
                          </div>


                        {/* <div align='left' className='col4'>
                            <label htmlFor='usr' style={{color:'white'}}>Duration (in days): </label>
                            <input align='left' required size='15' type='text' style={{marginRight:'30px', marginLeft:'0px'}} onChange={event=> this.setState({duration:event.target.value})}></input>

                            </div> */}


                    </div>
                    <br></br>
                    <hr align='left' className='dotted'></hr>

                </div>

                <div style={{ textAlign: 'left', marginLeft: '55px' }}>
                    <button className='button' onClick={this.handleAdd}>Add+</button>

                </div>
                <br></br>


            </div>

        );

    }

}

export default OptionMenu;
