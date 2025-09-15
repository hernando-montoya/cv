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
        <AboutSection />
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
