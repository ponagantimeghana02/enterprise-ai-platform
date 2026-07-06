import { useEffect, useState } from "react";

import {
  Box,
  Button,
  Card,
  CardContent,
  Grid,
  Typography,
} from "@mui/material";

import { Agent } from "../../types/agent";
import { agentService } from "../../services/agentService";

const Agents = () => {
  const [agents, setAgents] = useState<Agent[]>([]);

  useEffect(() => {
    loadAgents();
  }, []);

  async function loadAgents() {
    const response = await agentService.getAgents();
    setAgents(response.data);
  }

  async function start(id: string) {
    await agentService.startAgent(id);
    loadAgents();
  }

  async function stop(id: string) {
    await agentService.stopAgent(id);
    loadAgents();
  }

  async function restart(id: string) {
    await agentService.restartAgent(id);
    loadAgents();
  }

  return (
    <Box p={4}>
      <Typography variant="h4" mb={3}>
        AI Agent Dashboard
      </Typography>

      <Grid container spacing={3}>
        {agents.map((agent) => (
          <Grid item xs={12} md={6} key={agent.id}>
            <Card>
              <CardContent>

                <Typography variant="h6">
                  {agent.name}
                </Typography>

                <Typography>
                  Status: {agent.status}
                </Typography>

                <Typography>
                  Health: {agent.health}
                </Typography>

                <Typography>
                  Running Tasks: {agent.runningTasks}
                </Typography>

                <Typography>
                  Tool Usage: {agent.toolUsage}%
                </Typography>

                <Typography mt={2}>
                  <strong>Agent Logs</strong>
                </Typography>

                <Typography>
                  {agent.logs}
                </Typography>

                <Typography mt={2}>
                  <strong>Agent Memory</strong>
                </Typography>

                <Typography>
                  {agent.memory}
                </Typography>

                <Box mt={2}>
                  <Button
                    variant="contained"
                    onClick={() => start(agent.id)}
                  >
                    Start
                  </Button>

                  <Button
                    sx={{ mx: 1 }}
                    color="warning"
                    variant="contained"
                    onClick={() => stop(agent.id)}
                  >
                    Stop
                  </Button>

                  <Button
                    color="secondary"
                    variant="contained"
                    onClick={() => restart(agent.id)}
                  >
                    Restart
                  </Button>

                </Box>

              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Agents;