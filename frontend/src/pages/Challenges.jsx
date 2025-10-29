import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext, API } from '@/App';
import Layout from '@/components/Layout';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Shield, Lock, FileText, Gift, Users, Smartphone, TrendingUp, ChevronRight, Heart, Handshake, Star, Crown, Zap, Clock } from 'lucide-react';
import axios from 'axios';

const Challenges = () => {
  const { user, token } = React.useContext(AuthContext);
  const [challenges, setChallenges] = useState([]);
  const [filteredChallenges, setFilteredChallenges] = useState([]);
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [difficultyFilter, setDifficultyFilter] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchChallenges();
  }, []);

  useEffect(() => {
    filterChallenges();
  }, [challenges, categoryFilter, difficultyFilter]);

  const fetchChallenges = async () => {
    try {
      const response = await axios.get(`${API}/challenges`);
      setChallenges(response.data);
    } catch (error) {
      console.error('Failed to fetch challenges:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterChallenges = () => {
    let filtered = challenges;
    
    if (categoryFilter !== 'all') {
      filtered = filtered.filter(c => c.category === categoryFilter);
    }
    
    if (difficultyFilter !== 'all') {
      filtered = filtered.filter(c => c.difficulty === difficultyFilter);
    }
    
    setFilteredChallenges(filtered);
  };

  const groupByCialdini = () => {
    const grouped = {
      reciprocity: [],
      commitment: [],
      social_proof: [],
      authority: [],
      liking: [],
      scarcity: []
    };
    
    challenges.forEach(challenge => {
      const principle = challenge.cialdini_principle;
      if (grouped[principle]) {
        grouped[principle].push(challenge);
      }
    });
    
    return grouped;
  };

  const getCialdiniIcon = (principle) => {
    const icons = {
      reciprocity: <Gift className="w-5 h-5" />,
      commitment: <Handshake className="w-5 h-5" />,
      social_proof: <Users className="w-5 h-5" />,
      authority: <Crown className="w-5 h-5" />,
      liking: <Heart className="w-5 h-5" />,
      scarcity: <Zap className="w-5 h-5" />
    };
    return icons[principle] || <Star className="w-5 h-5" />;
  };

  const getCialdiniLabel = (principle) => {
    const labels = {
      reciprocity: "Reciprocity (Timbal Balik)",
      commitment: "Commitment & Consistency (Komitmen)",
      social_proof: "Social Proof (Bukti Sosial)",
      authority: "Authority (Otoritas)",
      liking: "Liking (Kesukaan)",
      scarcity: "Scarcity (Kelangkaan)"
    };
    return labels[principle] || principle;
  };

  const getCialdiniDescription = (principle) => {
    const descriptions = {
      reciprocity: "Orang merasa wajib membalas kebaikan yang diterima",
      commitment: "Orang cenderung konsisten dengan komitmen awal mereka",
      social_proof: "Orang mengikuti tindakan orang lain",
      authority: "Orang cenderung patuh pada figur otoritas",
      liking: "Orang lebih mudah dipengaruhi oleh orang yang mereka sukai",
      scarcity: "Orang menghargai hal yang langka atau terbatas"
    };
    return descriptions[principle] || "";
  };


  const getCategoryIcon = (category) => {
    const icons = {
      phishing: <Shield className="w-5 h-5" />,
      pretexting: <Users className="w-5 h-5" />,
      baiting: <FileText className="w-5 h-5" />,
      quid_pro_quo: <Gift className="w-5 h-5" />,
      tailgating: <Lock className="w-5 h-5" />,
      money_app: <Smartphone className="w-5 h-5" />,
      indonesian_case: <TrendingUp className="w-5 h-5" />
    };
    return icons[category] || <Shield className="w-5 h-5" />;
  };

  const getCategoryLabel = (category) => {
    const labels = {
      phishing: "Phishing",
      pretexting: "Pretexting",
      baiting: "Baiting",
      quid_pro_quo: "Quid Pro Quo",
      tailgating: "Tailgating",
      money_app: "Aplikasi Uang",
      indonesian_case: "Kasus Indonesia"
    };
    return labels[category] || category;
  };

  const getDifficultyColor = (difficulty) => {
    const colors = {
      beginner: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
      intermediate: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
      advanced: "bg-red-500/20 text-red-400 border-red-500/30"
    };
    return colors[difficulty] || colors.beginner;
  };

  const getDifficultyLabel = (difficulty) => {
    const labels = {
      beginner: "Pemula",
      intermediate: "Menengah",
      advanced: "Lanjutan"
    };
    return labels[difficulty] || difficulty;
  };

  const isCompleted = (challengeId) => {
    return user?.completed_challenges?.includes(challengeId);
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
      <div className="space-y-8" data-testid="challenges-container">
        <div>
          <h1 className="text-4xl font-bold mb-3">Challenges</h1>
          <p className="text-gray-400 text-lg">Pilih challenge dan uji kemampuan Anda dalam mendeteksi social engineering</p>
        </div>

        {/* Filters */}
        <Card className="glass border-zinc-800 p-6">
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm text-gray-400 mb-2 block">Kategori</label>
              <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                <SelectTrigger className="bg-zinc-900/50 border-zinc-800" data-testid="category-filter">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Semua Kategori</SelectItem>
                  <SelectItem value="phishing">Phishing</SelectItem>
                  <SelectItem value="pretexting">Pretexting</SelectItem>
                  <SelectItem value="baiting">Baiting</SelectItem>
                  <SelectItem value="quid_pro_quo">Quid Pro Quo</SelectItem>
                  <SelectItem value="tailgating">Tailgating</SelectItem>
                  <SelectItem value="money_app">Aplikasi Uang</SelectItem>
                  <SelectItem value="indonesian_case">Kasus Indonesia</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="text-sm text-gray-400 mb-2 block">Kesulitan</label>
              <Select value={difficultyFilter} onValueChange={setDifficultyFilter}>
                <SelectTrigger className="bg-zinc-900/50 border-zinc-800" data-testid="difficulty-filter">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Semua Level</SelectItem>
                  <SelectItem value="beginner">Pemula</SelectItem>
                  <SelectItem value="intermediate">Menengah</SelectItem>
                  <SelectItem value="advanced">Lanjutan</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </Card>

        {/* Challenges Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredChallenges.map((challenge) => (
            <Card 
              key={challenge.id} 
              className={`glass border-zinc-800 p-6 card-hover relative overflow-hidden ${
                isCompleted(challenge.id) ? 'border-emerald-500/30' : ''
              }`}
              data-testid={`challenge-card-${challenge.id}`}
            >
              {isCompleted(challenge.id) && (
                <div className="absolute top-4 right-4">
                  <Badge className="bg-emerald-500/20 text-emerald-400 border-emerald-500/30">
                    ✓ Selesai
                  </Badge>
                </div>
              )}
              
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-lg bg-emerald-500/10 flex items-center justify-center text-emerald-400">
                  {getCategoryIcon(challenge.category)}
                </div>
                <div className="flex-1">
                  <Badge variant="outline" className="text-xs">
                    {getCategoryLabel(challenge.category)}
                  </Badge>
                </div>
              </div>

              <h3 className="text-xl font-semibold mb-2">{challenge.title}</h3>
              <p className="text-gray-400 text-sm mb-4 line-clamp-2">{challenge.description}</p>

              <div className="flex items-center justify-between mb-4">
                <Badge className={getDifficultyColor(challenge.difficulty)}>
                  {getDifficultyLabel(challenge.difficulty)}
                </Badge>
                <span className="text-yellow-400 font-semibold">{challenge.points} pts</span>
              </div>

              <Link to={`/challenges/${challenge.id}`}>
                <Button className="w-full bg-emerald-600 hover:bg-emerald-700 btn-cyber" data-testid={`start-challenge-${challenge.id}`}>
                  {isCompleted(challenge.id) ? 'Lihat Lagi' : 'Mulai Challenge'}
                  <ChevronRight className="ml-2 w-4 h-4" />
                </Button>
              </Link>
            </Card>
          ))}
        </div>

        {filteredChallenges.length === 0 && (
          <div className="text-center py-16">
            <p className="text-gray-400 text-lg">Tidak ada challenge yang sesuai dengan filter</p>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default Challenges;