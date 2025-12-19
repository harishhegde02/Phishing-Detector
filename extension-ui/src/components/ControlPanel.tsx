import React, { useState } from 'react';
import { Settings, Volume2, VolumeX, Sliders } from 'lucide-react';
import { cn } from '@/lib/utils';

export function ControlPanel() {
  const [notifications, setNotifications] = useState(true);
  const [sensitivity, setSensitivity] = useState(50);

  return (
    <div className="rounded-lg border border-border bg-card p-4 shadow-sm">
      <div className="flex items-center gap-2 mb-4">
        <Settings className="w-4 h-4 text-muted-foreground" />
        <h2 className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Configuration</h2>
      </div>

      <div className="space-y-6">
        {/* Notifications Toggle */}
        <div className="flex items-center justify-between">
            <div className="flex gap-3 items-center">
                <div onClick={() => setNotifications(!notifications)} className="cursor-pointer bg-secondary p-2 rounded-md">
                    {notifications ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4 text-muted-foreground" />}
                </div>
                <div>
                    <h3 className="text-sm font-medium">Real-time Alerts</h3>
                    <p className="text-xs text-muted-foreground">Notify on high risk sites</p>
                </div>
            </div>
            <button 
                onClick={() => setNotifications(!notifications)}
                className={cn(
                    "w-10 h-5 rounded-full transition-colors relative",
                    notifications ? "bg-primary" : "bg-secondary"
                )}
            >
                <div className={cn(
                    "w-3 h-3 bg-background rounded-full absolute top-1 transition-transform",
                    notifications ? "left-6" : "left-1"
                )} />
            </button>
        </div>

        {/* Sensitivity Slider */}
        <div className="space-y-3">
            <div className="flex justify-between items-center">
                <div className="flex items-center gap-2">
                    <Sliders className="w-4 h-4 text-muted-foreground" />
                    <span className="text-sm font-medium">AI Sensitivity</span>
                </div>
                <span className="text-xs text-muted-foreground">{sensitivity > 75 ? 'Strict' : sensitivity < 25 ? 'Lax' : 'Balanced'}</span>
            </div>
            <input 
                type="range" 
                min="0" 
                max="100" 
                value={sensitivity}
                onChange={(e) => setSensitivity(parseInt(e.target.value))}
                className="w-full h-1.5 bg-secondary rounded-full appearance-none cursor-pointer accent-primary"
            />
             <div className="flex justify-between text-[10px] text-muted-foreground px-1">
                <span>Low</span>
                <span>High</span>
            </div>
        </div>
      </div>
    </div>
  );
}
