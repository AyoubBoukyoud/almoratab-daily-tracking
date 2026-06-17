import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { AdminLayout } from '../../components/layout/AdminLayout';
import { getUserProgress, getUserChart, getUserHistory } from '../../api/admin';
import { ProgressChart } from '../../components/ui/ProgressChart';
import { toast } from 'react-hot-toast';

export default function UserDetail() {
  const { userId } = useParams();
  const [user, setUser] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [userData, chartRes, historyRes] = await Promise.all([
        getUserProgress(userId),
        getUserChart(userId),
        getUserHistory(userId)
      ]);
      setUser(userData);
      setChartData(chartRes);
      setHistory(historyRes);
    } catch (err) {
      console.error(err);
      toast.error("Failed to load user details");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [userId]);

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
      <div className="space-y-6">
        <Link to="/admin" className="inline-flex items-center text-brand-teal font-bold text-sm hover:underline gap-1">
           ← Back to Dashboard
        </Link>

        <div className="flex flex-col md:flex-row justify-between items-start md:items-center bg-white p-6 rounded-2xl shadow-sm border border-brand-border/20 gap-4">
          <div>
            <h2 className="text-2xl font-playfair font-bold text-brand-dark">{user?.full_name}</h2>
            <p className="text-brand-muted">{user?.email}</p>
          </div>
          <div className="text-right">
             <p className="text-xs text-brand-muted uppercase font-bold tracking-widest mb-1">Total Points</p>
             <div className="flex items-baseline gap-1">
                <span className="text-4xl font-black text-brand-gold">{user?.total_points}</span>
                <span className="text-brand-teal font-bold text-xl">/ 400</span>
             </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Chart Column */}
          <div className="lg:col-span-2 space-y-6">
            <section className="space-y-3">
              <h3 className="font-playfair font-bold text-brand-dark text-lg">Points Over Time</h3>
              <ProgressChart data={chartData} />
            </section>

            <section className="bg-white rounded-2xl shadow-sm border border-brand-border/20 overflow-hidden">
              <div className="bg-gray-50 px-4 py-3 border-b border-gray-100">
                <h3 className="font-bold text-brand-dark text-sm">Submission History (Last 30 days)</h3>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-right text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-2 text-brand-muted font-bold">Date</th>
                      <th className="px-4 py-2 text-brand-muted font-bold">Daily</th>
                      <th className="px-4 py-2 text-brand-muted font-bold">Sport</th>
                      <th className="px-4 py-2 text-brand-muted font-bold">Project</th>
                      <th className="px-4 py-2 text-brand-muted font-bold">Pts</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {history.slice(0, 30).map((sub) => (
                      <tr key={sub.id}>
                        <td className="px-4 py-2 font-medium">{sub.submission_date}</td>
                        <td className="px-4 py-2">{sub.task1_done ? '✅' : '❌'}</td>
                        <td className="px-4 py-2">{sub.task2_done ? '✅' : '❌'}</td>
                        <td className="px-4 py-2">{sub.task3_done ? '✅' : '❌'}</td>
                        <td className="px-4 py-2 font-bold text-brand-teal">+{sub.points_earned}</td>
                      </tr>
                    ))}
                    {history.length === 0 && (
                      <tr>
                        <td colSpan="5" className="px-4 py-8 text-center text-brand-muted italic">No submissions yet</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </section>
          </div>

          {/* Sprint Breakdown Column */}
          <div className="space-y-6">
             <section className="bg-brand-teal text-white rounded-2xl p-6 shadow-lg shadow-brand-teal/20">
                <h3 className="font-playfair font-bold text-xl mb-4 text-brand-gold-pale">Sprint Breakdown</h3>
                <div className="space-y-4">
                  {user?.sprint_stats?.map((sprint) => (
                    <div key={sprint.sprint_number} className="border-b border-white/10 pb-3 last:border-0">
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-bold">Sprint {sprint.sprint_number}</span>
                        <span className="text-brand-gold font-black">{sprint.total} / 100</span>
                      </div>
                      <div className="flex gap-4 text-[10px] text-white/60 font-medium uppercase tracking-tighter">
                        <span>Tasks: {sprint.task_points}</span>
                        <span>Live: {sprint.live_points}</span>
                      </div>
                    </div>
                  ))}
                </div>
             </section>

             <section className="bg-brand-gold/10 border border-brand-gold/20 rounded-2xl p-6">
                <h3 className="font-bold text-brand-dark mb-2">Engagement Analytics</h3>
                <div className="space-y-3">
                   <div className="flex justify-between">
                      <span className="text-sm text-brand-muted">Completion Rate</span>
                      <span className="text-sm font-bold text-brand-teal">
                        {Math.round((user?.total_points / 400) * 100)}%
                      </span>
                   </div>
                   <div className="w-full h-1.5 bg-white rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-brand-teal" 
                        style={{ width: `${(user?.total_points / 400) * 100}%` }}
                      />
                   </div>
                </div>
             </section>
          </div>
        </div>
      </div>
    </AdminLayout>
  );
}
