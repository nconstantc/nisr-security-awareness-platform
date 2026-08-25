import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, ApiError } from "../../api/client";
import type { ConsoleDepartment, ConsoleEmployee, ConsoleWave, ConsoleWaveAssignment, WaveStatusValue } from "../../api/consoleTypes";
import { StatusBadge } from "../../components/StatusBadge";
import { WaveStatusBadge } from "../components/WaveStatusBadge";
import { formatDate } from "../../utils/date";
import { useTranslation } from "../../context/LanguageContext";

const STATUS_FLOW: Record<WaveStatusValue, WaveStatusValue | null> = {
  draft: "active",
  active: "closed",
  closed: null,
};

export function ConsoleWaveEditPage() {
  const { t } = useTranslation();
  const { waveId } = useParams();
  const [wave, setWave] = useState<ConsoleWave | null>(null);
  const [assignments, setAssignments] = useState<ConsoleWaveAssignment[] | null>(null);
  const [departments, setDepartments] = useState<ConsoleDepartment[] | null>(null);
  const [selectedDepts, setSelectedDepts] = useState<number[]>([]);
  const [search, setSearch] = useState("");
  const [searchResults, setSearchResults] = useState<ConsoleEmployee[]>([]);
  const [message, setMessage] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({
    start_date: "",
    deadline: "",
    pass_threshold: 80,
    max_attempts: null as number | null,
  });

  function reloadWave() {
    api.get<ConsoleWave>(`/api/console/waves/${waveId}/`).then((data) => {
      setWave(data);
      setEditData({
        start_date: data.start_date || "",
        deadline: data.deadline || "",
        pass_threshold: data.pass_threshold || 80,
        max_attempts: data.max_attempts ?? null,
      });
    });
  }
  function reloadAssignments() {
    api.get<ConsoleWaveAssignment[]>(`/api/console/wave-assignments/?wave=${waveId}`).then(setAssignments);
  }

  useEffect(() => {
    reloadWave();
    reloadAssignments();
    api.get<ConsoleDepartment[]>("/api/console/departments/").then(setDepartments);
  }, [waveId]);

  useEffect(() => {
    if (search.trim().length < 2) {
      setSearchResults([]);
      return;
    }
    const timeout = setTimeout(() => {
      api.get<ConsoleEmployee[]>(`/api/console/employees/?search=${encodeURIComponent(search)}`).then(setSearchResults);
    }, 250);
    return () => clearTimeout(timeout);
  }, [search]);

  async function handleStatusChange() {
    if (!wave) return;
    const next = STATUS_FLOW[wave.status];
    if (!next) return;
    const updated = await api.post<ConsoleWave>(`/api/console/waves/${wave.id}/set-status/`, { status: next });
    setWave(updated);
  }

  async function handleSaveEdit() {
    if (!wave) return;
    try {
      const updated = await api.patch<ConsoleWave>(`/api/console/waves/${wave.id}/`, {
        start_date: editData.start_date,
        deadline: editData.deadline,
        pass_threshold: editData.pass_threshold,
        max_attempts: editData.max_attempts,
      });
      setWave(updated);
      setIsEditing(false);
      setMessage("Wave updated successfully");
    } catch (err) {
      setMessage("Failed to update wave");
      console.error(err);
    }
  }

  async function handleAssignAll() {
    const res = await api.post<{ created: number }>(`/api/console/waves/${waveId}/assign-all/`);
    setMessage(t("consoleWaveEdit.assignedAllMessage", { count: res.created }));
    reloadAssignments();
    reloadWave();
  }

  async function handleAssignDepartments() {
    if (selectedDepts.length === 0) return;
    const res = await api.post<{ created: number }>(`/api/console/waves/${waveId}/assign-departments/`, {
      department_ids: selectedDepts,
    });
    setMessage(t("consoleWaveEdit.assignedDepartmentsMessage", { count: res.created }));
    setSelectedDepts([]);
    reloadAssignments();
    reloadWave();
  }

  async function handleAssignEmployee(employeeId: number) {
    try {
      await api.post(`/api/console/waves/${waveId}/assign-employees/`, { employee_ids: [employeeId] });
      setSearch("");
      setSearchResults([]);
      reloadAssignments();
      reloadWave();
    } catch (err) {
      setMessage(err instanceof ApiError ? String(err.detail) : t("consoleWaveEdit.assignEmployeeError"));
    }
  }

  async function handleRemove(assignmentId: number) {
    await api.delete(`/api/console/wave-assignments/${assignmentId}/`);
    reloadAssignments();
    reloadWave();
  }

  const STATUS_ACTION_LABEL: Record<WaveStatusValue, string> = {
    draft: t("consoleWaveEdit.statusActionDraft"),
    active: t("consoleWaveEdit.statusActionActive"),
    closed: t("consoleWaveEdit.statusActionClosed"),
  };

  if (!wave) return <p className="text-slate-500 dark:text-slate-400">{t("consoleWaveEdit.loading")}</p>;

  return (
    <div className="space-y-6">
      <div>
        <Link to="/console/waves" className="text-sm text-blue-600 hover:underline">
          {t("consoleWaveEdit.allWaves")}
        </Link>
        <div className="flex items-center justify-between mt-1">
          <h1 className="text-2xl font-semibold text-slate-800 dark:text-slate-100">{wave.name}</h1>
          <div className="flex items-center gap-3">
            <WaveStatusBadge status={wave.status} />
            {STATUS_FLOW[wave.status] && (
              <button
                onClick={handleStatusChange}
                className="px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium"
              >
                {STATUS_ACTION_LABEL[wave.status]}
              </button>
            )}
            <button
              onClick={() => setIsEditing(!isEditing)}
              className="px-3 py-1.5 rounded-lg bg-slate-600 hover:bg-slate-700 text-white text-sm font-medium"
            >
              {isEditing ? "Cancel" : "Edit"}
            </button>
          </div>
        </div>

        {/* Wave Details - View Mode */}
        {!isEditing && (
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            {t("consoleWaveEdit.courseLabelPrefix")} <strong className="text-slate-700 dark:text-slate-200">{wave.course_title}</strong> ·{" "}
            {t("consoleWaveEdit.startLabelPrefix")} {formatDate(wave.start_date)} ·{" "}
            {t("consoleWaveEdit.deadlineLabelPrefix")} {formatDate(wave.deadline)} ·{" "}
            {t("consoleWaveEdit.passThresholdLabelPrefix")} {wave.pass_threshold}% ·{" "}
            {t("consoleWaveEdit.attemptsLabelPrefix")}{" "}
            {wave.max_attempts ?? t("consoleWaveEdit.unlimitedAttempts")}
            {wave.is_overdue && <span className="text-red-600 dark:text-red-400 font-medium"> · {t("consoleWaveEdit.overdue")}</span>}
          </p>
        )}

        {/* Wave Details - Edit Mode */}
        {isEditing && (
          <div className="mt-4 p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg border border-slate-200 dark:border-slate-700">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">Start Date</label>
                <input
                  type="date"
                  value={editData.start_date}
                  onChange={(e) => setEditData({ ...editData, start_date: e.target.value })}
                  className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">Deadline</label>
                <input
                  type="date"
                  value={editData.deadline}
                  onChange={(e) => setEditData({ ...editData, deadline: e.target.value })}
                  className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">Pass Threshold (%)</label>
                <input
                  type="number"
                  min={1}
                  max={100}
                  value={editData.pass_threshold}
                  onChange={(e) => setEditData({ ...editData, pass_threshold: parseInt(e.target.value) })}
                  className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">Max Attempts (empty = unlimited)</label>
                <input
                  type="number"
                  min={1}
                  value={editData.max_attempts ?? ""}
                  onChange={(e) => {
                    const val = e.target.value;
                    setEditData({ ...editData, max_attempts: val === "" ? null : parseInt(val) });
                  }}
                  className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                  placeholder="Unlimited"
                />
              </div>
            </div>
            <div className="flex gap-3 mt-4">
              <button
                onClick={handleSaveEdit}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium"
              >
                Save Changes
              </button>
              <button
                onClick={() => setIsEditing(false)}
                className="px-4 py-2 bg-slate-200 hover:bg-slate-300 dark:bg-slate-700 dark:hover:bg-slate-600 rounded-lg text-sm font-medium"
              >
                Cancel
              </button>
            </div>
          </div>
        )}
      </div>

      <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 p-5">
        <h2 className="text-sm font-semibold text-slate-600 dark:text-slate-300 mb-3">{t("consoleWaveEdit.assignEmployeesTitle")}</h2>
        <div className="flex flex-wrap items-start gap-6">
          <div>
            <button
              onClick={handleAssignAll}
              className="px-3 py-1.5 rounded-lg bg-slate-700 hover:bg-slate-800 text-white text-sm font-medium"
            >
              {t("consoleWaveEdit.assignAllButton")}
            </button>
          </div>
          <div>
            <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">{t("consoleWaveEdit.byDepartmentLabel")}</p>
            <div className="flex flex-wrap gap-2 mb-2">
              {departments?.map((d) => (
                <label key={d.id} className="flex items-center gap-1 text-sm border border-slate-200 dark:border-slate-700 rounded-lg px-2 py-1">
                  <input
                    type="checkbox"
                    checked={selectedDepts.includes(d.id)}
                    onChange={(e) =>
                      setSelectedDepts((prev) => (e.target.checked ? [...prev, d.id] : prev.filter((id) => id !== d.id)))
                    }
                  />
                  {d.name} ({d.employee_count})
                </label>
              ))}
            </div>
            <button
              onClick={handleAssignDepartments}
              disabled={selectedDepts.length === 0}
              className="px-3 py-1.5 rounded-lg bg-slate-700 hover:bg-slate-800 disabled:opacity-50 text-white text-sm font-medium"
            >
              {t("consoleWaveEdit.assignDepartmentsButton")}
            </button>
          </div>
          <div className="relative">
            <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">{t("consoleWaveEdit.individualLabel")}</p>
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder={t("consoleWaveEdit.searchPlaceholder")}
              className="border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-1.5 text-sm w-64 dark:bg-slate-700 dark:text-slate-100"
            />
            {searchResults.length > 0 && (
              <div className="absolute z-10 mt-1 w-64 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg shadow-md max-h-56 overflow-y-auto">
                {searchResults.map((emp) => (
                  <button
                    key={emp.id}
                    onClick={() => handleAssignEmployee(emp.id)}
                    className="block w-full text-left px-3 py-2 text-sm hover:bg-slate-50 dark:hover:bg-slate-700"
                  >
                    {emp.full_name} <span className="text-slate-400">({emp.department_name ?? t("consoleWaveEdit.noDepartment")})</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
        {message && <p className="text-sm text-green-700 dark:text-green-400 mt-3">{message}</p>}
      </div>

      <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-slate-50 dark:bg-slate-700 text-slate-500 dark:text-slate-400 text-left">
              <tr>
                <th className="px-4 py-2 font-medium">{t("consoleWaveEdit.colEmployee")}</th>
                <th className="px-4 py-2 font-medium">{t("consoleWaveEdit.colDepartment")}</th>
                <th className="px-4 py-2 font-medium">{t("consoleWaveEdit.colStatus")}</th>
                <th className="px-4 py-2 font-medium">{t("consoleWaveEdit.colAttempts")}</th>
                <th className="px-4 py-2 font-medium">{t("consoleWaveEdit.colBestScore")}</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {assignments?.map((a) => (
                <tr key={a.id} className="border-t border-slate-100 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700">
                  <td className="px-4 py-2">
                    <div className="font-medium text-slate-800 dark:text-slate-100">{a.employee_name}</div>
                    <div className="text-xs text-slate-400">{a.employee_email}</div>
                  </td>
                  <td className="px-4 py-2 text-slate-600 dark:text-slate-300">{a.department ?? "-"}</td>
                  <td className="px-4 py-2">
                    <StatusBadge status={a.status} overdue={a.is_overdue} />
                  </td>
                  <td className="px-4 py-2 text-slate-600 dark:text-slate-300">{a.attempts_count}</td>
                  <td className="px-4 py-2 text-slate-600 dark:text-slate-300">{a.best_score !== null ? `${a.best_score}%` : "-"}</td>
                  <td className="px-4 py-2 text-right">
                    <button onClick={() => handleRemove(a.id)} className="text-red-600 dark:text-red-400 hover:underline text-xs">
                      {t("consoleWaveEdit.remove")}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {assignments?.length === 0 && <p className="p-4 text-slate-500 dark:text-slate-400">{t("consoleWaveEdit.noAssignments")}</p>}
      </div>
    </div>
  );
}