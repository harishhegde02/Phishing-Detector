import React from 'react';
import { cn } from '@/lib/utils';
import { Clock } from 'lucide-react';

const MOCK_HISTORY = [
    { url: 'brave.com', time: '10:42 AM', date: 'Today', score: 0.05 },
    { url: 'accounts.google.co.in', time: '10:15 AM', date: 'Today', score: 0.12 },
    { url: 'payment-update-urgent.com', time: '09:30 AM', date: 'Today', score: 0.92 },
    { url: 'github.com', time: 'Yesterday', date: 'Yesterday', score: 0.01 },
];

export function ActivityTimeline({ limit = 10 }: { limit?: number }) {
  const history = MOCK_HISTORY.slice(0, limit);

  return (
    <div className="rounded-lg border border-border bg-card p-4 shadow-sm">
      <div className="flex items-center gap-2 mb-4">
        <Clock className="w-4 h-4 text-muted-foreground" />
        <h2 className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Recent Activity</h2>
      </div>

      <div className="space-y-4">
        {history.map((item, i) => {
            const isRisk = item.score > 0.6;
            return (
                <div key={i} className="flex items-start gap-3 relative">
                    {/* Timeline Line */}
                    {i !== history.length - 1 && (
                        <div className="absolute left-[5px] top-6 bottom-[-16px] w-[1px] bg-border" />
                    )}
                    
                    <div className={cn(
                        "w-2.5 h-2.5 rounded-full mt-1.5 flex-shrink-0 z-10",
                        isRisk ? "bg-rose-500 ring-4 ring-rose-500/10" : "bg-emerald-500/50"
                    )} />
                    
                    <div className="flex-1 min-w-0">
                        <div className="flex justify-between items-baseline">
                            <h3 className="text-sm font-medium truncate">{item.url}</h3>
                            <span className="text-[10px] text-muted-foreground whitespace-nowrap">{item.time}</span>
                        </div>
                        <p className={cn(
                            "text-xs truncate", 
                            isRisk ? "text-rose-400" : "text-muted-foreground"
                        )}>
                            {isRisk ? "High Risk Detected" : "Safe Session"}
                        </p>
                    </div>
                </div>
            )
        })}
      </div>
    </div>
  );
}
