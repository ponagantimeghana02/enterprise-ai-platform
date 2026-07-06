import {
Card,
CardContent,
Typography
} from "@mui/material";

import {
PieChart,
Pie,
Cell,
Tooltip,
ResponsiveContainer,
Legend
} from "recharts";

const data=[
{ name:"Correct", value:84 },
{ name:"Partial", value:11 },
{ name:"Failed", value:5 },
];

const COLORS=[
"#4caf50",
"#ff9800",
"#f44336"
];

export default function RetrievalPerformanceChart(){

return(

<Card>

<CardContent>

<Typography variant="h6">
Retrieval Performance
</Typography>

<ResponsiveContainer
width="100%"
height={300}
>

<PieChart>

<Pie
data={data}
dataKey="value"
label
>

{data.map((entry,index)=>(

<Cell
key={index}
fill={COLORS[index]}
/>

))}

</Pie>

<Legend/>

<Tooltip/>

</PieChart>

</ResponsiveContainer>

</CardContent>

</Card>

)

}