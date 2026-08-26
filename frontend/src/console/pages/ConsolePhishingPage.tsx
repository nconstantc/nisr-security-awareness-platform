import { useEffect, useMemo, useState } from "react";
import type { FormEvent } from "react";
import { api } from "../../api/client";

interface PhishingCampaign {
    id: number;
    name: string;
    template: number;
    template_name: string;
    template_subject: string;
    status: string;
    start_date: string;
    end_date: string | null;
    created_at: string;
}

interface PhishingTemplate {
    id: number;
    name: string;
    subject: string;
    body: string;
    sender_name: string;
    sender_email: string;
    landing_page_url?: string | null;
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

interface PhishingReport {
    id: number;
    employee: number;
    employee_name: string;
    employee_email: string;
    sender_email: string;
    subject: string;
    body_preview: string;
    reason: string;
    status: "pending" | "investigating" | "confirmed_phishing" | "false_positive" | "resolved";
    reported_at: string;
    reviewed_at: string | null;
    reviewed_by: number | null;
    reviewed_by_email: string | null;
    notes: string;
    is_phishing: boolean | null;
}

interface SendPhishingResponse {
    success: boolean;
    message: string;
    output?: string;
    error?: string;
}

type PhishingTab = "campaigns" | "templates" | "results" | "reports";

const reportStatusLabels: Record<PhishingReport["status"], string> = {
    pending: "Pending Review",
    investigating: "Under Investigation",
    confirmed_phishing: "Confirmed Phishing",
    false_positive: "False Positive",
    resolved: "Resolved",
};

const reportStatusColors: Record<PhishingReport["status"], string> = {
    pending: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300",
    investigating: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300",
    confirmed_phishing: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300",
    false_positive: "bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-300",
    resolved: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300",
};

export function ConsolePhishingPage() {
    const [activeTab, setActiveTab] = useState<PhishingTab>("campaigns");
    const [campaigns, setCampaigns] = useState<PhishingCampaign[]>([]);
    const [templates, setTemplates] = useState<PhishingTemplate[]>([]);
    const [results, setResults] = useState<PhishingResult[]>([]);
    const [reports, setReports] = useState<PhishingReport[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [message, setMessage] = useState<string | null>(null);
    const [sending, setSending] = useState(false);
    const [showCampaignForm, setShowCampaignForm] = useState(false);
    const [showTemplateForm, setShowTemplateForm] = useState(false);
    const [editingTemplateId, setEditingTemplateId] = useState<number | null>(null);
    const [selectedReport, setSelectedReport] = useState<PhishingReport | null>(null);
    const [reportSearch, setReportSearch] = useState("");
    const [reportStatusFilter, setReportStatusFilter] = useState("all");

    const [campaignForm, setCampaignForm] = useState({
        name: "",
        template: "",
        status: "draft",
        start_date: "",
        end_date: "",
    });

    const [templateForm, setTemplateForm] = useState({
        name: "",
        subject: "",
        body: "",
        sender_name: "",
        sender_email: "",
        landing_page_url: "",
        is_active: true,
    });

    const loadData = async () => {
        setLoading(true);
        setError(null);
        try {
            const [campaignsRes, templatesRes, resultsRes, reportsRes] = await Promise.all([
                api.get<PhishingCampaign[]>("/api/console/phishing/campaigns/"),
                api.get<PhishingTemplate[]>("/api/console/phishing/templates/"),
                api.get<PhishingResult[]>("/api/console/phishing/results/"),
                api.get<PhishingReport[]>("/api/console/phishing/reports/"),
            ]);
            setCampaigns(campaignsRes);
            setTemplates(templatesRes);
            setResults(resultsRes);
            setReports(reportsRes);
        } catch (err) {
            console.error(err);
            setError("Failed to load phishing management data. Please refresh and try again.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { void loadData(); }, []);

    const filteredReports = useMemo(() => {
        const query = reportSearch.trim().toLowerCase();
        return reports.filter((report) => {
            const matchesStatus = reportStatusFilter === "all" || report.status === reportStatusFilter;
            const matchesQuery = !query || [
                report.employee_name,
                report.employee_email,
                report.sender_email,
                report.subject,
                report.reason,
            ].some((value) => value?.toLowerCase().includes(query));
            return matchesStatus && matchesQuery;
        });
    }, [reports, reportSearch, reportStatusFilter]);

    const resetCampaignForm = () => {
        setCampaignForm({ name: "", template: "", status: "draft", start_date: "", end_date: "" });
        setShowCampaignForm(false);
    };

    const resetTemplateForm = () => {
        setTemplateForm({ name: "", subject: "", body: "", sender_name: "", sender_email: "", landing_page_url: "", is_active: true });
        setShowTemplateForm(false);
        setEditingTemplateId(null);
    };

    const handleCampaignSubmit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setError(null);
        try {
            await api.post("/api/console/phishing/campaigns/", {
                ...campaignForm,
                template: Number(campaignForm.template),
                end_date: campaignForm.end_date || null,
            });
            resetCampaignForm();
            await loadData();
            setMessage("Phishing campaign created successfully.");
        } catch (err) {
            console.error(err);
            setError("Failed to create phishing campaign.");
        }
    };

    const handleTemplateSubmit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setError(null);
        try {
            const payload = { ...templateForm, landing_page_url: templateForm.landing_page_url || null };
            if (editingTemplateId) {
                await api.patch(`/api/console/phishing/templates/${editingTemplateId}/`, payload);
                setMessage("Phishing template updated successfully.");
            } else {
                await api.post("/api/console/phishing/templates/", payload);
                setMessage("Phishing template created successfully.");
            }
            resetTemplateForm();
            await loadData();
        } catch (err) {
            console.error(err);
            setError(editingTemplateId ? "Failed to update phishing template." : "Failed to create phishing template.");
        }
    };

    const editTemplate = (template: PhishingTemplate) => {
        setEditingTemplateId(template.id);
        setTemplateForm({
            name: template.name,
            subject: template.subject,
            body: template.body || "",
            sender_name: template.sender_name || "",
            sender_email: template.sender_email || "",
            landing_page_url: template.landing_page_url || "",
            is_active: template.is_active,
        });
        setShowTemplateForm(true);
    };

    const deleteCampaign = async (campaign: PhishingCampaign) => {
        if (!confirm(`Delete campaign "${campaign.name}"?`)) return;
        try {
            await api.delete(`/api/console/phishing/campaigns/${campaign.id}/`);
            await loadData();
        } catch (err) {
            console.error(err);
            setError("Failed to delete campaign.");
        }
    };

    const deleteTemplate = async (template: PhishingTemplate) => {
        if (!confirm(`Delete template "${template.name}"?`)) return;
        try {
            await api.delete(`/api/console/phishing/templates/${template.id}/`);
            await loadData();
        } catch (err) {
            console.error(err);
            setError("Failed to delete template.");
        }
    };

    const updateCampaignStatus = async (id: number, status: string) => {
        try {
            await api.patch(`/api/console/phishing/campaigns/${id}/`, { status });
            await loadData();
        } catch (err) {
            console.error(err);
            setError("Failed to update campaign status.");
        }
    };

    const sendPhishing = async () => {
        if (!confirm("Are you sure you want to send phishing emails to all assigned employees?")) return;
        setSending(true);
        setError(null);
        try {
            const response = await api.post<SendPhishingResponse>("/api/console/phishing/send/");
            if (response.success) setMessage(response.message || "Phishing emails sent successfully.");
            else setError(response.error || "Failed to send phishing emails.");
            await loadData();
        } catch (err) {
            console.error(err);
            setError("Failed to send phishing emails.");
        } finally {
            setSending(false);
        }
    };

    const deleteReport = async (report: PhishingReport) => {
        if (!confirm(`Delete phishing report #${report.id} from ${report.employee_email}?`)) return;
        try {
            await api.delete(`/api/console/phishing/reports/${report.id}/`);
            await loadData();
            setMessage("Phishing report deleted successfully.");
        } catch (err) {
            console.error(err);
            setError("Failed to delete phishing report.");
        }
    };

    const updateReport = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (!selectedReport) return;
        const form = new FormData(event.currentTarget);
        const status = String(form.get("status"));
        const notes = String(form.get("notes") || "");
        const isPhishingValue = String(form.get("is_phishing"));
        const isPhishing = isPhishingValue === "true" ? true : isPhishingValue === "false" ? false : null;
        try {
            await api.patch(`/api/console/phishing/reports/${selectedReport.id}/`, {
                status,
                notes,
                is_phishing: isPhishing,
            });
            setSelectedReport(null);
            await loadData();
            setMessage("Phishing report review saved successfully.");
        } catch (err) {
            console.error(err);
            setError("Failed to save phishing report review.");
        }
    };

    const campaignStatusColors: Record<string, string> = {
        draft: "bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-300",
        scheduled: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300",
        running: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300",
        completed: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300",
        cancelled: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300",
    };

    if (loading) return <div className="p-4 text-slate-500">Loading phishing data...</div>;

    return (
        <div className="p-4">
            <div className="mb-6">
                <h1 className="text-2xl font-semibold text-slate-800 dark:text-slate-100">Phishing Management</h1>
                <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                    Manage campaigns, templates, simulation results, and employee phishing reports from the Console.
                </p>
            </div>

            {error && <div className="mb-4 p-3 rounded-lg border border-red-400 bg-red-100 text-red-700 dark:bg-red-900/30 dark:border-red-700 dark:text-red-300">{error}</div>}
            {message && <div className="mb-4 p-3 rounded-lg border border-green-400 bg-green-100 text-green-700 dark:bg-green-900/30 dark:border-green-700 dark:text-green-300">{message}</div>}

            <div className="flex flex-wrap border-b border-slate-200 dark:border-slate-700 mb-6">
                {(["campaigns", "templates", "results", "reports"] as PhishingTab[]).map((tab) => (
                    <button key={tab} onClick={() => setActiveTab(tab)} className={`px-4 py-2 text-sm font-medium border-b-2 transition ${activeTab === tab ? "border-blue-600 text-blue-600 dark:text-blue-400" : "border-transparent text-slate-500 hover:text-slate-700 dark:text-slate-400"}`}>
                        {tab === "campaigns" && `Campaigns (${campaigns.length})`}
                        {tab === "templates" && `Templates (${templates.length})`}
                        {tab === "results" && `Results (${results.length})`}
                        {tab === "reports" && `Reports (${reports.length})`}
                    </button>
                ))}
            </div>

            {activeTab === "campaigns" && (
                <section>
                    <div className="flex flex-wrap justify-between gap-3 items-center mb-4">
                        <div><h2 className="text-lg font-medium text-slate-800 dark:text-slate-100">Campaigns</h2><p className="text-sm text-slate-500">Create, edit status, and delete campaigns.</p></div>
                        <div className="flex gap-2">
                            <button onClick={sendPhishing} disabled={sending} className="px-4 py-2 rounded-lg bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white text-sm font-medium">{sending ? "Sending..." : "📧 Send Phishing Emails"}</button>
                            <button onClick={() => setShowCampaignForm(true)} className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium">+ Create Campaign</button>
                        </div>
                    </div>

                    {showCampaignForm && (
                        <form onSubmit={handleCampaignSubmit} className="mb-6 p-6 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 space-y-4">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <label className="text-sm">Name<input required value={campaignForm.name} onChange={(e) => setCampaignForm({ ...campaignForm, name: e.target.value })} className="mt-1 w-full rounded-lg border p-2 dark:bg-slate-900 dark:border-slate-600" /></label>
                                <label className="text-sm">Template<select required value={campaignForm.template} onChange={(e) => setCampaignForm({ ...campaignForm, template: e.target.value })} className="mt-1 w-full rounded-lg border p-2 dark:bg-slate-900 dark:border-slate-600"><option value="">Select template</option>{templates.filter(t => t.is_active).map(t => <option key={t.id} value={t.id}>{t.name} — {t.subject}</option>)}</select></label>
                                <label className="text-sm">Start date<input required type="datetime-local" value={campaignForm.start_date} onChange={(e) => setCampaignForm({ ...campaignForm, start_date: e.target.value })} className="mt-1 w-full rounded-lg border p-2 dark:bg-slate-900 dark:border-slate-600" /></label>
                                <label className="text-sm">End date<input type="datetime-local" value={campaignForm.end_date} onChange={(e) => setCampaignForm({ ...campaignForm, end_date: e.target.value })} className="mt-1 w-full rounded-lg border p-2 dark:bg-slate-900 dark:border-slate-600" /></label>
                            </div>
                            <div className="flex gap-2"><button className="px-4 py-2 bg-blue-600 text-white rounded-lg">Create</button><button type="button" onClick={resetCampaignForm} className="px-4 py-2 border rounded-lg">Cancel</button></div>
                        </form>
                    )}

                    <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-x-auto">
                        <table className="w-full min-w-[900px]"><thead className="bg-slate-50 dark:bg-slate-700"><tr>{["Name", "Template", "Status", "Start", "End", "Actions"].map(h => <th key={h} className="px-4 py-3 text-left text-sm font-medium">{h}</th>)}</tr></thead>
                            <tbody className="divide-y divide-slate-200 dark:divide-slate-700">{campaigns.map(c => <tr key={c.id}>
                                <td className="px-4 py-3 text-sm">{c.name}</td><td className="px-4 py-3 text-sm">{c.template_name || `Template #${c.template}`}</td>
                                <td className="px-4 py-3"><select value={c.status} onChange={e => void updateCampaignStatus(c.id, e.target.value)} className={`rounded-full px-2 py-1 text-xs font-medium border-0 ${campaignStatusColors[c.status] || ""}`}><option value="draft">Draft</option><option value="scheduled">Scheduled</option><option value="running">Running</option><option value="completed">Completed</option><option value="cancelled">Cancelled</option></select></td>
                                <td className="px-4 py-3 text-sm">{new Date(c.start_date).toLocaleString()}</td><td className="px-4 py-3 text-sm">{c.end_date ? new Date(c.end_date).toLocaleString() : "-"}</td>
                                <td className="px-4 py-3"><button onClick={() => void deleteCampaign(c)} className="text-red-600 text-sm font-medium">Delete</button></td>
                            </tr>)}{campaigns.length === 0 && <tr><td colSpan={6} className="p-8 text-center text-slate-500">No campaigns found.</td></tr>}</tbody>
                        </table>
                    </div>
                </section>
            )}

            {activeTab === "templates" && (
                <section>
                    <div className="flex justify-between items-center mb-4"><div><h2 className="text-lg font-medium">Templates</h2><p className="text-sm text-slate-500">Manage the complete phishing email template.</p></div><button onClick={() => { resetTemplateForm(); setShowTemplateForm(true); }} className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm">+ Create Template</button></div>
                    {showTemplateForm && <form onSubmit={handleTemplateSubmit} className="mb-6 p-6 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <label className="text-sm">Name<input required value={templateForm.name} onChange={e => setTemplateForm({ ...templateForm, name: e.target.value })} className="mt-1 w-full rounded-lg border p-2 dark:bg-slate-900 dark:border-slate-600" /></label>
                            <label className="text-sm">Subject<input required value={templateForm.subject} onChange={e => setTemplateForm({ ...templateForm, subject: e.target.value })} className="mt-1 w-full rounded-lg border p-2 dark:bg-slate-900 dark:border-slate-600" /></label>
                            <label className="text-sm">Sender name<input required value={templateForm.sender_name} onChange={e => setTemplateForm({ ...templateForm, sender_name: e.target.value })} className="mt-1 w-full rounded-lg border p-2 dark:bg-slate-900 dark:border-slate-600" /></label>
                            <label className="text-sm">Sender email<input required type="email" value={templateForm.sender_email} onChange={e => setTemplateForm({ ...templateForm, sender_email: e.target.value })} className="mt-1 w-full rounded-lg border p-2 dark:bg-slate-900 dark:border-slate-600" /></label>
                            <label className="text-sm md:col-span-2">Landing page URL<input value={templateForm.landing_page_url} onChange={e => setTemplateForm({ ...templateForm, landing_page_url: e.target.value })} className="mt-1 w-full rounded-lg border p-2 dark:bg-slate-900 dark:border-slate-600" /></label>
                            <label className="text-sm md:col-span-2">Email body<textarea required rows={10} value={templateForm.body} onChange={e => setTemplateForm({ ...templateForm, body: e.target.value })} className="mt-1 w-full rounded-lg border p-2 dark:bg-slate-900 dark:border-slate-600" /></label>
                            <label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={templateForm.is_active} onChange={e => setTemplateForm({ ...templateForm, is_active: e.target.checked })} /> Active</label>
                        </div>
                        <div className="flex gap-2"><button className="px-4 py-2 bg-blue-600 text-white rounded-lg">{editingTemplateId ? "Save Changes" : "Create Template"}</button><button type="button" onClick={resetTemplateForm} className="px-4 py-2 border rounded-lg">Cancel</button></div>
                    </form>}
                    <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-x-auto"><table className="w-full min-w-[900px]"><thead className="bg-slate-50 dark:bg-slate-700"><tr>{["Name", "Subject", "Sender", "Active", "Actions"].map(h => <th key={h} className="px-4 py-3 text-left text-sm font-medium">{h}</th>)}</tr></thead><tbody className="divide-y divide-slate-200 dark:divide-slate-700">{templates.map(t => <tr key={t.id}><td className="px-4 py-3 text-sm">{t.name}</td><td className="px-4 py-3 text-sm">{t.subject}</td><td className="px-4 py-3 text-sm">{t.sender_name} &lt;{t.sender_email}&gt;</td><td className="px-4 py-3 text-sm">{t.is_active ? "Active" : "Inactive"}</td><td className="px-4 py-3"><button onClick={() => editTemplate(t)} className="text-blue-600 text-sm mr-3">Edit</button><button onClick={() => void deleteTemplate(t)} className="text-red-600 text-sm">Delete</button></td></tr>)}{templates.length === 0 && <tr><td colSpan={5} className="p-8 text-center text-slate-500">No templates found.</td></tr>}</tbody></table></div>
                </section>
            )}

            {activeTab === "results" && <section><div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-x-auto"><table className="w-full min-w-[1000px]"><thead className="bg-slate-50 dark:bg-slate-700"><tr>{["Employee", "Campaign", "Status", "Opened", "Clicked", "Submitted", "Reported"].map(h => <th key={h} className="px-4 py-3 text-left text-sm font-medium">{h}</th>)}</tr></thead><tbody className="divide-y divide-slate-200 dark:divide-slate-700">{results.map(r => <tr key={r.id}><td className="px-4 py-3 text-sm">{r.employee_email}</td><td className="px-4 py-3 text-sm">{r.campaign_name}</td><td className="px-4 py-3 text-sm">{r.status}</td><td className="px-4 py-3 text-sm">{r.opened_at ? new Date(r.opened_at).toLocaleString() : "-"}</td><td className="px-4 py-3 text-sm">{r.clicked_at ? new Date(r.clicked_at).toLocaleString() : "-"}</td><td className="px-4 py-3 text-sm">{r.submitted_at ? new Date(r.submitted_at).toLocaleString() : "-"}</td><td className="px-4 py-3 text-sm">{r.reported_at ? new Date(r.reported_at).toLocaleString() : "-"}</td></tr>)}{results.length === 0 && <tr><td colSpan={7} className="p-8 text-center text-slate-500">No phishing results found.</td></tr>}</tbody></table></div></section>}

            {activeTab === "reports" && <section>
                <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-3 mb-4"><div><h2 className="text-lg font-medium">Employee Reports</h2><p className="text-sm text-slate-500">Review and resolve suspicious-email reports submitted by employees.</p></div><div className="flex flex-wrap gap-2"><input value={reportSearch} onChange={e => setReportSearch(e.target.value)} placeholder="Search employee, sender, subject..." className="rounded-lg border p-2 text-sm dark:bg-slate-900 dark:border-slate-600" /><select value={reportStatusFilter} onChange={e => setReportStatusFilter(e.target.value)} className="rounded-lg border p-2 text-sm dark:bg-slate-900 dark:border-slate-600"><option value="all">All statuses</option>{Object.entries(reportStatusLabels).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></div></div>
                <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-x-auto"><table className="w-full min-w-[1100px]"><thead className="bg-slate-50 dark:bg-slate-700"><tr>{["Employee", "Sender", "Subject", "Reported", "Status", "Decision", "Actions"].map(h => <th key={h} className="px-4 py-3 text-left text-sm font-medium">{h}</th>)}</tr></thead><tbody className="divide-y divide-slate-200 dark:divide-slate-700">{filteredReports.map(r => <tr key={r.id} className="hover:bg-slate-50 dark:hover:bg-slate-700/40"><td className="px-4 py-3 text-sm"><div className="font-medium">{r.employee_name}</div><div className="text-xs text-slate-500">{r.employee_email}</div></td><td className="px-4 py-3 text-sm">{r.sender_email}</td><td className="px-4 py-3 text-sm max-w-xs truncate" title={r.subject}>{r.subject}</td><td className="px-4 py-3 text-sm">{new Date(r.reported_at).toLocaleString()}</td><td className="px-4 py-3"><span className={`px-2 py-1 rounded-full text-xs font-medium ${reportStatusColors[r.status]}`}>{reportStatusLabels[r.status]}</span></td><td className="px-4 py-3 text-sm">{r.is_phishing === true ? "Phishing" : r.is_phishing === false ? "False positive" : "Not decided"}</td><td className="px-4 py-3 whitespace-nowrap"><button onClick={() => setSelectedReport(r)} className="px-3 py-1.5 rounded-lg bg-blue-600 text-white text-sm mr-2">Review</button><button onClick={() => void deleteReport(r)} className="text-red-600 text-sm font-medium">Delete</button></td></tr>)}{filteredReports.length === 0 && <tr><td colSpan={7} className="p-8 text-center text-slate-500">No phishing reports match your filters.</td></tr>}</tbody></table></div>
            </section>}

            {selectedReport && <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4"><form onSubmit={updateReport} className="w-full max-w-3xl max-h-[90vh] overflow-y-auto bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-6"><div className="flex justify-between items-start mb-5"><div><h2 className="text-xl font-semibold">Review Phishing Report #{selectedReport.id}</h2><p className="text-sm text-slate-500 mt-1">Reported by {selectedReport.employee_name} ({selectedReport.employee_email})</p></div><button type="button" onClick={() => setSelectedReport(null)} className="text-slate-500 text-xl">×</button></div><div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-5"><div><div className="text-xs text-slate-500">Sender</div><div className="font-medium">{selectedReport.sender_email}</div></div><div><div className="text-xs text-slate-500">Reported</div><div>{new Date(selectedReport.reported_at).toLocaleString()}</div></div><div className="md:col-span-2"><div className="text-xs text-slate-500">Subject</div><div className="font-medium">{selectedReport.subject}</div></div></div><div className="space-y-4"><div><div className="text-xs font-medium text-slate-500 mb-1">Email body preview</div><div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900 whitespace-pre-wrap text-sm">{selectedReport.body_preview || "No preview provided."}</div></div><div><div className="text-xs font-medium text-slate-500 mb-1">Employee's reason</div><div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900 whitespace-pre-wrap text-sm">{selectedReport.reason}</div></div><div className="grid grid-cols-1 md:grid-cols-2 gap-4"><label className="text-sm">Review status<select name="status" defaultValue={selectedReport.status} className="mt-1 w-full rounded-lg border p-2 dark:bg-slate-900 dark:border-slate-600">{Object.entries(reportStatusLabels).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label><label className="text-sm">Decision<select name="is_phishing" defaultValue={selectedReport.is_phishing === null ? "null" : String(selectedReport.is_phishing)} className="mt-1 w-full rounded-lg border p-2 dark:bg-slate-900 dark:border-slate-600"><option value="null">Not decided</option><option value="true">Confirmed phishing</option><option value="false">False positive</option></select></label></div><label className="text-sm">Admin notes<textarea name="notes" defaultValue={selectedReport.notes} rows={5} className="mt-1 w-full rounded-lg border p-2 dark:bg-slate-900 dark:border-slate-600" placeholder="Add investigation or resolution notes..." /></label></div><div className="flex justify-end gap-2 mt-6"><button type="button" onClick={() => setSelectedReport(null)} className="px-4 py-2 border rounded-lg">Cancel</button><button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg">Save Review</button></div></form></div>}
        </div>
    );
}
