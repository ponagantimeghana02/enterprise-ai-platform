import {
    Card,
    CardContent,
    Typography
} from "@mui/material";

import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip
} from "recharts";

const data = [
    { day: "Mon", requests: 120 },
    { day: "Tue", requests: 145 },
    { day: "Wed", requests: 180 },
    { day: "Thu", requests: 210 },
    { day: "Fri", requests: 265 },
    { day: "Sat", requests: 170 },
    { day: "Sun", requests: 195 },
];

const DailyRequestsChart = () => (
    <Card>
        <CardContent>

            <Typography variant="h6" mb={2}>
                Daily Requests
            </Typography>

            <ResponsiveContainer
                width="100%"
                height={300}
            >
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3"/>

                    <XAxis dataKey="day"/>

                    <YAxis/>

                    <Tooltip/>

                    <Line
                        type="monotone"
                        dataKey="requests"
                    />
                </LineChart>
            </ResponsiveContainer>

        </CardContent>
    </Card>
);

export default DailyRequestsChart;