import { AppBar, Box, IconButton, ListItemButton, ListItemIcon, Toolbar, Typography } from "@mui/material";
import { Outlet, Link } from "react-router-dom";
import { useTheme, useMediaQuery, Drawer, List, ListItem, ListItemText } from "@mui/material";
import MenuIcon from '@mui/icons-material/Menu';
import React from "react";

const Layout = () => {
  const theme = useTheme();
  const drawerWidth = 240;
  const isDesktop = useMediaQuery(theme.breakpoints.up('sm'), { defaultMatches: true });

  const [mobileOpen, setMobileOpen] = React.useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const drawer = (
      <List>
        {['All Plans', 'Add Plan', 'Config'].map((text, index) => (
          <ListItem key={text}>
            <ListItemButton
              href={`/${index === 0 ? '' : text.toLowerCase().replace(' ', '')}`}
            >
              <ListItemIcon>
                <MenuIcon />
              </ListItemIcon>
              <ListItemText primary={text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
  );

  return (
    <>
      <AppBar 
      position="static"
      sx={{
        width: { sm: `calc(100% - ${drawerWidth}px)` },
        ml: { sm: `${drawerWidth}px` },
      }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" style={{ flexGrow: 1 }}>
            <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
              Home
            </Link>
          </Typography>
        </Toolbar>
      </AppBar>
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
        aria-label="mailbox folders"
      >
        <Drawer
          variant={isDesktop ? 'permanent' : 'temporary'}
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
          sx={{
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
      </Box>
      <Outlet />
    </>
  );
};

export default Layout