import {
Card,
CardContent,
Typography
} from "@mui/material";

import {
AreaChart,
Area,
ResponsiveContainer,
XAxis,
YAxis,
Tooltip,
CartesianGrid
} from "recharts";

const data = [
{ month:"Jan", usage:20 },
{ month:"Feb", usage:28 },
{ month:"Mar", usage:36 },
{ month:"Apr", usage:48 },
{ month:"May", usage:65 },
{ month:"Jun", usage:80 },
];

export default function AIUsageTrendChart(){

return(

<Card>

<CardContent>

<Typography variant="h6">
AI Usage Trends
</Typography>

<ResponsiveContainer
width="100%"
height={300}
>

<AreaChart data={data}>

<CartesianGrid strokeDasharray="3 3"/>

<XAxis dataKey="month"/>

<YAxis/>

<Tooltip/>

<Area
type="monotone"
dataKey="usage"
/>

</AreaChart>

</ResponsiveContainer>

</CardContent>

</Card>

)

}