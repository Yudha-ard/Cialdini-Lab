import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { AuthContext, API } from '@/App';
import Layout from '@/components/Layout';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Label } from '@/components/ui/label';
import { AlertCircle, CheckCircle, Lightbulb, ArrowLeft } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Separator } from '@/components/ui/separator';
import axios from 'axios';
import { toast } from 'sonner';

const ChallengeDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { token, refreshUser } = React.useContext(AuthContext);
  const [challenge, setChallenge] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchChallenge();
  }, [id]);

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

  const handleSubmit = async () => {
    if (selectedAnswer === null) {
      toast.error('Pilih jawaban terlebih dahulu');
      return;
    }

    setSubmitting(true);
    try {
      const response = await axios.post(
        `${API}/challenges/${id}/attempt`,
        { selected_answer: selectedAnswer },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setResult(response.data);
      await refreshUser();
      
      if (response.data.is_correct) {
        toast.success(`Benar! +${response.data.points_earned} poin`);
      } else {
        toast.error('Jawaban kurang tepat. Pelajari penjelasannya!');
      }
    } catch (error) {
      console.error('Failed to submit answer:', error);
      toast.error('Gagal submit jawaban');
    } finally {
      setSubmitting(false);
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
              Prinsip: {challenge.cialdini_principle}
            </Badge>
            <Badge className="bg-yellow-500/20 text-yellow-400 border-yellow-500/30">
              {challenge.points} Points
            </Badge>
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

        {/* Question & Answers */}
        {!result && (
          <Card className="glass border-zinc-800 p-8">
            <h3 className="text-xl font-semibold mb-6">{challenge.question}</h3>
            <RadioGroup value={selectedAnswer?.toString()} onValueChange={(v) => setSelectedAnswer(parseInt(v))}>
              <div className="space-y-4">
                {challenge.options.map((option, index) => (
                  <div key={index} className="flex items-start space-x-3">
                    <RadioGroupItem value={index.toString()} id={`option-${index}`} data-testid={`option-${index}`} />
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

            <Button 
              onClick={handleSubmit}
              disabled={submitting || selectedAnswer === null}
              className="w-full mt-8 bg-emerald-600 hover:bg-emerald-700 btn-cyber"
              data-testid="submit-answer-button"
            >
              {submitting ? 'Memproses...' : 'Submit Jawaban'}
            </Button>
          </Card>
        )}

        {/* Result */}
        {result && (
          <div className="space-y-6">
            <Alert className={result.is_correct ? 'bg-emerald-500/10 border-emerald-500/30' : 'bg-red-500/10 border-red-500/30'} data-testid="result-alert">
              {result.is_correct ? <CheckCircle className="h-5 w-5 text-emerald-400" /> : <AlertCircle className="h-5 w-5 text-red-400" />}
              <AlertDescription className={result.is_correct ? 'text-emerald-400' : 'text-red-400'}>
                <strong className="text-lg">
                  {result.is_correct ? '✓ Jawaban Benar!' : '✗ Jawaban Kurang Tepat'}
                </strong>
                {result.is_correct && (
                  <p className="mt-1">Selamat! Anda mendapatkan {result.points_earned} poin.</p>
                )}
              </AlertDescription>
            </Alert>

            <Card className="glass border-zinc-800 p-8">
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <AlertCircle className="w-5 h-5 text-cyan-400" />
                Penjelasan
              </h3>
              <p className="text-gray-300 leading-relaxed whitespace-pre-line">{result.explanation}</p>
            </Card>

            <Card className="glass border-zinc-800 p-8">
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Lightbulb className="w-5 h-5 text-yellow-400" />
                Tips Pencegahan
              </h3>
              <ul className="space-y-3">
                {result.tips.map((tip, index) => (
                  <li key={index} className="flex items-start gap-3 text-gray-300">
                    <span className="text-emerald-400 mt-1">✓</span>
                    <span>{tip}</span>
                  </li>
                ))}
              </ul>
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

export default ChallengeDetail;