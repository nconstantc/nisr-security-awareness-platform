import { useEffect, useState } from "react";
import { api, ApiError } from "../../api/client";
import type { ConsoleEmployee, EmployeeRole } from "../../api/consoleTypes";
import { useAuth } from "../../context/AuthContext";
import { useTranslation } from "../../context/LanguageContext";

export function ConsoleEmployeesPage() {
  const { t } = useTranslation();
  const { user } = useAuth();
  const [employees, setEmployees] = useState<ConsoleEmployee[] | null>(null);
  const [departments, setDepartments] = useState<{ id: number; name: string }[]>([]);
  const [search, setSearch] = useState("");
  const [resettingId, setResettingId] = useState<number | null>(null);
  const [changingRoleId, setChangingRoleId] = useState<number | null>(null);
  const [result, setResult] = useState<{ email: string; password: string } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    email: "",
    full_name: "",
    department: "",
    password: "",
    is_active: true,
    role: "employee" as EmployeeRole
  });

  const roleLabels: Record<EmployeeRole, string> = {
    employee: t("consoleEmployees.roleEmployee"),
    manager: t("consoleEmployees.roleManager"),
    admin: t("consoleEmployees.roleAdmin"),
  };

  // Load employees and departments
  function loadData() {
    const query = search ? `?search=${encodeURIComponent(search)}` : "";
    Promise.all([
      api.get<ConsoleEmployee[]>(`/api/console/employees/${query}`),
      api.get<{ id: number; name: string }[]>("/api/console/departments/")
    ]).then(([employeesRes, deptsRes]) => {
      setEmployees(employeesRes);
      setDepartments(deptsRes);
    }).catch(console.error);
  }

  useEffect(() => {
    const handle = setTimeout(loadData, 250);
    return () => clearTimeout(handle);
  }, [search]);

  // Reset form
  function resetForm() {
    setFormData({
      email: "",
      full_name: "",
      department: "",
      password: "",
      is_active: true,
      role: "employee"
    });
    setEditingId(null);
    setShowForm(false);
    setShowPassword(false);
    setError(null);
  }

  // Edit employee
  function editEmployee(emp: ConsoleEmployee) {
    setFormData({
      email: emp.email,
      full_name: emp.full_name,
      department: emp.department?.toString() || "",
      password: "",
      is_active: emp.is_active,
      role: emp.role
    });
    setEditingId(emp.id);
    setShowForm(true);
    setShowPassword(false);
  }

  // Handle form submission - FIXED: Type-safe approach without using 'delete'
  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      // Build data object with optional password field
      const data: {
        email: string;
        full_name: string;
        department: string;
        is_active: boolean;
        role: EmployeeRole;
        password?: string;
      } = {
        email: formData.email,
        full_name: formData.full_name,
        department: formData.department,
        is_active: formData.is_active,
        role: formData.role
      };

      // Only add password if it's provided
      if (formData.password) {
        if (formData.password.length < 8) {
          setError("Password must be at least 8 characters");
          return;
        }
        data.password = formData.password;
      }

      if (!data.department) {
        setError("Please select a department");
        return;
      }

      if (editingId) {
        await api.patch(`/api/console/employees/${editingId}/`, data);
      } else {
        await api.post("/api/console/employees/", data);
      }
      resetForm();
      loadData();
    } catch (err) {
      setError(err instanceof ApiError ? JSON.stringify(err.detail) : "Failed to save employee");
    }
  }

  // Handle delete
  async function handleDelete(id: number, name: string) {
    if (!confirm(`Are you sure you want to delete "${name}"?`)) return;
    try {
      await api.delete(`/api/console/employees/${id}/`);
      loadData();
    } catch (err) {
      setError(err instanceof ApiError ? JSON.stringify(err.detail) : "Failed to delete employee");
    }
  }

  // Handle reset password - generates random password
  async function handleReset(employee: ConsoleEmployee) {
    if (!confirm(t("consoleEmployees.confirmReset", { name: employee.full_name }))) return;
    setError(null);
    setResult(null);
    setResettingId(employee.id);
    try {
      const { temp_password } = await api.post<{ temp_password: string }>(
        `/api/console/employees/${employee.id}/reset-password/`,
      );
      setResult({ email: employee.email, password: temp_password });
    } catch (err) {
      setError(err instanceof ApiError ? JSON.stringify(err.detail) : t("consoleEmployees.resetFailed"));
    } finally {
      setResettingId(null);
    }
  }

  // Handle role change
  async function handleRoleChange(employee: ConsoleEmployee, role: EmployeeRole) {
    if (role === employee.role) return;
    setError(null);
    setChangingRoleId(employee.id);
    try {
      const updated = await api.patch<ConsoleEmployee>(`/api/console/employees/${employee.id}/role/`, { role });
      setEmployees((prev) => prev?.map((e) => (e.id === employee.id ? updated : e)) ?? prev);
    } catch (err) {
      setError(err instanceof ApiError ? JSON.stringify(err.detail) : t("consoleEmployees.roleChangeFailed"));
    } finally {
      setChangingRoleId(null);
    }
  }

  // Copy password to clipboard
  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      // You could add a toast notification here
    } catch (err) {
      console.error("Failed to copy:", err);
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold text-slate-800 dark:text-slate-100">{t("consoleEmployees.title")}</h1>
        <div className="flex gap-3">
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder={t("consoleEmployees.searchPlaceholder")}
            className="border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 text-sm w-64 dark:bg-slate-700 dark:text-slate-100"
          />
          <button
            onClick={() => setShowForm(true)}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium"
          >
            + Add Employee
          </button>
        </div>
      </div>

      {/* Temporary Password Display */}
      {result && (
        <div className="mb-6 bg-amber-50 dark:bg-amber-950 border border-amber-300 dark:border-amber-800 rounded-xl p-4">
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1">
              <p className="text-sm text-amber-900 dark:text-amber-300">
                {t("consoleEmployees.tempPasswordPrefix")} <span className="font-medium">{result.email}</span>
              </p>
              <div className="mt-2 flex items-center gap-3 flex-wrap">
                <code className="bg-white dark:bg-slate-800 px-3 py-1.5 rounded border border-amber-300 dark:border-amber-800 font-mono text-sm select-all break-all">
                  {result.password}
                </code>
                <button
                  onClick={() => copyToClipboard(result.password)}
                  className="text-amber-700 hover:text-amber-900 dark:text-amber-400 dark:hover:text-amber-300 text-sm font-medium flex items-center gap-1"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                  </svg>
                  Copy
                </button>
              </div>
              <p className="text-xs text-amber-700 dark:text-amber-400 mt-2">
                {t("consoleEmployees.tempPasswordSuffix")}
              </p>
            </div>
            <button 
              onClick={() => setResult(null)} 
              className="shrink-0 text-amber-700 hover:underline text-sm"
            >
              {t("consoleEmployees.close")}
            </button>
          </div>
        </div>
      )}
      
      {error && <p className="mb-4 text-sm text-red-600 dark:text-red-400">{error}</p>}

      {/* Add/Edit Form */}
      {showForm && (
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 p-6 mb-6">
          <h2 className="text-lg font-medium mb-4">
            {editingId ? "Edit Employee" : "Add New Employee"}
          </h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                  Full Name <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={formData.full_name}
                  onChange={(e) => setFormData({...formData, full_name: e.target.value})}
                  className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                  Email <span className="text-red-500">*</span>
                </label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                  Department <span className="text-red-500">*</span>
                </label>
                <select
                  value={formData.department}
                  onChange={(e) => setFormData({...formData, department: e.target.value})}
                  className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                  required
                >
                  <option value="">Select Department</option>
                  {departments.map(dept => (
                    <option key={dept.id} value={dept.id}>{dept.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                  Password {editingId ? "(Leave blank to keep current)" : "(Optional)"}
                </label>
                <div className="relative mt-1">
                  <input
                    type={showPassword ? "text" : "password"}
                    value={formData.password}
                    onChange={(e) => setFormData({...formData, password: e.target.value})}
                    className="w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 pr-10 dark:bg-slate-700 dark:text-slate-100"
                    placeholder={editingId ? "Leave blank to keep current" : "Enter password (optional)"}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
                    aria-label={showPassword ? "Hide password" : "Show password"}
                  >
                    {showPassword ? (
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                    ) : (
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                      </svg>
                    )}
                  </button>
                </div>
                <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                  {editingId 
                    ? "Leave blank to keep current password" 
                    : "Leave blank to set a temporary password later via Reset PW"}
                </p>
              </div>
              <div className="flex items-center gap-4">
                <label className="flex items-center gap-2 text-sm font-medium text-slate-700 dark:text-slate-300">
                  <input
                    type="checkbox"
                    checked={formData.is_active}
                    onChange={(e) => setFormData({...formData, is_active: e.target.checked})}
                    className="h-4 w-4 rounded"
                  />
                  Active
                </label>
                <label className="flex items-center gap-2 text-sm font-medium text-slate-700 dark:text-slate-300">
                  <select
                    value={formData.role}
                    onChange={(e) => setFormData({...formData, role: e.target.value as EmployeeRole})}
                    className="border border-slate-300 dark:border-slate-600 rounded-lg px-2 py-1 text-sm dark:bg-slate-700 dark:text-slate-100"
                  >
                    {(Object.keys(roleLabels) as EmployeeRole[]).map((role) => (
                      <option key={role} value={role}>{roleLabels[role]}</option>
                    ))}
                  </select>
                </label>
              </div>
            </div>
            <div className="flex gap-3">
              <button 
                type="submit" 
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium"
              >
                {editingId ? "Update" : "Create"} Employee
              </button>
              <button 
                type="button" 
                onClick={resetForm} 
                className="px-4 py-2 bg-slate-200 hover:bg-slate-300 dark:bg-slate-700 dark:hover:bg-slate-600 rounded-lg text-sm font-medium"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {employees === null && <p className="text-slate-500 dark:text-slate-400">{t("consoleEmployees.loading")}</p>}

      {/* Employees Table */}
      <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-slate-50 dark:bg-slate-700 text-slate-500 dark:text-slate-400 text-left">
              <tr>
                <th className="px-4 py-2 font-medium">{t("consoleEmployees.colFullName")}</th>
                <th className="px-4 py-2 font-medium">{t("consoleEmployees.colEmail")}</th>
                <th className="px-4 py-2 font-medium">{t("consoleEmployees.colDepartment")}</th>
                <th className="px-4 py-2 font-medium">{t("consoleEmployees.colRole")}</th>
                <th className="px-4 py-2 font-medium">Status</th>
                <th className="px-4 py-2 font-medium text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {employees?.map((e) => (
                <tr key={e.id} className="border-t border-slate-100 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700">
                  <td className="px-4 py-2 font-medium text-slate-800 dark:text-slate-100">{e.full_name}</td>
                  <td className="px-4 py-2 text-slate-600 dark:text-slate-300">{e.email}</td>
                  <td className="px-4 py-2 text-slate-600 dark:text-slate-300">{e.department_name ?? t("consoleEmployees.noDepartment")}</td>
                  <td className="px-4 py-2">
                    <select
                      value={e.role}
                      disabled={changingRoleId === e.id || (e.id === user?.id && e.role === "admin")}
                      onChange={(ev) => handleRoleChange(e, ev.target.value as EmployeeRole)}
                      className="border border-slate-300 dark:border-slate-600 rounded-lg px-2 py-1 text-sm dark:bg-slate-700 dark:text-slate-100 disabled:opacity-50"
                    >
                      {(Object.keys(roleLabels) as EmployeeRole[]).map((role) => (
                        <option key={role} value={role}>{roleLabels[role]}</option>
                      ))}
                    </select>
                    {changingRoleId === e.id && <span className="ml-2 text-xs text-slate-400">{t("consoleEmployees.roleChanging")}</span>}
                  </td>
                  <td className="px-4 py-2">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      e.is_active ? 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300' : 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300'
                    }`}>
                      {e.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td className="px-4 py-2 text-right whitespace-nowrap">
                    <button 
                      onClick={() => editEmployee(e)} 
                      className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 text-sm font-medium mr-2"
                    >
                      Edit
                    </button>
                    <button 
                      onClick={() => handleReset(e)} 
                      disabled={resettingId === e.id} 
                      className="text-blue-600 hover:underline disabled:opacity-50 mr-2"
                    >
                      {resettingId === e.id ? t("consoleEmployees.resetting") : "Reset PW"}
                    </button>
                    <button 
                      onClick={() => handleDelete(e.id, e.full_name)} 
                      className="text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 text-sm font-medium"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {employees?.length === 0 && <p className="p-4 text-slate-500 dark:text-slate-400">{t("consoleEmployees.noEmployeesFound")}</p>}
      </div>
    </div>
  );
}