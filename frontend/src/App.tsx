// frontend/src/App.tsx
import { Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "./context/AuthContext";
import { useTranslation } from "./context/LanguageContext";
import { LoginPage } from "./pages/LoginPage";
import { ChangePasswordPage } from "./pages/ChangePasswordPage";
import { SettingsPage } from "./pages/SettingsPage";
import { DashboardPage } from "./pages/DashboardPage";
import { CoursePage } from "./pages/CoursePage";
import { BadgesPage } from "./pages/BadgesPage";
import { BadgeVerificationPage } from "./pages/BadgeVerificationPage";
import { LeaderboardPage } from "./pages/LeaderboardPage";
import { ConsoleLayout } from "./console/ConsoleLayout";
import { ConsoleDashboardPage } from "./console/pages/ConsoleDashboardPage";
import { ConsoleWavesPage } from "./console/pages/ConsoleWavesPage";
import { ConsoleWaveEditPage } from "./console/pages/ConsoleWaveEditPage";
import { ConsoleCoursesPage } from "./console/pages/ConsoleCoursesPage";
import { ConsoleCourseEditPage } from "./console/pages/ConsoleCourseEditPage";
import { ConsoleProblemEmployeesPage } from "./console/pages/ConsoleProblemEmployeesPage";
import { ConsoleEmployeesPage } from "./console/pages/ConsoleEmployeesPage";
import { ConsoleDepartmentsPage } from "./console/pages/ConsoleDepartmentsPage";
import { ConsoleIntegrationsPage } from "./console/pages/ConsoleIntegrationsPage";
import { ConsoleNotificationsPage } from "./console/pages/ConsoleNotificationsPage";
import { ConsoleSecurityPage } from "./console/pages/ConsoleSecurityPage";
import { ConsoleLogsPage } from "./console/pages/ConsoleLogsPage";
import { ConsoleBadgesPage } from "./console/pages/ConsoleBadgesPage";
import { ConsoleLeaderboardPage } from "./console/pages/ConsoleLeaderboardPage";
import { ConsolePhishingPage } from "./console/pages/ConsolePhishingPage";
import { AppLayout } from "./components/AppLayout";

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const { t } = useTranslation();
  if (loading) return <div className="min-h-screen flex items-center justify-center text-slate-500">{t("common.loading")}</div>;
  if (!user) return <Navigate to="/login" replace />;
  if (user.must_change_password) return <Navigate to="/change-password" replace />;
  return <>{children}</>;
}

function SuperAdminRoute({ children }: { children: React.ReactNode }) {
  const { user } = useAuth();
  if (!user?.is_superuser) return <Navigate to="/console" replace />;
  return <>{children}</>;
}

function App() {
  return (
    <Routes>
      {/* Public Routes - No Footer */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/change-password" element={<ChangePasswordPage />} />
      <Route path="/badge/:token" element={<BadgeVerificationPage />} />
      
      {/* Protected Routes - With Footer */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <AppLayout>
              <DashboardPage />
            </AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/waves/:waveId"
        element={
          <ProtectedRoute>
            <AppLayout>
              <CoursePage />
            </AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/settings"
        element={
          <ProtectedRoute>
            <AppLayout>
              <SettingsPage />
            </AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/badges"
        element={
          <ProtectedRoute>
            <AppLayout>
              <BadgesPage />
            </AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/leaderboard"
        element={
          <ProtectedRoute>
            <AppLayout>
              <LeaderboardPage />
            </AppLayout>
          </ProtectedRoute>
        }
      />
      
      {/* Console Routes - Admin Interface (No Footer by default) */}
      <Route path="/console" element={<ConsoleLayout />}>
        <Route index element={<ConsoleDashboardPage />} />
        <Route path="waves" element={<ConsoleWavesPage />} />
        <Route path="waves/:waveId" element={<ConsoleWaveEditPage />} />
        <Route path="courses" element={<ConsoleCoursesPage />} />
        <Route path="courses/:courseId" element={<ConsoleCourseEditPage />} />
        <Route path="problem-employees" element={<ConsoleProblemEmployeesPage />} />
        <Route path="badges" element={<ConsoleBadgesPage />} />
        <Route
          path="employees"
          element={
            <SuperAdminRoute>
              <ConsoleEmployeesPage />
            </SuperAdminRoute>
          }
        />
        <Route
          path="departments"
          element={
            <SuperAdminRoute>
              <ConsoleDepartmentsPage />
            </SuperAdminRoute>
          }
        />
        <Route path="ldap" element={<Navigate to="/console/integrations" replace />} />
        <Route
          path="integrations"
          element={
            <SuperAdminRoute>
              <ConsoleIntegrationsPage />
            </SuperAdminRoute>
          }
        />
        <Route
          path="notifications"
          element={
            <SuperAdminRoute>
              <ConsoleNotificationsPage />
            </SuperAdminRoute>
          }
        />
        <Route
          path="security"
          element={
            <SuperAdminRoute>
              <ConsoleSecurityPage />
            </SuperAdminRoute>
          }
        />
        <Route
          path="leaderboard"
          element={
            <SuperAdminRoute>
              <ConsoleLeaderboardPage />
            </SuperAdminRoute>
          }
        />
        <Route 
          path="phishing" 
          element={
            <SuperAdminRoute>
              <ConsolePhishingPage />
            </SuperAdminRoute>
          } 
        />
        <Route
          path="logs"
          element={
            <SuperAdminRoute>
              <ConsoleLogsPage />
            </SuperAdminRoute>
          }
        />
      </Route>
      
      {/* Fallback Route */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;