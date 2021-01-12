import React from "react";
import './About.css'
import { Dimensions } from "react";
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles({
	thumbnail_img: {
		width: 250,
		height: 150,
		
		//width: 250px, /* ie8 */
		//max-width: 50vw,
		//max-height: 50vw,
	},
	button: {
		background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
		border: 0,
		borderRadius: 3,
		boxShadow: '0 3px 5px 2px rgba(255, 105, 135, .3)',
		color: 'white',
		height: 48,
		padding: '0 30px',
	  },
  });

  

class About extends React.Component {
	constructor () {
  		super();
  		this.MapDescription = "The Johns Hopkins Coronavirus Resource Center (CRC) is a continuously updated source of COVID-19 data and expert guidance. We aggregate and analyze the best data available on COVID-19—including cases, as well as testing, contact tracing and vaccine efforts—to help the public, policymakers and healthcare professionals worldwide respond to the pandemic.";
  		this.SimulationDescription = "Viruses, such as the one that causes COVID-19, spread quickly through large cities because of a complex web of interactions between people taking place in a densely populated area. But how viruses move from person to person in smaller, rural communities is less well understood, resulting in public health and economic decisions that are made on the basis of scant information and overgeneralized modeling. The Delineo project is developing a distributed programming environment to run the model over large numbers of computers to scale up the areas that can be accurately modeled.";
	 }
	 //classes = useStyles();
	 
	render() {
		return (
			
				<div className='CardBackground'>
				    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css"/>
			            <div className='CardGreenBackground'>
					<img className="w3-image" src="https://api.hub.jhu.edu/factory/sites/default/files/styles/landscape/public/Undergrad_teaching_laboratories_011917_900x600.jpg?itok=P83h8p2q" alt="Architecture" width="1500" height="800"/>
					
					
					<div className="w3-display-middle w3-margin-top w3-center">
					    <h1 className="w3-xxlarge w3-text-white"><span className="w3-padding w3-black w3-opacity-min"><b>De</b></span> <span className="w3-hide-small w3-text-light-grey">lineo</span></h1>
					</div>
				
					<div className="w3-container w3-padding-32" id="projects">
					    <h3 className="w3-border-bottom w3-border-light-grey w3-padding-16">Map Visualization</h3>
					    <p>{this.MapDescription}</p>
					</div>
					<div className="w3-row-padding">
					    <div className="w3-col l3 m6 w3-margin-bottom">
						<div className="w3-display-container">
						    <div className="w3-display-topleft w3-black w3-padding">County Level</div>
							<div class="thumbnail">
						    	<img className="w3-image" src="https://www.esri.com/arcgis-blog/wp-content/uploads/2020/03/USCounties_Coronavirus_Cases20200329.png" alt="Architecture" width="325" height="182" style={{'alignSelf':'stretch'}}/>
							</div>
						</div>
					    </div>
					    <div className="w3-col l3 m6 w3-margin-bottom">
						<div className="w3-display-container">
						    <div className="w3-display-topleft w3-black w3-padding">State Level</div>
							<div class="thumbnail">
						    <img className="w3-image" src="https://cdn.blog.ucsusa.org/wp-content/uploads/percent_confirmed.jpg" alt="Architecture" width="325" height="182" style={{'alignSelf':'stretch'}}/>
							</div>
						</div>
					    </div>
					    <div className="w3-col l3 m6 w3-margin-bottom">
						<div className="w3-display-container">
						    <div className="w3-display-topleft w3-black w3-padding">Motion Chart</div>
							<div class="thumbnail">
							<img className="w3-image" src="https://docs.dhis2.org/2.29/en/developer/html/resources/images/content/developer/r/google_vis_col_chart.PNG" alt="Architecture"  width="325" height="182" style={{'alignSelf':'stretch'}}/>
							</div>
						</div>
					    </div>
					    <div className="w3-col l3 m6 w3-margin-bottom">
						<div className="w3-display-container">
						    <div className="w3-display-topleft w3-black w3-padding">Daily Summary</div>
							<div class="thumbnail">
							<img className="w3-image" src="https://i.ytimg.com/vi/PeoKrURIVY4/maxresdefault.jpg" alt="Architecture" width="325" height="182" style={{'alignSelf':'stretch'}}/>
							</div>
						</div>
					    </div>
					</div>






					<div className="w3-container w3-padding-32" id="projects">
					    <h3 className="w3-border-bottom w3-border-light-grey w3-padding-16">Simulation</h3>
					    <p>{this.SimulationDescription}</p>
					</div>
					<div className="w3-row-padding">
					    <div className="w3-col l3 m6 w3-margin-bottom">
						<div className="w3-display-container">
						    <div className="w3-display-topleft w3-black w3-padding">Simulation 1</div>
							<div class="thumbnail">
						    <img className="w3-image" src="https://www.washingtonpost.com/rf/image_982w/2010-2019/WashingtonPost/2020/03/14/Health-Environment-Science/Graphics/promo2-coronavirus-simulator-0313.jpg" alt="House" width="325" height="182" style={{'alignSelf':'stretch'}}/>
							</div>
						</div>
					    </div>
					    <div className="w3-col l3 m6 w3-margin-bottom">
						<div className="w3-display-container">
						    <div className="w3-display-topleft w3-black w3-padding">Simulation 2</div>
							<div class="thumbnail">
						    <img className="w3-image" src="https://images.firstpost.com/fpimages/1200x800/fixed/jpg/2020/06/Covid-19-coronavirus-sneeze-simulation_Dassualt-Systemes-1.jpg" alt="House" width="325" height="182" style={{'alignSelf':'stretch'}}/>
							</div>
						</div>
					    </div>
					    <div className="w3-col l3 m6 w3-margin-bottom">
						<div className="w3-display-container">
						    <div className="w3-display-topleft w3-black w3-padding">Simulation 3</div>
							<div class="thumbnail">
							<img className="w3-image" src="https://images.theconversation.com/files/342926/original/file-20200619-70415-35zyha.jpg?ixlib=rb-1.1.0&rect=2057%2C0%2C5656%2C2822&q=45&auto=format&w=1356&h=668&fit=crop" alt="House"  width="325" height="500" style={{'alignSelf':'stretch'}}/>
							</div>
						</div>
					    </div>
					    <div className="w3-col l3 m6 w3-margin-bottom">
						<div className="w3-display-container">
						    <div className="w3-display-topleft w3-black w3-padding">Simulation 4</div>
							<div class="thumbnail">
							<img className="w3-image" src="https://blogs.solidworks.com/solidworksblog/wp-content/uploads/sites/2/2020/04/reza_cfd_1.png" alt="House" width="325" height="182" style={{'alignSelf':'stretch'}}/>
							</div>
						</div>
					    </div>
					</div>





				    <div className="w3-container w3-padding-32" id="contact">
					<h3 className="w3-border-bottom w3-border-light-grey w3-padding-16">Contact</h3>
					<p>Let's get in touch!</p>
					<form>
					    <input className="w3-input w3-border" type="text" placeholder="Name" required name="Name"/>
					    <input className="w3-input w3-section w3-border" type="text" placeholder="Email" required name="Email"/>
					    <input className="w3-input w3-section w3-border" type="text" placeholder="Subject" required name="Subject"/>
					    <input className="w3-input w3-section w3-border" type="text" placeholder="Comment" required name="Comment"/>
					    <button className="w3-button w3-black w3-section" type="submit">
					    <i className="fa fa-paper-plane"></i> SEND MESSAGE
					    </button>
					</form>
				    </div>
				</div>
			</div>
			);
	}
}
export default About;
