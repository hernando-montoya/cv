#!/bin/bash

# Script final para arreglar TODO: cambio de idiomas + admin panel completo
echo "🚀 ARREGLANDO TODO - CAMBIO DE IDIOMAS + ADMIN COMPLETO"
echo "======================================================="

CONTAINER_NAME="cv_app"

# Verificar contenedor
if ! docker ps --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
    echo "❌ Contenedor $CONTAINER_NAME no encontrado"
    exit 1
fi

echo "✅ Contenedor encontrado, actualizando archivos..."

# Crear index.html con cambio de idiomas funcional
docker exec $CONTAINER_NAME /bin/bash -c 'cat > /app/frontend_build/index.html << '"'"'EOL'"'"'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hernando Montoya Oliveros - Android Developer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <style>
        @import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap");
        body { font-family: "Inter", sans-serif; }
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
        .lang-button.active { background: #3b82f6 !important; color: white !important; }
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
                    <button onclick="changeLanguage('"'"'en'"'"')" class="lang-button active px-3 py-1 text-sm bg-blue-100 text-blue-800 rounded-full hover:bg-blue-200 transition-colors" id="lang-en">EN</button>
                    <button onclick="changeLanguage('"'"'es'"'"')" class="lang-button px-3 py-1 text-sm bg-blue-100 text-blue-800 rounded-full hover:bg-blue-200 transition-colors" id="lang-es">ES</button>
                    <button onclick="changeLanguage('"'"'fr'"'"')" class="lang-button px-3 py-1 text-sm bg-blue-100 text-blue-800 rounded-full hover:bg-blue-200 transition-colors" id="lang-fr">FR</button>
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

    <!-- Contact Section -->
    <section id="contact" class="py-20">
        <div class="max-w-4xl mx-auto px-4 text-center">
            <div class="glassmorphism rounded-3xl p-12">
                <h2 class="text-4xl font-bold text-gray-900 mb-8" data-i18n="letsWork">Let'"'"'s Work Together</h2>
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
        </div>
    </footer>

    <script>
        let currentLanguage = "en";
        let cvData = null;

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
                letsWork: "Let'"'"'s Work Together",
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
                letsWork: "Travaillons Ensemble",
                readyCreate: "Prêt à créer quelque chose d'"'"'incroyable?",
                sendEmail: "Envoyer Email",
                adminPanel: "Panneau Admin"
            }
        };

        document.addEventListener("DOMContentLoaded", function() {
            lucide.createIcons();
            loadCVData();
            updateTranslations();
        });

        async function loadCVData() {
            try {
                const response = await fetch("/api/content/");
                cvData = await response.json();
                updateContent();
            } catch (error) {
                console.error("Error loading CV data:", error);
            }
        }

        function updateContent() {
            if (!cvData) return;

            const nameParts = cvData.personalInfo.name.split(" ");
            document.getElementById("firstName").textContent = nameParts[0];
            document.getElementById("lastName").textContent = nameParts.slice(1).join(" ");
            document.getElementById("jobTitle").textContent = cvData.personalInfo.title;
            document.getElementById("email").textContent = cvData.personalInfo.email;
            document.getElementById("phone").textContent = cvData.personalInfo.phone;
            document.getElementById("website").textContent = cvData.personalInfo.website;
            document.getElementById("profileImage").src = cvData.personalInfo.profileImage;

            const aboutText = cvData.aboutDescription[currentLanguage] || cvData.aboutDescription.en || cvData.aboutDescription.es || "About description not available";
            document.getElementById("aboutText").textContent = aboutText;

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
                        ).join("")}
                    </ul>
                </div>
            `).join("");
            document.getElementById("experienceList").innerHTML = experiencesHtml;

            const skillsHtml = Object.entries(cvData.skills).map(([category, skills]) => `
                <div class="glassmorphism rounded-2xl p-6 text-center">
                    <h3 class="text-xl font-bold text-gray-900 mb-4 capitalize">${category}</h3>
                    <div class="flex flex-wrap gap-2 justify-center">
                        ${skills.map(skill => 
                            `<span class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">${skill}</span>`
                        ).join("")}
                    </div>
                </div>
            `).join("");
            document.getElementById("skillsGrid").innerHTML = skillsHtml;

            lucide.createIcons();
        }

        function changeLanguage(lang) {
            currentLanguage = lang;
            
            document.querySelectorAll(".lang-button").forEach(btn => btn.classList.remove("active"));
            document.getElementById(`lang-${lang}`).classList.add("active");
            
            updateTranslations();
            updateContent();
        }

        function updateTranslations() {
            const elements = document.querySelectorAll("[data-i18n]");
            elements.forEach(element => {
                const key = element.getAttribute("data-i18n");
                if (translations[currentLanguage] && translations[currentLanguage][key]) {
                    element.textContent = translations[currentLanguage][key];
                }
            });
        }

        function scrollToContact() {
            document.getElementById("contact").scrollIntoView({ behavior: "smooth" });
        }

        document.querySelectorAll("a[href^=\"#\"]").forEach(anchor => {
            anchor.addEventListener("click", function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute("href"));
                if (target) {
                    target.scrollIntoView({ behavior: "smooth", block: "start" });
                }
            });
        });
    </script>
</body>
</html>
EOL'

# Crear admin.html completo
docker exec $CONTAINER_NAME /bin/bash -c 'cat > /app/frontend_build/admin.html << '"'"'EOL'"'"'
<!DOCTYPE html>
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
        .tab-button.active { background: #3b82f6; color: white; border-color: #3b82f6; }
    </style>
</head>
<body class="bg-gray-50 min-h-screen">
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
        <div class="mb-8">
            <div class="border-b border-gray-200">
                <nav class="-mb-px flex space-x-8 overflow-x-auto">
                    <button onclick="showTab('"'"'personal'"'"')" class="tab-button active whitespace-nowrap py-2 px-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700">
                        <i data-lucide="user" class="w-4 h-4 mr-2 inline"></i>Personal
                    </button>
                    <button onclick="showTab('"'"'about'"'"')" class="tab-button whitespace-nowrap py-2 px-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700">
                        <i data-lucide="file-text" class="w-4 h-4 mr-2 inline"></i>About
                    </button>
                    <button onclick="showTab('"'"'experience'"'"')" class="tab-button whitespace-nowrap py-2 px-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700">
                        <i data-lucide="briefcase" class="w-4 h-4 mr-2 inline"></i>Experience
                    </button>
                    <button onclick="showTab('"'"'import'"'"')" class="tab-button whitespace-nowrap py-2 px-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700">
                        <i data-lucide="database" class="w-4 h-4 mr-2 inline"></i>Import/Export
                    </button>
                </nav>
            </div>
        </div>

        <div id="loading" class="text-center py-8">
            <i data-lucide="loader-2" class="w-8 h-8 animate-spin mx-auto text-blue-600"></i>
            <p class="mt-2 text-gray-600">Loading CV data...</p>
        </div>

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
                        <textarea id="about_en" rows="4" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Spanish</label>
                        <textarea id="about_es" rows="4" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">French</label>
                        <textarea id="about_fr" rows="4" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
                    </div>
                </div>
            </div>
        </div>

        <!-- Experience Tab -->
        <div id="experience" class="tab-content">
            <div class="bg-white rounded-lg shadow p-6">
                <h2 class="text-xl font-semibold text-gray-900 mb-6">Experience Management</h2>
                <div id="experienceList" class="space-y-4">
                    <!-- Content loaded dynamically -->
                </div>
            </div>
        </div>

        <!-- Import/Export Tab -->
        <div id="import" class="tab-content">
            <div class="bg-white rounded-lg shadow p-6">
                <h2 class="text-xl font-semibold text-gray-900 mb-6">Import/Export Data</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="border border-gray-200 rounded-lg p-6">
                        <h3 class="text-lg font-medium text-gray-900 mb-4">Import JSON Data</h3>
                        <input type="file" id="importFile" accept=".json" class="w-full px-3 py-2 border border-gray-300 rounded-md mb-4">
                        <button onclick="importData()" class="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                            Import Data
                        </button>
                    </div>
                    <div class="border border-gray-200 rounded-lg p-6">
                        <h3 class="text-lg font-medium text-gray-900 mb-4">Export JSON Data</h3>
                        <p class="text-gray-600 mb-4">Download current CV data as JSON file.</p>
                        <button onclick="exportData()" class="w-full bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700">
                            Export Data
                        </button>
                    </div>
                </div>
                <div class="mt-8 flex space-x-4">
                    <a href="/health" class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700">Health Check</a>
                    <a href="/api/content/" class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700">View API Data</a>
                </div>
            </div>
        </div>
    </div>

    <div id="notifications" class="fixed top-4 right-4 z-50 space-y-2"></div>

    <script>
        let cvData = null;

        document.addEventListener("DOMContentLoaded", function() {
            lucide.createIcons();
            loadCVData();
        });

        async function loadCVData() {
            try {
                const response = await fetch("/api/content/");
                if (response.ok) {
                    cvData = await response.json();
                    populateAllForms();
                    document.getElementById("loading").style.display = "none";
                    document.getElementById("personal").style.display = "block";
                } else {
                    throw new Error("Failed to load data");
                }
            } catch (error) {
                showNotification("Error loading data: " + error.message, "error");
            }
        }

        function showTab(tabName) {
            document.querySelectorAll(".tab-content").forEach(tab => {
                tab.classList.remove("active");
                tab.style.display = "none";
            });
            document.querySelectorAll(".tab-button").forEach(btn => {
                btn.classList.remove("active");
            });

            document.getElementById(tabName).classList.add("active");
            document.getElementById(tabName).style.display = "block";
            event.target.classList.add("active");
        }

        function populateAllForms() {
            if (!cvData) return;

            document.getElementById("personal_name").value = cvData.personalInfo?.name || "";
            document.getElementById("personal_title").value = cvData.personalInfo?.title || "";
            document.getElementById("personal_email").value = cvData.personalInfo?.email || "";
            document.getElementById("personal_phone").value = cvData.personalInfo?.phone || "";

            document.getElementById("about_en").value = cvData.aboutDescription?.en || "";
            document.getElementById("about_es").value = cvData.aboutDescription?.es || "";
            document.getElementById("about_fr").value = cvData.aboutDescription?.fr || "";

            populateExperiences();
        }

        function populateExperiences() {
            const container = document.getElementById("experienceList");
            if (!cvData.experiences) return;
            
            container.innerHTML = cvData.experiences.map((exp, index) => `
                <div class="border border-gray-200 rounded-lg p-4">
                    <h3 class="font-semibold mb-2">${exp.title} at ${exp.company}</h3>
                    <p class="text-gray-600 text-sm">${exp.period} • ${exp.location}</p>
                    <div class="mt-2">
                        ${(exp.description?.en || []).map(desc => `<p class="text-sm text-gray-700">• ${desc}</p>`).join("")}
                    </div>
                </div>
            `).join("");
        }

        async function saveAllChanges() {
            const saveBtn = document.getElementById("saveBtn");
            saveBtn.innerHTML = '"'"'<i data-lucide="loader-2" class="w-4 h-4 mr-2 animate-spin"></i>Saving...'"'"';
            saveBtn.disabled = true;

            try {
                cvData.personalInfo = {
                    name: document.getElementById("personal_name").value,
                    title: document.getElementById("personal_title").value,
                    email: document.getElementById("personal_email").value,
                    phone: document.getElementById("personal_phone").value,
                    website: cvData.personalInfo?.website || "",
                    profileImage: cvData.personalInfo?.profileImage || ""
                };

                cvData.aboutDescription = {
                    en: document.getElementById("about_en").value,
                    es: document.getElementById("about_es").value,
                    fr: document.getElementById("about_fr").value
                };

                const response = await fetch("/api/content/", {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(cvData)
                });

                if (response.ok) {
                    showNotification("Changes saved successfully!", "success");
                } else {
                    throw new Error("Failed to save");
                }
            } catch (error) {
                showNotification("Error saving changes: " + error.message, "error");
            }

            saveBtn.innerHTML = '"'"'<i data-lucide="save" class="w-4 h-4 mr-2"></i>Save All'"'"';
            saveBtn.disabled = false;
            lucide.createIcons();
        }

        async function importData() {
            const fileInput = document.getElementById("importFile");
            if (!fileInput.files[0]) {
                showNotification("Please select a file", "error");
                return;
            }

            const file = fileInput.files[0];
            const formData = new FormData();
            formData.append("file", file);

            try {
                const response = await fetch("/api/import/cv-data", {
                    method: "POST",
                    body: formData
                });

                if (response.ok) {
                    showNotification("Data imported successfully!", "success");
                    setTimeout(() => location.reload(), 1000);
                } else {
                    throw new Error("Import failed");
                }
            } catch (error) {
                showNotification("Error importing data: " + error.message, "error");
            }
        }

        async function exportData() {
            try {
                const response = await fetch("/api/import/export");
                if (!response.ok) throw new Error("Export failed");
                
                const data = await response.json();
                
                const blob = new Blob([JSON.stringify(data.data, null, 2)], { type: "application/json" });
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = `cv-data-${new Date().toISOString().split("T")[0]}.json`;
                a.click();
                URL.revokeObjectURL(url);
                
                showNotification("Data exported successfully!", "success");
            } catch (error) {
                showNotification("Error exporting data: " + error.message, "error");
            }
        }

        function showNotification(message, type = "info") {
            const notification = document.createElement("div");
            notification.className = `p-4 rounded-lg shadow-lg mb-4 max-w-sm ${
                type === "success" ? "bg-green-100 text-green-800 border border-green-200" :
                type === "error" ? "bg-red-100 text-red-800 border border-red-200" :
                "bg-blue-100 text-blue-800 border border-blue-200"
            }`;
            
            notification.innerHTML = `<div class="flex items-center"><span>${message}</span></div>`;
            
            document.getElementById("notifications").appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 5000);
        }
    </script>
</body>
</html>
EOL'

echo "✅ ACTUALIZACIÓN COMPLETADA!"
echo ""
echo "🎉 FUNCIONALIDADES ARREGLADAS:"
echo "  ✅ Cambio de idiomas funcional (EN/ES/FR)"
echo "  ✅ Admin Panel completo con gestión de contenido"
echo "  ✅ Formularios para Personal Info y About"
echo "  ✅ Vista de experiencias"
echo "  ✅ Import/Export funcional"
echo "  ✅ Guardado en tiempo real"
echo ""
echo "🌐 PRUEBA TU CV:"
echo "  - CV: http://tu-servidor:8006"
echo "  - Admin: http://tu-servidor:8006/admin"
echo "  - Cambia idioma con los botones EN/ES/FR en la nav"
echo ""
echo "🔧 ADMIN PANEL:"
echo "  - Pestañas: Personal, About, Experience, Import/Export"
echo "  - Botón 'Save All' para guardar cambios"
echo "  - Import/Export de datos JSON"