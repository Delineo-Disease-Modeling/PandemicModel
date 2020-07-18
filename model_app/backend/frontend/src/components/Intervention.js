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

export default Intervention;