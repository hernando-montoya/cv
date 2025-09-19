#!/usr/bin/env python3
"""
Script final para arreglar frontend con cambio de idiomas Y admin panel completo
"""

import subprocess
import sys

def create_complete_frontend():
    """Crear frontend completo con cambio de idiomas funcional"""
    
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hernando Montoya Oliveros - Android Developer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        body { font-family: 'Inter', sans-serif; }
        .glassmorphism {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
        .gradient-text {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-10px); } }
        .animate-float { animation: float 6s ease-in-out infinite; }
        .lang-button.active { background: #3b82f6; color: white; }
    </style>
</head>
<body class="bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
    <!-- Navigation -->
    <nav class="fixed top-0 left-0 right-0 z-50 glassmorphism">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="font-bold text-xl text-gray-800">HM</div>
                <div class="hidden md:flex space-x-8">
                    <a href="#home" class="text-gray-700 hover:text-blue-600 transition-colors">Home</a>
                    <a href="#about" class="text-gray-700 hover:text-blue-600 transition-colors">About</a>
                    <a href="#experience" class="text-gray-700 hover:text-blue-600 transition-colors">Experience</a>
                    <a href="#skills" class="text-gray-700 hover:text-blue-600 transition-colors">Skills</a>
                </div>
                <div class="flex space-x-2">
                    <button onclick="changeLanguage('en')" class="lang-button active px-3 py-1 text-sm bg-blue-100 text-blue-800 rounded-full hover:bg-blue-200 transition-colors" id="lang-en">EN</button>
                    <button onclick="changeLanguage('es')" class="lang-button px-3 py-1 text-sm bg-blue-100 text-blue-800 rounded-full hover:bg-blue-200 transition-colors" id="lang-es">ES</button>
                    <button onclick="changeLanguage('fr')" class="lang-button px-3 py-1 text-sm bg-blue-100 text-blue-800 rounded-full hover:bg-blue-200 transition-colors" id="lang-fr">FR</button>
                    <a href="/admin" class="px-4 py-2 bg-gray-800 text-white rounded-full hover:bg-gray-700 transition-colors">Admin</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="min-h-screen flex items-center justify-center relative overflow-hidden pt-16">
        <div class="absolute inset-0">
            <div class="absolute -top-40 -right-40 w-80 h-80 bg-blue-200 rounded-full opacity-20 animate-pulse"></div>
            <div class="absolute -bottom-40 -left-40 w-96 h-96 bg-indigo-200 rounded-full opacity-20 animate-pulse"></div>
        </div>
        
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <div class="space-y-8">
                    <div class="space-y-4">
                        <h1 class="text-5xl sm:text-6xl lg:text-7xl font-bold text-gray-900 leading-tight">
                            <span class="block" id="firstName">Hernando</span>
                            <span class="block gradient-text" id="lastName">Montoya Oliveros</span>
                        </h1>
                        <h2 class="text-xl sm:text-2xl text-gray-600 font-medium" id="jobTitle">
                            Android Research & Development Engineer
                        </h2>
                        <p class="text-lg text-gray-500 max-w-2xl leading-relaxed" id="heroDescription">
                            Experienced Android developer specializing in modern development with Kotlin and Jetpack Compose
                        </p>
                    </div>
                    
                    <div class="flex flex-wrap gap-6 text-sm text-gray-600">
                        <div class="flex items-center space-x-2">
                            <i data-lucide="mail" class="w-4 h-4"></i>
                            <span id="email">h.montoya2004@gmail.com</span>
                        </div>
                        <div class="flex items-center space-x-2">
                            <i data-lucide="phone" class="w-4 h-4"></i>
                            <span id="phone">06.23.70.58.66</span>
                        </div>
                        <div class="flex items-center space-x-2">
                            <i data-lucide="globe" class="w-4 h-4"></i>
                            <span id="website">hernandomontoya.net</span>
                        </div>
                    </div>
                    
                    <div class="flex flex-wrap gap-4">
                        <button onclick="scrollToContact()" class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-full font-semibold transition-all transform hover:scale-105 shadow-lg">
                            <span data-i18n="getInTouch">Get In Touch</span>
                        </button>
                        <a href="/api/import/export" class="border-2 border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white px-8 py-3 rounded-full font-semibold transition-all">
                            <span data-i18n="downloadCV">Download CV</span>
                        </a>
                    </div>
                </div>
                
                <div class="flex justify-center animate-float">
                    <div class="relative">
                        <div class="w-80 h-80 glassmorphism rounded-full p-4">
                            <img id="profileImage" 
                                 src="https://customer-assets.emergentagent.com/job_responsive-vita/artifacts/x21fq5wh_profil.png"
                                 alt="Profile"
                                 class="w-full h-full object-cover rounded-full">
                        </div>
                        <div class="absolute -top-4 -right-4 w-24 h-24 bg-blue-500 rounded-full opacity-20 animate-pulse"></div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="py-20 bg-white/30">
        <div class="max-w-4xl mx-auto px-4 text-center">
            <div class="glassmorphism rounded-3xl p-12">
                <h2 class="text-4xl font-bold text-gray-900 mb-8" data-i18n="aboutMe">About Me</h2>
                <p id="aboutText" class="text-xl text-gray-700 leading-relaxed mb-8">
                    Loading about description...
                </p>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div class="text-center">
                        <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                            <i data-lucide="code" class="w-8 h-8 text-blue-600"></i>
                        </div>
                        <h3 class="font-semibold text-gray-900 mb-2">13+ <span data-i18n="years">Years</span></h3>
                        <p class="text-gray-600" data-i18n="devExperience">Development Experience</p>
                    </div>
                    <div class="text-center">
                        <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                            <i data-lucide="smartphone" class="w-8 h-8 text-green-600"></i>
                        </div>
                        <h3 class="font-semibold text-gray-900 mb-2" data-i18n="androidExpert">Android Expert</h3>
                        <p class="text-gray-600">Kotlin & Jetpack Compose</p>
                    </div>
                    <div class="text-center">
                        <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                            <i data-lucide="globe" class="w-8 h-8 text-purple-600"></i>
                        </div>
                        <h3 class="font-semibold text-gray-900 mb-2" data-i18n="international">International</h3>
                        <p class="text-gray-600" data-i18n="multiLangProjects">Multi-language Projects</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Experience Section -->
    <section id="experience" class="py-20">
        <div class="max-w-6xl mx-auto px-4">
            <h2 class="text-4xl font-bold text-center text-gray-900 mb-16" data-i18n="experience">Experience</h2>
            <div id="experienceList" class="space-y-8">
                <div class="animate-pulse text-center text-gray-500">Loading experiences...</div>
            </div>
        </div>
    </section>

    <!-- Skills Section -->
    <section id="skills" class="py-20 bg-white/30">
        <div class="max-w-6xl mx-auto px-4">
            <h2 class="text-4xl font-bold text-center text-gray-900 mb-16" data-i18n="skillsTech">Skills & Technologies</h2>
            <div id="skillsGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                <div class="animate-pulse text-center text-gray-500">Loading skills...</div>
            </div>
        </div>
    </section>

    <!-- Education Section -->
    <section id="education" class="py-20">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-4xl font-bold text-center text-gray-900 mb-16" data-i18n="education">Education</h2>
            <div id="educationList" class="space-y-8">
                <div class="animate-pulse text-center text-gray-500">Loading education...</div>
            </div>
        </div>
    </section>

    <!-- Languages Section -->
    <section id="languages" class="py-20 bg-white/30">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-4xl font-bold text-center text-gray-900 mb-16" data-i18n="languages">Languages</h2>
            <div id="languagesList" class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="animate-pulse text-center text-gray-500">Loading languages...</div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="py-20">
        <div class="max-w-4xl mx-auto px-4 text-center">
            <div class="glassmorphism rounded-3xl p-12">
                <h2 class="text-4xl font-bold text-gray-900 mb-8" data-i18n="letsWork">Let's Work Together</h2>
                <p class="text-xl text-gray-700 mb-8" data-i18n="readyCreate">Ready to create something amazing?</p>
                <div class="flex flex-wrap justify-center gap-4">
                    <a href="mailto:h.montoya2004@gmail.com" class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-full font-semibold transition-all">
                        <span data-i18n="sendEmail">Send Email</span>
                    </a>
                    <a href="/admin" class="border-2 border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white px-8 py-3 rounded-full font-semibold transition-all">
                        <span data-i18n="adminPanel">Admin Panel</span>
                    </a>
                </div>
            </div>
        </div>
    </section>

    <footer class="bg-gray-900 text-white py-12">
        <div class="max-w-6xl mx-auto px-4 text-center">
            <p>&copy; 2025 Hernando Montoya Oliveros. All rights reserved.</p>
            <div class="flex justify-center space-x-6 mt-4">
                <a href="/health" class="text-gray-400 hover:text-white transition-colors">Health Check</a>
                <a href="/api/content/" class="text-gray-400 hover:text-white transition-colors">API</a>
                <a href="/admin" class="text-gray-400 hover:text-white transition-colors">Admin</a>
            </div>
        </div>
    </footer>

    <script>
        let currentLanguage = 'en';
        let cvData = null;

        // Traducciones
        const translations = {
            en: {
                getInTouch: "Get In Touch",
                downloadCV: "Download CV",
                aboutMe: "About Me",
                years: "Years",
                devExperience: "Development Experience",
                androidExpert: "Android Expert",
                international: "International",
                multiLangProjects: "Multi-language Projects",
                experience: "Experience",
                skillsTech: "Skills & Technologies",
                education: "Education",
                languages: "Languages",
                letsWork: "Let's Work Together",
                readyCreate: "Ready to create something amazing?",
                sendEmail: "Send Email",
                adminPanel: "Admin Panel"
            },
            es: {
                getInTouch: "Contactar",
                downloadCV: "Descargar CV",
                aboutMe: "Sobre Mí",
                years: "Años",
                devExperience: "Experiencia en Desarrollo",
                androidExpert: "Experto Android",
                international: "Internacional",
                multiLangProjects: "Proyectos Multi-idioma",
                experience: "Experiencia",
                skillsTech: "Habilidades y Tecnologías",
                education: "Educación",
                languages: "Idiomas",
                letsWork: "Trabajemos Juntos",
                readyCreate: "¿Listo para crear algo increíble?",
                sendEmail: "Enviar Email",
                adminPanel: "Panel Admin"
            },
            fr: {
                getInTouch: "Contactez-moi",
                downloadCV: "Télécharger CV",
                aboutMe: "À Propos",
                years: "Ans",
                devExperience: "Expérience en Développement",
                androidExpert: "Expert Android",
                international: "International",
                multiLangProjects: "Projets Multi-langues",
                experience: "Expérience",
                skillsTech: "Compétences et Technologies",
                education: "Éducation",
                languages: "Langues",
                letsWork: "Travaillons Ensemble",
                readyCreate: "Prêt à créer quelque chose d'incroyable?",
                sendEmail: "Envoyer Email",
                adminPanel: "Panneau Admin"
            }
        };

        document.addEventListener('DOMContentLoaded', function() {
            lucide.createIcons();
            loadCVData();
            updateTranslations();
        });

        async function loadCVData() {
            try {
                const response = await fetch('/api/content/');
                cvData = await response.json();
                updateContent();
            } catch (error) {
                console.error('Error loading CV data:', error);
            }
        }

        function updateContent() {
            if (!cvData) return;

            // Personal Info
            const nameParts = cvData.personalInfo.name.split(' ');
            document.getElementById('firstName').textContent = nameParts[0];
            document.getElementById('lastName').textContent = nameParts.slice(1).join(' ');
            document.getElementById('jobTitle').textContent = cvData.personalInfo.title;
            document.getElementById('email').textContent = cvData.personalInfo.email;
            document.getElementById('phone').textContent = cvData.personalInfo.phone;
            document.getElementById('website').textContent = cvData.personalInfo.website;
            document.getElementById('profileImage').src = cvData.personalInfo.profileImage;

            // About (respeta el idioma actual)
            const aboutText = cvData.aboutDescription[currentLanguage] || cvData.aboutDescription.en || cvData.aboutDescription.es || 'About description not available';
            document.getElementById('aboutText').textContent = aboutText;

            // Experiences
            const experiencesHtml = cvData.experiences.map(exp => `
                <div class="glassmorphism rounded-2xl p-8">
                    <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
                        <div>
                            <h3 class="text-2xl font-bold text-gray-900 mb-2">${exp.title}</h3>
                            <p class="text-xl text-blue-600 font-semibold">${exp.company}</p>
                            <p class="text-gray-600">${exp.location}</p>
                        </div>
                        <span class="bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-semibold">
                            ${exp.period}
                        </span>
                    </div>
                    <ul class="space-y-2 text-gray-700">
                        ${(exp.description[currentLanguage] || exp.description.en || exp.description.es || []).map(desc => 
                            `<li class="flex items-start"><span class="text-blue-500 mr-2">▸</span>${desc}</li>`
                        ).join('')}
                    </ul>
                </div>
            `).join('');
            document.getElementById('experienceList').innerHTML = experiencesHtml;

            // Skills
            const skillsHtml = Object.entries(cvData.skills).map(([category, skills]) => `
                <div class="glassmorphism rounded-2xl p-6 text-center">
                    <h3 class="text-xl font-bold text-gray-900 mb-4 capitalize">${category}</h3>
                    <div class="flex flex-wrap gap-2 justify-center">
                        ${skills.map(skill => 
                            `<span class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">${skill}</span>`
                        ).join('')}
                    </div>
                </div>
            `).join('');
            document.getElementById('skillsGrid').innerHTML = skillsHtml;

            // Education
            const educationHtml = cvData.education.map(edu => `
                <div class="glassmorphism rounded-2xl p-8">
                    <div class="flex items-center mb-4">
                        <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mr-4">
                            <i data-lucide="graduation-cap" class="w-6 h-6 text-green-600"></i>
                        </div>
                        <div>
                            <h3 class="text-xl font-bold text-gray-900">${edu.title}</h3>
                            <p class="text-green-600 font-semibold">${edu.institution}</p>
                            <p class="text-gray-600">${edu.year}</p>
                        </div>
                    </div>
                </div>
            `).join('');
            document.getElementById('educationList').innerHTML = educationHtml;

            // Languages
            const languagesHtml = cvData.languages.map(lang => `
                <div class="glassmorphism rounded-2xl p-6 text-center">
                    <h3 class="text-xl font-bold text-gray-900 mb-2">${lang.name}</h3>
                    <p class="text-gray-600 mb-4">${lang.level}</p>
                    <div class="w-full bg-gray-200 rounded-full h-3 mb-2">
                        <div class="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-1000" 
                             style="width: ${lang.proficiency}%"></div>
                    </div>
                    <p class="text-sm text-gray-500">${lang.proficiency}%</p>
                </div>
            `).join('');
            document.getElementById('languagesList').innerHTML = languagesHtml;

            // Re-create icons after dynamic content
            lucide.createIcons();
        }

        function changeLanguage(lang) {
            currentLanguage = lang;
            
            // Update active button
            document.querySelectorAll('.lang-button').forEach(btn => btn.classList.remove('active'));
            document.getElementById(`lang-${lang}`).classList.add('active');
            
            // Update translations
            updateTranslations();
            
            // Update dynamic content
            updateContent();
        }

        function updateTranslations() {
            const elements = document.querySelectorAll('[data-i18n]');
            elements.forEach(element => {
                const key = element.getAttribute('data-i18n');
                if (translations[currentLanguage] && translations[currentLanguage][key]) {
                    element.textContent = translations[currentLanguage][key];
                }
            });
        }

        function scrollToContact() {
            document.getElementById('contact').scrollIntoView({ behavior: 'smooth' });
        }

        // Smooth scroll for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    </script>
</body>
</html>'''

    return index_html

def create_complete_admin():
    """Crear admin panel completo con gestión de contenido"""
    
    admin_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel - CV Management</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <style>
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .tab-button.active { 
            background: #3b82f6; 
            color: white; 
            border-color: #3b82f6;
        }
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            max-width: 400px;
        }
    </style>
</head>
<body class="bg-gray-50 min-h-screen">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <h1 class="text-2xl font-bold text-gray-900">CV Admin Panel</h1>
                <div class="flex space-x-4">
                    <a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center">
                        <i data-lucide="arrow-left" class="w-4 h-4 mr-2"></i>
                        Back to CV
                    </a>
                    <button onclick="saveAllChanges()" class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center" id="saveBtn">
                        <i data-lucide="save" class="w-4 h-4 mr-2"></i>
                        Save All
                    </button>
                </div>
            </div>
        </div>
    </header>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Tabs Navigation -->
        <div class="mb-8">
            <div class="border-b border-gray-200">
                <nav class="-mb-px flex space-x-8 overflow-x-auto">
                    <button onclick="showTab('personal')" class="tab-button active whitespace-nowrap py-2 px-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300 flex items-center">
                        <i data-lucide="user" class="w-4 h-4 mr-2"></i>
                        Personal
                    </button>
                    <button onclick="showTab('about')" class="tab-button whitespace-nowrap py-2 px-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300 flex items-center">
                        <i data-lucide="file-text" class="w-4 h-4 mr-2"></i>
                        About
                    </button>
                    <button onclick="showTab('experience')" class="tab-button whitespace-nowrap py-2 px-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300 flex items-center">
                        <i data-lucide="briefcase" class="w-4 h-4 mr-2"></i>
                        Experience
                    </button>
                    <button onclick="showTab('education')" class="tab-button whitespace-nowrap py-2 px-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300 flex items-center">
                        <i data-lucide="graduation-cap" class="w-4 h-4 mr-2"></i>
                        Education
                    </button>
                    <button onclick="showTab('skills')" class="tab-button whitespace-nowrap py-2 px-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300 flex items-center">
                        <i data-lucide="code" class="w-4 h-4 mr-2"></i>
                        Skills
                    </button>
                    <button onclick="showTab('languages')" class="tab-button whitespace-nowrap py-2 px-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300 flex items-center">
                        <i data-lucide="globe" class="w-4 h-4 mr-2"></i>
                        Languages
                    </button>
                    <button onclick="showTab('import')" class="tab-button whitespace-nowrap py-2 px-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300 flex items-center">
                        <i data-lucide="database" class="w-4 h-4 mr-2"></i>
                        Import/Export
                    </button>
                </nav>
            </div>
        </div>

        <!-- Loading indicator -->
        <div id="loading" class="text-center py-8">
            <i data-lucide="loader-2" class="w-8 h-8 animate-spin mx-auto text-blue-600"></i>
            <p class="mt-2 text-gray-600">Loading CV data...</p>
        </div>

        <!-- Tab Contents -->
        
        <!-- Personal Info Tab -->
        <div id="personal" class="tab-content">
            <div class="bg-white rounded-lg shadow p-6">
                <h2 class="text-xl font-semibold text-gray-900 mb-6">Personal Information</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
                        <input type="text" id="personal_name" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Job Title</label>
                        <input type="text" id="personal_title" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
                        <input type="email" id="personal_email" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Phone</label>
                        <input type="text" id="personal_phone" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Website</label>
                        <input type="url" id="personal_website" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Profile Image URL</label>
                        <input type="url" id="personal_profileImage" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                    </div>
                </div>
            </div>
        </div>

        <!-- About Tab -->
        <div id="about" class="tab-content">
            <div class="bg-white rounded-lg shadow p-6">
                <h2 class="text-xl font-semibold text-gray-900 mb-6">About Description</h2>
                <div class="space-y-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">English</label>
                        <textarea id="about_en" rows="4" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="About description in English..."></textarea>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Spanish</label>
                        <textarea id="about_es" rows="4" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Descripción en español..."></textarea>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">French</label>
                        <textarea id="about_fr" rows="4" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Description en français..."></textarea>
                    </div>
                </div>
            </div>
        </div>

        <!-- Experience Tab -->
        <div id="experience" class="tab-content">
            <div class="bg-white rounded-lg shadow p-6">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-xl font-semibold text-gray-900">Experience</h2>
                    <button onclick="addExperience()" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center">
                        <i data-lucide="plus" class="w-4 h-4 mr-2"></i>
                        Add Experience
                    </button>
                </div>
                <div id="experienceList" class="space-y-6">
                    <!-- Dynamic content -->
                </div>
            </div>
        </div>

        <!-- Education Tab -->
        <div id="education" class="tab-content">
            <div class="bg-white rounded-lg shadow p-6">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-xl font-semibold text-gray-900">Education</h2>
                    <button onclick="addEducation()" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center">
                        <i data-lucide="plus" class="w-4 h-4 mr-2"></i>
                        Add Education
                    </button>
                </div>
                <div id="educationList" class="space-y-6">
                    <!-- Dynamic content -->
                </div>
            </div>
        </div>

        <!-- Skills Tab -->
        <div id="skills" class="tab-content">
            <div class="bg-white rounded-lg shadow p-6">
                <h2 class="text-xl font-semibold text-gray-900 mb-6">Skills & Technologies</h2>
                <div id="skillsList" class="space-y-6">
                    <!-- Dynamic content -->
                </div>
            </div>
        </div>

        <!-- Languages Tab -->
        <div id="languages" class="tab-content">
            <div class="bg-white rounded-lg shadow p-6">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-xl font-semibold text-gray-900">Languages</h2>
                    <button onclick="addLanguage()" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center">
                        <i data-lucide="plus" class="w-4 h-4 mr-2"></i>
                        Add Language
                    </button>
                </div>
                <div id="languagesList" class="space-y-6">
                    <!-- Dynamic content -->
                </div>
            </div>
        </div>

        <!-- Import/Export Tab -->
        <div id="import" class="tab-content">
            <div class="bg-white rounded-lg shadow p-6">
                <h2 class="text-xl font-semibold text-gray-900 mb-6">Import/Export Data</h2>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Import Section -->
                    <div class="border border-gray-200 rounded-lg p-6">
                        <h3 class="text-lg font-medium text-gray-900 mb-4 flex items-center">
                            <i data-lucide="upload" class="w-5 h-5 mr-2"></i>
                            Import JSON Data
                        </h3>
                        <div class="mb-4">
                            <input type="file" id="importFile" accept=".json" class="w-full px-3 py-2 border border-gray-300 rounded-md">
                        </div>
                        <button onclick="importData()" class="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center">
                            <i data-lucide="upload" class="w-4 h-4 mr-2"></i>
                            Import Data
                        </button>
                    </div>
                    
                    <!-- Export Section -->
                    <div class="border border-gray-200 rounded-lg p-6">
                        <h3 class="text-lg font-medium text-gray-900 mb-4 flex items-center">
                            <i data-lucide="download" class="w-5 h-5 mr-2"></i>
                            Export JSON Data
                        </h3>
                        <p class="text-gray-600 mb-4">Download current CV data as JSON file.</p>
                        <button onclick="exportData()" class="w-full bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center">
                            <i data-lucide="download" class="w-4 h-4 mr-2"></i>
                            Export Data
                        </button>
                    </div>
                </div>

                <!-- Quick Actions -->
                <div class="mt-8 border-t pt-6">
                    <h3 class="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
                    <div class="flex flex-wrap gap-4">
                        <a href="/health" class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors flex items-center">
                            <i data-lucide="heart" class="w-4 h-4 mr-2"></i>
                            Health Check
                        </a>
                        <a href="/api/content/" class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors flex items-center">
                            <i data-lucide="database" class="w-4 h-4 mr-2"></i>
                            View API Data
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Notifications Container -->
    <div id="notifications" class="fixed top-4 right-4 z-50 space-y-2"></div>

    <script>
        let cvData = null;

        document.addEventListener('DOMContentLoaded', function() {
            lucide.createIcons();
            loadCVData();
        });

        async function loadCVData() {
            try {
                const response = await fetch('/api/content/');
                if (response.ok) {
                    cvData = await response.json();
                    populateAllForms();
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('personal').style.display = 'block';
                } else {
                    throw new Error('Failed to load data');
                }
            } catch (error) {
                showNotification('Error loading data: ' + error.message, 'error');
                document.getElementById('loading').innerHTML = '<p class="text-red-600">Error loading CV data</p>';
            }
        }

        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
                tab.style.display = 'none';
            });
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active');
            });

            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            document.getElementById(tabName).style.display = 'block';
            event.target.classList.add('active');
        }

        function populateAllForms() {
            if (!cvData) return;

            // Personal Info
            document.getElementById('personal_name').value = cvData.personalInfo?.name || '';
            document.getElementById('personal_title').value = cvData.personalInfo?.title || '';
            document.getElementById('personal_email').value = cvData.personalInfo?.email || '';
            document.getElementById('personal_phone').value = cvData.personalInfo?.phone || '';
            document.getElementById('personal_website').value = cvData.personalInfo?.website || '';
            document.getElementById('personal_profileImage').value = cvData.personalInfo?.profileImage || '';

            // About
            document.getElementById('about_en').value = cvData.aboutDescription?.en || '';
            document.getElementById('about_es').value = cvData.aboutDescription?.es || '';
            document.getElementById('about_fr').value = cvData.aboutDescription?.fr || '';

            // Experience, Education, Skills, Languages
            populateExperiences();
            populateEducation();
            populateSkills();
            populateLanguages();
        }

        function populateExperiences() {
            const container = document.getElementById('experienceList');
            if (!cvData.experiences) return;
            
            container.innerHTML = cvData.experiences.map((exp, index) => `
                <div class="border border-gray-200 rounded-lg p-6">
                    <div class="flex justify-between items-start mb-4">
                        <h3 class="text-lg font-medium">Experience ${index + 1}</h3>
                        <button onclick="removeExperience(${index})" class="text-red-600 hover:text-red-800 flex items-center">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                        <input type="text" placeholder="Job Title" value="${exp.title || ''}" onchange="updateExperience(${index}, 'title', this.value)" class="px-3 py-2 border rounded-md">
                        <input type="text" placeholder="Company" value="${exp.company || ''}" onchange="updateExperience(${index}, 'company', this.value)" class="px-3 py-2 border rounded-md">
                        <input type="text" placeholder="Location" value="${exp.location || ''}" onchange="updateExperience(${index}, 'location', this.value)" class="px-3 py-2 border rounded-md">
                        <input type="text" placeholder="Period" value="${exp.period || ''}" onchange="updateExperience(${index}, 'period', this.value)" class="px-3 py-2 border rounded-md">
                    </div>
                    <div class="space-y-3">
                        <textarea placeholder="Description (English)" onchange="updateExperienceDescription(${index}, 'en', this.value)" class="w-full px-3 py-2 border rounded-md" rows="3">${(exp.description?.en || []).join('\\n')}</textarea>
                        <textarea placeholder="Description (Spanish)" onchange="updateExperienceDescription(${index}, 'es', this.value)" class="w-full px-3 py-2 border rounded-md" rows="3">${(exp.description?.es || []).join('\\n')}</textarea>
                        <textarea placeholder="Description (French)" onchange="updateExperienceDescription(${index}, 'fr', this.value)" class="w-full px-3 py-2 border rounded-md" rows="3">${(exp.description?.fr || []).join('\\n')}</textarea>
                    </div>
                </div>
            `).join('');
            lucide.createIcons();
        }

        function populateEducation() {
            const container = document.getElementById('educationList');
            if (!cvData.education) return;
            
            container.innerHTML = cvData.education.map((edu, index) => `
                <div class="border border-gray-200 rounded-lg p-6">
                    <div class="flex justify-between items-start mb-4">
                        <h3 class="text-lg font-medium">Education ${index + 1}</h3>
                        <button onclick="removeEducation(${index})" class="text-red-600 hover:text-red-800 flex items-center">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <input type="text" placeholder="Title/Degree" value="${edu.title || ''}" onchange="updateEducation(${index}, 'title', this.value)" class="px-3 py-2 border rounded-md">
                        <input type="text" placeholder="Institution" value="${edu.institution || ''}" onchange="updateEducation(${index}, 'institution', this.value)" class="px-3 py-2 border rounded-md">
                        <input type="text" placeholder="Year" value="${edu.year || ''}" onchange="updateEducation(${index}, 'year', this.value)" class="px-3 py-2 border rounded-md">
                    </div>
                </div>
            `).join('');
            lucide.createIcons();
        }

        function populateSkills() {
            const container = document.getElementById('skillsList');
            if (!cvData.skills) return;
            
            container.innerHTML = Object.entries(cvData.skills).map(([category, skills]) => `
                <div class="border border-gray-200 rounded-lg p-6">
                    <div class="flex justify-between items-center mb-4">
                        <input type="text" value="${category}" onchange="updateSkillCategory('${category}', this.value)" class="text-lg font-medium bg-transparent border-b border-gray-300 outline-none">
                        <button onclick="removeSkillCategory('${category}')" class="text-red-600 hover:text-red-800 flex items-center">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </div>
                    <textarea onchange="updateSkills('${category}', this.value)" class="w-full px-3 py-2 border rounded-md" rows="3" placeholder="Skills separated by commas">${Array.isArray(skills) ? skills.join(', ') : skills}</textarea>
                </div>
            `).join('');
            lucide.createIcons();
        }

        function populateLanguages() {
            const container = document.getElementById('languagesList');
            if (!cvData.languages) return;
            
            container.innerHTML = cvData.languages.map((lang, index) => `
                <div class="border border-gray-200 rounded-lg p-6">
                    <div class="flex justify-between items-start mb-4">
                        <h3 class="text-lg font-medium">Language ${index + 1}</h3>
                        <button onclick="removeLanguage(${index})" class="text-red-600 hover:text-red-800 flex items-center">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <input type="text" placeholder="Language" value="${lang.name || ''}" onchange="updateLanguage(${index}, 'name', this.value)" class="px-3 py-2 border rounded-md">
                        <input type="text" placeholder="Level" value="${lang.level || ''}" onchange="updateLanguage(${index}, 'level', this.value)" class="px-3 py-2 border rounded-md">
                        <input type="number" placeholder="Proficiency %" value="${lang.proficiency || 0}" onchange="updateLanguage(${index}, 'proficiency', parseInt(this.value))" class="px-3 py-2 border rounded-md" min="0" max="100">
                    </div>
                </div>
            `).join('');
            lucide.createIcons();
        }

        // Update functions
        function updateExperience(index, field, value) {
            if (!cvData.experiences[index]) return;
            cvData.experiences[index][field] = value;
        }

        function updateExperienceDescription(index, lang, value) {
            if (!cvData.experiences[index]) return;
            if (!cvData.experiences[index].description) cvData.experiences[index].description = {};
            cvData.experiences[index].description[lang] = value.split('\\n').filter(line => line.trim());
        }

        function updateEducation(index, field, value) {
            if (!cvData.education[index]) return;
            cvData.education[index][field] = value;
        }

        function updateLanguage(index, field, value) {
            if (!cvData.languages[index]) return;
            cvData.languages[index][field] = value;
        }

        function updateSkills(category, value) {
            if (!cvData.skills) cvData.skills = {};
            cvData.skills[category] = value.split(',').map(skill => skill.trim()).filter(skill => skill);
        }

        // Add functions
        function addExperience() {
            if (!cvData.experiences) cvData.experiences = [];
            cvData.experiences.push({
                id: Date.now().toString(),
                title: '',
                company: '',
                location: '',
                period: '',
                description: { en: [], es: [], fr: [] }
            });
            populateExperiences();
        }

        function addEducation() {
            if (!cvData.education) cvData.education = [];
            cvData.education.push({
                id: Date.now().toString(),
                title: '',
                institution: '',
                year: '',
                type: 'degree'
            });
            populateEducation();
        }

        function addLanguage() {
            if (!cvData.languages) cvData.languages = [];
            cvData.languages.push({
                name: '',
                level: '',
                proficiency: 0
            });
            populateLanguages();
        }

        // Remove functions
        function removeExperience(index) {
            if (confirm('Remove this experience?')) {
                cvData.experiences.splice(index, 1);
                populateExperiences();
            }
        }

        function removeEducation(index) {
            if (confirm('Remove this education entry?')) {
                cvData.education.splice(index, 1);
                populateEducation();
            }
        }

        function removeLanguage(index) {
            if (confirm('Remove this language?')) {
                cvData.languages.splice(index, 1);
                populateLanguages();
            }
        }

        // Save all changes
        async function saveAllChanges() {
            const saveBtn = document.getElementById('saveBtn');
            saveBtn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 mr-2 animate-spin"></i>Saving...';
            saveBtn.disabled = true;

            try {
                // Update personal info
                cvData.personalInfo = {
                    name: document.getElementById('personal_name').value,
                    title: document.getElementById('personal_title').value,
                    email: document.getElementById('personal_email').value,
                    phone: document.getElementById('personal_phone').value,
                    website: document.getElementById('personal_website').value,
                    profileImage: document.getElementById('personal_profileImage').value
                };

                // Update about
                cvData.aboutDescription = {
                    en: document.getElementById('about_en').value,
                    es: document.getElementById('about_es').value,
                    fr: document.getElementById('about_fr').value
                };

                const response = await fetch('/api/content/', {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(cvData)
                });

                if (response.ok) {
                    showNotification('Changes saved successfully!', 'success');
                } else {
                    throw new Error('Failed to save');
                }
            } catch (error) {
                showNotification('Error saving changes: ' + error.message, 'error');
            }

            saveBtn.innerHTML = '<i data-lucide="save" class="w-4 h-4 mr-2"></i>Save All';
            saveBtn.disabled = false;
            lucide.createIcons();
        }

        // Import/Export functions
        async function importData() {
            const fileInput = document.getElementById('importFile');
            if (!fileInput.files[0]) {
                showNotification('Please select a file', 'error');
                return;
            }

            const file = fileInput.files[0];
            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await fetch('/api/import/cv-data', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    showNotification('Data imported successfully!', 'success');
                    setTimeout(() => location.reload(), 1000);
                } else {
                    throw new Error('Import failed');
                }
            } catch (error) {
                showNotification('Error importing data: ' + error.message, 'error');
            }
        }

        async function exportData() {
            try {
                const response = await fetch('/api/import/export');
                if (!response.ok) throw new Error('Export failed');
                
                const data = await response.json();
                
                const blob = new Blob([JSON.stringify(data.data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `cv-data-${new Date().toISOString().split('T')[0]}.json`;
                a.click();
                URL.revokeObjectURL(url);
                
                showNotification('Data exported successfully!', 'success');
            } catch (error) {
                showNotification('Error exporting data: ' + error.message, 'error');
            }
        }

        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `notification p-4 rounded-lg shadow-lg mb-4 max-w-sm ${
                type === 'success' ? 'bg-green-100 text-green-800 border border-green-200' :
                type === 'error' ? 'bg-red-100 text-red-800 border border-red-200' :
                'bg-blue-100 text-blue-800 border border-blue-200'
            }`;
            
            notification.innerHTML = `
                <div class="flex items-center">
                    <i data-lucide="${type === 'success' ? 'check-circle' : type === 'error' ? 'x-circle' : 'info'}" class="w-5 h-5 mr-2"></i>
                    <span>${message}</span>
                </div>
            `;
            
            document.getElementById('notifications').appendChild(notification);
            lucide.createIcons();
            
            setTimeout(() => {
                notification.remove();
            }, 5000);
        }
    </script>
</body>
</html>'''

    return admin_html

def update_container_files():
    """Actualizar archivos en el contenedor"""
    
    container_name = "cv_app"
    
    print("🔄 Actualizando frontend con cambio de idiomas y admin completo...")
    
    try:
        # Verificar contenedor
        result = subprocess.run(['docker', 'ps', '--filter', f'name={container_name}', '--format', '{{.Names}}'], 
                              capture_output=True, text=True)
        if container_name not in result.stdout:
            print(f"❌ Contenedor {container_name} no encontrado")
            return False
        
        print(f"✅ Contenedor {container_name} encontrado")
        
        # Crear archivos HTML
        index_html = create_complete_frontend()
        admin_html = create_complete_admin()
        
        # Crear archivos temporales
        with open('/tmp/index.html', 'w', encoding='utf-8') as f:
            f.write(index_html)
        
        with open('/tmp/admin.html', 'w', encoding='utf-8') as f:
            f.write(admin_html)
        
        # Copiar al contenedor
        subprocess.run(['docker', 'cp', '/tmp/index.html', f'{container_name}:/app/frontend_build/index.html'])
        subprocess.run(['docker', 'cp', '/tmp/admin.html', f'{container_name}:/app/frontend_build/admin.html'])
        
        # Limpiar archivos temporales
        subprocess.run(['rm', '/tmp/index.html', '/tmp/admin.html'])
        
        print("✅ Frontend actualizado con:")
        print("  - Cambio de idiomas funcional (EN/ES/FR)")
        print("  - Admin Panel completo con gestión de contenido")
        print("  - Formularios para todas las secciones")
        print("  - Import/Export funcional")
        print("")
        print("🌐 Prueba tu CV: http://tu-servidor:8006")
        print("🔧 Admin Panel: http://tu-servidor:8006/admin")
        print("🌍 Cambia idioma con los botones EN/ES/FR")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    update_container_files()