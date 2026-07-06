import {
Card,
CardContent,
Typography
} from "@mui/material";

import {
BarChart,
Bar,
XAxis,
YAxis,
Tooltip,
CartesianGrid,
ResponsiveContainer
} from "recharts";

const data=[
{month:"Jan",cost:420},
{month:"Feb",cost:520},
{month:"Mar",cost:690},
{month:"Apr",cost:740},
{month:"May",cost:830},
{month:"Jun",cost:960},
];

export default function CostAnalyticsChart(){

return(

<Card>

<CardContent>

<Typography variant="h6">
Cost Analytics
</Typography>

<ResponsiveContainer
width="100%"
height={300}
>

<BarChart data={data}>

<CartesianGrid strokeDasharray="3 3"/>

<XAxis dataKey="month"/>

<YAxis/>

<Tooltip/>

<Bar dataKey="cost"/>

</BarChart>

</ResponsiveContainer>

</CardContent>

</Card>

)

}