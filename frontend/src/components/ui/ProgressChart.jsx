import { Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, ReferenceLine, Area, ComposedChart } from 'recharts';

export function ProgressChart({ data }) {
  // data: [{ date: "2026-06-02", cumulative_points: 6 }, ...]
  
  // Add a starting point at 0 if there's data
  let chartData = data ? [...data] : [];
  if (chartData.length > 0) {
    const firstDate = new Date(chartData[0].date);
    const startDate = new Date(firstDate);
    startDate.setDate(startDate.getDate() - 1); // Day before first activity
    
    chartData.unshift({
      date: startDate.toISOString().split('T')[0],
      cumulative_points: 0
    });
  }

  if (chartData.length === 0) {
    return (
      <div className="h-[280px] flex items-center justify-center bg-white rounded-2xl border border-brand-border/20 shadow-sm">
        <p className="text-brand-muted text-sm italic">No progress recorded yet. Start today!</p>
      </div>
    );
  }

  const formatDate = (dateStr) => {
    try {
      const d = new Date(dateStr);
      return d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' });
    } catch {
      return dateStr;
    }
  };

  return (
    <div className="bg-white p-4 rounded-2xl border border-brand-border/20 shadow-sm overflow-hidden relative">
      <div className="absolute top-4 right-6 flex items-center gap-2">
         <div className="w-3 h-3 rounded-full bg-brand-gold"></div>
         <span className="text-[10px] font-bold text-brand-muted uppercase tracking-tighter">Your Journey</span>
      </div>
      
      <ResponsiveContainer width="100%" height={280}>
        <ComposedChart data={chartData} margin={{ top: 20, right: 20, bottom: 10, left: -10 }}>
          <defs>
            <linearGradient id="colorPoints" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#C9982A" stopOpacity={0.1}/>
              <stop offset="95%" stopColor="#C9982A" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#F5F5F5" vertical={false} />
          <XAxis 
            dataKey="date" 
            tick={{ fontSize: 10, fill: '#6B8280' }} 
            tickFormatter={formatDate}
            axisLine={{ stroke: '#D4C5A0', strokeWidth: 1 }}
            tickLine={false}
            minTickGap={30}
          />
          <YAxis 
            domain={[0, 400]} 
            tick={{ fontSize: 10, fill: '#6B8280' }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip
            contentStyle={{ 
              borderRadius: '12px', 
              border: '1px solid #D4C5A0', 
              boxShadow: '0 8px 24px rgba(26, 77, 74, 0.1)',
              fontFamily: 'Lato, sans-serif',
              padding: '12px'
            }}
            labelFormatter={(label) => `Date: ${formatDate(label)}`}
            itemStyle={{ color: '#1A4D4A', fontWeight: 'bold' }}
            formatter={(value) => [`${value} pts`, 'Cumulative Score']}
          />
          
          <Area 
            type="monotone" 
            dataKey="cumulative_points" 
            stroke="none" 
            fillOpacity={1} 
            fill="url(#colorPoints)" 
          />
          
          <ReferenceLine y={400} stroke="#1A4D4A" strokeDasharray="3 3" label={{ position: 'top', value: '400 Target', fill: '#1A4D4A', fontSize: 10, fontWeight: 'bold' }} />
          
          <Line
            type="monotone"
            dataKey="cumulative_points"
            stroke="#C9982A"
            strokeWidth={3}
            dot={{ r: 4, fill: '#FFF', strokeWidth: 2, stroke: '#C9982A' }}
            activeDot={{ r: 6, fill: '#1A4D4A', stroke: '#FFF', strokeWidth: 2 }}
            animationDuration={1500}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
