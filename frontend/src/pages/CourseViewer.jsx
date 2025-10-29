import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { AuthContext, API } from '@/App';
import Layout from '@/components/Layout';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { ChevronLeft, ChevronRight, Clock, CheckCircle } from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';

const CourseViewer = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { token } = React.useContext(AuthContext);
  const [course, setCourse] = useState(null);
  const [currentModuleIndex, setCurrentModuleIndex] = useState(0);
  const [currentSlideIndex, setCurrentSlideIndex] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCourse();
  }, [id]);

  const fetchCourse = async () => {
    try {
      const response = await axios.get(`${API}/courses/${id}`);
      setCourse(response.data);
    } catch (error) {
      toast.error('Gagal load course');
    } finally {
      setLoading(false);
    }
  };

  const nextSlide = () => {
    const currentModule = course.modules[currentModuleIndex];
    if (currentSlideIndex < currentModule.slides.length - 1) {
      setCurrentSlideIndex(currentSlideIndex + 1);
    } else if (currentModuleIndex < course.modules.length - 1) {
      setCurrentModuleIndex(currentModuleIndex + 1);
      setCurrentSlideIndex(0);
    }
  };

  const prevSlide = () => {
    if (currentSlideIndex > 0) {
      setCurrentSlideIndex(currentSlideIndex - 1);
    } else if (currentModuleIndex > 0) {
      setCurrentModuleIndex(currentModuleIndex - 1);
      const prevModule = course.modules[currentModuleIndex - 1];
      setCurrentSlideIndex(prevModule.slides.length - 1);
    }
  };

  if (loading) return <Layout><div className="flex items-center justify-center min-h-screen"><div className="text-emerald-400">Loading...</div></div></Layout>;
  if (!course) return <Layout><div className="text-center py-16"><p className="text-gray-400">Course tidak ditemukan</p></div></Layout>;

  const currentModule = course.modules[currentModuleIndex];
  const currentSlide = currentModule.slides[currentSlideIndex];
  const totalSlides = course.modules.reduce((acc, m) => acc + m.slides.length, 0);
  const currentSlideGlobal = course.modules.slice(0, currentModuleIndex).reduce((acc, m) => acc + m.slides.length, 0) + currentSlideIndex + 1;
  const progressPercent = (currentSlideGlobal / totalSlides) * 100;

  return (
    <Layout>
      <div className="max-w-6xl mx-auto space-y-6">
        <Button variant="ghost" onClick={() => navigate('/courses')} className="text-gray-400 hover:text-gray-200">
          <ChevronLeft className="w-4 h-4 mr-2" />
          Kembali
        </Button>

        <Card className="glass border-zinc-800 p-6">
          <h1 className="text-3xl font-bold mb-2">{course.title}</h1>
          <div className="flex gap-3">
            <Badge className="bg-emerald-500/20 text-emerald-400">{course.difficulty}</Badge>
            <Badge variant="outline"><Clock className="w-3 h-3 mr-1" />{course.total_duration_minutes} min</Badge>
          </div>
        </Card>

        <Card className="glass border-zinc-800 p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-400">Progress</span>
            <span className="text-sm font-semibold text-emerald-400">Slide {currentSlideGlobal}/{totalSlides}</span>
          </div>
          <Progress value={progressPercent} className="h-2" />
        </Card>

        <Badge className="bg-purple-500/20 text-purple-400">Module {currentModuleIndex + 1}: {currentModule.title}</Badge>

        <Card className="glass border-zinc-800 p-8 min-h-[500px]">
          <h2 className="text-3xl font-bold mb-6 text-emerald-400">{currentSlide.title}</h2>
          <div className="prose prose-invert max-w-none text-gray-300 text-lg leading-relaxed whitespace-pre-line">
            {currentSlide.content}
          </div>
        </Card>

        <div className="flex items-center justify-between">
          <Button onClick={prevSlide} disabled={currentModuleIndex === 0 && currentSlideIndex === 0} variant="outline">
            <ChevronLeft className="w-4 h-4 mr-2" />Previous
          </Button>
          {currentModuleIndex === course.modules.length - 1 && currentSlideIndex === currentModule.slides.length - 1 ? (
            <Button className="bg-emerald-600 hover:bg-emerald-700" onClick={() => { toast.success('Course completed! 🎉'); navigate('/courses'); }}>
              <CheckCircle className="w-4 h-4 mr-2" />Complete
            </Button>
          ) : (
            <Button onClick={nextSlide} className="bg-emerald-600 hover:bg-emerald-700">
              Next<ChevronRight className="w-4 h-4 ml-2" />
            </Button>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default CourseViewer;
