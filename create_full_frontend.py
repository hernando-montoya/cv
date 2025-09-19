#!/usr/bin/env python3
"""
Recrear el frontend completo con diseño original y Admin Panel funcional
"""

import os

def create_complete_frontend():
    frontend_dir = "/app/frontend_build"
    os.makedirs(frontend_dir, exist_ok=True)
    
    # CSS styles para el diseño original
    styles = '''
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
            
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body { 
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                line-height: 1.6;
                color: #1f2937;
            }
            
            .glassmorphism {
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }
            
            .animate-fade-in { animation: fadeIn 0.8s ease-out; }
            .animate-slide-up { animation: slideUp 0.8s ease-out; }
            .animate-float { animation: float 6s ease-in-out infinite; }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes slideUp {
                from { transform: translateY(30px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-10px); }
            }
            
            .gradient-text {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .section-padding { padding: 5rem 1rem; }
            
            @media (max-width: 768px) {
                .section-padding { padding: 3rem 1rem; }
            }
        </style>
    '''
    
    # HTML principal con diseño original profesional
    index_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hernando Montoya Oliveros - Android Developer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    {styles}
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        'inter': ['Inter', 'sans-serif'],
                    }},
                    animation: {{
                        'fade-in': 'fadeIn 0.8s ease-out',
                        'slide-up': 'slideUp 0.8s ease-out',
                        'float': 'float 6s ease-in-out infinite',
                    }}
                }}
            }}
        }}
    </script>
