import React from 'react';
import {Header} from '../components'
import leaders from '../const/leader.js'
import './Team.css'

function Team(props){
  let supervisorList = [];
  let list = [];

  leaders.forEach(leader => {
    if (leader.designation === 'Research Supervisor') {
      supervisorList.push(leader);
    }
    else {
      list.push(leader);
    }
  });

  return(
     <div className = 'CardBackground'>
       <div className="MainHeader">
         <h2>Meet The Team</h2>
       </div>
      <div className = 'CardGreenBackground1'>
        <h3 align='left'>Research Supervisor</h3>
        <SupervisorList list={supervisorList} />
      </div>
      <div className = 'CardLightGreenBackground'>
        <h3 align="left">Team Leaders</h3>
        <br></br>
        <div  align="left" className='LeaderList'>
          <LeaderList list={list}/>
        </div>
        
      </div>
    </div>
  );
}


function LeaderList(props){

  let counter = 0;
  const leaderCards = props.list.map(leader => {
    return(
      <TeamLeaderCardLeft key={leader.name} name={leader.name} description = {leader.major} />
    );
    }
  );
  return(<div>{leaderCards}</div>);
}

function SupervisorList(props) {
  const supervisorCards = props.list.map(supervisor =>
    <SupervisorCard key={supervisor.name} name={supervisor.name} description={supervisor.profession} image={supervisor.image}/>
  );
  return <div>{supervisorCards}</div>;
}

function TeamLeaderCardLeft(props){
  return(
    <div align= "left" className="LeaderCard">
        <div className="Inner">
          <h4 className="LeaderName">{props.name}</h4>
          <h5 className="ProfessionText"> {props.description} </h5>
        </div>
    </div>

  );

}

function SupervisorCard(props){
  return(
    <div align= "left" className="SuperCard">
        <div className="Inner">
          <h4 className="LeaderName">{props.name}</h4>
          <h5 className="ProfessionText">{props.description}</h5>
        </div>
    </div>
  );
}

export default Team;
