import React, { useState } from "react";
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
import AdminPanel from './components/AdminPanel';
import AuthModal from './components/AuthModal';
import { Toaster } from './components/ui/sonner';

function App() {
  const [showAdmin, setShowAdmin] = useState(false);
  const [showAuth, setShowAuth] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleAdminToggle = () => {
    if (isAuthenticated) {
      setShowAdmin(!showAdmin);
    } else {
      setShowAuth(true);
    }
  };

  const handleAuthenticated = () => {
    setIsAuthenticated(true);
    setShowAuth(false);
    setShowAdmin(true);
  };

  const handleCloseAuth = () => {
    setShowAuth(false);
  };

  return (
    <LanguageProvider>
      <div className="App">
        <Header onToggleAdmin={() => setShowAdmin(!showAdmin)} />
        <HeroSection />
        <AboutSection />
        <ExperienceSection />
        <EducationSection />
        <SkillsSection />
        <ContactSection />
        <Footer />
        <AdminPanel 
          isVisible={showAdmin} 
          onToggle={() => setShowAdmin(!showAdmin)} 
        />
        <Toaster />
      </div>
    </LanguageProvider>
  );
}

export default App;
