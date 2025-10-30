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
  const [progress, setProgress] = useState(null);
  const [currentModuleIndex, setCurrentModuleIndex] = useState(0);
  const [currentSlideIndex, setCurrentSlideIndex] = useState(0);
  const [showQuiz, setShowQuiz] = useState(false);
  const [quizAnswers, setQuizAnswers] = useState([]);
  const [quizResult, setQuizResult] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCourse();
    fetchProgress();
  }, [id]);

  const fetchCourse = async () => {
    try {
      const response = await axios.get(`${API}/courses/${id}`);
      setCourse(response.data);
      if (response.data.quiz_questions) {
        setQuizAnswers(new Array(response.data.quiz_questions.length).fill(null));
      }
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
      console.error('Failed to fetch progress:', error);
    }
  };

  const nextSlide = () => {
    const currentModule = course.modules[currentModuleIndex];
    if (currentSlideIndex < currentModule.slides.length - 1) {
      setCurrentSlideIndex(currentSlideIndex + 1);
    } else if (currentModuleIndex < course.modules.length - 1) {
      setCurrentModuleIndex(currentModuleIndex + 1);
      setCurrentSlideIndex(0);
    } else {
      // Reached end of course, show quiz if available
      if (course.quiz_questions && course.quiz_questions.length > 0 && !progress?.quiz_completed) {
        setShowQuiz(true);
      }
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

  const handleQuizAnswer = (questionIndex, answerIndex) => {
    const newAnswers = [...quizAnswers];
    newAnswers[questionIndex] = answerIndex;
    setQuizAnswers(newAnswers);
  };

  const submitQuiz = async () => {
    if (quizAnswers.some(a => a === null)) {
      toast.error('Jawab semua pertanyaan terlebih dahulu');
      return;
    }

    try {
      const response = await axios.post(
        `${API}/courses/${id}/submit-quiz`,
        { answers: quizAnswers },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setQuizResult(response.data);
      if (response.data.passed) {
        toast.success('Selamat! Kamu lulus quiz dan mendapat certificate! 🎉');
      } else {
        toast.error(`Skor kamu ${response.data.score}%. Minimal ${response.data.passing_score}% untuk lulus.`);
      }
      fetchProgress();
    } catch (error) {
      toast.error('Gagal submit quiz');
    }
  };

  if (loading) return <Layout><div className="flex items-center justify-center min-h-screen"><div className="text-emerald-400">Loading...</div></div></Layout>;
  if (!course) return <Layout><div className="text-center py-16"><p className="text-gray-400">Course tidak ditemukan</p></div></Layout>;

  // Show quiz result if quiz completed
  if (quizResult) {
    return (
      <Layout>
        <div className="max-w-4xl mx-auto space-y-6">
          <Card className={`glass p-12 text-center ${quizResult.passed ? 'border-emerald-500/30' : 'border-red-500/30'}`}>
            <div className={`w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6 ${
              quizResult.passed ? 'bg-emerald-500/10' : 'bg-red-500/10'
            }`}>
              <CheckCircle className={`w-12 h-12 ${quizResult.passed ? 'text-emerald-400' : 'text-red-400'}`} />
            </div>
            <h1 className="text-4xl font-bold mb-4">
              {quizResult.passed ? '🎉 Selamat! Kamu Lulus!' : '😔 Belum Lulus'}
            </h1>
            
            <div className="grid md:grid-cols-3 gap-4 mb-8">
              <div className="bg-zinc-900/50 rounded-lg p-6">
                <div className="text-4xl font-bold text-emerald-400 mb-2">
                  {quizResult.correct_count}/{quizResult.total_questions}
                </div>
                <div className="text-gray-400">Correct</div>
              </div>
              <div className="bg-zinc-900/50 rounded-lg p-6">
                <div className={`text-4xl font-bold mb-2 ${
                  quizResult.passed ? 'text-emerald-400' : 'text-red-400'
                }`}>
                  {quizResult.score}%
                </div>
                <div className="text-gray-400">Score</div>
              </div>
              <div className="bg-zinc-900/50 rounded-lg p-6">
                <div className="text-4xl font-bold text-purple-400 mb-2">
                  {quizResult.passing_score}%
                </div>
                <div className="text-gray-400">Passing Score</div>
              </div>
            </div>

            {quizResult.passed ? (
              <>
                <div className="p-4 bg-emerald-900/20 border border-emerald-600/30 rounded-lg mb-6">
                  <p className="text-emerald-400 text-lg mb-2">
                    ✅ Course completed! Certificate issued.
                  </p>
                  <p className="text-sm text-gray-400">
                    +{quizResult.points_earned} points earned
                  </p>
                </div>
                <div className="flex gap-4 justify-center">
                  <Button onClick={() => navigate('/certificates')} className="bg-purple-600 hover:bg-purple-700">
                    View Certificate
                  </Button>
                  <Button onClick={() => navigate('/courses')} variant="outline">
                    Back to Courses
                  </Button>
                </div>
              </>
            ) : (
              <div className="p-4 bg-red-900/20 border border-red-600/30 rounded-lg mb-6">
                <p className="text-red-400">
                  Skor minimal untuk lulus adalah {quizResult.passing_score}%.
                  Silakan ulangi course untuk mencoba lagi.
                </p>
              </div>
            )}
          </Card>
        </div>
      </Layout>
    );
  }

  // Show quiz if triggered
  if (showQuiz && !progress?.quiz_completed) {
    return (
      <Layout>
        <div className="max-w-4xl mx-auto space-y-6">
          <Card className="glass border-zinc-800 p-8">
            <h1 className="text-3xl font-bold mb-2">📝 Course Quiz</h1>
            <p className="text-gray-400 mb-6">
              Jawab semua pertanyaan untuk menyelesaikan course. Passing score: {course.passing_score}%
            </p>

            <div className="space-y-6">
              {course.quiz_questions.map((question, qIndex) => (
                <Card key={qIndex} className="bg-zinc-900/50 border-zinc-800 p-6">
                  <h3 className="font-semibold mb-4">
                    {qIndex + 1}. {question.question}
                  </h3>
                  <div className="space-y-2">
                    {question.options.map((option, oIndex) => (
                      <label
                        key={oIndex}
                        className={`flex items-center p-3 rounded-lg cursor-pointer border transition-all ${
                          quizAnswers[qIndex] === oIndex
                            ? 'border-emerald-500 bg-emerald-500/10'
                            : 'border-zinc-700 hover:border-zinc-600'
                        }`}
                      >
                        <input
                          type="radio"
                          name={`question-${qIndex}`}
                          checked={quizAnswers[qIndex] === oIndex}
                          onChange={() => handleQuizAnswer(qIndex, oIndex)}
                          className="mr-3"
                        />
                        <span>{option}</span>
                      </label>
                    ))}
                  </div>
                </Card>
              ))}
            </div>

            <div className="flex justify-between mt-8">
              <Button onClick={() => setShowQuiz(false)} variant="outline">
                Back to Course
              </Button>
              <Button onClick={submitQuiz} className="bg-emerald-600 hover:bg-emerald-700">
                Submit Quiz
              </Button>
            </div>
          </Card>
        </div>
      </Layout>
    );
  }

  // Show completed quiz status if already completed
  if (progress?.quiz_completed) {
    return (
      <Layout>
        <div className="max-w-4xl mx-auto space-y-6">
          <Card className={`glass p-12 text-center ${
            progress.quiz_passed ? 'border-emerald-500/30' : 'border-yellow-500/30'
          }`}>
            <div className={`w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6 ${
              progress.quiz_passed ? 'bg-emerald-500/10' : 'bg-yellow-500/10'
            }`}>
              <CheckCircle className={`w-12 h-12 ${
                progress.quiz_passed ? 'text-emerald-400' : 'text-yellow-400'
              }`} />
            </div>
            <h1 className="text-4xl font-bold mb-4">
              {progress.quiz_passed ? '✅ Course Completed!' : '📝 Quiz Completed'}
            </h1>
            <p className="text-gray-400 mb-6">
              Skor kamu: {progress.quiz_score}%
            </p>
            
            {progress.quiz_passed ? (
              <div className="p-4 bg-emerald-900/20 border border-emerald-600/30 rounded-lg mb-6">
                <p className="text-emerald-400">
                  🎉 Selamat! Kamu telah menyelesaikan course ini dan mendapat certificate.
                </p>
              </div>
            ) : (
              <div className="p-4 bg-yellow-900/20 border border-yellow-600/30 rounded-lg mb-6">
                <p className="text-yellow-400">
                  Skor kamu belum mencapai passing score ({course.passing_score}%).
                </p>
              </div>
            )}

            <div className="flex gap-4 justify-center">
              {progress.quiz_passed && (
                <Button onClick={() => navigate('/certificates')} className="bg-purple-600 hover:bg-purple-700">
                  View Certificate
                </Button>
              )}
              <Button onClick={() => navigate('/courses')} variant="outline">
                Back to Courses
              </Button>
            </div>
          </Card>
        </div>
      </Layout>
    );
  }

  const currentModule = course.modules[currentModuleIndex];
  const currentSlide = currentModule.slides[currentSlideIndex];
  const totalSlides = course.modules.reduce((acc, m) => acc + m.slides.length, 0);
  const currentSlideGlobal = course.modules.slice(0, currentModuleIndex).reduce((acc, m) => acc + m.slides.length, 0) + currentSlideIndex + 1;
  const progressPercent = (currentSlideGlobal / totalSlides) * 100;
  const isLastSlide = currentModuleIndex === course.modules.length - 1 && currentSlideIndex === currentModule.slides.length - 1;

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
            {course.quiz_questions && course.quiz_questions.length > 0 && (
              <Badge className="bg-purple-500/20 text-purple-400">
                Quiz: {course.quiz_questions.length} questions
              </Badge>
            )}
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
          {isLastSlide ? (
            course.quiz_questions && course.quiz_questions.length > 0 ? (
              <Button className="bg-purple-600 hover:bg-purple-700" onClick={() => setShowQuiz(true)}>
                Take Quiz<ChevronRight className="w-4 h-4 ml-2" />
              </Button>
            ) : (
              <Button className="bg-emerald-600 hover:bg-emerald-700" onClick={() => { toast.success('Course completed! 🎉'); navigate('/courses'); }}>
                <CheckCircle className="w-4 h-4 mr-2" />Complete
              </Button>
            )
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
