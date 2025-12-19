import React from 'react'
import ReactDOM from 'react-dom/client'
import { DashboardHeader } from '@/components/DashboardHeader'
import { ContextCard } from '@/components/ContextCard'
import { ActivityTimeline } from '@/components/ActivityTimeline'
import '@/index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <div className="flex flex-col h-full bg-background text-foreground">
      <DashboardHeader compact={true} />
      <main className="flex-1 overflow-y-auto p-4 space-y-4">
        <ContextCard />
        <ActivityTimeline limit={3} />
      </main>
    </div>
  </React.StrictMode>,
)
