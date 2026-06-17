import { useState, useEffect } from 'react';
import { AdminLayout } from '../../components/layout/AdminLayout';
import { getLeaderboard, getLiveSessions, validateLiveAttendance, devalidateLiveAttendance } from '../../api/admin';
import { getSprints } from '../../api/sprints';
import { SprintLeaderboard } from '../../components/ui/SprintLeaderboard';
import { Link } from 'react-router-dom';
import { toast } from 'react-hot-toast';

export default function AdminPanel() {
  const [users, setUsers] = useState([]);
  const [liveSessions, setLiveSessions] = useState([]);
  const [sprints, setSprints] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [validatingId, setValidatingId] = useState(null);

  const fetchData = async () => {
    setIsLoading(true);
    // Fetch independently so one failure doesn't block the others
    const [leaderboardResult, sessionsResult, sprintsResult] = await Promise.allSettled([
      getLeaderboard(),
      getLiveSessions(),
      getSprints()
    ]);

    if (leaderboardResult.status === 'fulfilled') {
      setUsers(leaderboardResult.value);
    } else {
      console.error('Leaderboard fetch failed:', leaderboardResult.reason);
    }

    if (sessionsResult.status === 'fulfilled') {
      setLiveSessions(sessionsResult.value);
    } else {
      console.error('Live sessions fetch failed:', sessionsResult.reason);
    }

    if (sprintsResult.status === 'fulfilled') {
      setSprints(sprintsResult.value);
    } else {
      console.error('Sprints fetch failed:', sprintsResult.reason);
      toast.error("Failed to load sprint leaderboards");
    }

    setIsLoading(false);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleValidate = async (sessionId, userId) => {
    setValidatingId(`${sessionId}-${userId}`);
    try {
      await validateLiveAttendance(sessionId, userId);
      toast.success("Attendance validated! +8 pts awarded");
      fetchData();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Validation failed");
    } finally {
      setValidatingId(null);
    }
  };

  const handleDevalidate = async (sessionId, userId) => {
    setValidatingId(`${sessionId}-${userId}`);
    try {
      await devalidateLiveAttendance(sessionId, userId);
      toast.success("Attendance removed, points reset");
      fetchData();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Devalidation failed");
    } finally {
      setValidatingId(null);
    }
  };

  if (isLoading) {
    return (
      <AdminLayout>
        <div className="flex justify-center py-20">
          <div className="w-10 h-10 border-4 border-brand-gold border-t-transparent rounded-full animate-spin"></div>
        </div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout>
      <div className="space-y-10">
        {/* Global Leaderboard Section */}
        <section className="bg-white rounded-2xl shadow-sm border border-brand-border/20 overflow-hidden">
          <div className="bg-brand-teal px-6 py-4 flex justify-between items-center">
            <h2 className="text-white font-playfair font-bold text-lg flex items-center gap-2">
              <span className="text-xl">📊</span> Global Leaderboard
            </h2>
            <span className="text-brand-gold-pale/60 text-xs font-medium uppercase tracking-widest">Cumulative Scores</span>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-right">
              <thead className="bg-gray-50 border-b border-gray-100">
                <tr>
                  <th className="px-6 py-3 text-right text-xs font-bold text-brand-muted uppercase tracking-wider">Rank</th>
                  <th className="px-6 py-3 text-right text-xs font-bold text-brand-muted uppercase tracking-wider">Learner</th>
                  <th className="px-6 py-3 text-right text-xs font-bold text-brand-muted uppercase tracking-wider">Points</th>
                  <th className="px-6 py-3 text-right text-xs font-bold text-brand-muted uppercase tracking-wider">Progress</th>
                  <th className="px-6 py-3 text-right text-xs font-bold text-brand-muted uppercase tracking-wider">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {(Array.isArray(users) ? users : []).map((user, index) => (
                  <tr key={user.id} className="hover:bg-brand-gold/5 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      {index === 0 && <span className="text-2xl">🥇</span>}
                      {index === 1 && <span className="text-2xl">🥈</span>}
                      {index === 2 && <span className="text-2xl">🥉</span>}
                      {index > 2 && <span className="text-brand-muted font-bold ml-2">{index + 1}</span>}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <p className="font-bold text-brand-dark">{user.full_name}</p>
                      <p className="text-xs text-brand-muted">{user.email}</p>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-brand-teal font-black">{user.total_points}</span>
                      <span className="text-brand-muted text-xs"> / 400</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap w-48">
                      <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-brand-gold transition-all duration-1000"
                          style={{ width: `${(user.total_points / 400) * 100}%` }}
                        />
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-left">
                      <Link 
                        to={`/admin/users/${user.id}`}
                        className="text-brand-teal hover:text-brand-gold font-bold text-sm transition-colors"
                      >
                        Details →
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* Per-Sprint Leaderboards Section */}
        <section className="space-y-6">
          <div className="flex items-center gap-3">
            <h2 className="text-2xl font-playfair font-bold text-brand-dark">Sprint Leaderboards</h2>
            <div className="h-px flex-1 bg-brand-border/20"></div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {(Array.isArray(sprints) ? sprints : []).map((sprint) => (
              <SprintLeaderboard 
                key={sprint.id}
                sprintId={sprint.id}
                sprintNumber={sprint.sprint_number}
                isCurrent={sprint.is_active}
              />
            ))}
          </div>
        </section>

        {/* Live Sessions Validation */}
        <section className="bg-white rounded-2xl shadow-sm border border-brand-border/20 overflow-hidden">
           <div className="bg-brand-dark px-6 py-4">
              <h2 className="text-white font-playfair font-bold text-lg flex items-center gap-2">
                <span className="text-xl">🎥</span> Live Sessions
              </h2>
           </div>
           
           <div className="p-6 space-y-8">
              {(!Array.isArray(liveSessions) || liveSessions.length === 0) && <p className="text-center text-brand-muted italic">No live sessions created yet.</p>}
              
              {(Array.isArray(liveSessions) ? liveSessions : []).map((session) => (
                <div key={session.id} className="space-y-4">
                  <div className="flex items-center gap-4 border-b border-brand-border/20 pb-2">
                    <span className="bg-brand-gold text-brand-dark text-[10px] font-black px-2 py-0.5 rounded-md uppercase">
                      Sprint {session.sprint_number}
                    </span>
                    <h3 className="font-bold text-brand-dark">{session.title || `Live Session ${session.session_number}`}</h3>
                    <span className="text-xs text-brand-muted">{session.session_date}</span>
                  </div>
                  
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                    {(Array.isArray(users) ? users : []).map((user) => {
                      const isAttendee = Array.isArray(session.attendees) && session.attendees.find(a => a.user_id === user.id);
                      return (
                        <div key={user.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-100">
                          <span className="text-sm font-medium text-brand-dark truncate pr-2">{user.full_name.split(' ')[0]}</span>
                          {isAttendee ? (
                            <button
                              onClick={() => handleDevalidate(session.id, user.id)}
                              disabled={validatingId === `${session.id}-${user.id}`}
                              className="flex items-center gap-1 px-2 py-1 bg-brand-teal/10 hover:bg-red-100 text-brand-teal hover:text-red-600 text-[10px] font-bold rounded transition-colors disabled:opacity-50 group"
                            >
                              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path></svg>
                              <span className="group-hover:hidden">Validated</span>
                              <span className="hidden group-hover:inline">Remove</span>
                            </button>
                          ) : (
                            <button
                              onClick={() => handleValidate(session.id, user.id)}
                              disabled={validatingId === `${session.id}-${user.id}`}
                              className="px-2 py-1 bg-brand-gold/20 hover:bg-brand-gold text-brand-teal text-[10px] font-bold rounded transition-colors disabled:opacity-50"
                            >
                              {validatingId === `${session.id}-${user.id}` ? '...' : 'Validate'}
                            </button>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
           </div>
        </section>
      </div>
    </AdminLayout>
  );
}
