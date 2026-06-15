import { useState, useEffect } from 'react';
import { UserLayout } from '../components/layout/UserLayout';
import { PointsRing } from '../components/ui/PointsRing';
import { TaskCard } from '../components/ui/TaskCard';
import { SprintBar } from '../components/ui/SprintBar';
import { SprintLeaderboard } from '../components/ui/SprintLeaderboard';
import { getTodayStatus, submitTasks } from '../api/tasks';
import { getMyStats } from '../api/users';
import { getSprints, getCurrentSprint } from '../api/sprints';
import { toast } from 'react-hot-toast';

export default function UserDashboard() {
  const [stats, setStats] = useState(null);
  const [todaySub, setTodaySub] = useState({ submitted: false, submission: null });
  const [currentSprint, setCurrentSprint] = useState(null);
  const [allSprints, setAllSprints] = useState([]);
  const [tasks, setTasks] = useState({ task1: false, task2: false, task3: false });
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const isSunday = new Date().getDay() === 0;

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [statsData, todayData, sprintData, allSprintsData] = await Promise.all([
        getMyStats(),
        getTodayStatus(),
        getCurrentSprint(),
        getSprints()
      ]);
      setStats(statsData);
      setTodaySub(todayData);
      setCurrentSprint(sprintData);
      setAllSprints(allSprintsData);
      
      if (todayData.submitted) {
        setTasks({
          task1: todayData.submission.task1_done,
          task2: todayData.submission.task2_done,
          task3: todayData.submission.task3_done,
        });
      }
    } catch (error) {
      console.error("Failed to fetch dashboard data", error);
      toast.error("Failed to load your progress");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSubmit = async () => {
    if (!tasks.task1 && !tasks.task2 && !tasks.task3) {
      toast.error("Please complete at least one task!");
      return;
    }

    setIsSubmitting(true);
    try {
      const result = await submitTasks(tasks);
      toast.success(`Bravo! +${result.points_earned} points earned`);
      await fetchData(); // Refresh stats
    } catch (error) {
      const msg = error.response?.data?.detail || "Submission failed";
      toast.error(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <UserLayout>
        <div className="flex flex-col items-center justify-center min-h-[50vh]">
          <div className="w-12 h-12 border-4 border-brand-gold border-t-transparent rounded-full animate-spin"></div>
          <p className="mt-4 text-brand-muted animate-pulse font-medium">Loading your journey...</p>
        </div>
      </UserLayout>
    );
  }

  return (
    <UserLayout>
      <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
        {/* Points Summary */}
        <section className="bg-white rounded-2xl shadow-sm border border-brand-border/20 overflow-hidden">
          <div className="p-1 bg-brand-gold/10"></div>
          <PointsRing 
            current={stats?.total_points || 0} 
            max={400} 
            sprintInfo={{ name: 'Current Progress', currentDay: stats?.current_day || '?' }}
          />
        </section>

        {/* Task Section */}
        <section className="space-y-4">
          <div className="flex justify-between items-end">
            <div>
              <h2 className="text-xl font-playfair font-bold text-brand-dark">Today's Missions</h2>
              <p className="text-sm text-brand-muted">Monday – Saturday • 2 pts per task</p>
            </div>
            {isSunday && (
              <span className="px-3 py-1 bg-brand-gold/20 text-brand-gold text-xs font-bold rounded-full uppercase tracking-wider">
                Rest Day 🌿
              </span>
            )}
          </div>

          <div className="grid grid-cols-1 gap-3">
            <TaskCard 
              taskNumber={1}
              emoji="📓"
              label="My Daily (Organisation)"
              description="Planifier et structurer ma journée"
              checked={tasks.task1}
              onChange={(val) => setTasks(prev => ({ ...prev, task1: val }))}
              disabled={new Date().getDay() === 0 || todaySub.submitted || isSubmitting}
            />
            <TaskCard 
              taskNumber={2}
              emoji="🏃"
              label="My Physical Activity (Discipline)"
              description="Renforcer mon énergie et ma Discipline"
              checked={tasks.task2}
              onChange={(val) => setTasks(prev => ({ ...prev, task2: val }))}
              disabled={new Date().getDay() === 0 || todaySub.submitted || isSubmitting}
            />
            <TaskCard 
              taskNumber={3}
              emoji="🚀"
              label="My Project Contribution (Progression)"
              description="Créer une avancée concrète dans mon projet"
              checked={tasks.task3}
              onChange={(val) => setTasks(prev => ({ ...prev, task3: val }))}
              disabled={new Date().getDay() === 0 || todaySub.submitted || isSubmitting}
            />
          </div>

          {!todaySub.submitted && new Date().getDay() !== 0 && (
            <button
              onClick={handleSubmit}
              disabled={isSubmitting}
              className="w-full py-4 bg-brand-gold hover:bg-brand-gold-light text-brand-dark font-bold rounded-xl shadow-md transition-all active:scale-[0.98] disabled:opacity-50 disabled:active:scale-100"
            >
              {isSubmitting ? 'Submitting...' : 'Submit Today\'s Tasks'}
            </button>
          )}

          {todaySub.submitted && (
            <div className="p-4 bg-brand-teal text-white rounded-xl flex items-center justify-center gap-3 shadow-inner">
              <span className="text-xl">✨</span>
              <p className="font-bold">Tasks submitted! See you tomorrow.</p>
            </div>
          )}

          {new Date().getDay() === 0 && !todaySub.submitted && (
            <div className="p-4 bg-brand-gold/10 border border-brand-gold/20 text-brand-teal rounded-xl text-center italic">
              "Take a break, recharge your energy. Submissions resume on Monday!"
            </div>
          )}
        </section>

        {/* Sprint History */}
        <section className="space-y-4">
          <h2 className="text-xl font-playfair font-bold text-brand-dark">Sprint Progress</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {stats?.sprint_stats?.map((sprint, idx) => (
              <SprintBar 
                key={idx}
                sprintNumber={sprint.sprint_number}
                points={sprint.total}
                isActive={sprint.sprint_number === (stats?.current_sprint_number || 1)}
              />
            ))}
          </div>
        </section>

        {/* Motivation Board */}
        <section className="space-y-6">
          <div className="flex items-center gap-3">
            <h2 className="text-xl font-playfair font-bold text-brand-dark">Sprint Leaderboards</h2>
            <div className="h-px flex-1 bg-brand-border/20"></div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {(Array.isArray(allSprints) ? allSprints : []).map((sprint) => (
              <SprintLeaderboard 
                key={sprint.id}
                sprintId={sprint.id}
                sprintNumber={sprint.sprint_number}
                isCurrent={sprint.id === currentSprint?.id}
              />
            ))}
          </div>
        </section>
      </div>
    </UserLayout>
  );
}
