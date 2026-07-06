import { useEffect, useState } from "react";

import {
  Box,
  Button,
  Card,
  CardContent,
  Divider,
  Grid,
  Typography,
} from "@mui/material";

import { User, AISettings, AuditLog } from "../../types/admin";
import { adminService } from "../../services/adminService";

const Admin = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [settings, setSettings] = useState<AISettings | null>(null);
  const [logs, setLogs] = useState<AuditLog[]>([]);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    const usersRes = await adminService.getUsers();
    const settingsRes = await adminService.getAISettings();
    const logsRes = await adminService.getAuditLogs();

    setUsers(usersRes.data);
    setSettings(settingsRes.data);
    setLogs(logsRes.data);
  }

  async function deleteUser(id: string) {
    await adminService.deleteUser(id);
    loadData();
  }

  return (
    <Box p={4}>
      <Typography variant="h4" mb={3}>
        Admin Console
      </Typography>

      <Grid container spacing={3}>

        {/* User Management */}
        <Grid item xs={12}>
          <Card>
            <CardContent>

              <Typography variant="h6">
                User Management
              </Typography>

              <Divider sx={{ my: 2 }} />

              {users.map((user) => (
                <Box
                  key={user.id}
                  display="flex"
                  justifyContent="space-between"
                  mb={2}
                >
                  <Typography>
                    {user.name} ({user.role})
                  </Typography>

                  <Button
                    color="error"
                    variant="contained"
                    onClick={() => deleteUser(user.id)}
                  >
                    Delete
                  </Button>
                </Box>
              ))}

            </CardContent>
          </Card>
        </Grid>

        {/* AI Settings */}
        <Grid item xs={12}>
          <Card>
            <CardContent>

              <Typography variant="h6">
                AI Settings
              </Typography>

              <Divider sx={{ my: 2 }} />

              {settings && (
                <>
                  <Typography>
                    Model: {settings.model}
                  </Typography>

                  <Typography>
                    Temperature: {settings.temperature}
                  </Typography>

                  <Typography>
                    Token Limit: {settings.tokenLimit}
                  </Typography>

                  <Typography>
                    Prompt: {settings.promptTemplate}
                  </Typography>
                </>
              )}

            </CardContent>
          </Card>
        </Grid>

        {/* Audit Logs */}
        <Grid item xs={12}>
          <Card>
            <CardContent>

              <Typography variant="h6">
                Audit Logs
              </Typography>

              <Divider sx={{ my: 2 }} />

              {logs.map((log) => (
                <Typography key={log.id}>
                  {log.time} - {log.user} - {log.action}
                </Typography>
              ))}

            </CardContent>
          </Card>
        </Grid>

      </Grid>
    </Box>
  );
};

export default Admin;