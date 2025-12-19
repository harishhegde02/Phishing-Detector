import React, { useEffect, useState } from 'react';
import { ShieldCheck, ShieldAlert, Activity } from 'lucide-react';
import { cn } from '@/lib/utils';

export function DashboardHeader({ compact = false }: { compact?: boolean }) {
  const [status, setStatus] = useState<'active' | 'disconnected'>('active');

  // Listen for connection status (mocked for now)
  useEffect(() => {
    // Check if background script is reachable
    if (chrome?.runtime?.id) {
       setStatus('active');
    }
  }, []);

  return (
    <header className={cn(
      "border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50",
      compact ? "p-3" : "p-4"
    )}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="bg-primary/10 p-1.5 rounded-md">
            <ShieldCheck className="w-5 h-5 text-emerald-500" />
          </div>
          <div>
            <h1 className="font-semibold text-sm tracking-tight">SecureSentinel</h1>
            {!compact && <p className="text-xs text-muted-foreground">SOC-Lite Dashboard</p>}
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <div className={cn(
            "flex items-center gap-1.5 px-2 py-1 rounded-full text-[10px] font-medium border",
            status === 'active' 
              ? "bg-emerald-500/10 text-emerald-500 border-emerald-500/20" 
              : "bg-rose-500/10 text-rose-500 border-rose-500/20"
          )}>
            <span className={cn(
              "w-1.5 h-1.5 rounded-full animate-pulse",
              status === 'active' ? "bg-emerald-500" : "bg-rose-500"
            )} />
            {status === 'active' ? 'SYSTEM ACTIVE' : 'DISCONNECTED'}
          </div>
        </div>
      </div>
    </header>
  );
}
