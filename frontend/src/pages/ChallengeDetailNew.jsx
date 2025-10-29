import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { AuthContext, API } from '@/App';
import Layout from '@/components/Layout';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Label } from '@/components/ui/label';
import { Progress } from '@/components/ui/progress';
import { Textarea } from '@/components/ui/textarea';
import { AlertCircle, CheckCircle, Lightbulb, ArrowLeft, Clock, MessageSquare, Star } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Separator } from '@/components/ui/separator';
import axios from 'axios';
import { toast } from 'sonner';

const ChallengeDetailNew = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { token, refreshUser } = React.useContext(AuthContext);
  const [challenge, setChallenge] = useState(null);
  const [answers, setAnswers] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [startTime, setStartTime] = useState(null);
  const [feedbacks, setFeedbacks] = useState([]);
  const [showFeedbackForm, setShowFeedbackForm] = useState(false);
  const [feedbackData, setFeedbackData] = useState({ rating: 5, comment: '' });

  useEffect(() => {
    fetchChallenge();
    fetchFeedbacks();
  }, [id]);

  useEffect(() => {
    if (challenge && !startTime) {
      setStartTime(Date.now());
      setAnswers(new Array(challenge.questions?.length || 0).fill(null));
    }
  }, [challenge]);

  const fetchChallenge = async () => {
    try {
      const response = await axios.get(`${API}/challenges/${id}`);
      setChallenge(response.data);
    } catch (error) {
      console.error('Failed to fetch challenge:', error);
      toast.error('Gagal memuat challenge');
    } finally {
      setLoading(false);
    }
  };

  const fetchFeedbacks = async () => {
    try {
      const response = await axios.get(`${API}/challenges/${id}/feedback`);
      setFeedbacks(response.data);
    } catch (error) {
      console.error('Failed to fetch feedbacks:', error);
    }
  };

  const handleAnswerChange = (questionIndex, answerIndex) => {
    const newAnswers = [...answers];
    newAnswers[questionIndex] = answerIndex;
    setAnswers(newAnswers);
  };

  const handleSubmit = async () => {
    if (answers.some(a => a === null)) {
      toast.error('Jawab semua pertanyaan terlebih dahulu');
      return;
    }

    const timeTaken = Math.floor((Date.now() - startTime) / 1000);

    setSubmitting(true);
    try {
      const response = await axios.post(
        `${API}/challenges/${id}/attempt`,
        { answers, time_taken_seconds: timeTaken },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setResult(response.data);
      await refreshUser();
      
      if (response.data.is_completed) {
        toast.success(`Sempurna! Semua benar. +${response.data.points_earned} poin`);
      } else {
        toast.warning(`${response.data.correct_count}/${response.data.total_questions} benar. +${response.data.points_earned} poin`);
      }
    } catch (error) {
      console.error('Failed to submit answer:', error);
      toast.error('Gagal submit jawaban');
    } finally {
      setSubmitting(false);
    }
  };

  const handleFeedbackSubmit = async () => {
    try {
      await axios.post(
        `${API}/challenges/${id}/feedback`,
        feedbackData,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success('Terima kasih atas feedback Anda!');
      setShowFeedbackForm(false);
      setFeedbackData({ rating: 5, comment: '' });
      fetchFeedbacks();
    } catch (error) {
      toast.error('Gagal mengirim feedback');
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

  if (!challenge) {
    return (
      <Layout>
        <div className="text-center py-16">
          <p className="text-gray-400">Challenge tidak ditemukan</p>
        </div>
      </Layout>
    );
  }

  const answeredCount = answers.filter(a => a !== null).length;
  const progressPercent = (answeredCount / (challenge.questions?.length || 1)) * 100;

  return (
    <Layout>
      <div className="max-w-4xl mx-auto space-y-6" data-testid="challenge-detail-container">
        <Button 
          variant="ghost" 
          onClick={() => navigate('/challenges')}
          className="text-gray-400 hover:text-gray-200"
          data-testid="back-to-challenges-button"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Kembali ke Challenges
        </Button>

        {/* Challenge Header */}
        <Card className="glass border-zinc-800 p-8">
          <div className="flex flex-wrap gap-3 mb-4">
            <Badge variant="outline" className="text-emerald-400 border-emerald-500/30">
              {challenge.category.replace('_', ' ')}
            </Badge>
            <Badge className={`${
              challenge.difficulty === 'beginner' ? 'bg-emerald-500/20 text-emerald-400' :
              challenge.difficulty === 'intermediate' ? 'bg-yellow-500/20 text-yellow-400' :
              'bg-red-500/20 text-red-400'
            }`}>
              {challenge.difficulty === 'beginner' ? 'Pemula' :
               challenge.difficulty === 'intermediate' ? 'Menengah' : 'Lanjutan'}
            </Badge>
            <Badge className="bg-purple-500/20 text-purple-400 border-purple-500/30">
              {challenge.cialdini_principle}
            </Badge>
            <Badge className="bg-yellow-500/20 text-yellow-400 border-yellow-500/30">
              {challenge.points} Points
            </Badge>
            {challenge.time_limit_seconds && (
              <Badge variant="outline" className="text-cyan-400 border-cyan-500/30">
                <Clock className="w-3 h-3 mr-1" />
                {Math.floor(challenge.time_limit_seconds / 60)} menit
              </Badge>
            )}
          </div>

          <h1 className="text-3xl font-bold mb-4" data-testid="challenge-title">{challenge.title}</h1>
          <p className="text-gray-400 text-lg mb-6">{challenge.description}</p>

          {challenge.real_case_reference && (
            <Alert className="bg-cyan-500/10 border-cyan-500/30 mb-6">
              <AlertCircle className="h-4 w-4 text-cyan-400" />
              <AlertDescription className="text-cyan-400">
                <strong>Referensi Kasus Nyata:</strong> {challenge.real_case_reference}
              </AlertDescription>
            </Alert>
          )}

          <Separator className="my-6 bg-zinc-800" />

          <div className="space-y-4">
            <h3 className="text-xl font-semibold">Skenario:</h3>
            <Card className="bg-zinc-900/50 border-zinc-800 p-6">
              <p className="text-gray-300 leading-relaxed whitespace-pre-line">{challenge.scenario}</p>
            </Card>
          </div>
        </Card>

        {/* Progress Bar */}
        {!result && (
          <Card className="glass border-zinc-800 p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-400">Progress</span>
              <span className="text-sm font-semibold text-emerald-400">
                {answeredCount}/{challenge.questions?.length || 0} dijawab
              </span>
            </div>
            <Progress value={progressPercent} className="h-2" />
          </Card>
        )}

        {/* Questions */}
        {!result && challenge.questions?.map((question, qIndex) => (
          <Card key={qIndex} className="glass border-zinc-800 p-8" data-testid={`question-${qIndex}`}>
            <div className="flex items-start gap-4 mb-6">
              <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400 font-bold flex-shrink-0">
                {qIndex + 1}
              </div>
              <div className="flex-1">
                <h3 className="text-xl font-semibold mb-4">{question.question}</h3>
                <RadioGroup 
                  value={answers[qIndex]?.toString()} 
                  onValueChange={(v) => handleAnswerChange(qIndex, parseInt(v))}
                >
                  <div className="space-y-4">
                    {question.options.map((option, oIndex) => (
                      <div key={oIndex} className="flex items-start space-x-3">
                        <RadioGroupItem value={oIndex.toString()} id={`q${qIndex}-o${oIndex}`} data-testid={`q${qIndex}-option-${oIndex}`} />
                        <Label 
                          htmlFor={`q${qIndex}-o${oIndex}`} 
                          className="flex-1 cursor-pointer text-gray-300 hover:text-white p-4 rounded-lg border border-zinc-800 hover:border-emerald-500/50 transition-all"
                        >
                          {option}
                        </Label>
                      </div>
                    ))}
                  </div>
                </RadioGroup>
              </div>
            </div>
          </Card>
        ))}

        {/* Submit Button */}
        {!result && (
          <Button 
            onClick={handleSubmit}
            disabled={submitting || answeredCount < (challenge.questions?.length || 0)}
            className="w-full bg-emerald-600 hover:bg-emerald-700 btn-cyber py-6 text-lg"
            data-testid="submit-answer-button"
          >
            {submitting ? 'Memproses...' : 'Submit Semua Jawaban'}
          </Button>
        )}

        {/* Result */}
        {result && (
          <div className="space-y-6">
            <Alert className={result.is_completed ? 'bg-emerald-500/10 border-emerald-500/30' : 'bg-yellow-500/10 border-yellow-500/30'} data-testid="result-alert">
              {result.is_completed ? <CheckCircle className="h-5 w-5 text-emerald-400" /> : <AlertCircle className="h-5 w-5 text-yellow-400" />}
              <AlertDescription className={result.is_completed ? 'text-emerald-400' : 'text-yellow-400'}>
                <strong className="text-lg">
                  {result.is_completed ? '✓ Sempurna! Semua Benar!' : `${result.correct_count}/${result.total_questions} Jawaban Benar`}
                </strong>
                <p className="mt-1">Anda mendapatkan {result.points_earned} poin.</p>
              </AlertDescription>
            </Alert>

            {/* Individual Question Results */}
            {result.results?.map((res, idx) => (
              <Card key={idx} className={`glass p-6 ${res.is_correct ? 'border-emerald-500/30' : 'border-red-500/30'}`}>
                <div className="flex items-start gap-4">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold ${
                    res.is_correct ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'
                  }`}>
                    {res.is_correct ? '✓' : '✗'}
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold mb-2">Pertanyaan {idx + 1}</h4>
                    <p className={`mb-3 ${res.is_correct ? 'text-emerald-400' : 'text-red-400'}`}>
                      {res.is_correct ? 'Jawaban Anda BENAR!' : 'Jawaban Anda kurang tepat'}
                    </p>
                    <div className="bg-zinc-900/50 p-4 rounded-lg">
                      <p className="text-sm text-gray-400 mb-2">Penjelasan:</p>
                      <p className="text-gray-300">{res.explanation}</p>
                    </div>
                  </div>
                </div>
              </Card>
            ))}

            {/* Tips */}
            <Card className="glass border-zinc-800 p-8">
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Lightbulb className="w-5 h-5 text-yellow-400" />
                Tips Pencegahan
              </h3>
              <ul className="space-y-3">
                {result.tips?.map((tip, index) => (
                  <li key={index} className="flex items-start gap-3 text-gray-300">
                    <span className="text-emerald-400 mt-1">✓</span>
                    <span>{tip}</span>
                  </li>
                ))}
              </ul>
            </Card>

            {/* Feedback Section */}
            <Card className="glass border-zinc-800 p-8">
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <MessageSquare className="w-5 h-5 text-cyan-400" />
                Feedback & Diskusi
              </h3>
              
              {!showFeedbackForm ? (
                <Button 
                  onClick={() => setShowFeedbackForm(true)}
                  variant="outline"
                  className="w-full border-emerald-500/50 hover:bg-emerald-500/10"
                  data-testid="show-feedback-form-button"
                >
                  <MessageSquare className="w-4 h-4 mr-2" />
                  Berikan Feedback
                </Button>
              ) : (
                <div className="space-y-4">
                  <div>
                    <label className="text-sm text-gray-400 mb-2 block">Rating Challenge</label>
                    <div className="flex gap-2">
                      {[1, 2, 3, 4, 5].map(star => (
                        <button
                          key={star}
                          onClick={() => setFeedbackData({...feedbackData, rating: star})}
                          className={`text-2xl ${star <= feedbackData.rating ? 'text-yellow-400' : 'text-gray-600'}`}
                          data-testid={`rating-star-${star}`}
                        >
                          <Star className="w-6 h-6 fill-current" />
                        </button>
                      ))}
                    </div>
                  </div>
                  <div>
                    <label className="text-sm text-gray-400 mb-2 block">Komentar</label>
                    <Textarea
                      value={feedbackData.comment}
                      onChange={(e) => setFeedbackData({...feedbackData, comment: e.target.value})}
                      placeholder="Bagikan pendapat Anda tentang challenge ini..."
                      className="bg-zinc-900/50 border-zinc-800 min-h-24"
                      data-testid="feedback-comment-input"
                    />
                  </div>
                  <div className="flex gap-3">
                    <Button 
                      onClick={handleFeedbackSubmit}
                      className="flex-1 bg-emerald-600 hover:bg-emerald-700"
                      data-testid="submit-feedback-button"
                    >
                      Submit Feedback
                    </Button>
                    <Button 
                      onClick={() => setShowFeedbackForm(false)}
                      variant="outline"
                      className="flex-1"
                    >
                      Batal
                    </Button>
                  </div>
                </div>
              )}

              {/* Display Feedbacks */}
              {feedbacks.length > 0 && (
                <div className="mt-6 space-y-4">
                  <Separator className="bg-zinc-800" />
                  <h4 className="font-semibold">Feedback dari User Lain</h4>
                  {feedbacks.slice(0, 5).map((fb, idx) => (
                    <div key={idx} className="bg-zinc-900/50 p-4 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-semibold text-sm">@{fb.username}</span>
                        <div className="flex gap-1">
                          {[...Array(5)].map((_, i) => (
                            <Star key={i} className={`w-4 h-4 ${i < fb.rating ? 'text-yellow-400 fill-current' : 'text-gray-600'}`} />
                          ))}
                        </div>
                      </div>
                      <p className="text-gray-400 text-sm">{fb.comment}</p>
                    </div>
                  ))}
                </div>
              )}
            </Card>

            <div className="flex gap-4">
              <Button 
                onClick={() => navigate('/challenges')}
                variant="outline"
                className="flex-1 border-zinc-700"
                data-testid="back-to-list-button"
              >
                Kembali ke Daftar
              </Button>
              <Button 
                onClick={() => window.location.reload()}
                className="flex-1 bg-emerald-600 hover:bg-emerald-700"
                data-testid="try-again-button"
              >
                Coba Lagi
              </Button>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default ChallengeDetailNew;
