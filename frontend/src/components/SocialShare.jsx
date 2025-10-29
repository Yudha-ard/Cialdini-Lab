import React from 'react';
import { Button } from '@/components/ui/button';
import { Share2, Twitter, Facebook, Linkedin, Copy } from 'lucide-react';
import { toast } from 'sonner';

const SocialShare = ({ certificate }) => {
  const shareUrl = `${window.location.origin}/certificates/${certificate.id}`;
  const shareText = `Saya telah menyelesaikan course "${certificate.course_title}" di Tegalsec Social Engineering Lab! 🎓🔒`;

  const copyToClipboard = () => {
    navigator.clipboard.writeText(shareUrl);
    toast.success('Link berhasil disalin!');
  };

  const shareToTwitter = () => {
    const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}&url=${encodeURIComponent(shareUrl)}`;
    window.open(url, '_blank', 'width=550,height=420');
  };

  const shareToFacebook = () => {
    const url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`;
    window.open(url, '_blank', 'width=550,height=420');
  };

  const shareToLinkedIn = () => {
    const url = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(shareUrl)}`;
    window.open(url, '_blank', 'width=550,height=420');
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2 text-sm text-gray-400 mb-2">
        <Share2 className="w-4 h-4" />
        <span>Bagikan Sertifikat:</span>
      </div>
      
      <div className="flex flex-wrap gap-2">
        <Button
          onClick={shareToTwitter}
          size="sm"
          variant="outline"
          className="border-zinc-700 hover:border-blue-500 hover:bg-blue-500/10"
        >
          <Twitter className="w-4 h-4 mr-2" />
          Twitter
        </Button>
        
        <Button
          onClick={shareToFacebook}
          size="sm"
          variant="outline"
          className="border-zinc-700 hover:border-blue-600 hover:bg-blue-600/10"
        >
          <Facebook className="w-4 h-4 mr-2" />
          Facebook
        </Button>
        
        <Button
          onClick={shareToLinkedIn}
          size="sm"
          variant="outline"
          className="border-zinc-700 hover:border-blue-700 hover:bg-blue-700/10"
        >
          <Linkedin className="w-4 h-4 mr-2" />
          LinkedIn
        </Button>
        
        <Button
          onClick={copyToClipboard}
          size="sm"
          variant="outline"
          className="border-zinc-700 hover:border-emerald-500 hover:bg-emerald-500/10"
        >
          <Copy className="w-4 h-4 mr-2" />
          Copy Link
        </Button>
      </div>
      
      <div className="bg-zinc-900/50 rounded p-3 mt-3">
        <p className="text-xs text-gray-500 break-all">{shareUrl}</p>
      </div>
    </div>
  );
};

export default SocialShare;
