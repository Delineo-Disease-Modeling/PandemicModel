import React, {Component} from 'react';
import {Button, Label, Col, Row} from 'reactstrap';
import {Header} from '../components'
import {Control, LocalForm, Errors} from 'react-redux-form';

const required = (val) => val && val.length;
const maxLength = (len) => (val) => !(val) || (val.length <= len);
const minLength = (len) => (val) => (val) && (val.length >= len);
const isNumber = (val) => !isNaN(Number(val));
const validEmail = (val) => /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(val);

class Contact extends Component {

    constructor(props){
        super(props);

        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(values){
        console.log("Current State is: "+JSON.stringify(values));
        alert("Current State is: "+JSON.stringify(values));
    }

    render() {
        let nameValidators = { required,minLength: minLength(3), maxLength: maxLength(15) };
        let nameMessages = {
                            required: 'Required',
                            minLength: ' Must be greater than 2 characters',
                            maxLength: ' Must be 15 characters or less'
                        };
        let phoneValidators = {required, minLength: minLength(3), maxLength: maxLength(15), isNumber};
        let phoneMessages = {
                                required: 'Required',
                                minLength: ' Must be greater than 2 numbers',
                                maxLength: ' Must be 15 numbers or less',
                                isNumber: ' Must be a number'
                            };

        return(
            <div className="container">
                <Header text='Contact Us'/>
                <div className="row row-content" style={{border: '1px solid #ffffff', marginBottom:'5%', marginTop:'2%',boxShadow: '5px 10px 20px grey'  }}>
                    <Title text='Send Us Your Feedback'/>
                    <div className="col-12 col-md-9" style={{marginLeft:'auto', marginRight:'auto'}}>
                        <LocalForm onSubmit={(values)=>this.handleSubmit(values)}>
                            <TextInput model='.firstname' id='firstname' placeholder="First Name"
                                validators={nameValidators}
                                messages={nameMessages}
                            />

                            <TextInput model='.lastname' id='lastname' placeholder="Last Name"
                                validators={nameValidators}
                                messages={nameMessages}
                            />

                            <TextInput model='.telnum' id='telnum' placeholder="Tel. Number"
                                validators={phoneValidators}
                                messages={phoneMessages}
                            />

                            <TextInput model='.email' id='email' placeholder="Email"
                                validators={{required, validEmail}}
                                messages={{required: 'Required',validEmail: ' Invalid Email Address'}}
                            />

                            <ContactAgreement text="May we contact you?" options={["Tel.", "Email"]}/>

                            <Control.textarea model=".message" id="message" name="message"
                                                placeholder="Your Feedback"
                                                rows="12"
                                                className="form-control" />

                            <Button type="submit" color="primary">Send Feedback</Button>
                        </LocalForm>
                    </div>
                </div>
            </div>
        );
    }
}

function Title(props) {
    return <div className="col-12" > <h3>{props.text}</h3> </div>;
}

function TextInput(props) {
    return <Row className="form-group">
        <Col md={12}>
            <Control.text model={props.model} id={props.id} name={props.id}
                placeholder={props.placeholder}
                className="form-control"
                validators={props.validators}
            />
            <Errors className="text-danger" model={props.model} show="touched" 
                    messages={props.messages}
            />
        </Col>
    </Row>;
}

function ContactAgreement(props) {
    return <Row className="form-group">
        <Col md={{size: 6, offset: 0}}>
            <div className="form-check">
                <Label check>
                    <Control.checkbox model=".agree" name="agree"
                        className="form-check-input"
                         /> {' '}
                        <strong>{props.text}</strong>
                </Label>
            </div>
        </Col>

        <Col md={{size: 4, offset: 2}}>
            <Control.select model=".contactType" name="contactType"
                className="form-control">
                <option>{props.options[0]}</option>
                <option>{props.options[1]}</option>
            </Control.select>
        </Col>
    </Row>
}

export default Contact;