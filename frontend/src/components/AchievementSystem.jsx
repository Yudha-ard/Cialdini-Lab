import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Trophy, Lock, Star, Zap, Target, Award, Crown, Shield } from 'lucide-react';
import confetti from 'canvas-confetti';
import { toast } from 'sonner';

const AchievementSystem = ({ user, completedChallenges = [] }) => {
  const [achievements, setAchievements] = useState([]);
  const [newlyUnlocked, setNewlyUnlocked] = useState([]);

  const allAchievements = [
    {
      id: 'first_blood',
      title: 'First Blood',
      description: 'Selesaikan challenge pertama',
      icon: <Target className="w-6 h-6" />,
      requirement: (user) => (user.completed_challenges?.length || 0) >= 1,
      rarity: 'common',
      points: 10
    },
    {
      id: 'challenger',
      title: 'Challenger',
      description: 'Selesaikan 5 challenges',
      icon: <Shield className="w-6 h-6" />,
      requirement: (user) => (user.completed_challenges?.length || 0) >= 5,
      rarity: 'rare',
      points: 50
    },
    {
      id: 'master',
      title: 'SE Master',
      description: 'Selesaikan 10 challenges',
      icon: <Trophy className="w-6 h-6" />,
      requirement: (user) => (user.completed_challenges?.length || 0) >= 10,
      rarity: 'epic',
      points: 100
    },
    {
      id: 'legend',
      title: 'Legend',
      description: 'Selesaikan semua challenges',
      icon: <Crown className="w-6 h-6" />,
      requirement: (user, totalChallenges) => (user.completed_challenges?.length || 0) >= totalChallenges,
      rarity: 'legendary',
      points: 500
    },
    {
      id: 'speed_demon',
      title: 'Speed Demon',
      description: 'Total 500+ points',
      icon: <Zap className="w-6 h-6" />,
      requirement: (user) => (user.points || 0) >= 500,
      rarity: 'rare',
      points: 75
    },
    {
      id: 'scholar',
      title: 'Scholar',
      description: 'Baca semua materi edukasi',
      icon: <Star className="w-6 h-6" />,
      requirement: (user) => (user.education_read || 0) >= 6, // 6 Cialdini principles
      rarity: 'rare',
      points: 50
    },
    {
      id: 'perfect_score',
      title: 'Perfectionist',
      description: 'Dapatkan perfect score di 3 challenges',
      icon: <Award className="w-6 h-6" />,
      requirement: (user) => (user.perfect_scores || 0) >= 3,
      rarity: 'epic',
      points: 150
    },
    {
      id: 'streak_master',
      title: 'Streak Master',
      description: 'Streak 7 hari berturut-turut',
      icon: <Zap className="w-6 h-6" />,
      requirement: (user) => (user.streak_days || 0) >= 7,
      rarity: 'epic',
      points: 200
    }
  ];

  useEffect(() => {
    if (user && user.id) {
      checkAchievements();
    }
  }, [user, completedChallenges]);

  const checkAchievements = () => {
    if (!user || !user.id) return;
    
    const unlocked = [];
    const newUnlocks = [];
    
    // Total challenges available (26 as per our database)
    const totalChallenges = 26;

    allAchievements.forEach(achievement => {
      const isUnlocked = achievement.requirement(user, totalChallenges);
      
      if (isUnlocked) {
        unlocked.push(achievement);
        
        // Check if this is newly unlocked (not in localStorage)
        const storageKey = `achievement_${user.id}_${achievement.id}`;
        const wasUnlocked = localStorage.getItem(storageKey);
        
        if (!wasUnlocked) {
          newUnlocks.push(achievement);
          localStorage.setItem(storageKey, 'true');
        }
      }
    });

    setAchievements(unlocked);
    
    // Show celebration for new achievements
    if (newUnlocks.length > 0) {
      setNewlyUnlocked(newUnlocks);
      celebrateAchievement(newUnlocks[0]);
    }
  };

  const celebrateAchievement = (achievement) => {
    // Confetti animation
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 },
      colors: getRarityColors(achievement.rarity)
    });

    // Toast notification with custom styling
    toast.success(
      <div className="flex items-start gap-3">
        <div className={`w-12 h-12 rounded-lg ${getRarityBg(achievement.rarity)} flex items-center justify-center`}>
          {achievement.icon}
        </div>
        <div>
          <p className="font-bold">Achievement Unlocked!</p>
          <p className="text-sm">{achievement.title}</p>
          <p className="text-xs text-gray-400">+{achievement.points} points</p>
        </div>
      </div>,
      {
        duration: 5000,
        style: {
          background: '#18181b',
          border: `2px solid ${getRarityColor(achievement.rarity)}`,
        }
      }
    );
  };

  const getRarityColor = (rarity) => {
    const colors = {
      common: '#gray-400',
      rare: '#3b82f6',
      epic: '#a855f7',
      legendary: '#eab308'
    };
    return colors[rarity] || colors.common;
  };

  const getRarityColors = (rarity) => {
    const colorSets = {
      common: ['#9ca3af', '#6b7280'],
      rare: ['#60a5fa', '#3b82f6'],
      epic: ['#c084fc', '#a855f7'],
      legendary: ['#fbbf24', '#f59e0b']
    };
    return colorSets[rarity] || colorSets.common;
  };

  const getRarityBg = (rarity) => {
    const bgs = {
      common: 'bg-gray-500/20',
      rare: 'bg-blue-500/20',
      epic: 'bg-purple-500/20',
      legendary: 'bg-yellow-500/20'
    };
    return bgs[rarity] || bgs.common;
  };

  const getRarityText = (rarity) => {
    const texts = {
      common: 'text-gray-400',
      rare: 'text-blue-400',
      epic: 'text-purple-400',
      legendary: 'text-yellow-400'
    };
    return texts[rarity] || texts.common;
  };

  return (
    <Card className="glass border-zinc-800 p-6">
      <div className="flex items-center gap-3 mb-6">
        <Trophy className="w-6 h-6 text-yellow-400" />
        <div>
          <h3 className="text-xl font-semibold">Achievements</h3>
          <p className="text-sm text-gray-400">{achievements.length}/{allAchievements.length} Unlocked</p>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {allAchievements.map(achievement => {
          const isUnlocked = achievements.find(a => a.id === achievement.id);
          
          return (
            <div
              key={achievement.id}
              className={`relative p-4 rounded-lg border-2 transition-all ${
                isUnlocked
                  ? `${getRarityBg(achievement.rarity)} border-${achievement.rarity === 'legendary' ? 'yellow' : achievement.rarity === 'epic' ? 'purple' : achievement.rarity === 'rare' ? 'blue' : 'gray'}-500/50 hover:scale-105`
                  : 'bg-zinc-900/30 border-zinc-800 opacity-50 grayscale'
              }`}
            >
              {isUnlocked ? (
                <>
                  <div className={`w-12 h-12 mx-auto mb-3 rounded-lg ${getRarityBg(achievement.rarity)} flex items-center justify-center ${getRarityText(achievement.rarity)}`}>
                    {achievement.icon}
                  </div>
                  <h4 className={`font-semibold text-sm text-center mb-1 ${getRarityText(achievement.rarity)}`}>
                    {achievement.title}
                  </h4>
                  <p className="text-xs text-gray-400 text-center mb-2">{achievement.description}</p>
                  <div className="text-center">
                    <Badge variant="outline" className={`text-xs ${getRarityText(achievement.rarity)} border-${achievement.rarity === 'legendary' ? 'yellow' : achievement.rarity === 'epic' ? 'purple' : achievement.rarity === 'rare' ? 'blue' : 'gray'}-500/50`}>
                      {achievement.rarity.toUpperCase()}
                    </Badge>
                  </div>
                </>
              ) : (
                <>
                  <div className="w-12 h-12 mx-auto mb-3 rounded-lg bg-zinc-800 flex items-center justify-center text-gray-600">
                    <Lock className="w-6 h-6" />
                  </div>
                  <h4 className="font-semibold text-sm text-center mb-1 text-gray-500">
                    ???
                  </h4>
                  <p className="text-xs text-gray-600 text-center">Locked</p>
                </>
              )}
            </div>
          );
        })}
      </div>

      {achievements.length > 0 && (
        <div className="mt-6 p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-lg">
          <p className="text-sm text-emerald-400">
            🎉 Total Achievement Points: <span className="font-bold">{achievements.reduce((sum, a) => sum + a.points, 0)}</span>
          </p>
        </div>
      )}
    </Card>
  );
};

export default AchievementSystem;
