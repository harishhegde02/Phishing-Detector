"use client";

import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis } from "recharts";

const data = [
  { day: "Mon", threats: 2 },
  { day: "Tue", threats: 5 },
  { day: "Wed", threats: 1 },
  { day: "Thu", threats: 0 },
  { day: "Fri", threats: 3 },
  { day: "Sat", threats: 8 },
  { day: "Sun", threats: 2 },
];

export function TrendChart() {
  return (
    <div className="p-6 rounded-xl border border-border bg-card shadow-sm">
       <div className="mb-6">
          <h3 className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Activity Trend</h3>
          <p className="text-xs text-muted-foreground mt-1">Threats blocked this week</p>
       </div>
       <div className="h-[200px] w-full">
         <ResponsiveContainer width="100%" height="100%">
           <LineChart data={data}>
             <XAxis 
                dataKey="day" 
                stroke="#64748b" 
                fontSize={12} 
                tickLine={false} 
                axisLine={false} 
             />
             <Tooltip 
                contentStyle={{ 
                    backgroundColor: 'var(--card)', 
                    borderColor: 'var(--border)',
                    borderRadius: '8px',
                    color: 'var(--foreground)'
                }}
                itemStyle={{ color: 'var(--foreground)' }}
             />
             <Line 
                type="monotone" 
                dataKey="threats" 
                stroke="#f43f5e" 
                strokeWidth={2} 
                dot={{ r: 4, fill: "#f43f5e" }} 
                activeDot={{ r: 6 }} 
             />
           </LineChart>
         </ResponsiveContainer>
       </div>
    </div>
  );
}
