import React from 'react'

import leaders from '../const/leader.js';
import members from '../const/member.js';
import TeamGridList from '../components/TeamGridList.js'
import SupGridList from '../components/SupGridList.js'
import LeadGridList from '../components/LeaderGridList.js'

function FunctionClick() {
    function clickHandler() {
        console.log("hello world")
        
        


    }

    return (
        <div>
            <button onClick={clickHandler}>Click</button>
        </div>

    )
}


export default FunctionClick