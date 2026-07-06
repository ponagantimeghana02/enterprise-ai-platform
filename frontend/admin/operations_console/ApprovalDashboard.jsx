import StatCard from "../components/StatCard";

export default function ApprovalDashboard() {

    return (

        <>
            <h1>Approval Dashboard</h1>

            <div style={{ display: "flex", gap: 20 }}>

                <StatCard
                    title="Pending Approvals"
                    value="6"
                />

                <StatCard
                    title="Completed Approvals"
                    value="91"
                />

                <StatCard
                    title="Escalations"
                    value="1"
                />

            </div>

        </>

    );

}