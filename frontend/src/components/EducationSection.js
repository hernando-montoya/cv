import React from 'react';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { GraduationCap, Award, Calendar } from 'lucide-react';
import { education } from '../data/mockData';
import { useLanguage } from './LanguageProvider';

const EducationSection = () => {
  const { t } = useLanguage();

  return (
    <section id="education" className="section-padding bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-4">
            {t('educationTitle')}
          </h2>
          <div className="w-24 h-1 bg-gradient-to-r from-blue-500 to-cyan-500 mx-auto rounded-full"></div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {education.map((item, index) => (
            <Card 
              key={item.id} 
              className={`card-hover hover-lift bg-gradient-to-br ${
                item.type === 'degree' 
                  ? 'from-blue-50 to-cyan-50 border-blue-200' 
                  : 'from-gray-50 to-blue-50 border-gray-200'
              } shadow-md hover:shadow-xl transition-all duration-300 animate-fade-in-up`}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <CardContent className="p-6">
                <div className="flex items-start space-x-4">
                  <div className={`p-3 rounded-full ${
                    item.type === 'degree' 
                      ? 'bg-blue-100 text-blue-600' 
                      : 'bg-cyan-100 text-cyan-600'
                  }`}>
                    {item.type === 'degree' ? (
                      <GraduationCap className="w-6 h-6" />
                    ) : (
                      <Award className="w-6 h-6" />
                    )}
                  </div>
                  
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-2">
                      <Badge 
                        variant="secondary" 
                        className={`${
                          item.type === 'degree' 
                            ? 'bg-blue-100 text-blue-800' 
                            : 'bg-cyan-100 text-cyan-800'
                        } font-medium`}
                      >
                        {item.type === 'degree' ? 'Degree' : 'Certification'}
                      </Badge>
                      <div className="flex items-center text-gray-500 text-sm">
                        <Calendar className="w-4 h-4 mr-1" />
                        {item.year}
                      </div>
                    </div>
                    
                    <h3 className="font-bold text-gray-900 mb-2 text-lg leading-tight">
                      {item.title}
                    </h3>
                    
                    <p className="text-gray-600 text-sm font-medium">
                      {item.institution}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default EducationSection;