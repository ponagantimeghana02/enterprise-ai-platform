import StatCard from "../components/StatCard";

export default function AgentDashboard() {

    return (

        <>
            <h1>Agent Dashboard</h1>

            <div style={{ display: "flex", gap: 20 }}>

                <StatCard
                    title="Running Agents"
                    value="14"
                />

                <StatCard
                    title="Agent Health"
                    value="Healthy"
                />

                <StatCard
                    title="Active Sessions"
                    value="48"
                />

            </div>

        </>

    );

}