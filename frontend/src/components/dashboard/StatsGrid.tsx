import { Grid } from "@mui/material";
import StatsCard from "./StatsCard";
import { DashboardStats } from "../../types/dashboard";

interface Props {
  stats: DashboardStats;
}

const StatsGrid = ({ stats }: Props) => {
  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={3}>
        <StatsCard
          title="Active AI Sessions"
          value={stats.activeAISessions}
        />
      </Grid>

      <Grid item xs={12} md={3}>
        <StatsCard
          title="Active Users"
          value={stats.activeUsers}
          color="#43a047"
        />
      </Grid>

      <Grid item xs={12} md={3}>
        <StatsCard
          title="Running Agents"
          value={stats.runningAgents}
          color="#ef6c00"
        />
      </Grid>

      <Grid item xs={12} md={3}>
        <StatsCard
          title="Knowledge Base"
          value={`${stats.knowledgeBaseSize} Docs`}
          color="#8e24aa"
        />
      </Grid>

      <Grid item xs={12} md={3}>
        <StatsCard
          title="Today's Queries"
          value={stats.todayQueries}
        />
      </Grid>

      <Grid item xs={12} md={3}>
        <StatsCard
          title="Avg Response"
          value={`${stats.averageResponseTime} ms`}
          color="#e53935"
        />
      </Grid>

      <Grid item xs={12} md={3}>
        <StatsCard
          title="Token Usage"
          value={stats.tokenUsage.toLocaleString()}
          color="#00897b"
        />
      </Grid>

      <Grid item xs={12} md={3}>
        <StatsCard
          title="Workflow Status"
          value={stats.workflowStatus}
          color="#3949ab"
        />
      </Grid>
    </Grid>
  );
};

export default StatsGrid;