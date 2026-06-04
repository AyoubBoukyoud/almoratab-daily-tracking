export function SprintBar({ sprintNumber, points, maxPoints = 80, isActive }) {
  const percentage = Math.min((points / maxPoints) * 100, 100);
  
  return (
    <div className={`p-4 rounded-lg ${isActive ? 'bg-brand-gold/10 border border-brand-gold/20' : 'bg-white'}`}>
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-bold text-brand-dark">Sprint {sprintNumber}</span>
        <span className="text-xs font-medium text-brand-muted">{points} / {maxPoints} pts</span>
      </div>
      <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
        <div 
          className={`h-full transition-all duration-1000 ease-out ${isActive ? 'bg-brand-gold' : 'bg-brand-teal/40'}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
      {isActive && (
        <p className="text-[10px] text-brand-gold font-bold mt-1 uppercase tracking-wider">Active Sprint</p>
      )}
    </div>
  );
}
