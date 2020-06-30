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
    <>
      <Header text='Meet The Team'/>
      <h2 class="header2" >Research Supervisor</h2>
      <SupervisorList list={supervisorList} />
      <h2 class="header2" >Team Leaders</h2>
      <LeaderList list={list}/>
    </>
  );
}


function LeaderList(props){

  let counter = 0;
  const leaderCards = props.list.map(leader => {
    if(counter%2){
        counter++;
        return(
          <TeamLeaderCardRight name={leader.name} description = {leader.description} image={leader.image} />
        );
      }
    else{
        counter++;
        return(
          <TeamLeaderCardLeft name={leader.name} description = {leader.description} image={leader.image} />
        );
      }
    }
  );
  return(<div class="LeaderList">{leaderCards}</div>);
}

function SupervisorList(props) {
  const supervisorCards = props.list.map(supervisor =>
    <SupervisorCard name={supervisor.name} description={supervisor.description} image={supervisor.image}/>
  );
  return <div>{supervisorCards}</div>;
}

function TeamLeaderCardLeft(props){
  return(
    <div align= "left" class="Card">
        <img src={props.image} width="150px" height="150px" class="LeaderImage"></img>
        <div class="Inner">
          <h4 class="LeaderName">{props.name}</h4>
          <p class="Text">
            {props.description}
          </p>
        </div>
    </div>

  );

}

function TeamLeaderCardRight(props){
  return(
    <div align= "left" class="Card">
        <img src={props.image} width="150px" height="150px" class="LeaderImageRight"></img>
        <div class="InnerRight">
          <h4 class="LeaderNameRight">{props.name}</h4>
          <p class="TextRight">
            {props.description}
          </p>
        </div>
    </div>
  );
}

function SupervisorCard(props){
  return(
    <div align= "left" class="Card">
        <img src={props.image} width="250px" height="250px" class="LeaderImage"></img>
        <div class="Inner">
          <h4 class="LeaderName">{props.name}</h4>
          <p class="Text">
            {props.description}
          </p>
        </div>
    </div>
  );
}

export default Team;