import { createMuiTheme } from '@material-ui/core/styles';

export const theme = createMuiTheme({
  palette: {
    primary: {
      main: '#718486',
    },
    background: {
      default: '#22242A',
      paper: '#1E2325',
    },
    secondary: {
      main: '#11cb5f',
    },
  },

  button: {
    primary: {
      main: ''
    },
  
  },

  typography: {
    primary: {
      main: 'Calibri',
    }
  }
});


// '#212628'
// '#E4E5E6'
// '#1E2325'
// '#93BDC1'
// '#444F51'
// '#718486'
export default theme;
