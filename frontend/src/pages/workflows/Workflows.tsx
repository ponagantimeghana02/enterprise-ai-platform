import { useEffect, useState } from "react";

import {
  Box,
  Button,
  Card,
  CardContent,
  Grid,
  Typography,
} from "@mui/material";

import { Workflow } from "../../types/workflow";
import { workflowService } from "../../services/workflowService";

const Workflows = () => {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);

  useEffect(() => {
    loadWorkflows();
  }, []);

  async function loadWorkflows() {
    const response =
      await workflowService.getWorkflows();

    setWorkflows(response.data);
  }

  async function retry(id: string) {
    await workflowService.retryWorkflow(id);
    loadWorkflows();
  }

  return (
    <Box p={4}>
      <Typography variant="h4" mb={3}>
        Workflow Management
      </Typography>

      <Grid container spacing={3}>
        {workflows.map((workflow) => (
          <Grid item xs={12} md={6} key={workflow.id}>
            <Card>
              <CardContent>

                <Typography variant="h6">
                  {workflow.name}
                </Typography>

                <Typography>
                  Status: {workflow.status}
                </Typography>

                <Typography sx={{ mt: 2 }}>
                  <strong>Timeline</strong>
                </Typography>

                <Typography>
                  {workflow.timeline}
                </Typography>

                <Typography sx={{ mt: 2 }}>
                  <strong>Logs</strong>
                </Typography>

                <Typography>
                  {workflow.logs}
                </Typography>

                <Button
                  sx={{ mt: 2 }}
                  variant="contained"
                  onClick={() => retry(workflow.id)}
                >
                  Retry Workflow
                </Button>

              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Workflows;