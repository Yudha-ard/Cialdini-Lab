import React, { useState, useEffect } from 'react';
import { AuthContext, API } from '@/App';
import Layout from '@/components/Layout';
import { Card } from '@/components/ui/card';
import { Users, Target, Activity } from 'lucide-react';
import axios from 'axios';

const AdminPanel = () => {
  const { token } = React.useContext(AuthContext);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API}/admin/stats`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-emerald-400">Loading...</div>
        </div>
      </Layout>
    );
  }

  const adminStats = [
    {
      icon: <Users className="w-6 h-6" />,
      label: "Total Users",
      value: stats?.total_users || 0,
      color: "text-emerald-400",
      bg: "bg-emerald-500/10"
    },
    {
      icon: <Target className="w-6 h-6" />,
      label: "Total Challenges",
      value: stats?.total_challenges || 0,
      color: "text-cyan-400",
      bg: "bg-cyan-500/10"
    },
    {
      icon: <Activity className="w-6 h-6" />,
      label: "Total Attempts",
      value: stats?.total_attempts || 0,
      color: "text-purple-400",
      bg: "bg-purple-500/10"
    }
  ];

  return (
    <Layout>
      <div className="space-y-8" data-testid="admin-panel-container">
        <div>
          <h1 className="text-4xl font-bold mb-3">Admin Panel</h1>
          <p className="text-gray-400 text-lg">Statistik dan manajemen platform</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {adminStats.map((stat, index) => (
            <Card key={index} className="glass border-zinc-800 p-6" data-testid={`admin-stat-card-${index}`}>
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

        <Card className="glass border-zinc-800 p-8">
          <h3 className="text-xl font-semibold mb-4">Informasi</h3>
          <p className="text-gray-400">
            Panel admin untuk mengelola platform Tegalsec Lab. Fitur tambahan seperti manajemen challenge dan user dapat ditambahkan sesuai kebutuhan.
          </p>
        </Card>
      </div>
    </Layout>
  );
};

export default AdminPanel;