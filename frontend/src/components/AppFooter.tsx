// frontend/src/components/AppFooter.tsx

export function AppFooter() {
    const currentYear = new Date().getFullYear();
    
    return (
        <footer className="bg-white dark:bg-slate-800 border-t border-slate-200 dark:border-slate-700">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="py-4 md:py-6">
                    <div className="flex flex-col md:flex-row justify-between items-center space-y-3 md:space-y-0">
                        {/* Left: Logo + Copyright & Organization */}
                        <div className="flex items-center space-x-3">
                            {/* NISR Logo */}
                            <img 
                                src="/brand/nisr-logo.png" 
                                alt="NISR Logo" 
                                className="h-8 w-auto"
                            />
                            <div className="h-8 w-px bg-slate-300 dark:bg-slate-600 hidden sm:block"></div>
                            <div className="text-center sm:text-left">
                                <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400">
                                    Copyright© {currentYear} National Institute of Statistics Rwanda (NISR)
                                </p>
                                <p className="text-xs text-slate-400 dark:text-slate-500 mt-0.5">
                                    All Rights Reserved
                                </p>
                            </div>
                        </div>
                        
                        {/* Center: Quick Links */}
                        <div className="flex flex-wrap justify-center gap-x-4 gap-y-1">
                            <a 
                                href="/privacy" 
                                className="text-xs text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-300 transition-colors"
                            >
                                Privacy Policy
                            </a>
                            <span className="text-slate-300 dark:text-slate-600">|</span>
                            <a 
                                href="/terms" 
                                className="text-xs text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-300 transition-colors"
                            >
                                Terms of Service
                            </a>
                            <span className="text-slate-300 dark:text-slate-600">|</span>
                            <a 
                                href="/contact" 
                                className="text-xs text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-300 transition-colors"
                            >
                                Contact Us
                            </a>
                            <span className="text-slate-300 dark:text-slate-600">|</span>
                            <a 
                                href="/support" 
                                className="text-xs text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-300 transition-colors"
                            >
                                Help Desk
                            </a>
                        </div>
                        
                        {/* Right: Version */}
                        <div className="text-center md:text-right">
                            <p className="text-xs text-slate-400 dark:text-slate-500">
                                Security Awareness Platform
                            </p>
                            <p className="text-xs text-slate-400 dark:text-slate-500 mt-0.5">
                                Version 1.0.0
                            </p>
                        </div>
                    </div>
                    
                    {/* Bottom: Additional Info */}
                    <div className="mt-3 pt-3 border-t border-slate-200 dark:border-slate-700">
                        <p className="text-center text-[10px] text-slate-400 dark:text-slate-500">
                            This system is for authorized use only. All activities are monitored and recorded.
                        </p>
                    </div>
                </div>
            </div>
        </footer>
    );
}