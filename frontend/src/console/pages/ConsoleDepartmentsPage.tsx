import { useEffect, useState } from "react";
import type { FormEvent, ChangeEvent } from "react";
import { api } from "../../api/client";

interface Department {
    id: number;
    name: string;
}

export function ConsoleDepartmentsPage() {
    const [departments, setDepartments] = useState<Department[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [showForm, setShowForm] = useState<boolean>(false);
    const [editingId, setEditingId] = useState<number | null>(null);
    const [formData, setFormData] = useState<{ name: string }>({ name: "" });
    const [error, setError] = useState<string | null>(null);

    function loadDepartments(): void {
        setLoading(true);
        api.get<Department[]>("/api/console/departments/")
            .then((data: Department[]) => {
                setDepartments(data);
                setLoading(false);
            })
            .catch((err: unknown) => {
                console.error(err);
                setLoading(false);
            });
    }

    useEffect(() => {
        loadDepartments();
    }, []);

    function resetForm(): void {
        setFormData({ name: "" });
        setEditingId(null);
        setShowForm(false);
        setError(null);
    }

    function editDepartment(dept: Department): void {
        setFormData({ name: dept.name });
        setEditingId(dept.id);
        setShowForm(true);
    }

    function handleInputChange(e: ChangeEvent<HTMLInputElement>): void {
        setFormData({ name: e.target.value });
    }

    async function handleSubmit(e: FormEvent<HTMLFormElement>): Promise<void> {
        e.preventDefault();
        setError(null);
        try {
            if (!formData.name.trim()) {
                setError("Department name is required");
                return;
            }

            if (editingId) {
                await api.patch<Department>(`/api/console/departments/${editingId}/`, formData);
            } else {
                await api.post<Department>("/api/console/departments/", formData);
            }
            resetForm();
            loadDepartments();
        } catch (err) {
            setError("Failed to save department");
            console.error(err);
        }
    }

    async function handleDelete(id: number, name: string): Promise<void> {
        if (!confirm(`Are you sure you want to delete "${name}"?`)) return;
        try {
            await api.delete(`/api/console/departments/${id}/`);
            loadDepartments();
        } catch (err) {
            setError("Failed to delete department");
            console.error(err);
        }
    }

    if (loading) {
        return <div className="p-4 text-slate-500">Loading departments...</div>;
    }

    return (
        <div className="p-4">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-semibold text-slate-800 dark:text-slate-100">
                    Departments
                </h1>
                <button
                    onClick={() => setShowForm(true)}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium"
                >
                    + Add Department
                </button>
            </div>

            {error && (
                <div className="mb-4 p-3 bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-700 rounded-lg text-red-700 dark:text-red-300">
                    {error}
                </div>
            )}

            {/* Add/Edit Form */}
            {showForm && (
                <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 p-6 mb-6">
                    <h2 className="text-lg font-medium mb-4">
                        {editingId ? "Edit Department" : "Add New Department"}
                    </h2>
                    <form onSubmit={handleSubmit} className="flex gap-4">
                        <input
                            type="text"
                            value={formData.name}
                            onChange={handleInputChange}
                            placeholder="Department name"
                            className="flex-1 border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                            required
                        />
                        <button
                            type="submit"
                            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium"
                        >
                            {editingId ? "Update" : "Create"}
                        </button>
                        <button
                            type="button"
                            onClick={resetForm}
                            className="px-4 py-2 bg-slate-200 hover:bg-slate-300 dark:bg-slate-700 dark:hover:bg-slate-600 rounded-lg text-sm font-medium"
                        >
                            Cancel
                        </button>
                    </form>
                </div>
            )}

            {/* Departments List */}
            <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden">
                <table className="w-full">
                    <thead className="bg-slate-50 dark:bg-slate-700">
                        <tr>
                            <th className="px-4 py-3 text-left text-sm font-medium text-slate-600 dark:text-slate-300">Name</th>
                            <th className="px-4 py-3 text-right text-sm font-medium text-slate-600 dark:text-slate-300">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-200 dark:divide-slate-700">
                        {departments.map((dept) => (
                            <tr key={dept.id} className="hover:bg-slate-50 dark:hover:bg-slate-700/50">
                                <td className="px-4 py-3 text-sm text-slate-800 dark:text-slate-100">{dept.name}</td>
                                <td className="px-4 py-3 text-right">
                                    <button
                                        onClick={() => editDepartment(dept)}
                                        className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 text-sm font-medium mr-3"
                                    >
                                        Edit
                                    </button>
                                    <button
                                        onClick={() => handleDelete(dept.id, dept.name)}
                                        className="text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 text-sm font-medium"
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {departments.length === 0 && (
                            <tr>
                                <td colSpan={2} className="px-4 py-8 text-center text-slate-500 dark:text-slate-400">
                                    No departments found. Click "Add Department" to create one.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}