import { Box, Container, IconButton, TextField, Typography } from '@mui/material';
import Check from '@mui/icons-material/Check';
import React, { useState } from 'react';
import { addPlan } from '../api/actions';
import { getConfig } from "../api/actions";


function Config() {
  const [config, setConfig] = useState({});

  React.useEffect(() => {
    const fetchPlans = async () => {
      const allPlans = await getConfig();
      setConfig(allPlans.payload);
    };

    fetchPlans();
  }, []);

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" sx={{ mb: 2 }}>
          Config
        </Typography>
      </Box>
      <Box
        component="form"
        sx={{
          '& .MuiTextField-root': { m: 1, width: '25ch' },
        }}
        noValidate
        autoComplete="off"
      >
        <div>
          
        </div>
      </Box>
    </Container>
    
  );
}

export default Config;