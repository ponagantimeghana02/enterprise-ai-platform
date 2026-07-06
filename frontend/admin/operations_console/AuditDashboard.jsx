import StatCard from "../components/StatCard";

export default function AuditDashboard() {

    return (

        <>
            <h1>Audit Dashboard</h1>

            <div style={{ display: "flex", gap: 20 }}>

                <StatCard
                    title="User Actions"
                    value="1250"
                />

                <StatCard
                    title="Tool Calls"
                    value="4870"
                />

                <StatCard
                    title="Security Events"
                    value="8"
                />

            </div>

        </>

    );

}