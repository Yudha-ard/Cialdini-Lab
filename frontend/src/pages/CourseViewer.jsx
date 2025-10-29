import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { AuthContext, API } from '@/App';
import Layout from '@/components/Layout';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { ChevronLeft, ChevronRight, BookOpen, Clock, Award, CheckCircle } from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';

const CourseViewer = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { token } = React.useContext(AuthContext);
  const [course, setCourse] = useState(null);
  const [progress, setProgress] = useState(null);
  const [currentModuleIndex, setCurrentModuleIndex] = useState(0);
  const [currentSlideIndex, setCurrentSlideIndex] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCourse();
    fetchProgress();
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

  const fetchProgress = async () => {
    try {
      const response = await axios.get(`${API}/courses/${id}/progress`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setProgress(response.data);
    } catch (error) {
      console.error('Failed to fetch progress');
    }
  };

  const updateProgress = async () => {
    try {
      await axios.post(`${API}/courses/${id}/progress`, {
        module_number: currentModuleIndex + 1,
        slide_number: currentSlideIndex
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchProgress();
    } catch (error) {
      console.error('Failed to update progress');
    }
  };

  const nextSlide = () => {
    const currentModule = course.modules[currentModuleIndex];
    if (currentSlideIndex < currentModule.slides.length - 1) {
      setCurrentSlideIndex(currentSlideIndex + 1);
      updateProgress();
    } else if (currentModuleIndex < course.modules.length - 1) {
      setCurrentModuleIndex(currentModuleIndex + 1);
      setCurrentSlideIndex(0);
      updateProgress();
    }
  };

  const prevSlide = () => {
    if (currentSlideIndex > 0) {
      setCurrentSlideIndex(currentSlideIndex - 1);
    } else if (currentModuleIndex > 0) {
      setCurrentModuleIndex(currentModuleIndex - 1);
      setCurrentSlideIndex(course.modules[currentModuleIndex - 1].slides.length - 1);
    }
  };

  if (loading) return <Layout><div className=\"flex items-center justify-center min-h-screen\"><div className=\"text-emerald-400\">Loading...</div></div></Layout>;
  if (!course) return <Layout><div className=\"text-center py-16\"><p className=\"text-gray-400\">Course tidak ditemukan</p></div></Layout>;

  const currentModule = course.modules[currentModuleIndex];
  const currentSlide = currentModule.slides[currentSlideIndex];
  const totalSlides = course.modules.reduce((acc, m) => acc + m.slides.length, 0);
  const currentSlideGlobal = course.modules.slice(0, currentModuleIndex).reduce((acc, m) => acc + m.slides.length, 0) + currentSlideIndex + 1;
  const progressPercent = (currentSlideGlobal / totalSlides) * 100;

  return (
    <Layout>
      <div className=\"max-w-6xl mx-auto space-y-6\" data-testid=\"course-viewer\">
        <Button 
          variant=\"ghost\" 
          onClick={() => navigate('/courses')}
          className=\"text-gray-400 hover:text-gray-200\"
        >
          <ChevronLeft className=\"w-4 h-4 mr-2\" />
          Kembali ke Courses
        </Button>

        {/* Course Header */}
        <Card className=\"glass border-zinc-800 p-6\">
          <div className=\"flex items-start justify-between\">
            <div className=\"flex-1\">
              <h1 className=\"text-3xl font-bold mb-2\">{course.title}</h1>
              <p className=\"text-gray-400 mb-4\">{course.description}</p>
              <div className=\"flex gap-3\">
                <Badge className=\"bg-emerald-500/20 text-emerald-400\">{course.difficulty}</Badge>
                <Badge variant=\"outline\" className=\"text-cyan-400\">
                  <Clock className=\"w-3 h-3 mr-1\" />
                  {course.total_duration_minutes} min
                </Badge>
                <Badge variant=\"outline\" className=\"text-purple-400\">
                  {course.modules.length} Modules
                </Badge>
              </div>
            </div>
          </div>
        </Card>

        {/* Progress Bar */}
        <Card className=\"glass border-zinc-800 p-4\">
          <div className=\"flex items-center justify-between mb-2\">
            <span className=\"text-sm text-gray-400\">Progress Course</span>
            <span className=\"text-sm font-semibold text-emerald-400\">
              Slide {currentSlideGlobal}/{totalSlides}
            </span>
          </div>
          <Progress value={progressPercent} className=\"h-2\" />
        </Card>

        {/* Current Module Badge */}
        <div className=\"flex items-center gap-3\">
          <Badge className=\"bg-purple-500/20 text-purple-400 border-purple-500/30 text-sm\">
            Module {currentModuleIndex + 1}: {currentModule.title}
          </Badge>
          <span className=\"text-gray-400 text-sm\">
            Slide {currentSlideIndex + 1} dari {currentModule.slides.length}
          </span>
        </div>

        {/* Slide Content */}
        <Card className=\"glass border-zinc-800 p-8 min-h-[500px]\">
          <h2 className=\"text-3xl font-bold mb-6 text-emerald-400\">{currentSlide.title}</h2>
          
          <div className=\"prose prose-invert max-w-none\">
            {currentSlide.content.split('\
\
').map((paragraph, idx) => {
              // Check if heading (bold)
              if (paragraph.startsWith('**') && paragraph.includes(':**')) {
                const parts = paragraph.split(':**');
                const heading = parts[0].replace(/\*\*/g, '');
                const content = parts[1];
                return (
                  <div key={idx} className=\"mb-6\">
                    <h3 className=\"text-xl font-bold text-cyan-400 mb-3\">{heading}:</h3>
                    {content && <p className=\"text-gray-300 leading-relaxed\">{content}</p>}
                  </div>
                );
              }
              
              // Bullet list
              if (paragraph.includes('\
-') || paragraph.includes('\
✓')) {
                const items = paragraph.split('\
').filter(line => line.trim());
                return (
                  <ul key={idx} className=\"space-y-2 mb-6\">
                    {items.map((item, itemIdx) => {
                      if (item.startsWith('-') || item.startsWith('✓')) {
                        return (
                          <li key={itemIdx} className=\"flex items-start gap-3 text-gray-300\">
                            <span className=\"text-emerald-400 mt-1\">•</span>
                            <span>{item.replace(/^[-✓]\\s*/, '')}</span>
                          </li>
                        );
                      }
                      if (item.startsWith('**')) {
                        return <p key={itemIdx} className=\"font-semibold text-white mt-4\">{item.replace(/\*\*/g, '')}</p>;
                      }
                      return null;
                    })}
                  </ul>
                );
              }
              
              // Regular paragraph
              return (
                <p key={idx} className=\"text-gray-300 leading-relaxed mb-4 text-lg whitespace-pre-line\">
                  {paragraph}
                </p>
              );
            })}
          </div>

          {currentSlide.code_example && (
            <Card className=\"bg-zinc-900/50 border-zinc-800 p-4 mt-6\">
              <pre className=\"text-emerald-400 text-sm overflow-x-auto\">
                <code>{currentSlide.code_example}</code>
              </pre>
            </Card>
          )}
        </Card>

        {/* Navigation */}
        <div className=\"flex items-center justify-between\">
          <Button
            onClick={prevSlide}
            disabled={currentModuleIndex === 0 && currentSlideIndex === 0}
            variant=\"outline\"
            className=\"border-zinc-700\"
          >
            <ChevronLeft className=\"w-4 h-4 mr-2\" />
            Previous
          </Button>

          {currentModuleIndex === course.modules.length - 1 && 
           currentSlideIndex === currentModule.slides.length - 1 ? (
            <Button
              className=\"bg-emerald-600 hover:bg-emerald-700\"
              onClick={() => {
                toast.success('Course completed! 🎉');
                navigate('/courses');
              }}
            >
              <CheckCircle className=\"w-4 h-4 mr-2\" />
              Complete Course
            </Button>
          ) : (
            <Button
              onClick={nextSlide}
              className=\"bg-emerald-600 hover:bg-emerald-700\"
            >
              Next
              <ChevronRight className=\"w-4 h-4 ml-2\" />
            </Button>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default CourseViewer;
