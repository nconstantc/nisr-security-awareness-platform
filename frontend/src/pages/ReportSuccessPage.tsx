import { Link } from "react-router-dom";
import { Header } from "../components/Header";

export function ReportSuccessPage() {
  return (
    <div className="min-h-screen bg-slate-100 dark:bg-slate-900">
      <Header />
      <div className="flex items-center justify-center min-h-[80vh] px-4">
        <div className="max-w-md w-full bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 p-8 text-center">
          <div className="text-6xl mb-4">✅</div>
          <h1 className="text-2xl font-semibold text-slate-800 dark:text-slate-100 mb-2">
            Report Submitted!
          </h1>
          <p className="text-slate-600 dark:text-slate-300 mb-4">
            Thank you for reporting this suspicious email.
          </p>
          <p className="text-slate-500 dark:text-slate-400 text-sm mb-6">
            Our security team will review it and take appropriate action.
          </p>
          <Link
            to="/"
            className="inline-block px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium"
          >
            Return to Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
}