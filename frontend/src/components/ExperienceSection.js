import React from 'react';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Calendar, MapPin, Building } from 'lucide-react';
import { useContent } from '../hooks/useContent';
import { useLanguage } from './LanguageProvider';

const ExperienceSection = () => {
  const { language, t } = useLanguage();

  const getPeriod = (experience) => {
    if (language === 'es' && experience.period_es) return experience.period_es;
    if (language === 'fr' && experience.period_fr) return experience.period_fr;
    return experience.period;
  };

  return (
    <section id="experience" className="section-padding bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-4">
            {t('experienceTitle')}
          </h2>
          <div className="w-24 h-1 bg-gradient-to-r from-blue-500 to-cyan-500 mx-auto rounded-full"></div>
        </div>

        <div className="relative">
          {/* Timeline Line */}
          <div className="absolute left-4 md:left-1/2 transform md:-translate-x-1/2 w-1 h-full bg-gradient-to-b from-blue-500 to-cyan-500 rounded-full"></div>

          <div className="space-y-12">
            {experiences.map((experience, index) => (
              <div
                key={experience.id}
                className={`relative flex items-center ${
                  index % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse'
                } flex-col md:items-start`}
              >
                {/* Timeline Dot */}
                <div className="absolute left-4 md:left-1/2 transform md:-translate-x-1/2 w-4 h-4 bg-white border-4 border-blue-500 rounded-full z-10 animate-pulse-glow"></div>

                {/* Content Card */}
                <div className={`w-full md:w-5/12 ml-12 md:ml-0 ${index % 2 === 0 ? 'md:mr-8' : 'md:ml-8'}`}>
                  <Card className="card-hover hover-lift bg-white shadow-lg hover:shadow-2xl transition-all duration-300">
                    <CardContent className="p-8">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <h3 className="text-xl font-bold text-gray-900 mb-2">
                            {experience.title}
                          </h3>
                          <div className="flex items-center text-blue-600 font-semibold mb-2">
                            <Building className="w-4 h-4 mr-2" />
                            {experience.company}
                          </div>
                          <div className="flex items-center text-gray-600 text-sm mb-2">
                            <MapPin className="w-4 h-4 mr-2" />
                            {experience.location}
                          </div>
                          <div className="flex items-center text-gray-500 text-sm">
                            <Calendar className="w-4 h-4 mr-2" />
                            {getPeriod(experience)}
                          </div>
                        </div>
                      </div>

                      <ul className="space-y-2">
                        {experience.description[language] && experience.description[language].map((item, idx) => (
                          <li key={idx} className="flex items-start text-gray-700">
                            <div className="w-2 h-2 bg-blue-500 rounded-full mr-3 mt-2 flex-shrink-0"></div>
                            <span className="text-sm leading-relaxed">{item}</span>
                          </li>
                        ))}
                      </ul>
                    </CardContent>
                  </Card>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default ExperienceSection;