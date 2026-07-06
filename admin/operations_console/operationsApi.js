import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000",
});

export const getAgentStats = () =>
    api.get("/agents/dashboard");

export const getWorkflowStats = () =>
    api.get("/workflow/history");

export const getToolStats = () =>
    api.get("/tools/dashboard");

export const getApprovalStats = () =>
    api.get("/approvals/dashboard");

export const getAuditLogs = () =>
    api.get("/audit/logs");