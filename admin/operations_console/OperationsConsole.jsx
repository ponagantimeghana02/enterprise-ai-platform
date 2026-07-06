import DashboardLayout from "./components/DashboardLayout";
import AgentDashboard from "./pages/AgentDashboard";

export default function OperationsConsole() {
    return (
        <DashboardLayout>
            <AgentDashboard />
        </DashboardLayout>
    );
}