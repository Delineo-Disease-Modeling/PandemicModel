import React from 'react';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import ButtonGroup from '@material-ui/core/ButtonGroup';
 
 
function BlogPost (props) {
   return (

       <Container>
           <Typography variant="h1">Blog Title</Typography>
         
           <Container className="image-background">
               <Typography variant="h6" style={{ backgroundColor: '#cfe8fc', height: '50vh' }}>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum</Typography>
              

           </Container>
           
       <ButtonGroup color="primary" aria-label="outlined primary button group">
         <Button>Previous Post</Button>
         <Button>Next Post</Button>
       </ButtonGroup>
       </Container>
       
   );
}
 
export default BlogPost;