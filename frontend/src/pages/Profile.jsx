import React, { useState } from 'react';
import { AuthContext, API } from '@/App';
import Layout from '@/components/Layout';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { User, Lock, Mail, Save } from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';

const Profile = () => {
  const { user, token, setUser } = React.useContext(AuthContext);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    full_name: user?.full_name || '',
    email: user?.email || '',
    current_password: '',
    new_password: '',
    confirm_password: ''
  });

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    
    try {
      const updateData = {
        full_name: formData.full_name,
        email: formData.email
      };

      await axios.put(`${API}/user/profile`, updateData, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setUser({ ...user, ...updateData });
      toast.success('Profile berhasil diupdate!');
      setIsEditing(false);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Gagal update profile');
    }
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    
    if (formData.new_password !== formData.confirm_password) {
      toast.error('Password baru tidak cocok!');
      return;
    }

    if (formData.new_password.length < 6) {
      toast.error('Password minimal 6 karakter!');
      return;
    }

    try {
      await axios.put(`${API}/user/change-password`, {
        current_password: formData.current_password,
        new_password: formData.new_password
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      toast.success('Password berhasil diubah!');
      setFormData({
        ...formData,
        current_password: '',
        new_password: '',
        confirm_password: ''
      });
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Gagal ubah password');
    }
  };

  return (
    <Layout>
      <div className="max-w-4xl mx-auto space-y-8">
        <div>
          <h1 className="text-4xl font-bold mb-3">Profile Saya</h1>
          <p className="text-gray-400 text-lg">Kelola informasi profile dan keamanan akun Anda</p>
        </div>

        {/* Profile Info */}
        <Card className="glass border-zinc-800 p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-12 h-12 rounded-full bg-gradient-to-r from-emerald-500 to-cyan-500 flex items-center justify-center">
              <User className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold">{user?.full_name}</h2>
              <p className="text-gray-400">@{user?.username}</p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-6 mb-6">
            <div>
              <p className="text-sm text-gray-400 mb-1">Role</p>
              <p className="font-semibold capitalize">{user?.role}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400 mb-1">Level</p>
              <p className="font-semibold">{user?.level}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400 mb-1">Points</p>
              <p className="font-semibold text-yellow-400">{user?.points || 0}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400 mb-1">Challenges Completed</p>
              <p className="font-semibold text-emerald-400">{user?.completed_challenges?.length || 0}</p>
            </div>
          </div>

          <Button 
            onClick={() => setIsEditing(!isEditing)}
            variant="outline"
            className="w-full"
          >
            {isEditing ? 'Batal Edit' : 'Edit Profile'}
          </Button>
        </Card>

        {/* Edit Profile Form */}
        {isEditing && (
          <Card className="glass border-zinc-800 p-6">
            <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <Mail className="w-5 h-5 text-emerald-400" />
              Edit Profile Information
            </h3>
            <form onSubmit={handleUpdateProfile} className="space-y-4">
              <div>
                <Label>Nama Lengkap</Label>
                <Input
                  value={formData.full_name}
                  onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                  className="bg-zinc-900/50 border-zinc-800 mt-2"
                  required
                />
              </div>
              <div>
                <Label>Email</Label>
                <Input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="bg-zinc-900/50 border-zinc-800 mt-2"
                  required
                />
              </div>
              <Button type="submit" className="w-full bg-emerald-600 hover:bg-emerald-700">
                <Save className="w-4 h-4 mr-2" />
                Simpan Perubahan
              </Button>
            </form>
          </Card>
        )}

        {/* Change Password */}
        <Card className="glass border-zinc-800 p-6">
          <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Lock className="w-5 h-5 text-red-400" />
            Ubah Password
          </h3>
          <form onSubmit={handleChangePassword} className="space-y-4">
            <div>
              <Label>Password Saat Ini</Label>
              <Input
                type="password"
                value={formData.current_password}
                onChange={(e) => setFormData({ ...formData, current_password: e.target.value })}
                className="bg-zinc-900/50 border-zinc-800 mt-2"
                placeholder="Masukkan password saat ini"
                required
              />
            </div>
            <div>
              <Label>Password Baru</Label>
              <Input
                type="password"
                value={formData.new_password}
                onChange={(e) => setFormData({ ...formData, new_password: e.target.value })}
                className="bg-zinc-900/50 border-zinc-800 mt-2"
                placeholder="Minimal 6 karakter"
                required
              />
            </div>
            <div>
              <Label>Konfirmasi Password Baru</Label>
              <Input
                type="password"
                value={formData.confirm_password}
                onChange={(e) => setFormData({ ...formData, confirm_password: e.target.value })}
                className="bg-zinc-900/50 border-zinc-800 mt-2"
                placeholder="Ulangi password baru"
                required
              />
            </div>
            <Button type="submit" className="w-full bg-red-600 hover:bg-red-700">
              <Lock className="w-4 h-4 mr-2" />
              Ubah Password
            </Button>
          </form>
        </Card>
      </div>
    </Layout>
  );
};

export default Profile;
