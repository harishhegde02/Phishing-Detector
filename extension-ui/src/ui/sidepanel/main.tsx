import React from 'react'
import ReactDOM from 'react-dom/client'
import { DashboardHeader } from '@/components/DashboardHeader'
import { ContextCard } from '@/components/ContextCard'
import { ActivityTimeline } from '@/components/ActivityTimeline'
import { TrendInsights } from '@/components/TrendInsights'
import { ControlPanel } from '@/components/ControlPanel'
import '@/index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <div className="flex flex-col h-screen bg-background text-foreground">
      <DashboardHeader />
      <main className="flex-1 overflow-y-auto p-6 space-y-6">
        <ContextCard detailed={true} />
        <ActivityTimeline />
        <div className="grid grid-cols-1 gap-6">
          <TrendInsights />
          <ControlPanel />
        </div>
      </main>
    </div>
  </React.StrictMode>,
)
