import React, { useState, useEffect } from 'react';
import { AuthContext, API } from '@/App';
import Layout from '@/components/Layout';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Trophy, Medal, Award } from 'lucide-react';
import axios from 'axios';

const Leaderboard = () => {
  const { user } = React.useContext(AuthContext);
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      const response = await axios.get(`${API}/leaderboard`);
      setLeaderboard(response.data);
    } catch (error) {
      console.error('Failed to fetch leaderboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const getMedalIcon = (rank) => {
    if (rank === 1) return <Trophy className="w-6 h-6 text-yellow-400" />;
    if (rank === 2) return <Medal className="w-6 h-6 text-gray-400" />;
    if (rank === 3) return <Award className="w-6 h-6 text-amber-600" />;
    return null;
  };

  const getRankBadge = (rank) => {
    if (rank === 1) return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
    if (rank === 2) return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    if (rank === 3) return 'bg-amber-600/20 text-amber-600 border-amber-600/30';
    return 'bg-zinc-800 text-gray-400';
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

  return (
    <Layout>
      <div className="space-y-8" data-testid="leaderboard-container">
        <div>
          <h1 className="text-4xl font-bold mb-3">Leaderboard</h1>
          <p className="text-gray-400 text-lg">Top 10 peserta dengan poin tertinggi</p>
        </div>

        {/* Top 3 Highlight */}
        {leaderboard.length >= 3 && (
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            {/* 2nd Place */}
            <Card className="glass border-zinc-800 p-6 text-center order-1 md:order-1" data-testid="rank-2-card">
              <div className="flex justify-center mb-4">
                <div className="w-20 h-20 rounded-full bg-gray-500/20 flex items-center justify-center border-4 border-gray-500/30">
                  <Medal className="w-10 h-10 text-gray-400" />
                </div>
              </div>
              <Badge className="mb-3 bg-gray-500/20 text-gray-400 border-gray-500/30">Rank #2</Badge>
              <h3 className="text-xl font-bold mb-1">{leaderboard[1].full_name}</h3>
              <p className="text-sm text-gray-400 mb-3">@{leaderboard[1].username}</p>
              <div className="text-3xl font-bold text-gray-400">{leaderboard[1].points}</div>
              <p className="text-sm text-gray-400">points</p>
            </Card>

            {/* 1st Place */}
            <Card className="glass border-yellow-500/30 p-6 text-center md:-mt-4 order-0 md:order-2" data-testid="rank-1-card">
              <div className="flex justify-center mb-4">
                <div className="w-24 h-24 rounded-full bg-yellow-500/20 flex items-center justify-center border-4 border-yellow-500/30 animate-pulse-glow">
                  <Trophy className="w-12 h-12 text-yellow-400" />
                </div>
              </div>
              <Badge className="mb-3 bg-yellow-500/20 text-yellow-400 border-yellow-500/30">Rank #1</Badge>
              <h3 className="text-2xl font-bold mb-1">{leaderboard[0].full_name}</h3>
              <p className="text-sm text-gray-400 mb-3">@{leaderboard[0].username}</p>
              <div className="text-4xl font-bold text-yellow-400">{leaderboard[0].points}</div>
              <p className="text-sm text-gray-400">points</p>
            </Card>

            {/* 3rd Place */}
            <Card className="glass border-zinc-800 p-6 text-center order-2 md:order-3" data-testid="rank-3-card">
              <div className="flex justify-center mb-4">
                <div className="w-20 h-20 rounded-full bg-amber-600/20 flex items-center justify-center border-4 border-amber-600/30">
                  <Award className="w-10 h-10 text-amber-600" />
                </div>
              </div>
              <Badge className="mb-3 bg-amber-600/20 text-amber-600 border-amber-600/30">Rank #3</Badge>
              <h3 className="text-xl font-bold mb-1">{leaderboard[2].full_name}</h3>
              <p className="text-sm text-gray-400 mb-3">@{leaderboard[2].username}</p>
              <div className="text-3xl font-bold text-amber-600">{leaderboard[2].points}</div>
              <p className="text-sm text-gray-400">points</p>
            </Card>
          </div>
        )}

        {/* Full Leaderboard Table */}
        <Card className="glass border-zinc-800 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-zinc-900/50 border-b border-zinc-800">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Rank</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Nama</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Level</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Challenges</th>
                  <th className="px-6 py-4 text-right text-sm font-semibold text-gray-400">Points</th>
                </tr>
              </thead>
              <tbody>
                {leaderboard.map((person, index) => {
                  const rank = index + 1;
                  const isCurrentUser = person.id === user?.id;
                  return (
                    <tr 
                      key={person.id} 
                      className={`border-b border-zinc-800 hover:bg-zinc-900/30 transition-colors ${
                        isCurrentUser ? 'bg-emerald-500/5' : ''
                      }`}
                      data-testid={`leaderboard-row-${rank}`}
                    >
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          {getMedalIcon(rank)}
                          <Badge className={getRankBadge(rank)}>
                            #{rank}
                          </Badge>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div>
                          <p className="font-semibold">
                            {person.full_name}
                            {isCurrentUser && <span className="text-emerald-400 ml-2">(You)</span>}
                          </p>
                          <p className="text-sm text-gray-400">@{person.username}</p>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <Badge variant="outline" className="text-cyan-400 border-cyan-500/30">
                          {person.level}
                        </Badge>
                      </td>
                      <td className="px-6 py-4 text-gray-300">
                        {person.completed_challenges?.length || 0}
                      </td>
                      <td className="px-6 py-4 text-right">
                        <span className="text-xl font-bold text-emerald-400">{person.points}</span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </Card>

        {leaderboard.length === 0 && (
          <div className="text-center py-16">
            <p className="text-gray-400 text-lg">Belum ada data leaderboard</p>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default Leaderboard;