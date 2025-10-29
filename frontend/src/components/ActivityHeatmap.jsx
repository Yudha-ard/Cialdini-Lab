import React from 'react';
import { Card } from '@/components/ui/card';

const ActivityHeatmap = ({ activityData = [] }) => {
  // Generate last 12 weeks (84 days)
  const weeks = 12;
  const daysInWeek = 7;
  
  const today = new Date();
  const startDate = new Date(today);
  startDate.setDate(startDate.getDate() - (weeks * daysInWeek));
  
  // Create activity map for quick lookup
  const activityMap = {};
  if (Array.isArray(activityData)) {
    activityData.forEach(activity => {
      if (activity && activity.date) {
        const date = new Date(activity.date).toISOString().split('T')[0];
        activityMap[date] = activity.count || 0;
      }
    });
  }
  
  // Generate calendar grid
  const calendar = [];
  for (let week = 0; week < weeks; week++) {
    const weekDays = [];
    for (let day = 0; day < daysInWeek; day++) {
      const currentDate = new Date(startDate);
      currentDate.setDate(startDate.getDate() + (week * daysInWeek) + day);
      
      const dateStr = currentDate.toISOString().split('T')[0];
      const count = activityMap[dateStr] || 0;
      
      weekDays.push({
        date: currentDate,
        dateStr,
        count,
        level: getActivityLevel(count)
      });
    }
    calendar.push(weekDays);
  }
  
  function getActivityLevel(count) {
    if (count === 0) return 0;
    if (count <= 2) return 1;
    if (count <= 5) return 2;
    if (count <= 10) return 3;
    return 4;
  }
  
  function getColor(level) {
    const colors = {
      0: 'bg-zinc-800/50',
      1: 'bg-emerald-900/40',
      2: 'bg-emerald-700/60',
      3: 'bg-emerald-500/80',
      4: 'bg-emerald-400'
    };
    return colors[level] || colors[0];
  }
  
  const dayNames = ['Min', 'Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab'];
  
  return (
    <Card className="glass border-zinc-800 p-6">
      <h3 className="text-lg font-semibold mb-4">Aktivitas Harian</h3>
      
      <div className="flex gap-1 overflow-x-auto">
        {/* Day labels */}
        <div className="flex flex-col gap-1 text-xs text-gray-500 mr-2">
          {dayNames.map((day, idx) => (
            <div key={idx} className="h-3 flex items-center">
              {day}
            </div>
          ))}
        </div>
        
        {/* Calendar grid */}
        <div className="flex gap-1">
          {calendar.map((week, weekIdx) => (
            <div key={weekIdx} className="flex flex-col gap-1">
              {week.map((day, dayIdx) => (
                <div
                  key={dayIdx}
                  className={`w-3 h-3 rounded-sm ${getColor(day.level)} transition-all hover:ring-2 hover:ring-emerald-400 cursor-pointer`}
                  title={`${day.dateStr}: ${day.count} aktivitas`}
                />
              ))}
            </div>
          ))}
        </div>
      </div>
      
      {/* Legend */}
      <div className="flex items-center gap-2 mt-4 text-xs text-gray-400">
        <span>Sedikit</span>
        <div className="flex gap-1">
          {[0, 1, 2, 3, 4].map(level => (
            <div key={level} className={`w-3 h-3 rounded-sm ${getColor(level)}`} />
          ))}
        </div>
        <span>Banyak</span>
      </div>
    </Card>
  );
};

export default ActivityHeatmap;
