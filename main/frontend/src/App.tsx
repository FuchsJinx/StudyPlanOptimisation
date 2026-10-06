import { Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./auth/AuthContext";
import { RequireAuth } from "./auth/RequireAuth";
import { RequirePermission } from "./auth/RequirePermission";
import { AppLayout } from "./layouts/AppLayout";
import { DashboardPage } from "./pages/DashboardPage";
import { DirectoriesHubPage } from "./pages/DirectoriesHubPage";
import { DirectoryDetailPage } from "./pages/DirectoryDetailPage";
import { JournalPage } from "./pages/JournalPage";
import { LoginPage } from "./pages/LoginPage";
import { PlansPage } from "./pages/PlansPage";
import { ProfilePage } from "./pages/ProfilePage";
import { ReportsPage } from "./pages/ReportsPage";
import { SchedulePage } from "./pages/SchedulePage";
import { SessionExpiredPage } from "./pages/SessionExpiredPage";
import { SettingsPage } from "./pages/SettingsPage";
import { SubstitutionsPage } from "./pages/SubstitutionsPage";
import { WorkloadPage } from "./pages/WorkloadPage";
import { RegisterPage } from "./pages/RegisterPage";

function Perm({ permission, page }: { permission: string; page: React.ReactNode }) {
  return <RequirePermission permission={permission}>{page}</RequirePermission>;
}

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/session-expired" element={<SessionExpiredPage />} />
        <Route
          path="/"
          element={
            <RequireAuth>
              <AppLayout />
            </RequireAuth>
          }
        >
          <Route index element={<Perm permission="dashboard" page={<DashboardPage />} />} />
          <Route path="directories" element={<Perm permission="directories" page={<DirectoriesHubPage />} />} />
          <Route
            path="directories/:kind"
            element={<Perm permission="directories" page={<DirectoryDetailPage />} />}
          />
          <Route path="plans" element={<Perm permission="plans" page={<PlansPage />} />} />
          <Route path="import" element={<Perm permission="plans" page={<PlansPage />} />} />
          <Route path="workload" element={<Perm permission="workload" page={<WorkloadPage />} />} />
          <Route path="schedule" element={<Perm permission="schedule" page={<SchedulePage />} />} />
          <Route
            path="substitutions"
            element={<Perm permission="substitutions" page={<SubstitutionsPage />} />}
          />
          <Route path="journal" element={<Perm permission="journal" page={<JournalPage />} />} />
          <Route path="reports" element={<Perm permission="reports" page={<ReportsPage />} />} />
          <Route path="settings" element={<Perm permission="settings" page={<SettingsPage />} />} />
          <Route path="profile" element={<Perm permission="profile" page={<ProfilePage />} />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthProvider>
  );
}
