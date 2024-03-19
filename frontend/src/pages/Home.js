import { Box, Button, Container, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from "@mui/material";
import { List, ListItem, ListItemText } from "@mui/material";
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import { getAllPlans } from "../api/actions";
import React from "react";

const Home = () => {

  const [plans, setPlans] = React.useState([]);

  React.useEffect(() => {
    const fetchPlans = async () => {
      const allPlans = await getAllPlans();
      setPlans(allPlans.payload);
    };

    fetchPlans();
  }, []);

  const PlanList = () => {
    // Assuming you have an array of plans
    return (
      <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
        <TableRow>
          <TableCell align="left">Execute Plan</TableCell>
          <TableCell>Name</TableCell>
          <TableCell align="right">Diameter</TableCell>
          <TableCell align="right">Hole Coords</TableCell>
          <TableCell align="right">Size X</TableCell>
          <TableCell align="right">Size Y</TableCell>
        </TableRow>
        </TableHead>
        <TableBody>
        {plans.map((plan, index) => (
          <TableRow key={index}>
          <TableCell align="left">
            <Button variant="contained" color="primary">
              <PlayArrowIcon />
            </Button>
          </TableCell>
          <TableCell component="th" scope="row">
            {plan.name}
          </TableCell>
          <TableCell align="right">{plan.hole_diameter}</TableCell>
          <TableCell align="right">{plan.hole_coords}</TableCell>
          <TableCell align="right">{plan.size_x}</TableCell>
          <TableCell align="right">{plan.size_y}</TableCell>
          </TableRow>
        ))}
        </TableBody>
      </Table>
      </TableContainer>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" sx={{ mb: 2 }}>
          Driller Plan Manager
        </Typography>
      </Box>
      <PlanList />
    </Container>
  )
};

export default Home;