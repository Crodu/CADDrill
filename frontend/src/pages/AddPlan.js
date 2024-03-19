import { Box, Container, IconButton, TextField, Typography } from '@mui/material';
import Check from '@mui/icons-material/Check';
import React, { useState } from 'react';
import { addPlan } from '../api/actions';


function AddPlan() {
  const [plan, setPlan] = useState({ name: '', description: '' });

  const handleChange = (e) => {
    setPlan({ ...plan, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e) => {
    setPlan({ ...plan, file: e.target.files[0] });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    addPlan({ name: plan.name, hole_diameter: plan.holeWidth }, plan.file);
    console.log(plan);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" sx={{ mb: 2 }}>
          Add New Plan
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
          <TextField
            required
            label="Name"
            value={plan.name}
            name="name"
            onChange={handleChange}
          />
          <TextField
            label="Hole Width"
            value={plan.holeWidth}
            name="holeWidth"
            onChange={handleChange}
          />
          <TextField
            type="file"
            id="outlined-file"
            label="File"
            name="file"
            InputLabelProps={{
              shrink: true,
            }}
            onChange={handleFileChange}
          />
          <IconButton 
            color="primary"
            onClick={handleSubmit}
            sx={{ m: 1 }}
            size='large'
          >
            <Check />
          </IconButton>
        </div>
      </Box>
    </Container>
    
  );
}

export default AddPlan;