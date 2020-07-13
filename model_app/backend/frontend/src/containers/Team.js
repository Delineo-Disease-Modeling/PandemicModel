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
      <Header text='Meet The Team' />
      <div className = 'CardGreenBackground'>
      <h2 className="header2" >Research Supervisor</h2>
      <SupervisorList list={supervisorList} />
      </div>
      <div className = 'CardLightGreenBackground'>
      <h2 className="header2" >Team Leaders</h2>
      <LeaderList list={list}/>
      </div>
    </div>
  );
}


function LeaderList(props){

  let counter = 0;
  const leaderCards = props.list.map(leader => {
    if(counter%3){
        counter++;
        return(
          <TeamLeaderCardLeft key={leader.name} name={leader.name} description = {leader.description} />
        );
      }
    else if(counter%3 === 1){
      counter++;
        return(
          <TeamLeaderCardCenter key={leader.name} name={leader.name} description = {leader.description} />
        );
    }
    else{
        counter++;
        return(
          <TeamLeaderCardRight key={leader.name} name={leader.name} description = {leader.description} />
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
    <div align= "left" className="LeaderCard">
        <div className="Inner">
          <h4 className="LeaderName">{props.name}</h4>
          <p className="Text">
            {props.description}
          </p>
        </div>
    </div>

  );

}

function TeamLeaderCardCenter(props){
  return(
    <div align= "center" className="LeaderCard">
        <div className="Inner">
          <h4 className="LeaderNameC">{props.name}</h4>
          <p className="Text">
            {props.description}
          </p>
        </div>
    </div>

  );

}

function TeamLeaderCardRight(props){
  return(
    <div align= "left" className="LeaderCard">
        <div className="Inner">
          <h4 className="LeaderName">{props.name}</h4>
          <p className="TextRight">
            {props.description}
          </p>
        </div>
    </div>
  );
}

function SupervisorCard(props){
  return(
    <div align= "left" className="SuperCard">
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
