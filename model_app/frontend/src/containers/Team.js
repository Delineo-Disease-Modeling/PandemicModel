import React, { Component }  from 'react';

import leaders from '../const/leader.js';
import members from '../const/member.js';
import TeamGridList from '../components/TeamGridList.js'
import SupGridList from '../components/SupGridList.js'
import LeadGridList from '../components/LeaderGridList.js'
import { makeStyles } from '@material-ui/core/styles';
import TeamFilter from '../components/TeamFilter'
import FunctionClick from '../components/FunctionClick'
import Grid from '@material-ui/core/Grid';
import { styled } from "@material-ui/core/styles";
import { spacing } from "@material-ui/system";
import MuiButton from "@material-ui/core/Button";


import './Team.css';


const Button = styled(MuiButton)(spacing);

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

  const useStyles = makeStyles((theme) => ({
    root: {
      '& > *': {
        margin: theme.spacing(1),
      },
    },
    alignItemsAndJustifyContent: {
      width: 500,
      height: 80,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: 'pink',
    },
  }));



  return(

    <div className = 'CardBackground'>

      <div className="MainHeader">
        <h2>Meet The Team</h2>
      </div>

      
    
  

      <div className = "Supervisor" align="center" >
        <h3 align="center">Research Supervisor</h3>

       

        <SupGridList   container
  spacing={0}
  direction="column"
  alignItems="center"
  justify="center"
  style={{ minHeight: '100vh' }}  ></SupGridList>



     

      </div>

      <div className = 'TeamFilter'>

      
      <Button mt={2} variant="contained" color="primary" className='TeamFilter' onClick={() => { console.log('onClick'); }} >All
        </Button>
        <Button mt={2}  variant="contained" color="primary" className='TeamFilter' onClick={() => { console.log('onClick'); }} >Full Stack
        </Button>
        <Button mt={2} variant="contained" color="primary" className='TeamFilter' >Simulation
        </Button>
        <Button mt={2} variant="contained" color="primary" className='TeamFilter' >Machine Learning
        </Button>

        <Button mt={2} variant="contained" color="primary" className='TeamFilter' >Information Support
        </Button>
       
      </div>

      <div className = 'TeamAbout'>
        <h3> Team Responsibility Descriptions... </h3>
      </div>




      <div className = 'CardGreenBackground1'>
        <h3 align="left">Team Leaders</h3>
        <LeadGridList></LeadGridList>
      </div>

      <div className = 'CardGreenBackground1' >
        <h3 align="left">Team Members</h3>
        <TeamGridList></TeamGridList>
      </div>

   </div>


 );
}


// function LeaderList(props){

//   const leaderCards = props.list.map(leader => {
//     return(
//       <TeamLeaderCardLeft key={leader.name} name={leader.name} description = {leader.major} />
//     );
//     }
//   );
//   return(<div>{leaderCards}</div>);
// }

// function MemberList(props){

//   const memberCards = props.list.map(member => {
//     return(
//       <MemberCardLeft key={member.name} name={member.name} description = {member.major} />
//     );
//     }
//   );
//   return(<div>{memberCards}</div>);
// }

// function SupervisorList(props) {
//   const supervisorCards = props.list.map(supervisor =>
//     <SupervisorCard key={supervisor.name} name={supervisor.name} description={supervisor.profession} image={supervisor.image}/>
//   );
//   return <div>{supervisorCards}</div>;
// }

// function TeamLeaderCardLeft(props){
//   return(
//     <div align= "left" className="LeaderCard">
//         <div className="Inner">
//           <h4 className="LeaderName">{props.name}</h4>
//           <h5 className="ProfessionText"> {props.description} </h5>
//         </div>
//     </div>

//   );

// }

// function MemberCardLeft(props){
//   return(
//     <div align= "left" className="LeaderCard">
//         <div className="Inner">
//           <h4 className="LeaderName">{props.name}</h4>
//           <h5 className="ProfessionText"> {props.description} </h5>
//         </div>
//     </div>

//   );

// }

// function SupervisorCard(props){
//   return(
//     <div align= "left" className="SuperCard">
//         <div className="Inner">
//           <h4 className="LeaderName">{props.name}</h4>
//           <h5 className="ProfessionText">{props.description}</h5>
//         </div>
//     </div>
//   );
// }



export default Team;
