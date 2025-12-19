import React from 'react';
import { cn } from '@/lib/utils';
import { Clock } from 'lucide-react';

interface HistoryItem {
    url: string;
    time: string;
    date: string;
    score: number;
    timestamp: number;
}

export function ActivityTimeline({ limit = 10 }: { limit?: number }) {
  const [history, setHistory] = React.useState<HistoryItem[]>([]);

  React.useEffect(() => {
    if (chrome?.storage) {
        chrome.storage.local.get(null, (items) => {
            const parsed = Object.entries(items)
                .map(([key, val]: [string, any]) => {
                    if (!val?.timestamp || !val?.max_risk_score) return null;
                    const date = new Date(val.timestamp);
                    return {
                        url: key,
                        score: val.max_risk_score,
                        timestamp: val.timestamp,
                        time: date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                        date: date.toLocaleDateString() === new Date().toLocaleDateString() ? 'Today' : date.toLocaleDateString()
                    };
                })
                .filter(Boolean) as HistoryItem[];
            
            setHistory(parsed.sort((a, b) => b.timestamp - a.timestamp).slice(0, limit));
        });
    } else {
        // Fallback for dev
        setHistory(MOCK_HISTORY); 
    }
  }, [limit]);

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
