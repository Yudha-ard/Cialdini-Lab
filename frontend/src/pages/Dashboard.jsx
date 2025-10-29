import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext, API } from '@/App';
import Layout from '@/components/Layout';
import { Card } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Trophy, Target, TrendingUp, Zap, Flame, Gift, Calendar } from 'lucide-react';
import axios from 'axios';

const Dashboard = () => {
  const { user, token } = React.useContext(AuthContext);
  const navigate = useNavigate();
  const [progress, setProgress] = useState(null);
  const [dailyChallenge, setDailyChallenge] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProgress();
    fetchDailyChallenge();
  }, []);

  const fetchProgress = async () => {
    try {
      const response = await axios.get(`${API}/progress`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setProgress(response.data);
    } catch (error) {
      console.error('Failed to fetch progress:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchDailyChallenge = async () => {
    try {
      const response = await axios.get(`${API}/daily-challenge`);
      setDailyChallenge(response.data);
    } catch (error) {
      console.error('Failed to fetch daily challenge:', error);
    }
  };

  const completionPercentage = progress ? Math.round((progress.completed_challenges / progress.total_challenges) * 100) : 0;

  const stats = [
    {
      icon: <Trophy className="w-6 h-6" />,
      label: "Total Poin",
      value: user?.points || 0,
      color: "text-yellow-400",
      bg: "bg-yellow-500/10"
    },
    {
      icon: <Target className="w-6 h-6" />,
      label: "Challenges Selesai",
      value: `${progress?.completed_challenges || 0}/${progress?.total_challenges || 0}`,
      color: "text-emerald-400",
      bg: "bg-emerald-500/10"
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      label: "Level Saat Ini",
      value: user?.level || "Beginner",
      color: "text-cyan-400",
      bg: "bg-cyan-500/10"
    },
    {
      icon: <Zap className="w-6 h-6" />,
      label: "Progress",
      value: `${completionPercentage}%`,
      color: "text-purple-400",
      bg: "bg-purple-500/10"
    }
  ];

  const getLevelProgress = () => {
    const points = user?.points || 0;
    if (points < 200) return { current: 'Beginner', next: 'Intermediate', progress: (points / 200) * 100 };
    if (points < 500) return { current: 'Intermediate', next: 'Advanced', progress: ((points - 200) / 300) * 100 };
    return { current: 'Advanced', next: 'Master', progress: 100 };
  };

  const levelProgress = getLevelProgress();

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-emerald-400">Loading...</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-8" data-testid="dashboard-container">
        {/* Welcome Section */}
        <div className="relative overflow-hidden rounded-xl bg-gradient-to-r from-emerald-500/10 to-cyan-500/10 p-8 border border-emerald-500/20">
          <div className="relative z-10">
            <h1 className="text-3xl sm:text-4xl font-bold mb-2">
              Selamat Datang, <span className="text-emerald-400">{user?.full_name}</span>!
            </h1>
            <p className="text-gray-400 text-lg">Mari lanjutkan perjalanan belajar social engineering Anda</p>
          </div>
          <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/5 rounded-full blur-3xl"></div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat, index) => (
            <Card key={index} className="glass border-zinc-800 p-6 card-hover" data-testid={`stat-card-${index}`}>
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-gray-400 text-sm mb-2">{stat.label}</p>
                  <p className={`text-3xl font-bold ${stat.color}`}>{stat.value}</p>
                </div>
                <div className={`w-12 h-12 rounded-lg ${stat.bg} flex items-center justify-center ${stat.color}`}>
                  {stat.icon}
                </div>
              </div>
            </Card>
          ))}
        </div>

        {/* Level Progress */}
        <Card className="glass border-zinc-800 p-6" data-testid="level-progress-card">
          <h3 className="text-xl font-semibold mb-4">Progress Level</h3>
          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-gray-400">Level: <span className="text-emerald-400 font-semibold">{levelProgress.current}</span></span>
              <span className="text-gray-400">Target: <span className="text-cyan-400 font-semibold">{levelProgress.next}</span></span>
            </div>
            <Progress value={levelProgress.progress} className="h-3" />
            <p className="text-sm text-gray-400">
              {levelProgress.current === 'Advanced' ? 'Anda sudah mencapai level tertinggi!' : `${Math.round(levelProgress.progress)}% menuju ${levelProgress.next}`}
            </p>
          </div>
        </Card>

        {/* Overall Progress */}
        <Card className="glass border-zinc-800 p-6" data-testid="overall-progress-card">
          <h3 className="text-xl font-semibold mb-4">Progress Challenge</h3>
          <Progress value={completionPercentage} className="h-3 mb-3" />
          <p className="text-gray-400">
            Kamu telah menyelesaikan <span className="text-emerald-400 font-semibold">{progress?.completed_challenges || 0}</span> dari <span className="text-emerald-400 font-semibold">{progress?.total_challenges || 0}</span> challenge
          </p>
        </Card>

        {/* Quick Actions */}
        <div className="grid md:grid-cols-2 gap-6">
          <Link to="/challenges">
            <Card className="glass border-emerald-500/20 p-6 card-hover cursor-pointer" data-testid="quick-action-challenges">
              <Target className="w-8 h-8 text-emerald-400 mb-3" />
              <h3 className="text-xl font-semibold mb-2">Mulai Challenge</h3>
              <p className="text-gray-400">Uji kemampuan Anda dalam mendeteksi social engineering</p>
            </Card>
          </Link>
          <Link to="/leaderboard">
            <Card className="glass border-zinc-800 p-6 card-hover cursor-pointer" data-testid="quick-action-leaderboard">
              <Trophy className="w-8 h-8 text-yellow-400 mb-3" />
              <h3 className="text-xl font-semibold mb-2">Leaderboard</h3>
              <p className="text-gray-400">Lihat posisi Anda di papan peringkat</p>
            </Card>
          </Link>
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;