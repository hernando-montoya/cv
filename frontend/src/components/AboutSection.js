import React from 'react';
import { useLanguage } from './LanguageProvider';
import { useContent } from '../hooks/useContent';

const AboutSection = () => {
  const { t, language } = useLanguage();
  const { content } = useContent();

  return (
    <section id="about" className="section-padding bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-8">
            {t('aboutTitle')}
          </h2>
          <div className="w-24 h-1 bg-gradient-to-r from-blue-500 to-cyan-500 mx-auto rounded-full mb-8"></div>
          <p className="text-xl text-gray-600 max-w-4xl mx-auto leading-relaxed">
            {t('aboutDescription')}
          </p>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;