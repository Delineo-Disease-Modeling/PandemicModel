import React from 'react';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import ButtonGroup from '@material-ui/core/ButtonGroup';

function Example (props) {
    return (
        <Container>
            <Typography variant="h1">This is a header.</Typography>
            <Grid container>
                <Grid item xs>Something in grid</Grid>
                <Grid item xs>Another thing in grid</Grid>
                <Grid item xs>Last thing in grid</Grid>
            </Grid>
            <Container>
                <Typography variant="h6" style={{ backgroundColor: '#cfe8fc', height: '50vh' }}>This is a nested container.</Typography>
            </Container>
        <ButtonGroup color="primary" aria-label="outlined primary button group">
          <Button>One</Button>
          <Button>Two</Button>
          <Button>Three</Button>
        </ButtonGroup>
        </Container>
    );
}

export default Example;