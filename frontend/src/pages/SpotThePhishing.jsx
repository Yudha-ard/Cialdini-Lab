import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext, API } from '@/App';
import Layout from '@/components/Layout';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Shield, X, Check, Mail, AlertTriangle, Trophy, Clock, Zap } from 'lucide-react';
import confetti from 'canvas-confetti';
import { toast } from 'sonner';
import axios from 'axios';

const SpotThePhishing = () => {
  const navigate = useNavigate();
  const { token } = React.useContext(AuthContext);
  const [gameState, setGameState] = useState('menu'); // menu, playing, gameover, completed
  const [currentEmail, setCurrentEmail] = useState(null);
  const [score, setScore] = useState(0);
  const [lives, setLives] = useState(3);
  const [timeLeft, setTimeLeft] = useState(60);
  const [streak, setStreak] = useState(0);
  const [emailsAnswered, setEmailsAnswered] = useState(0);
  const [gameStartTime, setGameStartTime] = useState(null);
  const [alreadyCompleted, setAlreadyCompleted] = useState(false);
  const [previousResult, setPreviousResult] = useState(null);

  const emails = [
    {
      id: 1,
      from: 'support@banc-bca.co.id',
      subject: 'URGENT: Verifikasi Akun Anda Sekarang!',
      body: 'Dear valued customer, Akun Anda terdeteksi aktivitas mencurigakan. Klik link berikut dalam 24 jam atau akun akan ditutup: http://bca-verify.ml/login',
      isPhishing: true,
      redFlags: ['Domain mencurigakan (banc-bca.co.id, bukan bca.co.id)', 'Urgency tactic (24 jam)', 'Link ke domain .ml (free domain)', 'Generic greeting (valued customer)']
    },
    {
      id: 2,
      from: 'hr@company-internal.com',
      subject: 'Monthly Payslip - January 2025',
      body: 'Hi Team, Your January payslip is now available. Please download from the HR portal as usual. Best regards, HR Department',
      isPhishing: false,
      redFlags: []
    },
    {
      id: 3,
      from: 'admin@tokoped1a.com',
      subject: 'Selamat! Anda Memenangkan iPhone 15 Pro!',
      body: 'Selamat! Anda terpilih sebagai pemenang undian Tokopedia! Klaim iPhone 15 Pro Anda dengan klik link dan bayar ongkir Rp 50rb: http://bit.ly/claim-prize-now',
      isPhishing: true,
      redFlags: ['Domain typo (tokoped1a.com bukan tokopedia.com)', 'Too good to be true (iPhone gratis)', 'Bayar ongkir untuk hadiah (red flag)', 'Shortened link (bit.ly)']
    },
    {
      id: 4,
      from: 'notifications@shopee.co.id',
      subject: 'Order #SH123456 Telah Dikirim',
      body: 'Halo! Pesanan Anda #SH123456 telah dikirim oleh JNE. Estimasi tiba: 2-3 hari. Lacak pesanan: https://shopee.co.id/track/SH123456',
      isPhishing: false,
      redFlags: []
    },
    {
      id: 5,
      from: 'it.helpdesk@gmail.com',
      subject: '[ACTION REQUIRED] Email Storage Full',
      body: 'Your email storage is 99% full. Click here to upgrade now or email will stop receiving: http://storage-upgrade-now.com/verify.php?user=12345',
      isPhishing: true,
      redFlags: ['IT helpdesk using gmail (not corporate email)', 'External link for corporate action', 'Urgency (email will stop)', 'Suspicious URL parameter']
    },
    {
      id: 6,
      from: 'netflix@service-update.net',
      subject: 'Your Netflix subscription has been cancelled',
      body: 'We were unable to process your payment. Update your payment method now to avoid service interruption: http://netflix-payment-update.net',
      isPhishing: true,
      redFlags: ['Domain netflix-payment-update.net (bukan netflix.com)', 'Payment scare tactic', 'External link for payment', 'service-update.net sender domain']
    },
    {
      id: 7,
      from: 'team@notion.so',
      subject: 'Your Notion workspace invitation',
      body: 'You have been invited to join workspace "Project Alpha". Click to accept: https://notion.so/invite/abc123',
      isPhishing: false,
      redFlags: []
    },
    {
      id: 8,
      from: 'security@amaz0n.com',
      subject: 'Suspicious Login Detected',
      body: 'We detected login from unknown device in Russia. Was this you? If not, secure your account immediately: http://amazon-secure.tk/verify',
      isPhishing: true,
      redFlags: ['Domain typo (amaz0n.com dengan zero)', 'Scare tactic (Russia login)', '.tk domain (free/suspicious)', 'External verification link']
    },
    {
      id: 9,
      from: 'billing@aws.amazon.com',
      subject: 'AWS Invoice for December 2024',
      body: 'Your AWS invoice for December 2024 is ready. View and download from AWS Console: https://console.aws.amazon.com/billing/',
      isPhishing: false,
      redFlags: []
    },
    {
      id: 10,
      from: 'prizes@whatsapp-giveaway.com',
      subject: 'WhatsApp 15th Anniversary Giveaway!',
      body: 'Congratulations! You have been selected for WhatsApp 15th Anniversary! Claim your Rp 10 juta prize by completing survey: http://wa-prize.tk/survey',
      isPhishing: true,
      redFlags: ['WhatsApp tidak menggunakan whatsapp-giveaway.com', 'Too good to be true (Rp 10 juta)', 'Survey for prize (classic scam)', '.tk domain']
    }
  ];

  useEffect(() => {
    if (gameState === 'playing' && timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    } else if (gameState === 'playing' && timeLeft === 0) {
      endGame();
    }
  }, [gameState, timeLeft]);

  // Check completion status on mount
  useEffect(() => {
    checkCompletionStatus();
  }, []);

  const checkCompletionStatus = async () => {
    try {
      const response = await axios.get(`${API}/minigame/completion-status/spot_the_phishing`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      if (response.data.completed) {
        setAlreadyCompleted(true);
        setPreviousResult(response.data.completion_data);
        setGameState('completed');
      }
    } catch (error) {
      console.error('Failed to check completion status:', error);
    }
  };

  const submitGameCompletion = async (finalScore, timeTaken) => {
    try {
      await axios.post(
        `${API}/minigame/complete`,
        {
          game_type: 'spot_the_phishing',
          score: finalScore,
          time_taken_seconds: timeTaken,
          details: {
            emails_answered: emailsAnswered,
            lives_remaining: lives
          }
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success(`Mini game complete! +${finalScore} poin`);
    } catch (error) {
      if (error.response?.status === 400) {
        toast.error('Mini game sudah pernah diselesaikan sebelumnya!');
      } else {
        toast.error('Gagal menyimpan hasil mini game');
      }
    }
  };

  const startGame = () => {
    setGameState('playing');
    setScore(0);
    setLives(3);
    setTimeLeft(60);
    setStreak(0);
    setEmailsAnswered(0);
    setGameStartTime(Date.now());
    loadRandomEmail();
  };

  const loadRandomEmail = () => {
    const randomEmail = emails[Math.floor(Math.random() * emails.length)];
    setCurrentEmail(randomEmail);
  };

  const handleAnswer = (isPhishingGuess) => {
    const correct = isPhishingGuess === currentEmail.isPhishing;
    
    if (correct) {
      const points = 10 + (streak * 2); // Bonus points for streak
      setScore(score + points);
      setStreak(streak + 1);
      toast.success(`Benar! +${points} points!`, {
        icon: <Check className="w-4 h-4 text-green-400" />
      });
      
      if (streak > 0 && streak % 3 === 0) {
        confetti({
          particleCount: 50,
          spread: 60,
          origin: { y: 0.8 }
        });
      }
    } else {
      setLives(lives - 1);
      setStreak(0);
      toast.error('Salah! -1 Nyawa', {
        icon: <X className="w-4 h-4 text-red-400" />
      });
      
      if (lives - 1 === 0) {
        endGame();
        return;
      }
    }
    
    setEmailsAnswered(emailsAnswered + 1);
    
    setTimeout(() => {
      loadRandomEmail();
    }, 800);
  };

  const endGame = async () => {
    setGameState('gameover');
    const finalTime = Math.floor((Date.now() - gameStartTime) / 1000);
    
    // Submit game completion
    await submitGameCompletion(score, finalTime);
    
    if (score > 50) {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });
    }
  };

  const getScoreRating = () => {
    if (score >= 100) return { text: 'Security Expert!', color: 'text-yellow-400', icon: <Trophy className="w-6 h-6" /> };
    if (score >= 70) return { text: 'Phishing Hunter!', color: 'text-emerald-400', icon: <Shield className="w-6 h-6" /> };
    if (score >= 40) return { text: 'Good Awareness!', color: 'text-blue-400', icon: <Check className="w-6 h-6" /> };
    return { text: 'Keep Learning!', color: 'text-gray-400', icon: <AlertTriangle className="w-6 h-6" /> };
  };

  if (gameState === 'menu') {
    return (
      <Layout>
        <div className="max-w-4xl mx-auto py-12 space-y-8">
          <div className="text-center space-y-4">
            <div className="flex justify-center">
              <div className="w-20 h-20 rounded-full bg-gradient-to-r from-red-500 to-pink-500 flex items-center justify-center">
                <Mail className="w-10 h-10 text-white" />
              </div>
            </div>
            <h1 className="text-5xl font-bold">
              <span className="bg-gradient-to-r from-red-400 to-pink-400 bg-clip-text text-transparent">
                Spot the Phishing
              </span>
            </h1>
            <p className="text-xl text-gray-400">Mini game deteksi email phishing!</p>
          </div>

          <Card className="glass border-zinc-800 p-8">
            <div className="space-y-6">
              <div className="grid md:grid-cols-3 gap-4">
                <div className="text-center p-4 bg-emerald-500/10 rounded-lg border border-emerald-500/30">
                  <Clock className="w-8 h-8 mx-auto mb-2 text-emerald-400" />
                  <h3 className="font-semibold text-emerald-400">60 Detik</h3>
                  <p className="text-sm text-gray-400">Time Limit</p>
                </div>
                <div className="text-center p-4 bg-red-500/10 rounded-lg border border-red-500/30">
                  <Shield className="w-8 h-8 mx-auto mb-2 text-red-400" />
                  <h3 className="font-semibold text-red-400">3 Nyawa</h3>
                  <p className="text-sm text-gray-400">Jangan Sampai Habis!</p>
                </div>
                <div className="text-center p-4 bg-purple-500/10 rounded-lg border border-purple-500/30">
                  <Zap className="w-8 h-8 mx-auto mb-2 text-purple-400" />
                  <h3 className="font-semibold text-purple-400">Streak Bonus</h3>
                  <p className="text-sm text-gray-400">+2pts per streak</p>
                </div>
              </div>

              <div className="bg-zinc-900/50 rounded-lg p-6 space-y-3">
                <h3 className="font-semibold text-lg mb-3">Cara Bermain:</h3>
                <div className="space-y-2 text-gray-300">
                  <p>• Baca email yang muncul dengan seksama</p>
                  <p>• Tentukan apakah email tersebut PHISHING atau LEGITIMATE</p>
                  <p>• Jawab dengan cepat dan akurat untuk score tinggi!</p>
                  <p>• Streak bonus: semakin banyak jawaban benar beruntun, semakin banyak point!</p>
                  <p>• Game berakhir jika nyawa habis atau waktu habis</p>
                </div>
              </div>

              <Button 
                onClick={startGame} 
                className="w-full h-14 text-lg bg-gradient-to-r from-red-500 to-pink-500 hover:from-red-600 hover:to-pink-600"
              >
                <Shield className="w-5 h-5 mr-2" />
                Mulai Game!
              </Button>
            </div>
          </Card>
        </div>
      </Layout>
    );
  }

  if (gameState === 'playing') {
    return (
      <Layout>
        <div className="max-w-5xl mx-auto py-8 space-y-6">
          {/* Game Stats */}
          <div className="grid grid-cols-4 gap-4">
            <Card className="glass border-zinc-800 p-4">
              <div className="flex items-center gap-3">
                <Trophy className="w-8 h-8 text-yellow-400" />
                <div>
                  <p className="text-sm text-gray-400">Score</p>
                  <p className="text-2xl font-bold text-yellow-400">{score}</p>
                </div>
              </div>
            </Card>
            
            <Card className="glass border-zinc-800 p-4">
              <div className="flex items-center gap-3">
                <Clock className="w-8 h-8 text-blue-400" />
                <div>
                  <p className="text-sm text-gray-400">Time</p>
                  <p className={`text-2xl font-bold ${timeLeft <= 10 ? 'text-red-400 animate-pulse' : 'text-blue-400'}`}>
                    {timeLeft}s
                  </p>
                </div>
              </div>
            </Card>
            
            <Card className="glass border-zinc-800 p-4">
              <div className="flex items-center gap-3">
                <Shield className="w-8 h-8 text-red-400" />
                <div>
                  <p className="text-sm text-gray-400">Lives</p>
                  <p className="text-2xl font-bold text-red-400">
                    {'❤️'.repeat(lives)}
                  </p>
                </div>
              </div>
            </Card>
            
            <Card className="glass border-zinc-800 p-4">
              <div className="flex items-center gap-3">
                <Zap className="w-8 h-8 text-purple-400" />
                <div>
                  <p className="text-sm text-gray-400">Streak</p>
                  <p className="text-2xl font-bold text-purple-400">{streak}x</p>
                </div>
              </div>
            </Card>
          </div>

          {/* Email Display */}
          {currentEmail && (
            <Card className="glass border-zinc-800 p-6 space-y-4">
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-gray-400">From:</span>
                  <span className="font-mono text-emerald-400">{currentEmail.from}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-gray-400 text-sm">Subject:</span>
                  <span className="font-semibold">{currentEmail.subject}</span>
                </div>
              </div>
              
              <div className="border-t border-zinc-800 pt-4">
                <div className="bg-zinc-900/50 rounded-lg p-6 min-h-[200px]">
                  <p className="text-gray-300 whitespace-pre-line">{currentEmail.body}</p>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="grid grid-cols-2 gap-4 pt-4">
                <Button
                  onClick={() => handleAnswer(true)}
                  className="h-16 text-lg bg-red-600 hover:bg-red-700"
                >
                  <AlertTriangle className="w-5 h-5 mr-2" />
                  PHISHING!
                </Button>
                <Button
                  onClick={() => handleAnswer(false)}
                  className="h-16 text-lg bg-emerald-600 hover:bg-emerald-700"
                >
                  <Check className="w-5 h-5 mr-2" />
                  LEGITIMATE
                </Button>
              </div>
            </Card>
          )}
        </div>
      </Layout>
    );
  }

  if (gameState === 'gameover') {
    const rating = getScoreRating();
    
    return (
      <Layout>
        <div className="max-w-3xl mx-auto py-12 space-y-8">
          <Card className="glass border-zinc-800 p-8 text-center space-y-6">
            <div className="flex justify-center">
              <div className="w-20 h-20 rounded-full bg-gradient-to-r from-emerald-500 to-cyan-500 flex items-center justify-center">
                {rating.icon}
              </div>
            </div>
            
            <div>
              <h2 className="text-4xl font-bold mb-2">Game Over!</h2>
              <p className={`text-2xl font-semibold ${rating.color}`}>{rating.text}</p>
            </div>

            <div className="grid grid-cols-3 gap-6 py-6">
              <div className="space-y-2">
                <p className="text-sm text-gray-400">Final Score</p>
                <p className="text-3xl font-bold text-yellow-400">{score}</p>
              </div>
              <div className="space-y-2">
                <p className="text-sm text-gray-400">Emails Answered</p>
                <p className="text-3xl font-bold text-blue-400">{emailsAnswered}</p>
              </div>
              <div className="space-y-2">
                <p className="text-sm text-gray-400">Best Streak</p>
                <p className="text-3xl font-bold text-purple-400">{streak}x</p>
              </div>
            </div>

            {currentEmail && currentEmail.isPhishing && (
              <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 text-left">
                <h4 className="font-semibold text-red-400 mb-2">Red Flags pada Email Terakhir:</h4>
                <ul className="space-y-1 text-sm text-gray-300">
                  {currentEmail.redFlags.map((flag, idx) => (
                    <li key={idx}>• {flag}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="flex gap-4">
              <Button 
                onClick={startGame} 
                className="flex-1 h-12 bg-gradient-to-r from-red-500 to-pink-500 hover:from-red-600 hover:to-pink-600"
              >
                Main Lagi
              </Button>
              <Button 
                onClick={() => setGameState('menu')} 
                variant="outline"
                className="flex-1 h-12 border-zinc-700"
              >
                Ke Menu
              </Button>
            </div>
          </Card>
        </div>
      </Layout>
    );
  }

  return null;
};

export default SpotThePhishing;
