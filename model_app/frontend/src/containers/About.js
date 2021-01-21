import React from "react";
import { Dimensions } from "react";
import Accordion from '@material-ui/core/Accordion';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import { withStyles, makeStyles } from '@material-ui/core/styles';
import MuiAccordion from '@material-ui/core/Accordion';
import MuiAccordionSummary from '@material-ui/core/AccordionSummary';
import MuiAccordionDetails from '@material-ui/core/AccordionDetails';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';

const styles = {
	button: {
		borderColor: '#66FCF1',
		backgroundColor: '#66FCF1',
		border: '1px solid',
		"&:hover": {
			backgroundColor: 'transparent',
			color: '#66FCF1',
			borderColor: '#66FCF1',
		},
	},

	w3Image: {
		maxWidth: '22vw',
		height: '180px',
	},

	w3DisplayContainer: {
		width: '100%',
		display: 'flex',
		paddingBottom: '50px',
		flexDirection: 'row',
		justifyContent: 'center',
		alignItems: 'center',
		flexWrap: 'wrap'
	},

	buttonContainer: {
		width: '100%',
		alignContent: 'center',
		paddingTop: '0%',
		paddingBottom: '5%',
	},

	cardBackground: {
		backgroundColor: '#222629',
		height: '100%',
		width: '100vh',
		minHeight: '100%',
		minWidth: '100%',
		margin: '0',
		alignContent: 'center',
		paddingBottom: '5%',
	},

	cardGreenBackground: {
		marginTop: '0%',
		marginLeft: 'auto',
		marginRight: 'auto',
		backgroundColor: '#1b4441c2',
		width: '100%',
		alignSelf: 'center',
		alignItems: 'center',
	},

	paragraph: {
		color: 'white',
		paddingLeft: '5%',
		paddingRight: '5%',
	},

	thumbnail: {
		width: '22vw'
	}
}

const ColoredAccordion = withStyles({
	root: {
		backgroundColor: '#1b4441c2',
		fontSize: '20px',
		color: '#66FCF1'



	},
})(Accordion);

const AccordionDetails = withStyles((theme) => ({
	root: {
		padding: theme.spacing(2),
	},
}))(MuiAccordionDetails);

const ColAccordion = withStyles({
	root: {
		backgroundColor: '#444F51',
		fontSize: '20px',
		color: 'white',
		border: '0px solid rgba(0, 0, 0, .125)',
		boxShadow: 'none',
		'&:not(:last-child)': {
			borderBottom: 0,
		},
		'&:before': {
			display: 'none',
		},
		'&$expanded': {
			margin: 'auto',
		},
	},
	expanded: {},
})(MuiAccordion);

const ColAccordionSummary = withStyles({
	root: {
		backgroundColor: 'rgba(0, 0, 0, .4)',
		borderBottom: '0px solid rgba(0, 0, 0, .125)',
		marginBottom: 0,
		minHeight: 56,
		'&$expanded': {
			minHeight: 56,
		},
	},
	content: {
		'&$expanded': {
			margin: '12px 0',
		},
	},
	expanded: {},
})(MuiAccordionSummary);

class About extends React.Component {
	constructor() {
		super();
		this.MapDescription = "The Johns Hopkins Coronavirus Resource Center (CRC) is a continuously updated source of COVID-19 data and expert guidance. We aggregate and analyze the best data available on COVID-19—including cases, as well as testing, contact tracing and vaccine efforts—to help the public, policymakers and healthcare professionals worldwide respond to the pandemic.";
		this.SimulationDescription = "Viruses, such as the one that causes COVID-19, spread quickly through large cities because of a complex web of interactions between people taking place in a densely populated area. But how viruses move from person to person in smaller, rural communities is less well understood, resulting in public health and economic decisions that are made on the basis of scant information and overgeneralized modeling. The Delineo project is developing a distributed programming environment to run the model over large numbers of computers to scale up the areas that can be accurately modeled.";
	}

