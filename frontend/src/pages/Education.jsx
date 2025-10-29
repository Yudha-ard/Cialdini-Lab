import React, { useState, useEffect } from 'react';
import { AuthContext, API } from '@/App';
import Layout from '@/components/Layout';
import { Card } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { BookOpen, Shield, Lightbulb } from 'lucide-react';
import axios from 'axios';

const Education = () => {
  const [contents, setContents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEducation();
  }, []);

  const fetchEducation = async () => {
    try {
      const response = await axios.get(`${API}/education`);
      setContents(response.data);
    } catch (error) {
      console.error('Failed to fetch education content:', error);
    } finally {
      setLoading(false);
    }
  };

  const principles = contents.filter(c => c.content_type === 'cialdini_principle');
  const tips = contents.filter(c => c.content_type === 'prevention_tips');

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-emerald-400">Loading...</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-8" data-testid="education-container">
        <div>
          <h1 className="text-4xl font-bold mb-3">Pusat Edukasi</h1>
          <p className="text-gray-400 text-lg">Pelajari prinsip-prinsip social engineering dan cara melindungi diri</p>
        </div>

        <Tabs defaultValue="principles" className="w-full">
          <TabsList className="grid w-full grid-cols-2 bg-zinc-900/50 mb-8">
            <TabsTrigger value="principles" data-testid="principles-tab">
              <Shield className="w-4 h-4 mr-2" />
              Prinsip Cialdini
            </TabsTrigger>
            <TabsTrigger value="tips" data-testid="tips-tab">
              <Lightbulb className="w-4 h-4 mr-2" />
              Tips Pencegahan
            </TabsTrigger>
          </TabsList>

          <TabsContent value="principles" className="space-y-6">
            {principles.map((principle) => (
              <Card key={principle.id} className="glass border-zinc-800 p-8 card-hover" data-testid={`principle-card-${principle.principle}`}>
                <div className="flex items-start gap-4 mb-4">
                  <div className="w-12 h-12 rounded-lg bg-emerald-500/10 flex items-center justify-center flex-shrink-0">
                    <BookOpen className="w-6 h-6 text-emerald-400" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-2xl font-bold mb-2">{principle.title}</h3>
                    <Badge className="bg-purple-500/20 text-purple-400 border-purple-500/30">
                      {principle.principle}
                    </Badge>
                  </div>
                </div>
                <div className="prose prose-invert max-w-none">
                  {principle.content.split('\n\n').map((paragraph, idx) => {
                    // Check if paragraph is a heading (starts with **)
                    if (paragraph.startsWith('**') && paragraph.includes(':**')) {
                      const parts = paragraph.split(':**');
                      const heading = parts[0].replace(/\*\*/g, '');
                      const content = parts[1];
                      return (
                        <div key={idx} className="mb-4">
                          <h4 className="text-emerald-400 font-semibold mb-2">{heading}:</h4>
                          {content && <p className="text-gray-300 leading-relaxed">{content}</p>}
                        </div>
                      );
                    }
                    // Regular paragraph
                    return (
                      <p key={idx} className="text-gray-300 leading-relaxed mb-4 whitespace-pre-line">
                        {paragraph}
                      </p>
                    );
                  })}
                </div>
              </Card>
            ))}
          </TabsContent>

          <TabsContent value="tips" className="space-y-6">
            {tips.map((tip) => (
              <Card key={tip.id} className="glass border-zinc-800 p-8" data-testid="tips-card">
                <div className="flex items-start gap-4 mb-6">
                  <div className="w-12 h-12 rounded-lg bg-yellow-500/10 flex items-center justify-center flex-shrink-0">
                    <Lightbulb className="w-6 h-6 text-yellow-400" />
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold">{tip.title}</h3>
                  </div>
                </div>
                <div className="prose prose-invert max-w-none">
                  {tip.content.split('\n\n').map((section, idx) => {
                    // Check if it's a heading
                    if (section.startsWith('**') && section.endsWith('**')) {
                      return (
                        <h4 key={idx} className="text-emerald-400 font-semibold text-lg mb-3 mt-6">
                          {section.replace(/\*\*/g, '')}
                        </h4>
                      );
                    }
                    // Check if it's a numbered list
                    if (/^\d+\./.test(section)) {
                      const items = section.split('\n').filter(line => line.trim());
                      return (
                        <div key={idx} className="space-y-3 mb-6">
                          {items.map((item, itemIdx) => {
                            const match = item.match(/^(\d+)\.\s*\*\*(.+?)\*\*\s*-\s*(.+)$/);
                            if (match) {
                              const [, num, title, desc] = match;
                              return (
                                <div key={itemIdx} className="flex gap-3">
                                  <span className="text-emerald-400 font-bold flex-shrink-0">{num}.</span>
                                  <div>
                                    <span className="text-white font-semibold">{title}</span>
                                    <span className="text-gray-300"> - {desc}</span>
                                  </div>
                                </div>
                              );
                            }
                            return (
                              <p key={itemIdx} className="text-gray-300 leading-relaxed">
                                {item}
                              </p>
                            );
                          })}
                        </div>
                      );
                    }
                    // Bullet list
                    if (section.includes('\n-')) {
                      const items = section.split('\n').filter(line => line.trim());
                      return (
                        <ul key={idx} className="space-y-2 mb-6">
                          {items.map((item, itemIdx) => {
                            if (item.startsWith('-')) {
                              return (
                                <li key={itemIdx} className="flex items-start gap-3 text-gray-300">
                                  <span className="text-emerald-400 mt-1">✓</span>
                                  <span>{item.replace(/^-\s*/, '')}</span>
                                </li>
                              );
                            }
                            return null;
                          })}
                        </ul>
                      );
                    }
                    // Regular paragraph
                    return (
                      <p key={idx} className="text-gray-300 leading-relaxed mb-4">
                        {section}
                      </p>
                    );
                  })}
                </div>
              </Card>
            ))}
          </TabsContent>
        </Tabs>
      </div>
    </Layout>
  );
};

export default Education;