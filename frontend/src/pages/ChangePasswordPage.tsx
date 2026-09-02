import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { api, ApiError } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { useTranslation } from "../context/LanguageContext";
import type { User } from "../api/types";

export function ChangePasswordPage() {
  const { setUser } = useAuth();
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const [errors, setErrors] = useState<string[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [showPassword1, setShowPassword1] = useState(false);
  const [showPassword2, setShowPassword2] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setErrors([]);
    
    if (password1.length < 8) {
      setErrors([t("changePassword.passwordMinLength") || "Password must be at least 8 characters"]);
      return;
    }
    
    if (password1 !== password2) {
      setErrors([t("changePassword.passwordsMismatch") || "Passwords do not match"]);
      return;
    }
    
    setSubmitting(true);
    try {
      const user = await api.post<User>("/api/auth/change-password/", { new_password: password1 });
      setUser(user);
      navigate("/");
    } catch (err) {
      if (err instanceof ApiError && Array.isArray(err.detail)) {
        setErrors(err.detail as string[]);
      } else {
        setErrors([t("changePassword.genericError") || "Failed to change password"]);
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100 dark:bg-slate-900">
      <form onSubmit={handleSubmit} className="bg-white dark:bg-slate-800 shadow-md rounded-xl p-8 w-full max-w-sm space-y-4">
        <h1 className="text-xl font-semibold text-slate-800 dark:text-slate-100">
          {t("changePassword.title") || "Change Password"}
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          {t("changePassword.firstLoginNotice") || "This is your first login - you need to set a permanent password."}
        </p>
        
        <div>
          <label className="block text-sm text-slate-600 dark:text-slate-300 mb-1">
            {t("changePassword.newPasswordLabel") || "New Password"}
          </label>
          <div className="relative">
            <input
              type={showPassword1 ? "text" : "password"}
              required
              value={password1}
              onChange={(e) => setPassword1(e.target.value)}
              className="w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 pr-10 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-slate-700 dark:text-slate-100"
              placeholder={t("changePassword.enterNewPassword") || "Enter new password"}
              minLength={8}
            />
            <button
              type="button"
              onClick={() => setShowPassword1(!showPassword1)}
              className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
              aria-label={showPassword1 ? "Hide password" : "Show password"}
            >
              {showPassword1 ? (
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
            {t("changePassword.passwordHint") || "Password must be at least 8 characters"}
          </p>
        </div>
        
        <div>
          <label className="block text-sm text-slate-600 dark:text-slate-300 mb-1">
            {t("changePassword.repeatPasswordLabel") || "Repeat Password"}
          </label>
          <div className="relative">
            <input
              type={showPassword2 ? "text" : "password"}
              required
              value={password2}
              onChange={(e) => setPassword2(e.target.value)}
              className="w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2 pr-10 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-slate-700 dark:text-slate-100"
              placeholder={t("changePassword.repeatNewPassword") || "Repeat new password"}
            />
            <button
              type="button"
              onClick={() => setShowPassword2(!showPassword2)}
              className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
              aria-label={showPassword2 ? "Hide password" : "Show password"}
            >
              {showPassword2 ? (
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
        </div>
        
        {errors.length > 0 && (
          <ul className="text-sm text-red-600 dark:text-red-400 list-disc list-inside">
            {errors.map((e, i) => (
              <li key={i}>{e}</li>
            ))}
          </ul>
        )}
        
        <button
          type="submit"
          disabled={submitting}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-60 text-white rounded-lg py-2 font-medium transition-colors"
        >
          {submitting ? t("changePassword.saving") || "Saving..." : t("changePassword.submit") || "Save Password"}
        </button>
      </form>
    </div>
  );
}