	render() {
		const { classes } = this.props;
		return (
			<div className={classes.cardBackground}>
				<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css" />
				<div className={classes.cardGreenBackground}>
					<img src="https://api.hub.jhu.edu/factory/sites/default/files/styles/landscape/public/Undergrad_teaching_laboratories_011917_900x600.jpg?itok=P83h8p2q" alt="Architecture" width="100%" height="800vh" />


					<div className="w3-display-middle w3-margin-top w3-center w3">
						<h1 className="w3-xxlarge w3-text-white"><span className="w3-padding w3-black w3-opacity-min"><b>De</b></span> <span className="w3-hide-small w3-text-light-grey">lineo</span></h1>
					</div>

					<div className="w3-container w3-padding-32 w3-grey" id="projects">
						<h3 className="w3-border-bottom w3-border-light-grey w3-padding-16">Map Visualization</h3>
						<p className={classes.paragraph}>{this.MapDescription}</p>
					</div>
					<div className="w3-row-padding w3-grey" style={{ padding: '0 50px 20px 50px' }}>
						<div className={classes.w3DisplayContainer} >
							<div className="w3-col l3 m6">
								<div>
									<div className={classes.thumbnail}>
										<div className="w3-black w3-padding">County Level</div>
										<img className={classes.w3Image} src="https://www.esri.com/arcgis-blog/wp-content/uploads/2020/03/USCounties_Coronavirus_Cases20200329.png" alt="Architecture" width="325" height="182" style={{ 'alignSelf': 'stretch' }} />
									</div>
								</div>
							</div>
							<div className="w3-col l3 m6">
								<div >
									<div className={classes.thumbnail}>
										<div className="w3-black w3-padding">State Level</div>
										<img className={classes.w3Image} src="https://cdn.blog.ucsusa.org/wp-content/uploads/percent_confirmed.jpg" alt="Architecture" width="325" height="182" style={{ 'alignSelf': 'stretch' }} />

									</div>
								</div>
							</div>
							<div className="w3-col l3 m6">
								<div >
									<div className={classes.thumbnail}>
										<div className="w3-black w3-padding">Motion Chart</div>
										<img className={classes.w3Image} src="https://docs.dhis2.org/2.29/en/developer/html/resources/images/content/developer/r/google_vis_col_chart.PNG" alt="Architecture" width="325" height="182" style={{ 'alignSelf': 'stretch' }} />
									</div>
								</div>
							</div>
							<div className="w3-col l3 m6 ">
								<div>
									<div className={classes.thumbnail}>
										<div className="w3-black w3-padding">Daily Summary</div>
										<img className={classes.w3Image} src="https://i.ytimg.com/vi/PeoKrURIVY4/maxresdefault.jpg" alt="Architecture" width="325" height="182" style={{ 'alignSelf': 'stretch' }} />
									</div>
								</div>
							</div>
						</div>
						<div className={classes.buttonContainer}>
							<Button className={classes.button} variant="contained" color="inherit" href="#top">
								View Map
              				</Button>
						</div>
					</div>


					<div className="w3-container w3-padding-32 w3-" id="projects">
						<h3 className="w3-border-bottom w3-border-light-grey w3-padding-16">Simulation</h3>
						<p className={classes.paragraph}>{this.SimulationDescription}</p>
					</div>
					<div className="w3-row-padding" style={{ padding: '0 50px 20px 50px' }}>
						<div className={classes.w3DisplayContainer} >
							<div className="w3-col l3 m6 w3-margin-bottom">
								<div>
									<div className={classes.thumbnail}>
										<div className="w3-black w3-padding">Simulation 1</div>
										<img className={classes.w3Image} src="https://www.washingtonpost.com/rf/image_982w/2010-2019/WashingtonPost/2020/03/14/Health-Environment-Science/Graphics/promo2-coronavirus-simulator-0313.jpg" alt="House" width="325" height="182" style={{ 'alignSelf': 'stretch' }} />
									</div>
								</div>
							</div>
							<div className="w3-col l3 m6 w3-margin-bottom">
								<div>
									<div className={classes.thumbnail}>
										<div className="w3-black w3-padding">Simulation 2</div>
										<img className={classes.w3Image} src="https://images.firstpost.com/fpimages/1200x800/fixed/jpg/2020/06/Covid-19-coronavirus-sneeze-simulation_Dassualt-Systemes-1.jpg" alt="House" width="325" height="182" style={{ 'alignSelf': 'stretch' }} />
									</div>
								</div>
							</div>
							<div className="w3-col l3 m6 w3-margin-bottom">
								<div>
									<div className={classes.thumbnail}>
										<div className="w3-black w3-padding">Simulation 3</div>
										<img className={classes.w3Image} src="https://images.theconversation.com/files/342926/original/file-20200619-70415-35zyha.jpg?ixlib=rb-1.1.0&rect=2057%2C0%2C5656%2C2822&q=45&auto=format&w=1356&h=668&fit=crop" alt="House" width="325" height="500" style={{ 'alignSelf': 'stretch' }} />
									</div>
								</div>
							</div>
							<div className="w3-col l3 m6 w3-margin-bottom">
								<div>
									<div className={classes.thumbnail}>
										<div className="w3-black w3-padding">Simulation 4</div>
										<img className={classes.w3Image} src="https://blogs.solidworks.com/solidworksblog/wp-content/uploads/sites/2/2020/04/reza_cfd_1.png" alt="House" width="325" height="182" style={{ 'alignSelf': 'stretch' }} />
									</div>
								</div>
							</div>
						</div>

						<div className={classes.buttonContainer}>
							<Button className={classes.button} variant="contained" color="inherit" href="./simulator">
								View Simulation
              					</Button>
						</div>
					</div>
					<div className="w3-container w3-padding-32 w3-grey" id="contact" >
						<h3 className="w3-border-bottom w3-border-light-grey w3-padding-16">Frequently Asked Questions</h3>

						<div style={{ padding: '50px' }}>
							<ColAccordion>
								<ColAccordionSummary
									expandIcon={<ExpandMoreIcon />}
									aria-controls="Model Param-content"
									id="Model Param-header"
								>
									What is this simulator?
						</ColAccordionSummary>
								<AccordionDetails>
									<Typography>
										Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse malesuada lacus ex,
										sit amet blandit leo lobortis eget. Lorem ipsum dolor sit amet, consectetur adipiscing
										elit. Suspendisse malesuada lacus ex, sit amet blandit leo lobortis eget.
		          </Typography>
								</AccordionDetails>

							</ColAccordion>
							<br></br>
							<ColAccordion>
								<ColAccordionSummary
									expandIcon={<ExpandMoreIcon />}
									aria-controls="Model Param-content"
									id="Model Param-header"
								>
									What is this simulator?
						</ColAccordionSummary>
								<AccordionDetails>
									<Typography>
										Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse malesuada lacus ex,
										sit amet blandit leo lobortis eget. Lorem ipsum dolor sit amet, consectetur adipiscing
										elit. Suspendisse malesuada lacus ex, sit amet blandit leo lobortis eget.
		          				</Typography>
								</AccordionDetails>

							</ColAccordion>
						</div>
					</div>




					<div className="w3-container w3-padding-32" id="contact" >
						<h3 className="w3-border-bottom w3-border-light-grey w3-padding-16">Contact</h3>
						<p className={classes.paragraph}>Let's get in touch!</p>
						<form style={{ padding: '0 50px' }}>
							<input className="w3-input w3-border" type="text" placeholder="Name" required name="Name" />
							<input className="w3-input w3-section w3-border" type="text" placeholder="Email" required name="Email" />
							<input className="w3-input w3-section w3-border" type="text" placeholder="Subject" required name="Subject" />
							<input className="w3-input w3-section w3-border" type="text" placeholder="Comment" required name="Comment" />
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
export default withStyles(styles)(About);
