import { Box, Container, IconButton, Typography } from '@mui/material';
import Check from '@mui/icons-material/Check';
import React, { useState } from 'react';
import { updateConfig } from '../api/actions';
import { getConfig } from "../api/actions";


function Config() {
  const [config, setConfig] = useState("Config...");

  React.useEffect(() => {
    const fetchPlans = async () => {
      const configs = await getConfig();
      setConfig(JSON.stringify(configs.payload, null, 2));
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
          <textarea
            value={config}
            onChange={(e) => setConfig(e.target.value)}
            style={{ width: '100%', height: '400px' }}
          />
        </div>
        <IconButton
          onClick={async () => {
            const res = await updateConfig(JSON.parse(config));
            console.log(res);
          }}
        >
          <Check />
        </IconButton>
      </Box>
    </Container>
    
  );
}

export default Config;