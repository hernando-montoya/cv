import React from "react";
import "./App.css";
import { LanguageProvider } from './components/LanguageProvider';
import Header from './components/Header';
import HeroSection from './components/HeroSection';
import AboutSection from './components/AboutSection';
import ExperienceSection from './components/ExperienceSection';
import EducationSection from './components/EducationSection';
import SkillsSection from './components/SkillsSection';
import ContactSection from './components/ContactSection';
import Footer from './components/Footer';
import { Toaster } from './components/ui/sonner';

function App() {
  return (
    <LanguageProvider>
      <div className="App">
        <Header />
        <HeroSection />
        <div id="about" className="section-padding bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-8">
                About Me
              </h2>
              <div className="w-24 h-1 bg-gradient-to-r from-blue-500 to-cyan-500 mx-auto rounded-full mb-8"></div>
              <p className="text-xl text-gray-600 max-w-4xl mx-auto leading-relaxed">
                Experienced Android developer with 13+ years in software development, 
                specializing in modern Android development with Kotlin, Jetpack Compose, 
                and cutting-edge mobile technologies. Passionate about creating innovative 
                solutions that push the boundaries of mobile development.
              </p>
            </div>
          </div>
        </div>
        <ExperienceSection />
        <EducationSection />
        <SkillsSection />
        <ContactSection />
        <Footer />
        <Toaster />
      </div>
    </LanguageProvider>
  );
}

export default App;
