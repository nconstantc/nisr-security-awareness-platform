// frontend/src/components/AppLayout.tsx

import { AppFooter } from './AppFooter';

interface AppLayoutProps {
    children: React.ReactNode;
}

export function AppLayout({ children }: AppLayoutProps) {
    return (
        <div className="min-h-screen flex flex-col">
            <div className="flex-1">{children}</div>
            <AppFooter />
        </div>
    );
}