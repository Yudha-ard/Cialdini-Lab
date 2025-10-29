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
  const [courses, setCourses] = useState([]);
  const [education, setEducation] = useState([]);
  const [users, setUsers] = useState([]);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [showCreateCourseDialog, setShowCreateCourseDialog] = useState(false);
  const [showCreateEducationDialog, setShowCreateEducationDialog] = useState(false);
  const [editingChallenge, setEditingChallenge] = useState(null);
  const [editingCourse, setEditingCourse] = useState(null);
  const [editingEducation, setEditingEducation] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, challengesRes, coursesRes, usersRes] = await Promise.all([
        axios.get(`${API}/admin/stats`, { headers: { Authorization: `Bearer ${token}` } }),
        axios.get(`${API}/challenges`),
        axios.get(`${API}/courses`),
        axios.get(`${API}/admin/users`, { headers: { Authorization: `Bearer ${token}` } })
      ]);
      setStats(statsRes.data);
      setChallenges(challengesRes.data);
      setCourses(coursesRes.data);
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

  const handleDeleteCourse = async (courseId) => {
    if (!confirm('Yakin ingin menghapus course ini?')) return;
    
    try {
      await axios.delete(`${API}/admin/courses/${courseId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success('Course berhasil dihapus');
      fetchData();
    } catch (error) {
      toast.error('Gagal menghapus course');
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

          {/* Courses Tab */}
          <TabsContent value='courses' className='space-y-4 mt-6'>
            <div className='flex justify-between items-center mb-4'>
              <h3 className='text-xl font-semibold'>Manajemen Course</h3>
              <Dialog open={showCreateCourseDialog} onOpenChange={setShowCreateCourseDialog}>
                <DialogTrigger asChild>
                  <Button className='bg-emerald-500 hover:bg-emerald-600'>
                    <Plus className='w-4 h-4 mr-2' /> Create Course
                  </Button>
                </DialogTrigger>
                <DialogContent className='max-w-4xl max-h-[90vh] overflow-y-auto glass border-zinc-800'>
                  <DialogHeader>
                    <DialogTitle>Create New Course</DialogTitle>
                  </DialogHeader>
                  <CourseForm 
                    token={token} 
                    onSuccess={() => { 
                      setShowCreateCourseDialog(false); 
                      fetchData(); 
                    }} 
                  />
                </DialogContent>
              </Dialog>
            </div>
            
            <Card className='glass border-zinc-800 overflow-hidden'>
              <div className='overflow-x-auto'>
                <Table>
                  <TableHeader>
                    <TableRow className='border-zinc-800'>
                      <TableHead>Judul</TableHead>
                      <TableHead>Kategori</TableHead>
                      <TableHead>Tingkat</TableHead>
                      <TableHead>Modules</TableHead>
                      <TableHead>Durasi (min)</TableHead>
                      <TableHead className='text-right'>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {courses.map((course) => (
                      <TableRow key={course.id} className='border-zinc-800'>
                        <TableCell className='font-medium'>{course.title}</TableCell>
                        <TableCell>
                          <span className='px-2 py-1 rounded text-xs bg-purple-500/20 text-purple-400'>
                            {course.category}
                          </span>
                        </TableCell>
                        <TableCell>
                          <span className={`px-2 py-1 rounded text-xs ${
                            course.difficulty === 'beginner' ? 'bg-green-500/20 text-green-400' :
                            course.difficulty === 'intermediate' ? 'bg-yellow-500/20 text-yellow-400' :
                            'bg-red-500/20 text-red-400'
                          }`}>
                            {course.difficulty}
                          </span>
                        </TableCell>
                        <TableCell>{course.modules?.length || 0}</TableCell>
                        <TableCell>{course.total_duration_minutes}</TableCell>
                        <TableCell className='text-right space-x-2'>
                          <Button
                            variant='ghost'
                            size='sm'
                            onClick={() => setEditingCourse(course)}
                          >
                            <Edit className='w-4 h-4' />
                          </Button>
                          <Button
                            variant='ghost'
                            size='sm'
                            onClick={() => handleDeleteCourse(course.id)}
                            className='text-red-400 hover:text-red-300'
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

            {/* Edit Course Dialog */}
            {editingCourse && (
              <Dialog open={!!editingCourse} onOpenChange={() => setEditingCourse(null)}>
                <DialogContent className='max-w-4xl max-h-[90vh] overflow-y-auto glass border-zinc-800'>
                  <DialogHeader>
                    <DialogTitle>Edit Course</DialogTitle>
                  </DialogHeader>
                  <CourseForm 
                    token={token} 
                    courseData={editingCourse}
                    onSuccess={() => { 
                      setEditingCourse(null); 
                      fetchData(); 
                    }} 
                  />
                </DialogContent>
              </Dialog>
            )}
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

// Course Form Component
const CourseForm = ({ token, courseData, onSuccess }) => {
  const [formData, setFormData] = useState(courseData || {
    title: '',
    description: '',
    category: 'social_engineering',
    difficulty: 'beginner',
    modules: [],
    total_duration_minutes: 0,
    prerequisites: [],
    learning_outcomes: [],
    created_by: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      if (courseData) {
        await axios.put(`${API}/admin/courses/${courseData.id}`, formData, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Course berhasil diupdate');
      } else {
        await axios.post(`${API}/admin/courses`, formData, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Course berhasil dibuat');
      }
      onSuccess();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Gagal menyimpan course');
    }
  };

  const addModule = () => {
    setFormData({
      ...formData,
      modules: [
        ...formData.modules,
        {
          module_number: formData.modules.length + 1,
          title: '',
          description: '',
          slides: []
        }
      ]
    });
  };

  const updateModule = (index, field, value) => {
    const newModules = [...formData.modules];
    newModules[index][field] = value;
    setFormData({ ...formData, modules: newModules });
  };

  const removeModule = (index) => {
    const newModules = formData.modules.filter((_, i) => i !== index);
    // Renumber modules
    newModules.forEach((mod, idx) => {
      mod.module_number = idx + 1;
    });
    setFormData({ ...formData, modules: newModules });
  };

  const addSlide = (moduleIndex) => {
    const newModules = [...formData.modules];
    newModules[moduleIndex].slides = [
      ...(newModules[moduleIndex].slides || []),
      {
        title: '',
        content: '',
        code_example: '',
        image_url: ''
      }
    ];
    setFormData({ ...formData, modules: newModules });
  };

  const updateSlide = (moduleIndex, slideIndex, field, value) => {
    const newModules = [...formData.modules];
    newModules[moduleIndex].slides[slideIndex][field] = value;
    setFormData({ ...formData, modules: newModules });
  };

  const removeSlide = (moduleIndex, slideIndex) => {
    const newModules = [...formData.modules];
    newModules[moduleIndex].slides = newModules[moduleIndex].slides.filter((_, i) => i !== slideIndex);
    setFormData({ ...formData, modules: newModules });
  };

  const addPrerequisite = () => {
    setFormData({
      ...formData,
      prerequisites: [...formData.prerequisites, '']
    });
  };

  const updatePrerequisite = (index, value) => {
    const newPrereqs = [...formData.prerequisites];
    newPrereqs[index] = value;
    setFormData({ ...formData, prerequisites: newPrereqs });
  };

  const removePrerequisite = (index) => {
    setFormData({
      ...formData,
      prerequisites: formData.prerequisites.filter((_, i) => i !== index)
    });
  };

  const addLearningOutcome = () => {
    setFormData({
      ...formData,
      learning_outcomes: [...formData.learning_outcomes, '']
    });
  };

  const updateLearningOutcome = (index, value) => {
    const newOutcomes = [...formData.learning_outcomes];
    newOutcomes[index] = value;
    setFormData({ ...formData, learning_outcomes: newOutcomes });
  };

  const removeLearningOutcome = (index) => {
    setFormData({
      ...formData,
      learning_outcomes: formData.learning_outcomes.filter((_, i) => i !== index)
    });
  };

  return (
    <form onSubmit={handleSubmit} className='space-y-6'>
      {/* Basic Info */}
      <div className='space-y-4'>
        <div>
          <Label>Judul Course</Label>
          <Input
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className='bg-zinc-900/50 border-zinc-800 mt-2'
            placeholder='Masukkan judul course'
            required
          />
        </div>

        <div>
          <Label>Deskripsi</Label>
          <Textarea
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className='bg-zinc-900/50 border-zinc-800 mt-2'
            rows={3}
            placeholder='Deskripsi course'
            required
          />
        </div>

        <div className='grid grid-cols-3 gap-4'>
          <div>
            <Label>Kategori</Label>
            <Select value={formData.category} onValueChange={(v) => setFormData({ ...formData, category: v })}>
              <SelectTrigger className='bg-zinc-900/50 border-zinc-800 mt-2'>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value='social_engineering'>Social Engineering</SelectItem>
                <SelectItem value='phishing'>Phishing</SelectItem>
                <SelectItem value='security'>Security Awareness</SelectItem>
                <SelectItem value='psychology'>Psychology</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div>
            <Label>Tingkat</Label>
            <Select value={formData.difficulty} onValueChange={(v) => setFormData({ ...formData, difficulty: v })}>
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
            <Label>Durasi Total (menit)</Label>
            <Input
              type='number'
              value={formData.total_duration_minutes}
              onChange={(e) => setFormData({ ...formData, total_duration_minutes: parseInt(e.target.value) || 0 })}
              className='bg-zinc-900/50 border-zinc-800 mt-2'
              placeholder='60'
              required
            />
          </div>
        </div>
      </div>

      {/* Prerequisites */}
      <div>
        <div className='flex justify-between items-center mb-2'>
          <Label>Prerequisites</Label>
          <Button type='button' onClick={addPrerequisite} size='sm' variant='outline'>
            <Plus className='w-3 h-3 mr-1' /> Add
          </Button>
        </div>
        {formData.prerequisites.map((prereq, idx) => (
          <div key={idx} className='flex gap-2 mb-2'>
            <Input
              value={prereq}
              onChange={(e) => updatePrerequisite(idx, e.target.value)}
              className='bg-zinc-900/50 border-zinc-800'
              placeholder='Prerequisite'
            />
            <Button type='button' onClick={() => removePrerequisite(idx)} size='sm' variant='ghost' className='text-red-400'>
              <Trash2 className='w-4 h-4' />
            </Button>
          </div>
        ))}
      </div>

      {/* Learning Outcomes */}
      <div>
        <div className='flex justify-between items-center mb-2'>
          <Label>Learning Outcomes</Label>
          <Button type='button' onClick={addLearningOutcome} size='sm' variant='outline'>
            <Plus className='w-3 h-3 mr-1' /> Add
          </Button>
        </div>
        {formData.learning_outcomes.map((outcome, idx) => (
          <div key={idx} className='flex gap-2 mb-2'>
            <Input
              value={outcome}
              onChange={(e) => updateLearningOutcome(idx, e.target.value)}
              className='bg-zinc-900/50 border-zinc-800'
              placeholder='Learning outcome'
            />
            <Button type='button' onClick={() => removeLearningOutcome(idx)} size='sm' variant='ghost' className='text-red-400'>
              <Trash2 className='w-4 h-4' />
            </Button>
          </div>
        ))}
      </div>

      {/* Modules */}
      <div>
        <div className='flex justify-between items-center mb-4'>
          <Label className='text-lg font-semibold'>Modules</Label>
          <Button type='button' onClick={addModule} className='bg-emerald-500 hover:bg-emerald-600'>
            <Plus className='w-4 h-4 mr-2' /> Add Module
          </Button>
        </div>

        {formData.modules.map((module, moduleIdx) => (
          <Card key={moduleIdx} className='glass border-zinc-800 p-4 mb-4'>
            <div className='flex justify-between items-start mb-4'>
              <h4 className='font-semibold'>Module {module.module_number}</h4>
              <Button type='button' onClick={() => removeModule(moduleIdx)} size='sm' variant='ghost' className='text-red-400'>
                <Trash2 className='w-4 h-4' />
              </Button>
            </div>

            <div className='space-y-3'>
              <div>
                <Label>Judul Module</Label>
                <Input
                  value={module.title}
                  onChange={(e) => updateModule(moduleIdx, 'title', e.target.value)}
                  className='bg-zinc-900/50 border-zinc-800 mt-2'
                  placeholder='Module title'
                  required
                />
              </div>

              <div>
                <Label>Deskripsi Module</Label>
                <Textarea
                  value={module.description}
                  onChange={(e) => updateModule(moduleIdx, 'description', e.target.value)}
                  className='bg-zinc-900/50 border-zinc-800 mt-2'
                  rows={2}
                  placeholder='Module description'
                  required
                />
              </div>

              {/* Slides */}
              <div className='mt-4'>
                <div className='flex justify-between items-center mb-2'>
                  <Label className='text-sm font-medium'>Slides</Label>
                  <Button type='button' onClick={() => addSlide(moduleIdx)} size='sm' variant='outline'>
                    <Plus className='w-3 h-3 mr-1' /> Add Slide
                  </Button>
                </div>

                {module.slides?.map((slide, slideIdx) => (
                  <Card key={slideIdx} className='bg-zinc-900/30 border-zinc-700 p-3 mb-2'>
                    <div className='flex justify-between items-start mb-3'>
                      <span className='text-xs text-gray-400'>Slide {slideIdx + 1}</span>
                      <Button type='button' onClick={() => removeSlide(moduleIdx, slideIdx)} size='sm' variant='ghost' className='text-red-400 h-6 w-6 p-0'>
                        <Trash2 className='w-3 h-3' />
                      </Button>
                    </div>

                    <div className='space-y-2'>
                      <Input
                        value={slide.title}
                        onChange={(e) => updateSlide(moduleIdx, slideIdx, 'title', e.target.value)}
                        className='bg-zinc-900/50 border-zinc-800'
                        placeholder='Slide title'
                        required
                      />
                      <Textarea
                        value={slide.content}
                        onChange={(e) => updateSlide(moduleIdx, slideIdx, 'content', e.target.value)}
                        className='bg-zinc-900/50 border-zinc-800'
                        rows={2}
                        placeholder='Slide content'
                        required
                      />
                      <Input
                        value={slide.code_example || ''}
                        onChange={(e) => updateSlide(moduleIdx, slideIdx, 'code_example', e.target.value)}
                        className='bg-zinc-900/50 border-zinc-800'
                        placeholder='Code example (optional)'
                      />
                      <Input
                        value={slide.image_url || ''}
                        onChange={(e) => updateSlide(moduleIdx, slideIdx, 'image_url', e.target.value)}
                        className='bg-zinc-900/50 border-zinc-800'
                        placeholder='Image URL (optional)'
                      />
                    </div>
                  </Card>
                ))}
              </div>
            </div>
          </Card>
        ))}
      </div>

      <Button type='submit' className='w-full bg-emerald-600 hover:bg-emerald-700'>
        {courseData ? 'Update Course' : 'Create Course'}
      </Button>
    </form>
  );
};


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
