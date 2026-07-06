import StatCard from "../components/StatCard";

export default function WorkflowDashboard() {

    return (

        <>
            <h1>Workflow Dashboard</h1>

            <div style={{ display: "flex", gap: 20 }}>

                <StatCard
                    title="Running Workflows"
                    value="9"
                />

                <StatCard
                    title="Failed Workflows"
                    value="2"
                />

                <StatCard
                    title="Retry Queue"
                    value="4"
                />

            </div>

        </>

    );

}