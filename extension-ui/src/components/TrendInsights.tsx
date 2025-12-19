import React from 'react';
import { TrendingUp, ShieldCheck } from 'lucide-react';

export function TrendInsights() {
  return (
    <div className="grid grid-cols-2 gap-4">
        <div className="bg-card border border-border rounded-lg p-4">
            <div className="flex items-center gap-2 text-emerald-500 mb-2">
                <ShieldCheck className="w-4 h-4" />
                <span className="text-xs font-medium">Safety Score</span>
            </div>
            <div className="text-2xl font-bold">98%</div>
            <div className="text-[10px] text-muted-foreground">Safe interactions today</div>
        </div>
        
        <div className="bg-card border border-border rounded-lg p-4">
            <div className="flex items-center gap-2 text-amber-500 mb-2">
                <TrendingUp className="w-4 h-4" />
                <span className="text-xs font-medium">Top Threat</span>
            </div>
            <div className="text-sm font-medium">Urgency</div>
            <div className="text-[10px] text-muted-foreground">Most common trigger</div>
        </div>
    </div>
  );
}
