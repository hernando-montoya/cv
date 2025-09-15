import React from 'react';
import { Button } from './ui/button';
import { Mail, Globe, Phone, ArrowDown } from 'lucide-react';
import { useContent } from '../hooks/useContent';
import { useLanguage } from './LanguageProvider';

const HeroSection = () => {
  const { t } = useLanguage();

  const scrollToContact = () => {
    const element = document.getElementById('contact');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-cyan-50 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-100 rounded-full opacity-20 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-cyan-100 rounded-full opacity-20 animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-blue-200 rounded-full opacity-10 animate-spin" style={{animationDuration: '20s'}}></div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left Column - Content */}
          <div className="space-y-8 animate-fade-in-up">
            <div className="space-y-4">
              <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-gray-900 leading-tight">
                <span className="block">Hernando</span>
                <span className="block bg-gradient-to-r from-blue-600 via-blue-500 to-cyan-500 bg-clip-text text-transparent">
                  Montoya
                </span>
              </h1>
              <h2 className="text-xl sm:text-2xl text-gray-600 font-medium">
                {t('heroTitle')}
              </h2>
              <p className="text-lg text-gray-500 max-w-2xl leading-relaxed">
                {t('heroSubtitle')}
              </p>
            </div>

            {/* Contact Info */}
            <div className="flex flex-wrap gap-6 text-sm text-gray-600">
              <div className="flex items-center space-x-2 hover:text-blue-600 transition-colors cursor-pointer">
                <Mail className="w-4 h-4" />
                <span>{personalInfo.email}</span>
              </div>
              <div className="flex items-center space-x-2 hover:text-blue-600 transition-colors cursor-pointer">
                <Phone className="w-4 h-4" />
                <span>{personalInfo.phone}</span>
              </div>
              <div className="flex items-center space-x-2 hover:text-blue-600 transition-colors cursor-pointer">
                <Globe className="w-4 h-4" />
                <span>{personalInfo.website}</span>
              </div>
            </div>

            {/* CTA Button */}
            <div className="pt-6">
              <Button 
                onClick={scrollToContact}
                size="lg"
                className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white px-8 py-4 text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
              >
                {t('contactMe')}
                <ArrowDown className="w-5 h-5 ml-2 animate-bounce" />
              </Button>
            </div>
          </div>

          {/* Right Column - Profile Image */}
          <div className="flex justify-center lg:justify-end animate-fade-in-up delay-200">
            <div className="relative">
              {/* Decorative Elements */}
              <div className="absolute -inset-4 bg-gradient-to-r from-blue-400 to-cyan-400 rounded-3xl opacity-20 animate-pulse"></div>
              <div className="absolute -inset-8 bg-gradient-to-r from-blue-300 to-cyan-300 rounded-3xl opacity-10 animate-pulse delay-500"></div>
              
              {/* Profile Image */}
              <div className="relative z-10 w-80 h-80 sm:w-96 sm:h-96 lg:w-[420px] lg:h-[420px] rounded-3xl overflow-hidden shadow-2xl transform hover:scale-105 transition-transform duration-500">
                <img
                  src={personalInfo.profileImage}
                  alt="Hernando Montoya"
                  className="w-full h-full object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-blue-900/20 to-transparent"></div>
              </div>

              {/* Floating Elements */}
              <div className="absolute -top-6 -right-6 w-16 h-16 bg-blue-500 rounded-2xl opacity-80 animate-float shadow-lg flex items-center justify-center">
                <Globe className="w-8 h-8 text-white" />
              </div>
              <div className="absolute -bottom-6 -left-6 w-20 h-20 bg-cyan-500 rounded-2xl opacity-80 animate-float delay-1000 shadow-lg flex items-center justify-center">
                <Mail className="w-10 h-10 text-white" />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div className="w-6 h-10 border-2 border-blue-400 rounded-full flex justify-center">
          <div className="w-1 h-3 bg-blue-400 rounded-full mt-2 animate-pulse"></div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;