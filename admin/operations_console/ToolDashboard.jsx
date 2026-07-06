import StatCard from "../components/StatCard";

export default function ToolDashboard() {

    return (

        <>
            <h1>Tool Dashboard</h1>

            <div style={{ display: "flex", gap: 20 }}>

                <StatCard
                    title="Connected Tools"
                    value="11"
                />

                <StatCard
                    title="MCP Health"
                    value="Online"
                />

                <StatCard
                    title="API Latency"
                    value="122 ms"
                />

            </div>

        </>

    );

}