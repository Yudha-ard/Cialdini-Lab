import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { AuthContext } from '@/App';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { Home, Target, BookOpen, Trophy, Shield, LogOut, Menu, Settings, Zap, Gamepad2 } from 'lucide-react';

const Layout = ({ children }) => {
  const { user, logout } = React.useContext(AuthContext);
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = React.useState(false);

  const navigation = [
    { name: 'Dashboard', path: '/dashboard', icon: <Home className="w-5 h-5" /> },
    { name: 'Challenges', path: '/challenges', icon: <Target className="w-5 h-5" /> },
    { name: 'Courses', path: '/courses', icon: <BookOpen className="w-5 h-5" /> },
    { name: 'Mini Game', path: '/spot-the-phishing', icon: <Gamepad2 className="w-5 h-5" /> },
    { name: 'Quiz Mode', path: '/quiz', icon: <Zap className="w-5 h-5" /> },
    { name: 'Edukasi', path: '/education', icon: <BookOpen className="w-5 h-5" /> },
    { name: 'Leaderboard', path: '/leaderboard', icon: <Trophy className="w-5 h-5" /> },
  ];

  if (user?.role === 'admin') {
    navigation.push({ name: 'Admin Panel', path: '/admin', icon: <Settings className="w-5 h-5" /> });
  }

  const NavLinks = ({ mobile = false }) => (
    <>
      {navigation.map((item) => {
        const isActive = location.pathname === item.path;
        return (
          <Link
            key={item.path}
            to={item.path}
            onClick={() => mobile && setMobileOpen(false)}
            className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
              isActive
                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                : 'text-gray-400 hover:bg-zinc-800/50 hover:text-gray-200'
            }`}
            data-testid={`nav-link-${item.name.toLowerCase().replace(' ', '-')}`}
          >
            {item.icon}
            <span>{item.name}</span>
          </Link>
        );
      })}
    </>
  );

  return (
    <div className="min-h-screen bg-[#0a0a0b] cyber-grid">
      {/* Sidebar - Desktop */}
      <aside className="hidden lg:block fixed left-0 top-0 h-screen w-64 glass border-r border-zinc-800 p-6">
        <Link to="/dashboard" className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 rounded-lg bg-emerald-500/20 flex items-center justify-center">
            <Shield className="w-6 h-6 text-emerald-400" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-emerald-400">Tegalsec Lab</h1>
            <p className="text-xs text-gray-400">Social Engineering</p>
          </div>
        </Link>

        <nav className="space-y-2 mb-8">
          <NavLinks />
        </nav>

        <div className="absolute bottom-6 left-6 right-6">
          <div className="glass border border-zinc-800 rounded-lg p-4 mb-4">
            <p className="text-sm font-semibold mb-1">{user?.full_name}</p>
            <p className="text-xs text-gray-400 mb-2">@{user?.username}</p>
            <div className="flex items-center justify-between text-xs">
              <span className="text-gray-400">Level</span>
              <span className="text-emerald-400 font-semibold">{user?.level}</span>
            </div>
            <div className="flex items-center justify-between text-xs mt-1">
              <span className="text-gray-400">Poin</span>
              <span className="text-yellow-400 font-semibold">{user?.points}</span>
            </div>
          </div>
          <Button 
            variant="outline" 
            className="w-full border-red-500/50 hover:bg-red-500/10 text-red-400"
            onClick={logout}
            data-testid="logout-button"
          >
            <LogOut className="w-4 h-4 mr-2" />
            Logout
          </Button>
        </div>
      </aside>

      {/* Mobile Header */}
      <header className="lg:hidden fixed top-0 left-0 right-0 z-50 glass border-b border-zinc-800 px-4 py-3">
        <div className="flex items-center justify-between">
          <Link to="/dashboard" className="flex items-center gap-2">
            <Shield className="w-6 h-6 text-emerald-400" />
            <span className="font-bold text-emerald-400">Tegalsec Lab</span>
          </Link>
          <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon" data-testid="mobile-menu-button">
                <Menu className="w-6 h-6" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="bg-zinc-950 border-zinc-800 w-64">
              <div className="py-4">
                <div className="mb-6">
                  <p className="text-sm font-semibold mb-1">{user?.full_name}</p>
                  <p className="text-xs text-gray-400">@{user?.username}</p>
                  <div className="flex gap-4 mt-3 text-xs">
                    <div>
                      <span className="text-gray-400">Level: </span>
                      <span className="text-emerald-400 font-semibold">{user?.level}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Poin: </span>
                      <span className="text-yellow-400 font-semibold">{user?.points}</span>
                    </div>
                  </div>
                </div>
                <nav className="space-y-2 mb-6">
                  <NavLinks mobile={true} />
                </nav>
                <Button 
                  variant="outline" 
                  className="w-full border-red-500/50 hover:bg-red-500/10 text-red-400"
                  onClick={() => { logout(); setMobileOpen(false); }}
                >
                  <LogOut className="w-4 h-4 mr-2" />
                  Logout
                </Button>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </header>

      {/* Main Content */}
      <main className="lg:ml-64 min-h-screen p-4 lg:p-8 pt-20 lg:pt-8">
        <div className="max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;