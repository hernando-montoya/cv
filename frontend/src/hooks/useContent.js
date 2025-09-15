import { useState, useEffect } from 'react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Fallback data in case backend is not available
const fallbackData = {
  personalInfo: {
    name: "Hernando Montoya Oliveros",
    title: "Android Research & Development Engineer",
    phone: "06.23.70.58.66",
    email: "h.montoya2004@gmail.com",
    website: "hernandomontoya.net",
    profileImage: "https://customer-assets.emergentagent.com/job_responsive-vita/artifacts/x21fq5wh_profil.png"
  },
  experiences: [
    {
      id: "1",
      title: "Développeur Android",
      company: "Veepee",
      location: "Full Remote",
      period: "2022 – Present",
      period_es: "2022 – Presente",
      period_fr: "2022 – Présent",
      description: {
        en: [
          "Developed the Veepee/Privalia application for a group present in several European countries",
          "Created new functionalities and integrated Jetpack Compose",
          "Corrected bugs and improved performance",
          "Created unit and UI tests",
          "Deployed the app to the Play Store and App Gallery",
          "Monitored different releases"
        ],
        es: [
          "Desarrollé la aplicación Veepee/Privalia para un grupo presente en varios países europeos",
          "Creé nuevas funcionalidades e integré Jetpack Compose",
          "Corregí errores y mejoré el rendimiento",
          "Creé pruebas unitarias y de UI",
          "Desplegué la aplicación en Play Store y App Gallery",
          "Monitoreé diferentes versiones"
        ],
        fr: [
          "Développé l'application Veepee/Privalia pour un groupe présent dans plusieurs pays européens",
          "Créé de nouvelles fonctionnalités et intégré Jetpack Compose",
          "Corrigé des bugs et amélioré les performances",
          "Créé des tests unitaires et UI",
          "Déployé l'application sur le Play Store et App Gallery",
          "Surveillé différentes versions"
        ]
      }
    }
  ],
  education: [
    {
      id: "1",
      title: "Kotlin for Android Developers",
      institution: "Antonio Leiva",
      year: "2017",
      type: "certification"
    }
  ],
  skills: {
    languages: ["Kotlin", "Java"],
    android: ["Gradle", "Firebase", "Dagger2", "Dagger Hilt", "RxJava", "Coroutines", "Jetpack Compose"],
    tools: ["Android Studio", "VS Code", "Git", "Bitrise"],
    methodologies: ["MVVM", "UML", "Scrum"]
  },
  languages: [
    { name: "English", level: "B2", proficiency: 75 },
    { name: "Spanish", level: "Native", proficiency: 100 },
    { name: "French", level: "Bilingual", proficiency: 95 }
  ],
  aboutDescription: {
    en: "Experienced Android developer with 13+ years in software development, specializing in modern Android development with Kotlin, Jetpack Compose, and cutting-edge mobile technologies. Passionate about creating innovative solutions that push the boundaries of mobile development.",
    es: "Desarrollador Android experimentado con más de 13 años en desarrollo de software, especializado en desarrollo Android moderno con Kotlin, Jetpack Compose y tecnologías móviles de vanguardia. Apasionado por crear soluciones innovadoras que expanden los límites del desarrollo móvil.",
    fr: "Développeur Android expérimenté avec plus de 13 ans en développement logiciel, spécialisé dans le développement Android moderne avec Kotlin, Jetpack Compose et les technologies mobiles de pointe. Passionné par la création de solutions innovantes qui repoussent les limites du développement mobile."
  }
};

export const useContent = () => {
  const [content, setContent] = useState(fallbackData);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadContent = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${API}/content/`);
      
      if (response.ok) {
        const data = await response.json();
        setContent(data);
      } else {
        // Use fallback data if backend is not available
        console.log('Backend not available, using fallback data');
        setContent(fallbackData);
      }
    } catch (err) {
      console.log('Error loading content, using fallback data:', err);
      setContent(fallbackData);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadContent();
  }, []);

  return {
    content,
    loading,
    error,
    refreshContent: loadContent
  };
};

export default useContent;