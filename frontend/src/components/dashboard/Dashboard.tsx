import { useEffect, useState } from "react";

import { Box } from "@mui/material";

import DashboardHeader from "../../components/dashboard/DashboardHeader";
import DashboardToolbar from "../../components/dashboard/DashboardToolbar";
import DashboardCharts from "../../components/dashboard/DashboardCharts";
import StatsGrid from "../../components/dashboard/StatsGrid";
import LoadingSkeleton from "../../components/dashboard/LoadingSkeleton";
import ErrorState from "../../components/dashboard/ErrorState";

import { dashboardService } from "../../services/dashboardService";

export default function Dashboard() {

  const [stats, setStats] = useState<any>(null);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState(false);

  const [filter, setFilter] =
    useState("today");

  const [lastUpdated, setLastUpdated] =
    useState("");

  useEffect(() => {

    loadDashboard();

    const timer = setInterval(() => {
      loadDashboard();
    }, 30000);

    return () => clearInterval(timer);

  }, [filter]);

  async function loadDashboard() {

    try {

      setLoading(true);

      setError(false);

      const data =
        await dashboardService.getDashboard(
          filter
        );

      setStats(data.stats);

      setLastUpdated(
        new Date().toLocaleTimeString()
      );

    } catch {

      setError(true);

    } finally {

      setLoading(false);

    }

  }

  return (

    <Box p={4}>

      <DashboardHeader />

      <DashboardToolbar
        filter={filter}
        loading={loading}
        lastUpdated={lastUpdated}
        onRefresh={loadDashboard}
        onFilterChange={setFilter}
      />

      {loading && <LoadingSkeleton />}

      {!loading && error && (
        <ErrorState retry={loadDashboard}/>
      )}

      {!loading && !error && stats && (
        <>
          <StatsGrid stats={stats}/>
          <DashboardCharts/>
        </>
      )}

    </Box>

  );

}