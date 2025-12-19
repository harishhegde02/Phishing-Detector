"use client";

import { Shield, Globe, Clock, AlertTriangle } from "lucide-react";

const MOCK_ACTIVITY = [
  { id: 1, domain: "accounts.google.com", time: "10:45 AM", status: "SAFE", risk: 0.05, category: "Infrastructure" },
  { id: 2, domain: "github.com", time: "10:30 AM", status: "SAFE", risk: 0.1, category: "Work" },
  { id: 3, domain: "payment-confirm-u8.net", time: "09:15 AM", status: "BLOCKED", risk: 0.95, category: "Phishing" },
  { id: 4, domain: "slack.com", time: "09:00 AM", status: "SAFE", risk: 0.02, category: "Work" },
  { id: 5, domain: "urgent-bonus.xyz", time: "Yesterday", status: "WARNED", risk: 0.65, category: "Scam" },
];

export default function ActivityPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Activity Insights</h1>
          <p className="text-muted-foreground">Detailed log of scanned interactions and blocked threats.</p>
        </div>
        <div className="flex gap-2">
           <button className="px-3 py-1.5 text-sm font-medium border border-border rounded-md hover:bg-secondary">Export CSV</button>
           <button className="px-3 py-1.5 text-sm font-medium border border-border rounded-md hover:bg-secondary">Filter</button>
        </div>
      </div>

      <div className="rounded-xl border border-border bg-card overflow-hidden">
        <table className="w-full text-sm text-left">
          <thead className="bg-secondary/50 border-b border-border/50 text-muted-foreground font-medium">
             <tr>
               <th className="px-4 py-3">Timestamp</th>
               <th className="px-4 py-3">Domain</th>
               <th className="px-4 py-3">Risk Category</th>
               <th className="px-4 py-3">Status</th>
               <th className="px-4 py-3 text-right">Risk Score</th>
             </tr>
          </thead>
          <tbody className="divide-y divide-border/50">
             {MOCK_ACTIVITY.map((item) => (
                <tr key={item.id} className="hover:bg-secondary/10 group">
                   <td className="px-4 py-3 flex items-center gap-2 text-muted-foreground whitespace-nowrap">
                      <Clock size={14} /> {item.time}
                   </td>
                   <td className="px-4 py-3 font-medium text-foreground">
                      {item.domain}
                   </td>
                   <td className="px-4 py-3">
                      <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-secondary/50 text-xs">
                        <Globe size={10} /> {item.category}
                      </span>
                   </td>
                   <td className="px-4 py-3">
                      {item.status === 'SAFE' && (
                        <span className="text-emerald-500 flex items-center gap-1 font-medium text-xs">
                           <Shield size={12} /> Safe
                        </span>
                      )}
                      {item.status === 'BLOCKED' && (
                        <span className="text-rose-500 flex items-center gap-1 font-medium text-xs">
                           <Shield size={12} fill="currentColor" /> Blocked
                        </span>
                      )}
                      {item.status === 'WARNED' && (
                        <span className="text-amber-500 flex items-center gap-1 font-medium text-xs">
                           <AlertTriangle size={12} /> Warned
                        </span>
                      )}
                   </td>
                   <td className="px-4 py-3 text-right font-mono text-muted-foreground">
                      {(item.risk * 100).toFixed(0)}%
                   </td>
                </tr>
             ))}
          </tbody>
        </table>
        <div className="p-4 border-t border-border/50 text-center text-xs text-muted-foreground">
           Showing last 5 of 1,248 formatted events.
        </div>
      </div>
    </div>
  );
}