</head>
<body class="font-inter bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
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
                    <a href="#education" class="text-gray-700 hover:text-blue-600 transition-colors">Education</a>
                    <a href="#contact" class="text-gray-700 hover:text-blue-600 transition-colors">Contact</a>
                </div>
                <div class="flex space-x-2">
                    <button onclick="changeLanguage('en')" class="px-3 py-1 text-sm bg-blue-100 text-blue-800 rounded-full hover:bg-blue-200 transition-colors">EN</button>
                    <button onclick="changeLanguage('es')" class="px-3 py-1 text-sm bg-blue-100 text-blue-800 rounded-full hover:bg-blue-200 transition-colors">ES</button>
                    <button onclick="changeLanguage('fr')" class="px-3 py-1 text-sm bg-blue-100 text-blue-800 rounded-full hover:bg-blue-200 transition-colors">FR</button>
                    <a href="/admin" class="px-3 py-1 text-sm bg-gray-800 text-white rounded-full hover:bg-gray-700 transition-colors">Admin</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="min-h-screen flex items-center justify-center relative overflow-hidden pt-16">
        <!-- Animated Background -->
        <div class="absolute inset-0">
            <div class="absolute -top-40 -right-40 w-80 h-80 bg-blue-200 rounded-full opacity-20 animate-pulse"></div>
            <div class="absolute -bottom-40 -left-40 w-96 h-96 bg-indigo-200 rounded-full opacity-20 animate-pulse delay-1000"></div>
            <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-blue-300 rounded-full opacity-10 animate-spin" style="animation-duration: 20s;"></div>
        </div>
        
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <!-- Content -->
                <div class="space-y-8 animate-fade-in">
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
                    
                    <!-- Contact Info -->
                    <div class="flex flex-wrap gap-6 text-sm text-gray-600">
                        <div class="flex items-center space-x-2 hover:text-blue-600 transition-colors cursor-pointer">
                            <i data-lucide="mail" class="w-4 h-4"></i>
                            <span id="email">h.montoya2004@gmail.com</span>
                        </div>
                        <div class="flex items-center space-x-2 hover:text-blue-600 transition-colors cursor-pointer">
                            <i data-lucide="phone" class="w-4 h-4"></i>
                            <span id="phone">06.23.70.58.66</span>
                        </div>
                        <div class="flex items-center space-x-2 hover:text-blue-600 transition-colors cursor-pointer">
                            <i data-lucide="globe" class="w-4 h-4"></i>
                            <span id="website">hernandomontoya.net</span>
                        </div>
                    </div>
                    
                    <!-- CTA Buttons -->
                    <div class="flex flex-wrap gap-4">
                        <button onclick="scrollToSection('contact')" class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-full font-semibold transition-all transform hover:scale-105 shadow-lg">
                            Get In Touch
                        </button>
                        <button onclick="downloadCV()" class="border-2 border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white px-8 py-3 rounded-full font-semibold transition-all">
                            Download CV
                        </button>
                    </div>
                </div>
                
                <!-- Profile Image -->
                <div class="flex justify-center animate-float">
                    <div class="relative">
                        <div class="w-80 h-80 glassmorphism rounded-full p-4">
                            <img id="profileImage" 
                                 src="https://customer-assets.emergentagent.com/job_responsive-vita/artifacts/x21fq5wh_profil.png"
                                 alt="Profile"
                                 class="w-full h-full object-cover rounded-full">
                        </div>
                        <div class="absolute -top-4 -right-4 w-24 h-24 bg-blue-500 rounded-full opacity-20 animate-pulse"></div>
                        <div class="absolute -bottom-4 -left-4 w-32 h-32 bg-indigo-500 rounded-full opacity-20 animate-pulse delay-500"></div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="section-padding bg-white/30">
        <div class="max-w-4xl mx-auto text-center">
            <div class="glassmorphism rounded-3xl p-12 animate-slide-up">
                <h2 class="text-4xl font-bold text-gray-900 mb-8">About Me</h2>
                <p id="aboutText" class="text-xl text-gray-700 leading-relaxed mb-8">
                    Loading about description...
                </p>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div class="text-center">
                        <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                            <i data-lucide="code" class="w-8 h-8 text-blue-600"></i>
                        </div>
                        <h3 class="font-semibold text-gray-900 mb-2">13+ Years</h3>
                        <p class="text-gray-600">Development Experience</p>
                    </div>
                    <div class="text-center">
                        <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                            <i data-lucide="smartphone" class="w-8 h-8 text-green-600"></i>
                        </div>
                        <h3 class="font-semibold text-gray-900 mb-2">Android Expert</h3>
                        <p class="text-gray-600">Kotlin & Jetpack Compose</p>
                    </div>
                    <div class="text-center">
                        <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                            <i data-lucide="globe" class="w-8 h-8 text-purple-600"></i>
                        </div>
                        <h3 class="font-semibold text-gray-900 mb-2">International</h3>
                        <p class="text-gray-600">Multi-language Projects</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Experience Section -->
    <section id="experience" class="section-padding">
        <div class="max-w-6xl mx-auto">
            <h2 class="text-4xl font-bold text-center text-gray-900 mb-16">Experience</h2>
            <div id="experienceList" class="space-y-8">
                <div class="animate-pulse text-center text-gray-500">Loading experiences...</div>
            </div>
        </div>
    </section>

    <!-- Skills Section -->
    <section id="skills" class="section-padding bg-white/30">
        <div class="max-w-6xl mx-auto">
            <h2 class="text-4xl font-bold text-center text-gray-900 mb-16">Skills & Technologies</h2>
            <div id="skillsGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                <div class="animate-pulse text-center text-gray-500">Loading skills...</div>
            </div>
        </div>
    </section>

    <!-- Education Section -->
    <section id="education" class="section-padding">
        <div class="max-w-4xl mx-auto">
            <h2 class="text-4xl font-bold text-center text-gray-900 mb-16">Education</h2>
            <div id="educationList" class="space-y-8">
                <div class="animate-pulse text-center text-gray-500">Loading education...</div>
            </div>
        </div>
    </section>

    <!-- Languages Section -->
    <section id="languages" class="section-padding bg-white/30">
        <div class="max-w-4xl mx-auto">
            <h2 class="text-4xl font-bold text-center text-gray-900 mb-16">Languages</h2>
            <div id="languagesList" class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="animate-pulse text-center text-gray-500">Loading languages...</div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="section-padding">
        <div class="max-w-4xl mx-auto text-center">
            <div class="glassmorphism rounded-3xl p-12">
                <h2 class="text-4xl font-bold text-gray-900 mb-8">Let's Work Together</h2>
                <p class="text-xl text-gray-700 mb-8">Ready to create something amazing?</p>
                <div class="flex flex-wrap justify-center gap-4">
                    <a href="mailto:h.montoya2004@gmail.com" class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-full font-semibold transition-all transform hover:scale-105">
                        Send Email
                    </a>
                    <a href="/admin" class="border-2 border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white px-8 py-3 rounded-full font-semibold transition-all">
                        Admin Panel
                    </a>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
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

        // Initialize Lucide icons
        document.addEventListener('DOMContentLoaded', function() {{
            lucide.createIcons();
            loadCVData();
        }});

        // Load CV data from API
        async function loadCVData() {{
            try {{
                const response = await fetch('/api/content/');
                cvData = await response.json();
                updateContent();
            }} catch (error) {{
                console.error('Error loading CV data:', error);
            }}
        }}

        // Update content based on current language
        function updateContent() {{
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

            // About
            const aboutText = cvData.aboutDescription[currentLanguage] || cvData.aboutDescription.en;
            document.getElementById('aboutText').textContent = aboutText;

            // Experiences
            const experiencesHtml = cvData.experiences.map(exp => `
                <div class="glassmorphism rounded-2xl p-8 animate-slide-up">
                    <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
                        <div>
                            <h3 class="text-2xl font-bold text-gray-900 mb-2">${{exp.title}}</h3>
                            <p class="text-xl text-blue-600 font-semibold">${{exp.company}}</p>
                            <p class="text-gray-600">${{exp.location}}</p>
                        </div>
                        <div class="text-right">
                            <span class="bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-semibold">
                                ${{exp.period}}
                            </span>
                        </div>
                    </div>
                    <ul class="space-y-2 text-gray-700">
                        ${{(exp.description[currentLanguage] || exp.description.en || []).map(desc => 
                            `<li class="flex items-start"><span class="text-blue-500 mr-2">▸</span>${{desc}}</li>`
                        ).join('')}}
                    </ul>
                </div>
            `).join('');
            document.getElementById('experienceList').innerHTML = experiencesHtml;

            // Skills
            const skillsHtml = Object.entries(cvData.skills).map(([category, skills]) => `
                <div class="glassmorphism rounded-2xl p-6 text-center animate-slide-up">
                    <h3 class="text-xl font-bold text-gray-900 mb-4 capitalize">${{category}}</h3>
                    <div class="flex flex-wrap gap-2 justify-center">
                        ${{skills.map(skill => 
                            `<span class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">${{skill}}</span>`
                        ).join('')}}
                    </div>
                </div>
            `).join('');
            document.getElementById('skillsGrid').innerHTML = skillsHtml;

            // Education
            const educationHtml = cvData.education.map(edu => `
                <div class="glassmorphism rounded-2xl p-8 animate-slide-up">
                    <div class="flex items-center mb-4">
                        <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mr-4">
                            <i data-lucide="graduation-cap" class="w-6 h-6 text-green-600"></i>
                        </div>
                        <div>
                            <h3 class="text-xl font-bold text-gray-900">${{edu.title}}</h3>
                            <p class="text-green-600 font-semibold">${{edu.institution}}</p>
                            <p class="text-gray-600">${{edu.year}}</p>
                        </div>
                    </div>
                </div>
            `).join('');
            document.getElementById('educationList').innerHTML = educationHtml;

            // Languages
            const languagesHtml = cvData.languages.map(lang => `
                <div class="glassmorphism rounded-2xl p-6 text-center animate-slide-up">
                    <h3 class="text-xl font-bold text-gray-900 mb-2">${{lang.name}}</h3>
                    <p class="text-gray-600 mb-4">${{lang.level}}</p>
                    <div class="w-full bg-gray-200 rounded-full h-3 mb-2">
                        <div class="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-1000" 
                             style="width: ${{lang.proficiency}}%"></div>
                    </div>
                    <p class="text-sm text-gray-500">${{lang.proficiency}}%</p>
                </div>
            `).join('');
            document.getElementById('languagesList').innerHTML = languagesHtml;

            // Re-create icons after dynamic content
            lucide.createIcons();
        }}

        // Language switcher
        function changeLanguage(lang) {{
            currentLanguage = lang;
            updateContent();
        }}

        // Smooth scrolling
        function scrollToSection(sectionId) {{
            document.getElementById(sectionId).scrollIntoView({{ behavior: 'smooth' }});
        }}

        // Download CV
        function downloadCV() {{
            window.open('/api/import/export', '_blank');
        }}

        // Smooth scroll for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}
            }});
        }});
    </script>
</body>
</html>'''

    # Admin Panel HTML completo con formularios funcionales
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
                    <a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                        <i data-lucide="arrow-left" class="w-4 h-4 inline mr-2"></i>
                        Back to CV
                    </a>
                    <button onclick="saveAllChanges()" class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors" id="saveBtn">
                        <i data-lucide="save" class="w-4 h-4 inline mr-2"></i>
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
                <nav class="-mb-px flex space-x-8">
                    <button onclick="showTab('personal')" class="tab-button active py-2 px-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300">
                        <i data-lucide="user" class="w-4 h-4 inline mr-2"></i>
                        Personal Info
                    </button>
                    <button onclick="showTab('about')" class="tab-button py-2 px-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300">
                        <i data-lucide="file-text" class="w-4 h-4 inline mr-2"></i>
                        About
                    </button>
                    <button onclick="showTab('experience')" class="tab-button py-2 px-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300">
                        <i data-lucide="briefcase" class="w-4 h-4 inline mr-2"></i>
                        Experience
                    </button>
                    <button onclick="showTab('education')" class="tab-button py-2 px-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300">
                        <i data-lucide="graduation-cap" class="w-4 h-4 inline mr-2"></i>
                        Education
                    </button>
                    <button onclick="showTab('skills')" class="tab-button py-2 px-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300">
                        <i data-lucide="code" class="w-4 h-4 inline mr-2"></i>
                        Skills
                    </button>
                    <button onclick="showTab('languages')" class="tab-button py-2 px-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300">
                        <i data-lucide="globe" class="w-4 h-4 inline mr-2"></i>
                        Languages
                    </button>
                    <button onclick="showTab('import')" class="tab-button py-2 px-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300">
                        <i data-lucide="database" class="w-4 h-4 inline mr-2"></i>
                        Import/Export
                    </button>
                </nav>
            </div>
        </div>

        <!-- Tab Contents -->
        
        <!-- Personal Info Tab -->
        <div id="personal" class="tab-content active">
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
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-xl font-semibold text-gray-900">Experience</h2>
                    <button onclick="addExperience()" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                        <i data-lucide="plus" class="w-4 h-4 inline mr-2"></i>
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
                    <button onclick="addEducation()" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                        <i data-lucide="plus" class="w-4 h-4 inline mr-2"></i>
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
                    <button onclick="addLanguage()" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                        <i data-lucide="plus" class="w-4 h-4 inline mr-2"></i>
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
                        <h3 class="text-lg font-medium text-gray-900 mb-4">Import JSON Data</h3>
                        <div class="mb-4">
                            <input type="file" id="importFile" accept=".json" class="w-full px-3 py-2 border border-gray-300 rounded-md">
                        </div>
                        <button onclick="importData()" class="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                            <i data-lucide="upload" class="w-4 h-4 inline mr-2"></i>
                            Import Data
                        </button>
                    </div>
                    
                    <!-- Export Section -->
                    <div class="border border-gray-200 rounded-lg p-6">
                        <h3 class="text-lg font-medium text-gray-900 mb-4">Export JSON Data</h3>
                        <p class="text-gray-600 mb-4">Download current CV data as JSON file.</p>
                        <button onclick="exportData()" class="w-full bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors">
                            <i data-lucide="download" class="w-4 h-4 inline mr-2"></i>
                            Export Data
                        </button>
                    </div>
                </div>

                <!-- Quick Actions -->
                <div class="mt-8 border-t pt-6">
                    <h3 class="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
                    <div class="flex flex-wrap gap-4">
                        <a href="/health" class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors">
                            <i data-lucide="heart" class="w-4 h-4 inline mr-2"></i>
                            Health Check
                        </a>
                        <a href="/api/content/" class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors">
                            <i data-lucide="database" class="w-4 h-4 inline mr-2"></i>
                            View API Data
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Loading/Success Messages -->
    <div id="notifications" class="fixed top-4 right-4 z-50"></div>

    <script>
        let cvData = null;

        document.addEventListener('DOMContentLoaded', function() {
            lucide.createIcons();
            loadCVData();
        });

        async function loadCVData() {
            try {
                const response = await fetch('/api/content/');
                cvData = await response.json();
                populateAllForms();
            } catch (error) {
                showNotification('Error loading data', 'error');
            }
        }

        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active');
            });

            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }

        function populateAllForms() {
            if (!cvData) return;

            // Personal Info
            document.getElementById('personal_name').value = cvData.personalInfo.name || '';
            document.getElementById('personal_title').value = cvData.personalInfo.title || '';
            document.getElementById('personal_email').value = cvData.personalInfo.email || '';
            document.getElementById('personal_phone').value = cvData.personalInfo.phone || '';
            document.getElementById('personal_website').value = cvData.personalInfo.website || '';
            document.getElementById('personal_profileImage').value = cvData.personalInfo.profileImage || '';

            // About
            document.getElementById('about_en').value = cvData.aboutDescription.en || '';
            document.getElementById('about_es').value = cvData.aboutDescription.es || '';
            document.getElementById('about_fr').value = cvData.aboutDescription.fr || '';

            // Experience
            populateExperiences();
            
            // Education
            populateEducation();
            
            // Skills
            populateSkills();
            
            // Languages
            populateLanguages();
        }

        function populateExperiences() {
            const container = document.getElementById('experienceList');
            container.innerHTML = cvData.experiences.map((exp, index) => `
                <div class="border border-gray-200 rounded-lg p-6">
                    <div class="flex justify-between items-start mb-4">
                        <h3 class="text-lg font-medium">Experience ${index + 1}</h3>
                        <button onclick="removeExperience(${index})" class="text-red-600 hover:text-red-800">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <input type="text" placeholder="Job Title" value="${exp.title}" onchange="updateExperience(${index}, 'title', this.value)" class="px-3 py-2 border rounded-md">
                        <input type="text" placeholder="Company" value="${exp.company}" onchange="updateExperience(${index}, 'company', this.value)" class="px-3 py-2 border rounded-md">
                        <input type="text" placeholder="Location" value="${exp.location}" onchange="updateExperience(${index}, 'location', this.value)" class="px-3 py-2 border rounded-md">
                        <input type="text" placeholder="Period" value="${exp.period}" onchange="updateExperience(${index}, 'period', this.value)" class="px-3 py-2 border rounded-md">
                    </div>
                    <div class="mt-4 space-y-3">
                        <textarea placeholder="Description (English)" onchange="updateExperienceDescription(${index}, 'en', this.value)" class="w-full px-3 py-2 border rounded-md" rows="3">${(exp.description.en || []).join('\\n')}</textarea>
                        <textarea placeholder="Description (Spanish)" onchange="updateExperienceDescription(${index}, 'es', this.value)" class="w-full px-3 py-2 border rounded-md" rows="3">${(exp.description.es || []).join('\\n')}</textarea>
                        <textarea placeholder="Description (French)" onchange="updateExperienceDescription(${index}, 'fr', this.value)" class="w-full px-3 py-2 border rounded-md" rows="3">${(exp.description.fr || []).join('\\n')}</textarea>
                    </div>
                </div>
            `).join('');
            lucide.createIcons();
        }

        function populateEducation() {
            const container = document.getElementById('educationList');
            container.innerHTML = cvData.education.map((edu, index) => `
                <div class="border border-gray-200 rounded-lg p-6">
                    <div class="flex justify-between items-start mb-4">
                        <h3 class="text-lg font-medium">Education ${index + 1}</h3>
                        <button onclick="removeEducation(${index})" class="text-red-600 hover:text-red-800">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <input type="text" placeholder="Title/Degree" value="${edu.title}" onchange="updateEducation(${index}, 'title', this.value)" class="px-3 py-2 border rounded-md">
                        <input type="text" placeholder="Institution" value="${edu.institution}" onchange="updateEducation(${index}, 'institution', this.value)" class="px-3 py-2 border rounded-md">
                        <input type="text" placeholder="Year" value="${edu.year}" onchange="updateEducation(${index}, 'year', this.value)" class="px-3 py-2 border rounded-md">
                    </div>
                </div>
            `).join('');
            lucide.createIcons();
        }

        function populateSkills() {
            const container = document.getElementById('skillsList');
            container.innerHTML = Object.entries(cvData.skills).map(([category, skills]) => `
                <div class="border border-gray-200 rounded-lg p-6">
                    <div class="flex justify-between items-center mb-4">
                        <input type="text" value="${category}" onchange="updateSkillCategory('${category}', this.value)" class="text-lg font-medium bg-transparent border-none outline-none">
                        <button onclick="removeSkillCategory('${category}')" class="text-red-600 hover:text-red-800">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </div>
                    <textarea onchange="updateSkills('${category}', this.value)" class="w-full px-3 py-2 border rounded-md" rows="3" placeholder="Skills separated by commas">${skills.join(', ')}</textarea>
                </div>
            `).join('');
            lucide.createIcons();
        }

        function populateLanguages() {
            const container = document.getElementById('languagesList');
            container.innerHTML = cvData.languages.map((lang, index) => `
                <div class="border border-gray-200 rounded-lg p-6">
                    <div class="flex justify-between items-start mb-4">
                        <h3 class="text-lg font-medium">Language ${index + 1}</h3>
                        <button onclick="removeLanguage(${index})" class="text-red-600 hover:text-red-800">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <input type="text" placeholder="Language" value="${lang.name}" onchange="updateLanguage(${index}, 'name', this.value)" class="px-3 py-2 border rounded-md">
                        <input type="text" placeholder="Level" value="${lang.level}" onchange="updateLanguage(${index}, 'level', this.value)" class="px-3 py-2 border rounded-md">
                        <input type="number" placeholder="Proficiency %" value="${lang.proficiency}" onchange="updateLanguage(${index}, 'proficiency', parseInt(this.value))" class="px-3 py-2 border rounded-md" min="0" max="100">
                    </div>
                </div>
            `).join('');
            lucide.createIcons();
        }

        // Update functions
        function updateExperience(index, field, value) {
            cvData.experiences[index][field] = value;
        }

        function updateExperienceDescription(index, lang, value) {
            cvData.experiences[index].description[lang] = value.split('\\n').filter(line => line.trim());
        }

        function updateEducation(index, field, value) {
            cvData.education[index][field] = value;
        }

        function updateLanguage(index, field, value) {
            cvData.languages[index][field] = value;
        }

        function updateSkills(category, value) {
            cvData.skills[category] = value.split(',').map(skill => skill.trim()).filter(skill => skill);
        }

        // Add functions
        function addExperience() {
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
            cvData.languages.push({
                name: '',
                level: '',
                proficiency: 0
            });
            populateLanguages();
        }

        // Remove functions
        function removeExperience(index) {
            cvData.experiences.splice(index, 1);
            populateExperiences();
        }

        function removeEducation(index) {
            cvData.education.splice(index, 1);
            populateEducation();
        }

        function removeLanguage(index) {
            cvData.languages.splice(index, 1);
            populateLanguages();
        }

        // Save all changes
        async function saveAllChanges() {
            const saveBtn = document.getElementById('saveBtn');
            saveBtn.innerHTML = '<i data-lucide="loader" class="w-4 h-4 inline mr-2 animate-spin"></i>Saving...';

            // Update personal info
            cvData.personalInfo.name = document.getElementById('personal_name').value;
            cvData.personalInfo.title = document.getElementById('personal_title').value;
            cvData.personalInfo.email = document.getElementById('personal_email').value;
            cvData.personalInfo.phone = document.getElementById('personal_phone').value;
            cvData.personalInfo.website = document.getElementById('personal_website').value;
            cvData.personalInfo.profileImage = document.getElementById('personal_profileImage').value;

            // Update about
            cvData.aboutDescription.en = document.getElementById('about_en').value;
            cvData.aboutDescription.es = document.getElementById('about_es').value;
            cvData.aboutDescription.fr = document.getElementById('about_fr').value;

            try {
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
                showNotification('Error saving changes', 'error');
            }

            saveBtn.innerHTML = '<i data-lucide="save" class="w-4 h-4 inline mr-2"></i>Save All';
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
                showNotification('Error importing data', 'error');
            }
        }

        async function exportData() {
            try {
                const response = await fetch('/api/import/export');
                const data = await response.json();
                
                const blob = new Blob([JSON.stringify(data.data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'cv-data.json';
                a.click();
                URL.revokeObjectURL(url);
                
                showNotification('Data exported successfully!', 'success');
            } catch (error) {
                showNotification('Error exporting data', 'error');
            }
        }

        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `p-4 rounded-lg shadow-lg mb-4 ${
                type === 'success' ? 'bg-green-100 text-green-800 border border-green-200' :
                type === 'error' ? 'bg-red-100 text-red-800 border border-red-200' :
                'bg-blue-100 text-blue-800 border border-blue-200'
            }`;
            notification.textContent = message;
            
            document.getElementById('notifications').appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 5000);
        }
    </script>
</body>
</html>'''

    # Escribir archivos
    with open(f"{frontend_dir}/index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    
    with open(f"{frontend_dir}/admin.html", "w", encoding="utf-8") as f:
        f.write(admin_html)
    
    print("✅ Complete frontend with original design created!")
    print("📁 Files created:")
    print(f"  - {frontend_dir}/index.html (Professional CV with original design)")
    print(f"  - {frontend_dir}/admin.html (Full Admin Panel with content management)")

if __name__ == "__main__":
    create_complete_frontend()