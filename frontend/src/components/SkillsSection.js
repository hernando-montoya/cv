import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Code, Smartphone, Tool, Target, Globe, BarChart } from 'lucide-react';
import { skills, languages } from '../data/mockData';
import { useLanguage } from './LanguageProvider';

const SkillsSection = () => {
  const { t } = useLanguage();

  const skillCategories = [
    {
      title: t('languages'),
      icon: Code,
      skills: skills.languages,
      color: 'from-blue-500 to-blue-600',
      bgColor: 'bg-blue-50',
      iconColor: 'text-blue-600'
    },
    {
      title: t('android'),
      icon: Smartphone,
      skills: skills.android,
      color: 'from-cyan-500 to-cyan-600',
      bgColor: 'bg-cyan-50',
      iconColor: 'text-cyan-600'
    },
    {
      title: t('tools'),
      icon: Tool,
      skills: skills.tools,
      color: 'from-indigo-500 to-indigo-600',
      bgColor: 'bg-indigo-50',
      iconColor: 'text-indigo-600'
    },
    {
      title: t('methodologies'),
      icon: Target,
      skills: skills.methodologies,
      color: 'from-purple-500 to-purple-600',
      bgColor: 'bg-purple-50',
      iconColor: 'text-purple-600'
    }
  ];

  return (
    <section id="skills" className="section-padding bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-4">
            {t('skillsTitle')}
          </h2>
          <div className="w-24 h-1 bg-gradient-to-r from-blue-500 to-cyan-500 mx-auto rounded-full"></div>
        </div>

        {/* Technical Skills Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          {skillCategories.map((category, index) => (
            <Card 
              key={category.title}
              className={`card-hover hover-lift ${category.bgColor} border-0 shadow-lg hover:shadow-xl transition-all duration-300 animate-fade-in-up`}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <CardHeader className="pb-4">
                <div className="flex items-center space-x-3">
                  <div className={`p-2 rounded-lg bg-white ${category.iconColor}`}>
                    <category.icon className="w-6 h-6" />
                  </div>
                  <CardTitle className="text-lg font-bold text-gray-900">
                    {category.title}
                  </CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {category.skills.map((skill) => (
                    <Badge
                      key={skill}
                      variant="secondary"
                      className="bg-white text-gray-700 font-medium hover:bg-gray-100 transition-colors cursor-default"
                    >
                      {skill}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Language Proficiency */}
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h3 className="text-3xl font-bold text-gray-900 mb-4 flex items-center justify-center">
              <Globe className="w-8 h-8 mr-3 text-blue-600" />
              {t('languageTitle')}
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {languages.map((lang, index) => (
              <Card 
                key={lang.name}
                className={`card-hover hover-lift bg-white shadow-lg hover:shadow-xl transition-all duration-300 animate-fade-in-up`}
                style={{ animationDelay: `${index * 0.2}s` }}
              >
                <CardContent className="p-8">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h4 className="text-xl font-bold text-gray-900">{lang.name}</h4>
                      <p className="text-gray-600 font-medium">{lang.level}</p>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-blue-600">{lang.proficiency}%</div>
                    </div>
                  </div>
                  
                  <div className="skill-bar">
                    <div 
                      className="skill-progress"
                      style={{ 
                        width: `${lang.proficiency}%`,
                        animationDelay: `${index * 0.5}s`
                      }}
                    ></div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default SkillsSection;