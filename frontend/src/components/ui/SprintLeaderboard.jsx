import { useState, useEffect } from 'react';
import { getSprintLeaderboard } from '../../api/sprints';
import { toast } from 'react-hot-toast';

export function SprintLeaderboard({ sprintId, sprintNumber, isCurrent = false }) {
  const [leaderboard, setLeaderboard] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchLeaderboard = async () => {
    setIsLoading(true);
    try {
      const data = await getSprintLeaderboard(sprintId);
      setLeaderboard(data);
    } catch (err) {
      console.error(err);
      toast.error(`Failed to load leaderboard for Sprint ${sprintNumber}`);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (sprintId) {
      fetchLeaderboard();
    }
  }, [sprintId]);

  if (isLoading) {
    return (
      <div className="flex justify-center p-4">
        <div className="w-6 h-6 border-2 border-brand-gold border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl border border-brand-border/20 overflow-hidden shadow-sm">
      <div className={`${isCurrent ? 'bg-brand-teal' : 'bg-brand-dark'} px-4 py-2 flex justify-between items-center`}>
        <h3 className="text-white font-bold text-sm">
          Sprint {sprintNumber} Leaderboard
        </h3>
        {isCurrent && <span className="text-[10px] bg-white/20 text-white px-1.5 rounded uppercase font-bold animate-pulse">Live</span>}
      </div>
      
      <div className="divide-y divide-gray-50 max-h-60 overflow-y-auto">
        {leaderboard.length === 0 && (
          <div className="p-8 text-center text-brand-muted italic text-xs">No activity yet</div>
        )}
        
        {leaderboard.map((user, index) => (
          <div key={user.id} className="px-4 py-2 flex items-center justify-between hover:bg-gray-50 transition-colors">
            <div className="flex items-center gap-3">
              <span className={`w-5 h-5 flex items-center justify-center rounded-full text-[10px] font-bold ${index === 0 ? 'bg-brand-gold text-brand-dark' : 'bg-gray-100 text-brand-muted'}`}>
                {index + 1}
              </span>
              <span className="text-sm font-medium text-brand-dark truncate max-w-[100px]">
                {user.full_name?.split(' ')[0] || 'User'}
              </span>
            </div>
            <div className="flex items-center gap-2">
               <span className="text-xs font-black text-brand-teal">{user.sprint_points}</span>
               <span className="text-[10px] text-brand-muted">pts</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
