import { useEffect, useState } from "react";
import type { FormEvent, ChangeEvent } from "react";
import { api } from "../../api/client";

interface PhishingCampaign {
    id: number;
    name: string;
    template: {
        id: number;
        name: string;
        subject: string;
    };
    status: string;
    start_date: string;
    end_date: string;
    created_at: string;
}

interface PhishingTemplate {
    id: number;
    name: string;
    subject: string;
    body?: string;
    sender_name: string;
    sender_email: string;
    is_active: boolean;
}

interface PhishingResult {
    id: number;
    campaign: number;
    campaign_name: string;
    employee: number;
    employee_email: string;
    status: string;
    opened_at: string | null;
    clicked_at: string | null;
    submitted_at: string | null;
    reported_at: string | null;
}

interface SendPhishingResponse {
    success: boolean;
    message: string;
    output?: string;
    error?: string;
}

type PhishingTab = "campaigns" | "templates" | "results";

export function ConsolePhishingPage() {
    const [activeTab, setActiveTab] = useState<PhishingTab>("campaigns");
    const [campaigns, setCampaigns] = useState<PhishingCampaign[]>([]);
    const [templates, setTemplates] = useState<PhishingTemplate[]>([]);
    const [results, setResults] = useState<PhishingResult[]>([]);
    const [loading, setLoading] = useState(true);
    const [showForm, setShowForm] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [message, setMessage] = useState<string | null>(null);
    const [sending, setSending] = useState(false);
    const [showTemplateForm, setShowTemplateForm] = useState(false);
    const [showEditTemplateForm, setShowEditTemplateForm] = useState(false);
    const [editingTemplateId, setEditingTemplateId] = useState<number | null>(null);
    const [editingTemplate, setEditingTemplate] = useState<PhishingTemplate | null>(null);
    const [formData, setFormData] = useState({
        name: "",
        template: "",
        status: "draft",
        start_date: "",
        end_date: "",
    });
    const [templateFormData, setTemplateFormData] = useState({
        name: "",
        subject: "",
        body: "",
        sender_name: "",
        sender_email: "",
        is_active: true,
    });

    function loadData() {
        setLoading(true);
        Promise.all([
            api.get<PhishingCampaign[]>("/api/console/phishing/campaigns/"),
            api.get<PhishingTemplate[]>("/api/console/phishing/templates/"),
            api.get<PhishingResult[]>("/api/console/phishing/results/")
        ])
        .then(([campaignsRes, templatesRes, resultsRes]) => {
            setCampaigns(campaignsRes);
            setTemplates(templatesRes);
            setResults(resultsRes);
            setLoading(false);
        })
        .catch((err) => {
            console.error(err);
            setLoading(false);
        });
    }

    useEffect(loadData, []);

    function resetForm() {
        setFormData({
            name: "",
            template: "",
            status: "draft",
            start_date: "",
            end_date: "",
        });
        setShowForm(false);
        setError(null);
    }

    function resetTemplateForm() {
        setTemplateFormData({
            name: "",
            subject: "",
            body: "",
            sender_name: "",
            sender_email: "",
            is_active: true,
        });
        setShowTemplateForm(false);
        setShowEditTemplateForm(false);
        setEditingTemplateId(null);
        setEditingTemplate(null);
        setError(null);
    }

    function handleInputChange(e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    }

    function handleTemplateInputChange(e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
        setTemplateFormData({ ...templateFormData, [e.target.name]: e.target.value });
    }

    async function handleSubmit(e: FormEvent<HTMLFormElement>) {
        e.preventDefault();
        setError(null);
        try {
            await api.post("/api/console/phishing/campaigns/", formData);
            resetForm();
            loadData();
        } catch (err) {
            setError("Failed to create phishing campaign");
            console.error(err);
        }
    }

    async function handleTemplateSubmit(e: FormEvent<HTMLFormElement>) {
        e.preventDefault();
        setError(null);
        try {
            await api.post("/api/console/phishing/templates/", templateFormData);
            resetTemplateForm();
            loadData();
        } catch (err) {
            setError("Failed to create phishing template");
            console.error(err);
        }
    }

    async function handleEditTemplateSubmit(e: FormEvent<HTMLFormElement>) {
        e.preventDefault();
        setError(null);
        try {
            await api.patch(`/api/console/phishing/templates/${editingTemplateId}/`, templateFormData);
            resetTemplateForm();
            loadData();
        } catch (err) {
            setError("Failed to update phishing template");
            console.error(err);
        }
    }

    function editTemplate(template: PhishingTemplate) {
        setEditingTemplate(template);
        setTemplateFormData({
            name: template.name,
            subject: template.subject,
            body: template.body || "",
            sender_name: template.sender_name || "",
            sender_email: template.sender_email || "",
            is_active: template.is_active,
        });
        setEditingTemplateId(template.id);
        setShowEditTemplateForm(true);
    }

    async function handleSendPhishing() {
        if (!confirm('Are you sure you want to send phishing emails to all assigned employees?')) return;
        setSending(true);
        setError(null);
        setMessage(null);
        try {
            const response = await api.post<SendPhishingResponse>('/api/console/phishing/send/');
            if (response.success) {
                setMessage('✅ Phishing emails sent successfully!');
            } else {
                setError(response.error || 'Failed to send emails');
            }
        } catch (err) {
            setError('Failed to send phishing emails');
            console.error(err);
        } finally {
            setSending(false);
        }
    }

    async function handleStatusChange(id: number, status: string) {
        try {
            await api.patch(`/api/console/phishing/campaigns/${id}/`, { status });
            loadData();
        } catch (err) {
            setError("Failed to update campaign status");
            console.error(err);
        }
    }

    async function handleDeleteCampaign(id: number, name: string) {
        if (!confirm(`Are you sure you want to delete campaign "${name}"?`)) return;
        try {
            await api.delete(`/api/console/phishing/campaigns/${id}/`);
            loadData();
        } catch (err) {
            setError("Failed to delete campaign");
            console.error(err);
        }
    }

    async function handleDeleteTemplate(id: number, name: string) {
        if (!confirm(`Are you sure you want to delete template "${name}"?`)) return;
        try {
            await api.delete(`/api/console/phishing/templates/${id}/`);
            loadData();
        } catch (err) {
            setError("Failed to delete template");
            console.error(err);
        }
    }

    const statusColors: Record<string, string> = {
        draft: "bg-gray-200 text-gray-700",
        scheduled: "bg-yellow-200 text-yellow-700",
        running: "bg-green-200 text-green-700",
        completed: "bg-blue-200 text-blue-700",
        cancelled: "bg-red-200 text-red-700",
    };

    const resultStatusColors: Record<string, string> = {
        sent: "bg-gray-200 text-gray-700",
        opened: "bg-blue-200 text-blue-700",
        clicked: "bg-yellow-200 text-yellow-700",
        submitted: "bg-red-200 text-red-700",
        reported: "bg-green-200 text-green-700",
        failed: "bg-red-200 text-red-700",
    };

    if (loading) {
        return <div className="p-4 text-slate-500">Loading phishing data...</div>;
    }

    return (
        <div className="p-4">
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h1 className="text-2xl font-semibold text-slate-800 dark:text-slate-100">
                        Phishing Management
                    </h1>
                    <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                        Create and manage phishing campaigns, templates, and results
                    </p>
                </div>
            </div>

            {error && (
                <div className="mb-4 p-3 bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-700 rounded-lg text-red-700 dark:text-red-300">
                    {error}
                </div>
            )}

            {message && (
                <div className="mb-4 p-3 bg-green-100 dark:bg-green-900/30 border border-green-400 dark:border-green-700 rounded-lg text-green-700 dark:text-green-300">
                    {message}
                </div>
            )}

            {/* Tab Navigation */}
            <div className="flex border-b border-slate-200 dark:border-slate-700 mb-6">
                <button
                    onClick={() => setActiveTab("campaigns")}
                    className={`px-4 py-2 text-sm font-medium border-b-2 transition ${
                        activeTab === "campaigns"
                            ? "border-blue-600 text-blue-600 dark:text-blue-400"
                            : "border-transparent text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-300"
                    }`}
                >
                    Campaigns ({campaigns.length})
                </button>
                <button
                    onClick={() => setActiveTab("templates")}
                    className={`px-4 py-2 text-sm font-medium border-b-2 transition ${
                        activeTab === "templates"
                            ? "border-blue-600 text-blue-600 dark:text-blue-400"
                            : "border-transparent text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-300"
                    }`}
                >
                    Templates ({templates.length})
                </button>
                <button
                    onClick={() => setActiveTab("results")}
                    className={`px-4 py-2 text-sm font-medium border-b-2 transition ${
                        activeTab === "results"
                            ? "border-blue-600 text-blue-600 dark:text-blue-400"
                            : "border-transparent text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-300"
                    }`}
                >
                    Results ({results.length})
                </button>
            </div>

            {/* ========== CAMPAIGNS TAB ========== */}
            {activeTab === "campaigns" && (
                <div>
                    <div className="flex justify-between items-center mb-4">
                        <div>
                            <h2 className="text-lg font-medium text-slate-800 dark:text-slate-100">Campaigns</h2>
                            <p className="text-sm text-slate-500 dark:text-slate-400">Manage your phishing campaigns</p>
                        </div>
                        <div className="flex gap-2">
                            <button
                                onClick={handleSendPhishing}
                                disabled={sending}
                                className="px-4 py-2 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white rounded-lg text-sm font-medium flex items-center gap-2"
                            >
                                {sending ? (
                                    <>
                                        <span className="animate-spin">⏳</span>
                                        Sending...
                                    </>
                                ) : (
                                    '📧 Send Phishing Emails'
                                )}
                            </button>
                            <button
                                onClick={() => setShowForm(true)}
                                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium"
                            >
                                + Create Campaign
                            </button>
                        </div>
                    </div>

                    {/* Create Campaign Form */}
                    {showForm && (
                        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 p-6 mb-6">
                            <h2 className="text-lg font-medium mb-4">Create New Phishing Campaign</h2>
                            <form onSubmit={handleSubmit} className="space-y-4">
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                                            Campaign Name *
                                        </label>
                                        <input
                                            type="text"
                                            name="name"
                                            value={formData.name}
                                            onChange={handleInputChange}
                                            className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                                            Template *
                                        </label>
                                        <select
                                            name="template"
                                            value={formData.template}
                                            onChange={handleInputChange}
                                            className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                                            required
                                        >
                                            <option value="">Select Template</option>
                                            {templates.map((t) => (
                                                <option key={t.id} value={t.id}>
                                                    {t.name}
                                                </option>
                                            ))}
                                        </select>
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                                            Start Date *
                                        </label>
                                        <input
                                            type="date"
                                            name="start_date"
                                            value={formData.start_date}
                                            onChange={handleInputChange}
                                            className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                                            End Date
                                        </label>
                                        <input
                                            type="date"
                                            name="end_date"
                                            value={formData.end_date}
                                            onChange={handleInputChange}
                                            className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                                            Status
                                        </label>
                                        <select
                                            name="status"
                                            value={formData.status}
                                            onChange={handleInputChange}
                                            className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                                        >
                                            <option value="draft">Draft</option>
                                            <option value="scheduled">Scheduled</option>
                                            <option value="running">Running</option>
                                        </select>
                                    </div>
                                </div>
                                <div className="flex gap-3">
                                    <button
                                        type="submit"
                                        className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium"
                                    >
                                        Create Campaign
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

                    {/* Campaigns List */}
                    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-x-auto">
                        <table className="w-full min-w-[600px]">
                            <thead className="bg-slate-50 dark:bg-slate-700">
                                <tr>
                                    <th className="px-4 py-3 text-left text-sm font-medium text-slate-600 dark:text-slate-300">Name</th>
                                    <th className="px-4 py-3 text-left text-sm font-medium text-slate-600 dark:text-slate-300">Template</th>
                                    <th className="px-4 py-3 text-left text-sm font-medium text-slate-600 dark:text-slate-300">Status</th>
                                    <th className="px-4 py-3 text-left text-sm font-medium text-slate-600 dark:text-slate-300">Start Date</th>
                                    <th className="px-4 py-3 text-right text-sm font-medium text-slate-600 dark:text-slate-300">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-200 dark:divide-slate-700">
                                {campaigns.map((campaign) => (
                                    <tr key={campaign.id} className="hover:bg-slate-50 dark:hover:bg-slate-700/50">
                                        <td className="px-4 py-3 text-sm text-slate-800 dark:text-slate-100">{campaign.name}</td>
                                        <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-300">
                                            {campaign.template?.name || "N/A"}
                                        </td>
                                        <td className="px-4 py-3">
                                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusColors[campaign.status] || "bg-gray-200"}`}>
                                                {campaign.status}
                                            </span>
                                        </td>
                                        <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-300">
                                            {campaign.start_date ? new Date(campaign.start_date).toLocaleDateString() : "N/A"}
                                        </td>
                                        <td className="px-4 py-3 text-right">
                                            <select
                                                value={campaign.status}
                                                onChange={(e) => handleStatusChange(campaign.id, e.target.value)}
                                                className="border border-slate-300 dark:border-slate-600 rounded-lg px-2 py-1 text-sm dark:bg-slate-700 dark:text-slate-100 mr-2"
                                            >
                                                <option value="draft">Draft</option>
                                                <option value="scheduled">Scheduled</option>
                                                <option value="running">Running</option>
                                                <option value="completed">Completed</option>
                                                <option value="cancelled">Cancelled</option>
                                            </select>
                                            <button
                                                onClick={() => handleDeleteCampaign(campaign.id, campaign.name)}
                                                className="text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 text-sm font-medium"
                                            >
                                                Delete
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                                {campaigns.length === 0 && (
                                    <tr>
                                        <td colSpan={5} className="px-4 py-8 text-center text-slate-500 dark:text-slate-400">
                                            No phishing campaigns found. Click "Create Campaign" to start one.
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}

            {/* ========== TEMPLATES TAB ========== */}
            {activeTab === "templates" && (
                <div>
                    <div className="flex justify-end mb-4">
                        <button
                            onClick={() => setShowTemplateForm(true)}
                            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium"
                        >
                            + Create Template
                        </button>
                    </div>

                    {/* Create Template Form */}
                    {showTemplateForm && !showEditTemplateForm && (
                        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 p-6 mb-6">
                            <h2 className="text-lg font-medium mb-4">Create New Phishing Template</h2>
                            <form onSubmit={handleTemplateSubmit} className="space-y-4">
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                                            Template Name *
                                        </label>
                                        <input
                                            type="text"
                                            name="name"
                                            value={templateFormData.name}
                                            onChange={handleTemplateInputChange}
                                            className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                                            Subject *
                                        </label>
                                        <input
                                            type="text"
                                            name="subject"
                                            value={templateFormData.subject}
                                            onChange={handleTemplateInputChange}
                                            className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                                            required
                                        />
                                    </div>
                                    <div className="col-span-2">
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                                            Email Body (HTML) *
                                        </label>
                                        <textarea
                                            name="body"
                                            value={templateFormData.body}
                                            onChange={handleTemplateInputChange}
                                            rows={4}
                                            className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                                            Sender Name *
                                        </label>
                                        <input
                                            type="text"
                                            name="sender_name"
                                            value={templateFormData.sender_name}
                                            onChange={handleTemplateInputChange}
                                            className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                                            Sender Email *
                                        </label>
                                        <input
                                            type="email"
                                            name="sender_email"
                                            value={templateFormData.sender_email}
                                            onChange={handleTemplateInputChange}
                                            className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="flex items-center gap-2 text-sm font-medium text-slate-700 dark:text-slate-300">
                                            <input
                                                type="checkbox"
                                                name="is_active"
                                                checked={templateFormData.is_active}
                                                onChange={(e) => setTemplateFormData({...templateFormData, is_active: e.target.checked})}
                                                className="h-4 w-4"
                                            />
                                            Active
                                        </label>
                                    </div>
                                </div>
                                <div className="flex gap-3">
                                    <button
                                        type="submit"
                                        className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium"
                                    >
                                        Create Template
                                    </button>
                                    <button
                                        type="button"
                                        onClick={resetTemplateForm}
                                        className="px-4 py-2 bg-slate-200 hover:bg-slate-300 dark:bg-slate-700 dark:hover:bg-slate-600 rounded-lg text-sm font-medium"
                                    >
                                        Cancel
                                    </button>
                                </div>
                            </form>
                        </div>
                    )}

                    {/* Edit Template Form */}
                    {showEditTemplateForm && editingTemplate && (
                        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 p-6 mb-6">
                            <h2 className="text-lg font-medium mb-4">Edit Template: {editingTemplate.name}</h2>
                            <form onSubmit={handleEditTemplateSubmit} className="space-y-4">
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                                            Template Name *
                                        </label>
                                        <input
                                            type="text"
                                            name="name"
                                            value={templateFormData.name}
                                            onChange={handleTemplateInputChange}
                                            className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                                            Subject *
                                        </label>
                                        <input
                                            type="text"
                                            name="subject"
                                            value={templateFormData.subject}
                                            onChange={handleTemplateInputChange}
                                            className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                                            required
                                        />
                                    </div>
                                    <div className="col-span-2">
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                                            Email Body (HTML) *
                                        </label>
                                        <textarea
                                            name="body"
                                            value={templateFormData.body}
                                            onChange={handleTemplateInputChange}
                                            rows={4}
                                            className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                                            Sender Name *
                                        </label>
                                        <input
                                            type="text"
                                            name="sender_name"
                                            value={templateFormData.sender_name}
                                            onChange={handleTemplateInputChange}
                                            className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                                            Sender Email *
                                        </label>
                                        <input
                                            type="email"
                                            name="sender_email"
                                            value={templateFormData.sender_email}
                                            onChange={handleTemplateInputChange}
                                            className="mt-1 w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 dark:bg-slate-700 dark:text-slate-100"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="flex items-center gap-2 text-sm font-medium text-slate-700 dark:text-slate-300">
                                            <input
                                                type="checkbox"
                                                name="is_active"
                                                checked={templateFormData.is_active}
                                                onChange={(e) => setTemplateFormData({...templateFormData, is_active: e.target.checked})}
                                                className="h-4 w-4"
                                            />
                                            Active
                                        </label>
                                    </div>
                                </div>
                                <div className="flex gap-3">
                                    <button
                                        type="submit"
                                        className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium"
                                    >
                                        Update Template
                                    </button>
                                    <button
                                        type="button"
                                        onClick={resetTemplateForm}
                                        className="px-4 py-2 bg-slate-200 hover:bg-slate-300 dark:bg-slate-700 dark:hover:bg-slate-600 rounded-lg text-sm font-medium"
                                    >
                                        Cancel
                                    </button>
                                </div>
                            </form>
                        </div>
                    )}

                    {/* Templates List */}
                    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-x-auto">
                        <table className="w-full min-w-[500px]">
                            <thead className="bg-slate-50 dark:bg-slate-700">
                                <tr>
                                    <th className="px-4 py-3 text-left text-sm font-medium text-slate-600 dark:text-slate-300">Name</th>
                                    <th className="px-4 py-3 text-left text-sm font-medium text-slate-600 dark:text-slate-300">Subject</th>
                                    <th className="px-4 py-3 text-left text-sm font-medium text-slate-600 dark:text-slate-300">Status</th>
                                    <th className="px-4 py-3 text-right text-sm font-medium text-slate-600 dark:text-slate-300">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-200 dark:divide-slate-700">
                                {templates.map((template) => (
                                    <tr key={template.id} className="hover:bg-slate-50 dark:hover:bg-slate-700/50">
                                        <td className="px-4 py-3 text-sm text-slate-800 dark:text-slate-100">{template.name}</td>
                                        <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-300">{template.subject}</td>
                                        <td className="px-4 py-3">
                                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${template.is_active ? 'bg-green-200 text-green-700' : 'bg-red-200 text-red-700'}`}>
                                                {template.is_active ? 'Active' : 'Inactive'}
                                            </span>
                                        </td>
                                        <td className="px-4 py-3 text-right">
                                            <button
                                                onClick={() => editTemplate(template)}
                                                className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 text-sm font-medium mr-3"
                                            >
                                                Edit
                                            </button>
                                            <button
                                                onClick={() => handleDeleteTemplate(template.id, template.name)}
                                                className="text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 text-sm font-medium"
                                            >
                                                Delete
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                                {templates.length === 0 && (
                                    <tr>
                                        <td colSpan={4} className="px-4 py-8 text-center text-slate-500 dark:text-slate-400">
                                            No phishing templates found. Click "Create Template" to start one.
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}

            {/* ========== RESULTS TAB ========== */}
            {activeTab === "results" && (
                <div>
                    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-x-auto">
                        <table className="w-full min-w-[900px]">
                            <thead className="bg-slate-50 dark:bg-slate-700">
                                <tr>
                                    <th className="px-4 py-3 text-left text-sm font-medium text-slate-600 dark:text-slate-300">Employee</th>
                                    <th className="px-4 py-3 text-left text-sm font-medium text-slate-600 dark:text-slate-300">Campaign</th>
                                    <th className="px-4 py-3 text-left text-sm font-medium text-slate-600 dark:text-slate-300">Status</th>
                                    <th className="px-4 py-3 text-left text-sm font-medium text-slate-600 dark:text-slate-300">Opened At</th>
                                    <th className="px-4 py-3 text-left text-sm font-medium text-slate-600 dark:text-slate-300">Clicked At</th>
                                    <th className="px-4 py-3 text-left text-sm font-medium text-slate-600 dark:text-slate-300">Submitted At</th>
                                    <th className="px-4 py-3 text-left text-sm font-medium text-slate-600 dark:text-slate-300">Reported At</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-200 dark:divide-slate-700">
                                {results.map((result) => (
                                    <tr key={result.id} className="hover:bg-slate-50 dark:hover:bg-slate-700/50">
                                        <td className="px-4 py-3 text-sm text-slate-800 dark:text-slate-100">{result.employee_email}</td>
                                        <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-300">{result.campaign_name}</td>
                                        <td className="px-4 py-3">
                                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${resultStatusColors[result.status] || "bg-gray-200"}`}>
                                                {result.status}
                                            </span>
                                        </td>
                                        <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-300">
                                            {result.opened_at ? new Date(result.opened_at).toLocaleString() : "-"}
                                        </td>
                                        <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-300">
                                            {result.clicked_at ? new Date(result.clicked_at).toLocaleString() : "-"}
                                        </td>
                                        <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-300">
                                            {result.submitted_at ? new Date(result.submitted_at).toLocaleString() : "-"}
                                        </td>
                                        <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-300">
                                            {result.reported_at ? new Date(result.reported_at).toLocaleString() : "-"}
                                        </td>
                                    </tr>
                                ))}
                                {results.length === 0 && (
                                    <tr>
                                        <td colSpan={7} className="px-4 py-8 text-center text-slate-500 dark:text-slate-400">
                                            No phishing results found.
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
}