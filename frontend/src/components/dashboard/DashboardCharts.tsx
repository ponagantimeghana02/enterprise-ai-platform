import { Grid } from "@mui/material";

import DailyRequestsChart from "./DailyRequestsChart";
import AIUsageTrendChart from "./AIUsageTrendChart";
import CostAnalyticsChart from "./CostAnalyticsChart";
import RetrievalPerformanceChart from "./RetrievalPerformanceChart";

export default function DashboardCharts(){

return(

<Grid
container
spacing={3}
mt={2}
>

<Grid item xs={12} lg={6}>

<DailyRequestsChart/>

</Grid>

<Grid item xs={12} lg={6}>

<AIUsageTrendChart/>

</Grid>

<Grid item xs={12} lg={6}>

<CostAnalyticsChart/>

</Grid>

<Grid item xs={12} lg={6}>

<RetrievalPerformanceChart/>

</Grid>

</Grid>

)

}