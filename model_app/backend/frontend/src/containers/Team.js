import React from 'react';
import {Header} from '../components'
import leaders from '../const/leader.js'
import members from '../const/member.js'
import './Team.css'

function Team(props){
  let supervisorList = [];
  let list = [];
  let memberlist = [];

  members.forEach(member => {
    memberlist.push(member);
  })

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

     <div className = 'CardGreenBackground1' >
        <h3 align="left">Team Members</h3>
        <br></br>
        <div  align="left" className='MemberList'>
          <MemberList list={memberlist}/>
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

function MemberList(props){

  let counter = 0;
  const memberCards = props.list.map(member => {
    return(
      <MemberCardLeft key={member.name} name={member.name} description = {member.major} />
    );
    }
  );
  return(<div>{memberCards}</div>);
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

function MemberCardLeft(props){
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
