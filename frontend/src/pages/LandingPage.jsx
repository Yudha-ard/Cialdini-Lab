import React, { useState } from 'react';
import { Shield, Lock, Eye, Users, Award, BookOpen, ChevronRight, Terminal } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import axios from 'axios';
import { API, AuthContext } from '@/App';
import { toast } from 'sonner';

const LandingPage = () => {
  const { login } = React.useContext(AuthContext);
  const [showAuth, setShowAuth] = useState(false);
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    full_name: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const endpoint = isLogin ? '/auth/login' : '/auth/register';
      const payload = isLogin 
        ? { username: formData.username, password: formData.password }
        : formData;
      
      const response = await axios.post(`${API}${endpoint}`, payload);
      login(response.data.token, response.data.user);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Terjadi kesalahan');
    } finally {
      setLoading(false);
    }
  };

  const features = [
    {
      icon: <Shield className="w-8 h-8" />,
      title: "Skenario Realistis",
      description: "Belajar dari kasus nyata yang terjadi di Indonesia"
    },
    {
      icon: <Lock className="w-8 h-8" />,
      title: "6 Prinsip Cialdini",
      description: "Pahami teknik manipulasi psikologis"
    },
    {
      icon: <Award className="w-8 h-8" />,
      title: "Sistem Gamifikasi",
      description: "Level, poin, dan leaderboard untuk motivasi belajar"
    },
    {
      icon: <BookOpen className="w-8 h-8" />,
      title: "Konten Edukatif",
      description: "Penjelasan mendalam dan tips pencegahan"
    }
  ];

  if (showAuth) {
    return (
      <div className="min-h-screen bg-[#0a0a0b] cyber-grid relative overflow-hidden">
        <div className="noise"></div>
        
        {/* Background Effects */}
        <div className="absolute top-20 left-20 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>

        <div className="relative z-10 min-h-screen flex items-center justify-center p-4">
          <Card className="w-full max-w-md glass border-emerald-500/20 p-8" data-testid="auth-card">
            <div className="text-center mb-6">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-emerald-500/10 mb-4">
                <Shield className="w-8 h-8 text-emerald-400" />
              </div>
              <h2 className="text-2xl font-bold text-emerald-400 mb-2">Tegalsec Lab</h2>
              <p className="text-gray-400">Social Engineering Training Platform</p>
            </div>

            <Tabs value={isLogin ? "login" : "register"} onValueChange={(v) => setIsLogin(v === "login")} className="w-full">
              <TabsList className="grid w-full grid-cols-2 mb-6 bg-zinc-900/50">
                <TabsTrigger value="login" data-testid="login-tab">Login</TabsTrigger>
                <TabsTrigger value="register" data-testid="register-tab">Register</TabsTrigger>
              </TabsList>

              <TabsContent value="login">
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <Label htmlFor="username">Username</Label>
                    <Input
                      id="username"
                      data-testid="login-username-input"
                      className="bg-zinc-900/50 border-zinc-800 mt-2"
                      value={formData.username}
                      onChange={(e) => setFormData({...formData, username: e.target.value})}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="password">Password</Label>
                    <Input
                      id="password"
                      type="password"
                      data-testid="login-password-input"
                      className="bg-zinc-900/50 border-zinc-800 mt-2"
                      value={formData.password}
                      onChange={(e) => setFormData({...formData, password: e.target.value})}
                      required
                    />
                  </div>
                  <Button 
                    type="submit" 
                    className="w-full bg-emerald-600 hover:bg-emerald-700 btn-cyber"
                    disabled={loading}
                    data-testid="login-submit-button"
                  >
                    {loading ? 'Loading...' : 'Login'}
                  </Button>
                </form>
              </TabsContent>

              <TabsContent value="register">
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <Label htmlFor="reg-username">Username</Label>
                    <Input
                      id="reg-username"
                      data-testid="register-username-input"
                      className="bg-zinc-900/50 border-zinc-800 mt-2"
                      value={formData.username}
                      onChange={(e) => setFormData({...formData, username: e.target.value})}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="email">Email</Label>
                    <Input
                      id="email"
                      type="email"
                      data-testid="register-email-input"
                      className="bg-zinc-900/50 border-zinc-800 mt-2"
                      value={formData.email}
                      onChange={(e) => setFormData({...formData, email: e.target.value})}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="full_name">Nama Lengkap</Label>
                    <Input
                      id="full_name"
                      data-testid="register-fullname-input"
                      className="bg-zinc-900/50 border-zinc-800 mt-2"
                      value={formData.full_name}
                      onChange={(e) => setFormData({...formData, full_name: e.target.value})}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="reg-password">Password</Label>
                    <Input
                      id="reg-password"
                      type="password"
                      data-testid="register-password-input"
                      className="bg-zinc-900/50 border-zinc-800 mt-2"
                      value={formData.password}
                      onChange={(e) => setFormData({...formData, password: e.target.value})}
                      required
                    />
                  </div>
                  <Button 
                    type="submit" 
                    className="w-full bg-emerald-600 hover:bg-emerald-700 btn-cyber"
                    disabled={loading}
                    data-testid="register-submit-button"
                  >
                    {loading ? 'Loading...' : 'Register'}
                  </Button>
                </form>
              </TabsContent>
            </Tabs>

            <div className="mt-6 text-center">
              <Button 
                variant="ghost" 
                className="text-gray-400 hover:text-emerald-400"
                onClick={() => setShowAuth(false)}
                data-testid="back-to-landing-button"
              >
                Kembali ke Landing Page
              </Button>
            </div>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a0b] text-gray-100">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center cyber-grid overflow-hidden">
        <div className="noise"></div>
        
        {/* Animated Background */}
        <div className="absolute top-20 left-20 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '1s'}}></div>
        
        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-emerald-500/10 border border-emerald-500/20 mb-8">
              <Terminal className="w-4 h-4 text-emerald-400" />
              <span className="text-sm text-emerald-400 font-medium">By Tegalsec Community</span>
            </div>
            
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
              <span className="text-emerald-400 text-glow">Social Engineering</span>
              <br />
              <span className="text-white">Training Lab</span>
            </h1>
            
            <p className="text-lg sm:text-xl text-gray-400 mb-12 max-w-2xl mx-auto">
              Platform pembelajaran interaktif untuk memahami teknik social engineering berdasarkan prinsip Cialdini dengan kasus nyata di Indonesia
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Button 
                size="lg" 
                className="bg-emerald-600 hover:bg-emerald-700 text-white px-8 py-6 text-lg btn-cyber glow-emerald"
                onClick={() => setShowAuth(true)}
                data-testid="get-started-button"
              >
                Mulai Belajar
                <ChevronRight className="ml-2" />
              </Button>
              <Button 
                size="lg" 
                variant="outline"
                className="border-emerald-500/50 hover:bg-emerald-500/10 px-8 py-6 text-lg"
                onClick={() => document.getElementById('features').scrollIntoView({behavior: 'smooth'})}
                data-testid="learn-more-button"
              >
                Pelajari Lebih Lanjut
              </Button>
            </div>

            <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8">
              <div className="text-center">
                <div className="text-3xl font-bold text-emerald-400 mb-2">8+</div>
                <div className="text-sm text-gray-400">Challenges</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-emerald-400 mb-2">6</div>
                <div className="text-sm text-gray-400">Prinsip Cialdini</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-emerald-400 mb-2">100%</div>
                <div className="text-sm text-gray-400">Kasus Lokal</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-emerald-400 mb-2">Gratis</div>
                <div className="text-sm text-gray-400">Open Access</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 bg-zinc-950/50 relative">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto text-center mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold mb-6">
              Kenapa <span className="text-emerald-400">Tegalsec Lab</span>?
            </h2>
            <p className="text-gray-400 text-lg">
              Platform pertama di Indonesia yang fokus pada pembelajaran social engineering dengan metodologi Cialdini
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
            {features.map((feature, index) => (
              <Card 
                key={index}
                className="glass border-emerald-500/20 p-6 card-hover"
                data-testid={`feature-card-${index}`}
              >
                <div className="w-16 h-16 rounded-lg bg-emerald-500/10 flex items-center justify-center mb-4 text-emerald-400">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                <p className="text-gray-400">{feature.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 relative overflow-hidden">
        <div className="absolute inset-0 cyber-grid opacity-30"></div>
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-emerald-500/5 to-transparent"></div>
        
        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-3xl mx-auto text-center">
            <Shield className="w-16 h-16 text-emerald-400 mx-auto mb-6 animate-float" />
            <h2 className="text-4xl lg:text-5xl font-bold mb-6">
              Siap Menjadi <span className="text-emerald-400">Cyber Aware</span>?
            </h2>
            <p className="text-gray-400 text-lg mb-8">
              Bergabung dengan Tegalsec Lab dan tingkatkan kemampuan Anda dalam mendeteksi dan mencegah serangan social engineering
            </p>
            <Button 
              size="lg"
              className="bg-emerald-600 hover:bg-emerald-700 px-8 py-6 text-lg btn-cyber animate-pulse-glow"
              onClick={() => setShowAuth(true)}
              data-testid="cta-start-button"
            >
              Mulai Sekarang - Gratis!
              <ChevronRight className="ml-2" />
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-zinc-800 bg-zinc-950/50">
        <div className="container mx-auto px-4 text-center text-gray-400">
          <p>© 2025 Tegalsec Community. Lab Social Engineering untuk edukasi cybersecurity.</p>
          <p className="mt-2 text-sm">Visit: <a href="https://tegalsec.org" target="_blank" rel="noopener noreferrer" className="text-emerald-400 hover:underline">tegalsec.org</a></p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;