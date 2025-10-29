import React, { useState, useEffect } from 'react';
import { AuthContext, API } from '@/App';
import Layout from '@/components/Layout';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Users, Target, Activity, MessageSquare, Plus, Edit, Trash2, TrendingUp } from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';

const AdminPanelNew = () => {
  const { token } = React.useContext(AuthContext);
  const [stats, setStats] = useState(null);
  const [challenges, setChallenges] = useState([]);
  const [users, setUsers] = useState([]);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [editingChallenge, setEditingChallenge] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, challengesRes, usersRes] = await Promise.all([
        axios.get(`${API}/admin/stats`, { headers: { Authorization: `Bearer ${token}` } }),
        axios.get(`${API}/challenges`),
        axios.get(`${API}/admin/users`, { headers: { Authorization: `Bearer ${token}` } })
      ]);
      setStats(statsRes.data);
      setChallenges(challengesRes.data);
      setUsers(usersRes.data);
    } catch (error) {
      toast.error('Gagal load data admin');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteChallenge = async (challengeId) => {
    if (!confirm('Yakin ingin menghapus challenge ini?')) return;
    
    try {
      await axios.delete(`${API}/admin/challenges/${challengeId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success('Challenge berhasil dihapus');
      fetchData();
    } catch (error) {
      toast.error('Gagal menghapus challenge');
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className='flex items-center justify-center min-h-screen'>
          <div className='text-emerald-400'>Loading...</div>
        </div>
      </Layout>
    );
  }

  const adminStats = [
    {
      icon: <Users className='w-6 h-6' />,
      label: 'Total Users',
      value: stats?.total_users || 0,
      color: 'text-emerald-400',
      bg: 'bg-emerald-500/10'
    },
    {
      icon: <Target className='w-6 h-6' />,
      label: 'Total Challenges',
      value: stats?.total_challenges || 0,
      color: 'text-cyan-400',
      bg: 'bg-cyan-500/10'
    },
    {
      icon: <Activity className='w-6 h-6' />,
      label: 'Total Attempts',
      value: stats?.total_attempts || 0,
      color: 'text-purple-400',
      bg: 'bg-purple-500/10'
    },
    {
      icon: <MessageSquare className='w-6 h-6' />,
      label: 'Total Feedbacks',
      value: stats?.total_feedbacks || 0,
      color: 'text-yellow-400',
      bg: 'bg-yellow-500/10'
    }
  ];

  return (
    <Layout>
      <div className='space-y-8' data-testid='admin-panel-container'>
        <div className='flex items-center justify-between'>
          <div>
            <h1 className='text-4xl font-bold mb-3'>Admin Panel</h1>
            <p className='text-gray-400 text-lg'>Kelola platform Tegalsec Lab</p>
          </div>
          <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
            <DialogTrigger asChild>
              <Button className='bg-emerald-600 hover:bg-emerald-700' data-testid='create-challenge-button'>
                <Plus className='w-4 h-4 mr-2' />
                Buat Challenge Baru
              </Button>
            </DialogTrigger>
            <DialogContent className='max-w-4xl max-h-[90vh] overflow-y-auto bg-zinc-950 border-zinc-800'>
              <DialogHeader>
                <DialogTitle className='text-2xl'>Buat Challenge Baru</DialogTitle>
              </DialogHeader>
              <ChallengeForm 
                token={token} 
                onSuccess={() => { 
                  setShowCreateDialog(false); 
                  fetchData(); 
                }} 
              />
            </DialogContent>
          </Dialog>
        </div>

        {/* Stats Grid */}
        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6'>
          {adminStats.map((stat, index) => (
            <Card key={index} className='glass border-zinc-800 p-6 card-hover' data-testid={`admin-stat-${index}`}>
              <div className='flex items-start justify-between'>
                <div>
                  <p className='text-gray-400 text-sm mb-2'>{stat.label}</p>
                  <p className={`text-3xl font-bold ${stat.color}`}>{stat.value}</p>
                </div>
                <div className={`w-12 h-12 rounded-lg ${stat.bg} flex items-center justify-center ${stat.color}`}>
                  {stat.icon}
                </div>
              </div>
            </Card>
          ))}
        </div>

        {/* Tabs */}
        <Tabs defaultValue='challenges' className='w-full'>
          <TabsList className='grid w-full grid-cols-4 bg-zinc-900/50'>
            <TabsTrigger value='challenges'>Challenges</TabsTrigger>
            <TabsTrigger value='courses'>Courses</TabsTrigger>
            <TabsTrigger value='users'>Users</TabsTrigger>
            <TabsTrigger value='activity'>Recent Activity</TabsTrigger>
          </TabsList>

          {/* Challenges Tab */}
          <TabsContent value='challenges' className='space-y-4 mt-6'>
            <Card className='glass border-zinc-800 overflow-hidden'>
              <div className='overflow-x-auto'>
                <Table>
                  <TableHeader>
                    <TableRow className='border-zinc-800'>
                      <TableHead>Title</TableHead>
                      <TableHead>Category</TableHead>
                      <TableHead>Difficulty</TableHead>
                      <TableHead>Points</TableHead>
                      <TableHead>Questions</TableHead>
                      <TableHead className='text-right'>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {challenges.map((challenge) => (
                      <TableRow key={challenge.id} className='border-zinc-800'>
                        <TableCell className='font-medium'>{challenge.title}</TableCell>
                        <TableCell>{challenge.category}</TableCell>
                        <TableCell>
                          <span className={`px-2 py-1 rounded text-xs ${
                            challenge.difficulty === 'beginner' ? 'bg-emerald-500/20 text-emerald-400' :
                            challenge.difficulty === 'intermediate' ? 'bg-yellow-500/20 text-yellow-400' :
                            'bg-red-500/20 text-red-400'
                          }`}>
                            {challenge.difficulty}
                          </span>
                        </TableCell>
                        <TableCell>{challenge.points}</TableCell>
                        <TableCell>{challenge.questions?.length || 0}</TableCell>
                        <TableCell className='text-right space-x-2'>
                          <Button
                            variant='ghost'
                            size='sm'
                            onClick={() => setEditingChallenge(challenge)}
                            data-testid={`edit-challenge-${challenge.id}`}
                          >
                            <Edit className='w-4 h-4' />
                          </Button>
                          <Button
                            variant='ghost'
                            size='sm'
                            onClick={() => handleDeleteChallenge(challenge.id)}
                            className='text-red-400 hover:text-red-300'
                            data-testid={`delete-challenge-${challenge.id}`}
                          >
                            <Trash2 className='w-4 h-4' />
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </Card>
          </TabsContent>

          {/* Users Tab */}
          <TabsContent value='users' className='space-y-4 mt-6'>
            <Card className='glass border-zinc-800 overflow-hidden'>
              <div className='overflow-x-auto'>
                <Table>
                  <TableHeader>
                    <TableRow className='border-zinc-800'>
                      <TableHead>Username</TableHead>
                      <TableHead>Full Name</TableHead>
                      <TableHead>Email</TableHead>
                      <TableHead>Role</TableHead>
                      <TableHead>Level</TableHead>
                      <TableHead>Points</TableHead>
                      <TableHead>Completed</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {users.map((user) => (
                      <TableRow key={user.id} className='border-zinc-800'>
                        <TableCell className='font-medium'>@{user.username}</TableCell>
                        <TableCell>{user.full_name}</TableCell>
                        <TableCell>{user.email}</TableCell>
                        <TableCell>
                          <span className={`px-2 py-1 rounded text-xs ${
                            user.role === 'admin' ? 'bg-red-500/20 text-red-400' : 'bg-blue-500/20 text-blue-400'
                          }`}>
                            {user.role}
                          </span>
                        </TableCell>
                        <TableCell>{user.level}</TableCell>
                        <TableCell className='text-emerald-400 font-semibold'>{user.points}</TableCell>
                        <TableCell>{user.completed_challenges?.length || 0}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </Card>
          </TabsContent>

          {/* Activity Tab */}
          <TabsContent value='activity' className='space-y-6 mt-6'>
            <Card className='glass border-zinc-800 p-6'>
              <h3 className='text-xl font-semibold mb-4 flex items-center gap-2'>
                <TrendingUp className='w-5 h-5 text-emerald-400' />
                Recent Attempts
              </h3>
              <div className='space-y-3'>
                {stats?.recent_attempts?.slice(0, 5).map((attempt, idx) => (
                  <div key={idx} className='bg-zinc-900/50 p-4 rounded-lg'>
                    <div className='flex items-center justify-between'>
                      <div>
                        <p className='text-sm text-gray-400'>User ID: {attempt.user_id.slice(0, 8)}...</p>
                        <p className='font-semibold'>{attempt.correct_count}/{attempt.total_questions} correct</p>
                      </div>
                      <span className={`text-sm font-semibold ${
                        attempt.is_completed ? 'text-emerald-400' : 'text-yellow-400'
                      }`}>
                        +{attempt.points_earned} pts
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </Card>

            <Card className='glass border-zinc-800 p-6'>
              <h3 className='text-xl font-semibold mb-4 flex items-center gap-2'>
                <MessageSquare className='w-5 h-5 text-cyan-400' />
                Recent Feedbacks
              </h3>
              <div className='space-y-3'>
                {stats?.recent_feedbacks?.slice(0, 5).map((feedback, idx) => (
                  <div key={idx} className='bg-zinc-900/50 p-4 rounded-lg'>
                    <div className='flex items-center justify-between mb-2'>
                      <span className='font-semibold'>@{feedback.username}</span>
                      <div className='flex gap-1'>
                        {[...Array(5)].map((_, i) => (
                          <span key={i} className={i < feedback.rating ? 'text-yellow-400' : 'text-gray-600'}>★</span>
                        ))}
                      </div>
                    </div>
                    <p className='text-sm text-gray-400'>{feedback.comment}</p>
                  </div>
                ))}
              </div>
            </Card>
          </TabsContent>
        </Tabs>
      </div>

      {/* Edit Dialog */}
      {editingChallenge && (
        <Dialog open={!!editingChallenge} onOpenChange={() => setEditingChallenge(null)}>
          <DialogContent className='max-w-4xl max-h-[90vh] overflow-y-auto bg-zinc-950 border-zinc-800'>
            <DialogHeader>
              <DialogTitle className='text-2xl'>Edit Challenge</DialogTitle>
            </DialogHeader>
            <ChallengeForm 
              token={token}
              challenge={editingChallenge}
              onSuccess={() => { 
                setEditingChallenge(null); 
                fetchData(); 
              }} 
            />
          </DialogContent>
        </Dialog>
      )}
    </Layout>
  );
};

// Challenge Form Component
const ChallengeForm = ({ token, challenge, onSuccess }) => {
  const [formData, setFormData] = useState(challenge || {
    title: '',
    category: 'phishing',
    difficulty: 'beginner',
    cialdini_principle: 'authority',
    challenge_type: 'multi_choice',
    description: '',
    scenario: '',
    questions: [{ question: '', options: ['', '', '', ''], correct_answer: 0, explanation: '' }],
    points: 50,
    tips: [''],
    real_case_reference: '',
    time_limit_seconds: 180
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      if (challenge) {
        await axios.put(`${API}/admin/challenges/${challenge.id}`, formData, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Challenge berhasil diupdate');
      } else {
        await axios.post(`${API}/admin/challenges`, formData, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Challenge berhasil dibuat');
      }
      onSuccess();
    } catch (error) {
      toast.error('Gagal menyimpan challenge');
    }
  };

  const addQuestion = () => {
    setFormData({
      ...formData,
      questions: [...formData.questions, { question: '', options: ['', '', '', ''], correct_answer: 0, explanation: '' }]
    });
  };

  const updateQuestion = (index, field, value) => {
    const newQuestions = [...formData.questions];
    newQuestions[index] = { ...newQuestions[index], [field]: value };
    setFormData({ ...formData, questions: newQuestions });
  };

  return (
    <form onSubmit={handleSubmit} className='space-y-6'>
      <div className='grid md:grid-cols-2 gap-4'>
        <div>
          <Label>Title</Label>
          <Input
            value={formData.title}
            onChange={(e) => setFormData({...formData, title: e.target.value})}
            className='bg-zinc-900/50 border-zinc-800 mt-2'
            required
          />
        </div>
        <div>
          <Label>Category</Label>
          <Select value={formData.category} onValueChange={(v) => setFormData({...formData, category: v})}>
            <SelectTrigger className='bg-zinc-900/50 border-zinc-800 mt-2'>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value='phishing'>Phishing</SelectItem>
              <SelectItem value='pretexting'>Pretexting</SelectItem>
              <SelectItem value='baiting'>Baiting</SelectItem>
              <SelectItem value='quid_pro_quo'>Quid Pro Quo</SelectItem>
              <SelectItem value='tailgating'>Tailgating</SelectItem>
              <SelectItem value='money_app'>Money App</SelectItem>
              <SelectItem value='indonesian_case'>Indonesian Case</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className='grid md:grid-cols-3 gap-4'>
        <div>
          <Label>Difficulty</Label>
          <Select value={formData.difficulty} onValueChange={(v) => setFormData({...formData, difficulty: v})}>
            <SelectTrigger className='bg-zinc-900/50 border-zinc-800 mt-2'>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value='beginner'>Beginner</SelectItem>
              <SelectItem value='intermediate'>Intermediate</SelectItem>
              <SelectItem value='advanced'>Advanced</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div>
          <Label>Cialdini Principle</Label>
          <Select value={formData.cialdini_principle} onValueChange={(v) => setFormData({...formData, cialdini_principle: v})}>
            <SelectTrigger className='bg-zinc-900/50 border-zinc-800 mt-2'>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value='authority'>Authority</SelectItem>
              <SelectItem value='reciprocity'>Reciprocity</SelectItem>
              <SelectItem value='scarcity'>Scarcity</SelectItem>
              <SelectItem value='social_proof'>Social Proof</SelectItem>
              <SelectItem value='liking'>Liking</SelectItem>
              <SelectItem value='commitment'>Commitment</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div>
          <Label>Points</Label>
          <Input
            type='number'
            value={formData.points}
            onChange={(e) => setFormData({...formData, points: parseInt(e.target.value)})}
            className='bg-zinc-900/50 border-zinc-800 mt-2'
          />
        </div>
      </div>

      <div>
        <Label>Description</Label>
        <Textarea
          value={formData.description}
          onChange={(e) => setFormData({...formData, description: e.target.value})}
          className='bg-zinc-900/50 border-zinc-800 mt-2 min-h-20'
          required
        />
      </div>

      <div>
        <Label>Scenario</Label>
        <Textarea
          value={formData.scenario}
          onChange={(e) => setFormData({...formData, scenario: e.target.value})}
          className='bg-zinc-900/50 border-zinc-800 mt-2 min-h-32'
          required
        />
      </div>

      {/* Questions */}
      <div className='space-y-4'>
        <div className='flex items-center justify-between'>
          <Label className='text-lg'>Questions</Label>
          <Button type='button' onClick={addQuestion} variant='outline' size='sm'>
            <Plus className='w-4 h-4 mr-2' />
            Add Question
          </Button>
        </div>

        {formData.questions.map((q, idx) => (
          <Card key={idx} className='bg-zinc-900/30 border-zinc-800 p-4 space-y-3'>
            <Label>Question {idx + 1}</Label>
            <Textarea
              value={q.question}
              onChange={(e) => updateQuestion(idx, 'question', e.target.value)}
              className='bg-zinc-900/50 border-zinc-800'
              placeholder='Enter question'
            />
            
            <Label>Options</Label>
            {q.options.map((opt, oIdx) => (
              <Input
                key={oIdx}
                value={opt}
                onChange={(e) => {
                  const newOptions = [...q.options];
                  newOptions[oIdx] = e.target.value;
                  updateQuestion(idx, 'options', newOptions);
                }}
                className='bg-zinc-900/50 border-zinc-800'
                placeholder={`Option ${oIdx + 1}`}
              />
            ))}
            
            <div className='grid grid-cols-2 gap-4'>
              <div>
                <Label>Correct Answer (index)</Label>
                <Input
                  type='number'
                  value={q.correct_answer}
                  onChange={(e) => updateQuestion(idx, 'correct_answer', parseInt(e.target.value))}
                  className='bg-zinc-900/50 border-zinc-800 mt-2'
                  min='0'
                  max='3'
                />
              </div>
            </div>

            <div>
              <Label>Explanation</Label>
              <Textarea
                value={q.explanation}
                onChange={(e) => updateQuestion(idx, 'explanation', e.target.value)}
                className='bg-zinc-900/50 border-zinc-800 mt-2'
                placeholder='Explain why this is the correct answer'
              />
            </div>
          </Card>
        ))}
      </div>

      <Button type='submit' className='w-full bg-emerald-600 hover:bg-emerald-700'>
        {challenge ? 'Update Challenge' : 'Create Challenge'}
      </Button>
    </form>
  );
};

export default AdminPanelNew;
