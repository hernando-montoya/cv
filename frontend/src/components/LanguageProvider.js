import React, { createContext, useContext, useState } from 'react';

const translations = {
  en: {
    // Header
    downloadCV: 'Download CV',
    
    // Hero Section
    heroTitle: 'Android Research & Development Engineer',
    heroSubtitle: 'Passionate about creating innovative mobile solutions with cutting-edge technology',
    contactMe: 'Contact Me',
    
    // Navigation
    about: 'About',
    experience: 'Experience',
    education: 'Education',
    skills: 'Skills',
    contact: 'Contact',
    
    // About Section
    aboutTitle: 'About Me',
    aboutDescription: 'Experienced Android developer with 13+ years in software development, specializing in modern Android development with Kotlin, Jetpack Compose, and cutting-edge mobile technologies. Passionate about creating innovative solutions that push the boundaries of mobile development.',
    
    // Experience Section
    experienceTitle: 'Professional Experience',
    present: 'Present',
    
    // Education Section
    educationTitle: 'Education & Certifications',
    
    // Skills Section
    skillsTitle: 'Technical Skills',
    languages: 'Languages',
    android: 'Android',
    tools: 'Tools & IDE',
    methodologies: 'Methodologies',
    
    // Contact Section
    contactTitle: 'Get In Touch',
    contactSubtitle: 'Ready to collaborate on your next project',
    name: 'Name',
    email: 'Email',
    message: 'Message',
    sendMessage: 'Send Message',
    
    // Languages
    languageTitle: 'Languages',
    english: 'English (B2)',
    spanish: 'Spanish (Native)',
    
    // Footer
    footerText: 'Built with React & Modern Web Technologies'
  },
  es: {
    // Header
    downloadCV: 'Descargar CV',
    
    // Hero Section
    heroTitle: 'Ingeniero de Investigación y Desarrollo Android',
    heroSubtitle: 'Apasionado por crear soluciones móviles innovadoras con tecnología de vanguardia',
    contactMe: 'Contáctame',
    
    // Navigation
    about: 'Acerca de',
    experience: 'Experiencia',
    education: 'Educación',
    skills: 'Habilidades',
    contact: 'Contacto',
    
    // About Section
    aboutTitle: 'Acerca de Mí',
    aboutDescription: 'Desarrollador Android experimentado con más de 13 años en desarrollo de software, especializado en desarrollo Android moderno con Kotlin, Jetpack Compose y tecnologías móviles de vanguardia. Apasionado por crear soluciones innovadoras que expanden los límites del desarrollo móvil.',
    
    // Experience Section
    experienceTitle: 'Experiencia Profesional',
    present: 'Presente',
    
    // Education Section
    educationTitle: 'Educación y Certificaciones',
    
    // Skills Section
    skillsTitle: 'Habilidades Técnicas',
    languages: 'Lenguajes',
    android: 'Android',
    tools: 'Herramientas e IDE',
    methodologies: 'Metodologías',
    
    // Contact Section
    contactTitle: 'Ponte en Contacto',
    contactSubtitle: 'Listo para colaborar en tu próximo proyecto',
    name: 'Nombre',
    email: 'Correo',
    message: 'Mensaje',
    sendMessage: 'Enviar Mensaje',
    
    // Languages
    languageTitle: 'Idiomas',
    english: 'Inglés (B2)',
    spanish: 'Español (Nativo)',
    
    // Footer
    footerText: 'Construido con React y Tecnologías Web Modernas'
  },
  fr: {
    // Header
    downloadCV: 'Télécharger CV',
    
    // Hero Section
    heroTitle: 'Ingénieur de Recherche et Développement Android',
    heroSubtitle: 'Passionné par la création de solutions mobiles innovantes avec des technologies de pointe',
    contactMe: 'Me Contacter',
    
    // Navigation
    about: 'À Propos',
    experience: 'Expérience',
    education: 'Éducation',
    skills: 'Compétences',
    contact: 'Contact',
    
    // About Section
    aboutTitle: 'À Propos de Moi',
    aboutDescription: 'Développeur Android expérimenté avec plus de 13 ans en développement logiciel, spécialisé dans le développement Android moderne avec Kotlin, Jetpack Compose et les technologies mobiles de pointe.',
    
    // Experience Section
    experienceTitle: 'Expérience Professionnelle',
    present: 'Présent',
    
    // Education Section
    educationTitle: 'Éducation et Certifications',
    
    // Skills Section
    skillsTitle: 'Compétences Techniques',
    languages: 'Langages',
    android: 'Android',
    tools: 'Outils et IDE',
    methodologies: 'Méthodologies',
    
    // Contact Section
    contactTitle: 'Entrer en Contact',
    contactSubtitle: 'Prêt à collaborer sur votre prochain projet',
    name: 'Nom',
    email: 'Email',
    message: 'Message',
    sendMessage: 'Envoyer le Message',
    
    // Languages
    languageTitle: 'Langues',
    english: 'Anglais (B2)',
    spanish: 'Espagnol (Bilingue)',
    
    // Footer
    footerText: 'Construit avec React et Technologies Web Modernes'
  }
};

const LanguageContext = createContext();

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState('en');
  
  const t = (key) => {
    return translations[language][key] || key;
  };
  
  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};