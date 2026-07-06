import { useEffect, useState } from "react";

import {
  Box,
  Button,
  Card,
  CardContent,
  Grid,
  Typography,
} from "@mui/material";

import { Analytics as AnalyticsType } from "../../types/analytics";
import { analyticsService } from "../../services/analyticsService";

const Analytics = () => {
  const [data, setData] =
    useState<AnalyticsType>();

  useEffect(() => {
    loadAnalytics();
  }, []);

  async function loadAnalytics() {
    const response =
      await analyticsService.getAnalytics();

    setData(response.data);
  }

  async function exportCSV() {
    await analyticsService.exportCSV();
    alert("CSV Exported");
  }

  async function exportPDF() {
    await analyticsService.exportPDF();
    alert("PDF Exported");
  }

  if (!data) return <p>Loading...</p>;

  return (
    <Box p={4}>
      <Typography variant="h4" mb={3}>
        Analytics Dashboard
      </Typography>

      <Grid container spacing={3}>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography>
                AI Requests
              </Typography>
              <Typography variant="h5">
                {data.aiRequests}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography>
                Cost
              </Typography>
              <Typography variant="h5">
                ${data.cost}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography>
                Agent Performance
              </Typography>
              <Typography variant="h5">
                {data.agentPerformance}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography>
                RAG Accuracy
              </Typography>
              <Typography variant="h5">
                {data.ragAccuracy}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography>
                Hallucination Rate
              </Typography>
              <Typography variant="h5">
                {data.hallucinationRate}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography>
                Response Time
              </Typography>
              <Typography variant="h5">
                {data.responseTime} ms
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography>
                Top Knowledge Source
              </Typography>
              <Typography>
                {data.topKnowledgeSource}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography>
                User Satisfaction
              </Typography>
              <Typography variant="h5">
                {data.userSatisfaction}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

      </Grid>

      <Box mt={4}>
        <Button
          variant="contained"
          onClick={exportCSV}
        >
          Export CSV
        </Button>

        <Button
          sx={{ ml: 2 }}
          variant="contained"
          color="secondary"
          onClick={exportPDF}
        >
          Export PDF
        </Button>
      </Box>
    </Box>
  );
};

export default Analytics;