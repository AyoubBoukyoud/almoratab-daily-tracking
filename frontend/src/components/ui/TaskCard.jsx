export function TaskCard({ taskNumber, label, description, emoji, checked, onChange, disabled }) {
  return (
    <div
      className={`
        flex items-center gap-4 p-4 rounded-xl border cursor-pointer
        transition-all duration-200
        ${checked
          ? 'bg-brand-teal/5 border-brand-teal shadow-sm'
          : 'bg-white border-brand-border/30 hover:border-brand-teal/50'}
        ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
      `}
      onClick={() => !disabled && onChange(!checked)}
    >
      <span className="text-2xl">{emoji}</span>
      <div className="flex-1 text-right">
        <p className="text-[10px] font-bold text-brand-gold uppercase tracking-wider mb-0.5">Task {taskNumber}</p>
        <p className="text-sm font-bold text-brand-dark leading-tight">{label}</p>
        {description && <p className="text-xs text-brand-muted mt-1 leading-relaxed">{description}</p>}
      </div>
      <div className={`
        w-6 h-6 rounded-full border-2 flex items-center justify-center flex-shrink-0
        ${checked ? 'bg-brand-teal border-brand-teal' : 'border-gray-300'}
      `}>
        {checked && <span className="text-white text-xs">✓</span>}
      </div>
    </div>
  );
}
