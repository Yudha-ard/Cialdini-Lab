import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext, API } from '@/App';
import Layout from '@/components/Layout';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Label } from '@/components/ui/label';
import { Zap, Clock, Target } from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';
import confetti from 'canvas-confetti';

const QuizMode = () => {
  const navigate = useNavigate();
  const { token, refreshUser } = React.useContext(AuthContext);
  const [quiz, setQuiz] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [timeLeft, setTimeLeft] = useState(60);
  const [started, setStarted] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [alreadyCompleted, setAlreadyCompleted] = useState(false);
  const [previousResult, setPreviousResult] = useState(null);

  // Check completion status on mount
  useEffect(() => {
    checkCompletionStatus();
  }, []);

  const checkCompletionStatus = async () => {
    try {
      const response = await axios.get(`${API}/quiz/completion-status`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      if (response.data.completed) {
        setAlreadyCompleted(true);
        setPreviousResult(response.data.completion_data);
      }
    } catch (error) {
      console.error('Failed to check quiz completion status:', error);
    }
  };

  useEffect(() => {
    if (started && timeLeft > 0 && !result) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    } else if (timeLeft === 0 && !result) {
      handleSubmit();
    }
  }, [timeLeft, started, result]);

  const fetchQuiz = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/quiz/random`);
      setQuiz(response.data);
      setAnswers(new Array(response.data.questions.length).fill(null));
      setTimeLeft(response.data.time_limit_seconds);
      setStarted(true);
    } catch (error) {
      toast.error('Gagal load quiz');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSelect = (answerIndex) => {
    const newAnswers = [...answers];
    newAnswers[currentQuestion] = answerIndex;
    setAnswers(newAnswers);
    setSelectedAnswer(answerIndex);

    // Auto next after 0.5s
    setTimeout(() => {
      if (currentQuestion < quiz.questions.length - 1) {
        setCurrentQuestion(currentQuestion + 1);
        setSelectedAnswer(null);
      } else {
        handleSubmit();
      }
    }, 500);
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await axios.post(
        `${API}/quiz/submit`,
        {
          answers,
          questions: quiz.questions,
          time_taken: 60 - timeLeft
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setResult(response.data);
      await refreshUser();

      // Confetti if good score
      if (response.data.accuracy >= 80) {
        confetti({
          particleCount: 100,
          spread: 70,
          origin: { y: 0.6 }
        });
      }

      toast.success(`Quiz complete! +${response.data.points_earned} poin`);
    } catch (error) {
      toast.error('Gagal submit quiz');
    } finally {
      setLoading(false);
    }
  };

  if (!started) {
    return (
      <Layout>
        <div className="max-w-3xl mx-auto space-y-6">
          <Card className="glass border-zinc-800 p-12 text-center">
            <div className="w-24 h-24 rounded-full bg-yellow-500/10 flex items-center justify-center mx-auto mb-6">
              <Zap className="w-12 h-12 text-yellow-400" />
            </div>
            <h1 className="text-4xl font-bold mb-4">⚡ RAPID FIRE QUIZ ⚡</h1>
            <p className="text-gray-400 text-lg mb-8">
              10 pertanyaan random dari challenges\n60 detik untuk jawab semua\nSpeed bonus untuk fast completion!
            </p>
            <div className="grid md:grid-cols-3 gap-4 mb-8 text-center">
              <div className="bg-zinc-900/50 rounded-lg p-4">
                <div className="text-3xl font-bold text-emerald-400 mb-1">10</div>
                <div className="text-sm text-gray-400">Questions</div>
              </div>
              <div className="bg-zinc-900/50 rounded-lg p-4">
                <div className="text-3xl font-bold text-yellow-400 mb-1">60s</div>
                <div className="text-sm text-gray-400">Time Limit</div>
              </div>
              <div className="bg-zinc-900/50 rounded-lg p-4">
                <div className="text-3xl font-bold text-purple-400 mb-1">1.5x</div>
                <div className="text-sm text-gray-400">Speed Bonus</div>
              </div>
            </div>
            <Button
              size="lg"
              className="bg-yellow-600 hover:bg-yellow-700 px-12 py-6 text-xl"
              onClick={fetchQuiz}
              disabled={loading}
            >
              {loading ? 'Loading...' : 'START QUIZ!'}
            </Button>
          </Card>
        </div>
      </Layout>
    );
  }

  if (result) {
    return (
      <Layout>
        <div className="max-w-3xl mx-auto space-y-6">
          <Card className={`glass p-12 text-center ${
            result.accuracy >= 80 ? 'border-emerald-500/30' : 'border-yellow-500/30'
          }`}>
            <div className={`w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6 ${
              result.accuracy >= 80 ? 'bg-emerald-500/10' : 'bg-yellow-500/10'
            }`}>
              <Target className={`w-12 h-12 ${
                result.accuracy >= 80 ? 'text-emerald-400' : 'text-yellow-400'
              }`} />
            </div>
            <h2 className="text-4xl font-bold mb-4">
              {result.accuracy >= 80 ? '🎉 Excellent!' : result.accuracy >= 60 ? '👍 Good Job!' : '💪 Keep Learning!'}
            </h2>
            <div className="grid md:grid-cols-3 gap-4 mb-8">
              <div className="bg-zinc-900/50 rounded-lg p-6">
                <div className="text-4xl font-bold text-emerald-400 mb-2">{result.correct}/{result.total}</div>
                <div className="text-gray-400">Correct</div>
              </div>
              <div className="bg-zinc-900/50 rounded-lg p-6">
                <div className="text-4xl font-bold text-yellow-400 mb-2">{result.accuracy}%</div>
                <div className="text-gray-400">Accuracy</div>
              </div>
              <div className="bg-zinc-900/50 rounded-lg p-6">
                <div className="text-4xl font-bold text-purple-400 mb-2">+{result.points_earned}</div>
                <div className="text-gray-400">Points</div>
              </div>
            </div>
            <div className="flex gap-4 justify-center">
              <Button
                onClick={() => window.location.reload()}
                className="bg-emerald-600 hover:bg-emerald-700"
              >
                Try Again
              </Button>
              <Button
                onClick={() => navigate('/challenges')}
                variant="outline"
              >
                Back to Challenges
              </Button>
            </div>
          </Card>
        </div>
      </Layout>
    );
  }

  const question = quiz?.questions[currentQuestion];
  const progressPercent = ((currentQuestion + 1) / quiz.questions.length) * 100;

  return (
    <Layout>
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Timer & Progress */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className={`text-3xl font-bold ${
              timeLeft <= 10 ? 'text-red-400 animate-pulse' : 'text-yellow-400'
            }`}>
              <Clock className="w-6 h-6 inline mr-2" />
              {timeLeft}s
            </div>
            <div className="text-gray-400">
              Question {currentQuestion + 1}/{quiz.questions.length}
            </div>
          </div>
        </div>

        <Progress value={progressPercent} className="h-2" />

        {/* Question */}
        <Card className="glass border-zinc-800 p-8">
          <div className="mb-6">
            <p className="text-sm text-cyan-400 mb-2">{question.challenge_title}</p>
            <h2 className="text-2xl font-bold">{question.question}</h2>
          </div>

          <RadioGroup value={selectedAnswer?.toString()} onValueChange={(v) => handleAnswerSelect(parseInt(v))}>
            <div className="space-y-4">
              {question.options.map((option, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <RadioGroupItem value={index.toString()} id={`option-${index}`} />
                  <Label
                    htmlFor={`option-${index}`}
                    className="flex-1 cursor-pointer text-gray-300 hover:text-white p-4 rounded-lg border border-zinc-800 hover:border-emerald-500/50 transition-all"
                  >
                    {option}
                  </Label>
                </div>
              ))}
            </div>
          </RadioGroup>
        </Card>
      </div>
    </Layout>
  );
};

export default QuizMode;