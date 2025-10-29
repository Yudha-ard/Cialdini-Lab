import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { API } from '@/App';
import axios from 'axios';
import { toast } from 'sonner';
import { Mail, Lock, ArrowLeft } from 'lucide-react';

const ForgotPassword = ({ open, onClose }) => {
  const [step, setStep] = useState(1); // 1: email, 2: code, 3: new password
  const [email, setEmail] = useState('');
  const [resetCode, setResetCode] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [generatedCode, setGeneratedCode] = useState('');

  const handleRequestCode = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post(`${API}/auth/forgot-password`, { email });
      setGeneratedCode(response.data.reset_code); // Demo: show code (in prod, sent via email)
      toast.success('Kode reset telah dikirim ke email Anda');
      setStep(2);
    } catch (error) {
      toast.error('Gagal mengirim kode reset');
    } finally {
      setLoading(false);
    }
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await axios.post(`${API}/auth/reset-password`, {
        email,
        reset_code: resetCode,
        new_password: newPassword
      });
      toast.success('Password berhasil direset!');
      onClose();
      setStep(1);
      setEmail('');
      setResetCode('');
      setNewPassword('');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Gagal reset password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="bg-zinc-950 border-zinc-800">
        <DialogHeader>
          <DialogTitle className="text-2xl">Reset Password</DialogTitle>
        </DialogHeader>

        {step === 1 && (
          <form onSubmit={handleRequestCode} className="space-y-4">
            <div>
              <Label>Email</Label>
              <div className="relative mt-2">
                <Mail className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
                <Input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="pl-10 bg-zinc-900/50 border-zinc-800"
                  placeholder="email@example.com"
                  required
                />
              </div>
            </div>
            <Button 
              type="submit" 
              className="w-full bg-emerald-600 hover:bg-emerald-700"
              disabled={loading}
            >
              {loading ? 'Mengirim...' : 'Kirim Kode Reset'}
            </Button>
          </form>
        )}

        {step === 2 && (
          <form onSubmit={handleResetPassword} className="space-y-4">
            {generatedCode && (
              <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4">
                <p className="text-sm text-yellow-400">
                  <strong>Demo Mode:</strong> Kode reset Anda: <span className="font-mono text-lg">{generatedCode}</span>
                </p>
                <p className="text-xs text-gray-400 mt-2">Dalam production, kode ini akan dikirim via email</p>
              </div>
            )}
            
            <div>
              <Label>Kode Reset (6 digit)</Label>
              <Input
                type="text"
                value={resetCode}
                onChange={(e) => setResetCode(e.target.value)}
                className="bg-zinc-900/50 border-zinc-800 mt-2"
                placeholder="123456"
                maxLength={6}
                required
              />
            </div>
            
            <div>
              <Label>Password Baru</Label>
              <div className="relative mt-2">
                <Lock className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
                <Input
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="pl-10 bg-zinc-900/50 border-zinc-800"
                  placeholder="Minimal 6 karakter"
                  required
                />
              </div>
            </div>

            <div className="flex gap-3">
              <Button 
                type="button"
                variant="outline"
                onClick={() => setStep(1)}
                className="flex-1"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Kembali
              </Button>
              <Button 
                type="submit" 
                className="flex-1 bg-emerald-600 hover:bg-emerald-700"
                disabled={loading}
              >
                {loading ? 'Mereset...' : 'Reset Password'}
              </Button>
            </div>
          </form>
        )}
      </DialogContent>
    </Dialog>
  );
};

export default ForgotPassword;
