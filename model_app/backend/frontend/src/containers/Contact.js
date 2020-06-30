import React from 'react';
/*
import image from './profile2.jpg'
import {leaders} from './teamLeaders.js'
import dotImage from './dots.PNG'
import './TeamStyle.css'

function LeaderList(){

  var length = leaders.length;
  console.log("Length: "+length)

  
  let counter = 0;
  const leaderCards = leaders.map(leader => {
      if(counter%2 == 0){
        counter++;
        return(
          <TeamLeaderCardLeft name={leader.name} bio = {leader.bio}></TeamLeaderCardLeft>
        );
      }
      else{
        counter++;
        return(
          <TeamLeaderCardRight name={leader.name} bio = {leader.bio}></TeamLeaderCardRight>
        );
      }
    }
  );
  return(<div class="LeaderList">{leaderCards}</div>);
}

function TeamLeaderCardLeft(props){
  return(
    <div align= "left" class="Card">
        <img src={image} width="150px" height="150px" class="LeaderImage"></img>
        <div class="Inner">
          <h4 class="LeaderName">{props.name}</h4>
          <p class="Text">
            {props.bio}
          </p>
        </div>
    </div>

  );

}

function TeamLeaderCardRight(props){
  return(
    <div align= "left" class="Card">
        <img src={image} width="150px" height="150px" class="LeaderImageRight"></img>
        <div class="InnerRight">
          <h4 class="LeaderNameRight">{props.name}</h4>
          <p class="TextRgit">
            {props.bio}
          </p>
        </div>
    </div>

  );

}


function SupervisorCard(props){
  return(
    <div align= "left" class="Card">
        <img src={image} width="250px" height="250px" class="LeaderImage"></img>
        <div class="Inner">
          <h4 class="LeaderName">{props.name}</h4>
          <p class="Text">
            {props.bio}
          </p>
        </div>
    </div>

  );

}
*/
function Contact(){
    return <div className="container">WIP</div>;
        /*
  return(
    <>
      <h3 class="header">Meet The Team</h3> 
      <img src={dotImage} class = "DoteImage" ></img>
      <h2 class="header2" >Reasearch Supervisor</h2>
      <SupervisorCard name="Supervisor Name" bio = "Hello World" ></ SupervisorCard>
      <img src={dotImage} class = "DoteImage" ></img>
      <h2 class="header3" >Team Leaders</h2>
      <LeaderList></LeaderList>
    </>
  ); */
}



export default Contact;