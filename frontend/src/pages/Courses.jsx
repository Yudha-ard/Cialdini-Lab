import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { API } from '@/App';
import Layout from '@/components/Layout';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { BookOpen, Clock, Award, ChevronRight } from 'lucide-react';
import axios from 'axios';

const Courses = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const response = await axios.get(`${API}/courses`);
      setCourses(response.data);
    } catch (error) {
      console.error('Failed to fetch courses');
    } finally {
      setLoading(false);
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

  return (
    <Layout>
      <div className="space-y-8">
        <div>
          <h1 className="text-4xl font-bold mb-3">Courses</h1>
          <p className="text-gray-400 text-lg">Pelajari social engineering secara mendalam dengan course terstruktur</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((course) => (
            <Card key={course.id} className="glass border-zinc-800 p-6 card-hover">
              <div className="flex items-start gap-3 mb-4">
                <div className="w-12 h-12 rounded-lg bg-cyan-500/10 flex items-center justify-center">
                  <BookOpen className="w-6 h-6 text-cyan-400" />
                </div>
                <div className="flex-1">
                  <Badge className={`${
                    course.difficulty === 'beginner' ? 'bg-emerald-500/20 text-emerald-400' :
                    course.difficulty === 'intermediate' ? 'bg-yellow-500/20 text-yellow-400' :
                    'bg-red-500/20 text-red-400'
                  } mb-2`}>
                    {course.difficulty}
                  </Badge>
                </div>
              </div>

              <h3 className="text-xl font-bold mb-2">{course.title}</h3>
              <p className="text-gray-400 text-sm mb-4 line-clamp-3">{course.description}</p>

              <div className="flex items-center gap-4 mb-4 text-sm text-gray-400">
                <div className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  <span>{course.total_duration_minutes} min</span>
                </div>
                <div className="flex items-center gap-1">
                  <BookOpen className="w-4 h-4" />
                  <span>{course.modules.length} modules</span>
                </div>
              </div>

              <Link to={`/courses/${course.id}`}>
                <Button className="w-full bg-cyan-600 hover:bg-cyan-700">
                  Mulai Course
                  <ChevronRight className="w-4 h-4 ml-2" />
                </Button>
              </Link>
            </Card>
          ))}
        </div>

        {courses.length === 0 && (
          <div className="text-center py-16">
            <p className="text-gray-400 text-lg">Belum ada course tersedia</p>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default Courses;