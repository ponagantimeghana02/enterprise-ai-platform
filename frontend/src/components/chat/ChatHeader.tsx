import {
  AppBar,
  Toolbar,
  Typography,
} from "@mui/material";

const ChatHeader = () => {
  return (
    <AppBar
      position="static"
      color="transparent"
      elevation={1}
    >
      <Toolbar>

        <Typography
          variant="h6"
          fontWeight="bold"
        >
          Enterprise AI Chat
        </Typography>

      </Toolbar>
    </AppBar>
  );
};

export default ChatHeader;