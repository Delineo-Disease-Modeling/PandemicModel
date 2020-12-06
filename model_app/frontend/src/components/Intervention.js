import React, {Component} from 'react';
import '../containers/Simulator.css'

class Intervention extends Component{

    remove = ()=>{
        this.props.remove(this.props.position, this.props.policy);
    }
    render(){
        return(
            <div align='left' className='row'>

                <div className='col'>
                    <p style={{color:'white', marginRight:'10%', textAlign:'left', fontSize:'20px'}}>{this.props.policy}</p>
                </div>

                <div className='col5'>
                    <p style={{color:'white', fontSize:'20px'}}>Duration:</p>
                    <p className='durationText' style={{backgroundColor:'#1b4441ad', padding:'2px', textAlign:'center', border:'2px solid #66FCF1', borderRadius:'40px', minWidth:'90px'}}>{this.props.days} days</p>
                </div>

                <div className='col4'>
                    <i  align='left' onClick={this.remove} className="fa fa-close" style={{fontSize:'30px', color:'#66FCF1'}}></i>
                </div>

                <hr align='left' className='dotted'></hr>

            </div>
        );

    }


}

export default Intervention;
