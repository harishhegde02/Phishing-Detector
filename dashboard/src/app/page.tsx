import { RiskScoreCard } from "@/components/overview/RiskScoreCard";
import { TrendChart } from "@/components/overview/TrendChart";
import { AlertTriangle, Activity } from "lucide-react";

export default function Home() {
  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Overview</h1>
        <p className="text-muted-foreground mt-2">
          Your security posture is currently <span className="text-emerald-500 font-medium">stable</span>. 
          No critical threats detected in the last 24 hours.
        </p>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <RiskScoreCard score={0.15} />
        
        <div className="p-6 rounded-xl border border-border bg-card shadow-sm flex flex-col justify-between">
            <div>
              <h3 className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Total Scans</h3>
              <div className="mt-4 flex items-baseline gap-2">
                <span className="text-3xl font-bold">1,248</span>
                <span className="text-xs text-emerald-500 flex items-center gap-1">
                  <Activity size={12} /> +12%
                </span>
              </div>
            </div>
            <div className="mt-4 text-xs text-muted-foreground">
              Pages analyzed across 4 devices.
            </div>
        </div>

        <div className="p-6 rounded-xl border border-border bg-card shadow-sm flex flex-col justify-between">
            <div>
              <h3 className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Threats Blocked</h3>
              <div className="mt-4 flex items-baseline gap-2">
                <span className="text-3xl font-bold text-rose-500">14</span>
                <span className="text-xs text-rose-500 bg-rose-500/10 px-2 py-0.5 rounded-full">
                  2 Critical
                </span>
              </div>
            </div>
            <div className="mt-4 text-xs text-muted-foreground">
              Most frequent: <strong>Urgency Patterns</strong>
            </div>
        </div>
      </div>

      {/* Main Content Split */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
           <TrendChart />
        </div>
        
        <div className="space-y-6">
           {/* Recent Alerts Feed */}
           <div className="rounded-xl border border-border bg-card shadow-sm overflow-hidden">
              <div className="p-4 border-b border-border/50 bg-secondary/20">
                 <h3 className="text-sm font-medium">Recent Interventions</h3>
              </div>
              <div className="divide-y divide-border/50">
                 {[
                   { domain: 'pay-pal-secure.com', time: '2h ago', type: 'Phishing', risk: 'High' },
                   { domain: 'urgent-hr-update.net', time: '5h ago', type: 'Social Eng.', risk: 'Moderate' },
                   { domain: 'unknown-crypto.io', time: '1d ago', type: 'Scam', risk: 'High' },
                 ].map((item, i) => (
                   <div key={i} className="p-4 flex items-start justify-between hover:bg-secondary/10 transition-colors">
                      <div className="flex gap-3">
                         <div className="mt-1">
                           <AlertTriangle size={16} className="text-rose-500" />
                         </div>
                         <div>
                           <div className="text-sm font-medium">{item.domain}</div>
                           <div className="text-xs text-muted-foreground">{item.type} • {item.time}</div>
                         </div>
                      </div>
                      <span className="text-[10px] font-mono border border-rose-500/20 text-rose-500 px-1.5 py-0.5 rounded bg-rose-500/5">
                        {item.risk.toUpperCase()}
                      </span>
                   </div>
                 ))}
                 <div className="p-3 text-center text-xs text-muted-foreground hover:text-foreground cursor-pointer">
                    View all activity →
                 </div>
              </div>
           </div>
        </div>
      </div>
    </div>
  );
}
