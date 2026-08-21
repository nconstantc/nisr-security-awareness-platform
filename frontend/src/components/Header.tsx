import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useTranslation } from "../context/LanguageContext";
import { ProfileMenu } from "./ProfileMenu";
import { ShieldIcon } from "./icons";

export function Header({ centerSlot }: { centerSlot?: React.ReactNode }) {
  const { user } = useAuth();
  const { t } = useTranslation();

  return (
    <header className="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700">
      <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between gap-4">
        <Link to="/" className="flex items-center gap-2 font-semibold text-slate-800 dark:text-slate-100 shrink-0">
          <img src="/brand/nisr-logo.png" alt="NISR Logo" className="h-8 w-auto" />
          {t("common.appName")}
        </Link>
        
        <div className="flex items-center gap-4">
          {/* Report Suspicious Email Link - using a tag to go to Django template */}
          {user && (
            <a
              href="/phishing/report/"
              className="text-sm text-slate-600 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 font-medium"
            >
              📧 Report Suspicious Email
            </a>
          )}
          
          {centerSlot && <div className="flex-1 flex justify-end min-w-0">{centerSlot}</div>}
          {user && (
            <ProfileMenu
              extraLinks={user.is_staff ? [{ to: "/console", label: t("common.adminConsole"), icon: <ShieldIcon /> }] : []}
            />
          )}
        </div>
      </div>
    </header>
  );
}