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
      <div className = 'CardGreenBackground'>
      <Header text='Meet The Team' />
      <h2 className="header2" >Research Supervisor</h2>
      <SupervisorList list={supervisorList} />
      <h2 className="header2" >Team Leaders</h2>
      <LeaderList list={list}/>
      </div>
    </div>
  );
}


function LeaderList(props){

  let counter = 0;
  const leaderCards = props.list.map(leader => {
    if(counter%2){
        counter++;
        return(
          <TeamLeaderCardRight key={leader.name} name={leader.name} description = {leader.description} image={leader.image} />
        );
      }
    else{
        counter++;
        return(
          <TeamLeaderCardLeft key={leader.name} name={leader.name} description = {leader.description} image={leader.image} />
        );
      }
    }
  );
  return(<div className="LeaderList">{leaderCards}</div>);
}

function SupervisorList(props) {
  const supervisorCards = props.list.map(supervisor =>
    <SupervisorCard key={supervisor.name} name={supervisor.name} description={supervisor.description} image={supervisor.image}/>
  );
  return <div>{supervisorCards}</div>;
}

function TeamLeaderCardLeft(props){
  return(
    <div align= "left" className="Card">
        <img alt='team leader' src={props.image} width="150px" height="150px" className="LeaderImage"></img>
        <div className="Inner">
          <h4 className="LeaderName">{props.name}</h4>
          <p className="Text">
            {props.description}
          </p>
        </div>
    </div>

  );

}

function TeamLeaderCardRight(props){
  return(
    <div align= "left" className="Card">
        <img  alt='team leader' src={props.image} width="150px" height="150px" className="LeaderImageRight"></img>
        <div className="InnerRight">
          <h4 className="LeaderNameRight">{props.name}</h4>
          <p className="TextRight">
            {props.description}
          </p>
        </div>
    </div>
  );
}

function SupervisorCard(props){
  return(
    <div align= "left" className="Card">
        <img  alt='supervisor' src={props.image} width="250px" height="250px" className="LeaderImage"></img>
        <div className="Inner">
          <h4 className="LeaderName">{props.name}</h4>
          <p className="Text">
            {props.description}
          </p>
        </div>
    </div>
  );
}

export default Team;
