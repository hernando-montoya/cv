#!/usr/bin/env python3
"""
Script para crear frontend HTML completo que funciona con las APIs
"""

import os

def create_frontend_files():
    frontend_dir = "/app/frontend_build"
    os.makedirs(frontend_dir, exist_ok=True)
    
    # HTML principal con CV completo
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hernando Montoya Oliveros - CV</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    animation: {
                        'fade-in': 'fadeIn 0.5s ease-in-out',
                        'slide-up': 'slideUp 0.6s ease-out',
                    }
                }
            }
        }
    </script>
    <style>
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes slideUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        .glassmorphism {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
    <div id="app" class="animate-fade-in">
        <div class="container mx-auto px-4 py-8">
            <!-- Header -->
            <header class="text-center mb-12 animate-slide-up">
                <div class="glassmorphism rounded-2xl p-8 shadow-xl">
                    <img id="profileImage" src="https://customer-assets.emergentagent.com/job_responsive-vita/artifacts/x21fq5wh_profil.png" 
                         alt="Profile" class="w-32 h-32 rounded-full mx-auto mb-6 border-4 border-blue-200 shadow-lg">
                    <h1 id="name" class="text-4xl md:text-5xl font-bold text-gray-800 mb-2">Loading...</h1>
                    <p id="title" class="text-xl md:text-2xl text-blue-600 mb-4">Loading...</p>
                    <div id="contact" class="flex flex-wrap justify-center gap-4 text-gray-600">
                        <span id="email">📧 Loading...</span>
                        <span id="phone">📱 Loading...</span>
                        <span id="website">🌐 Loading...</span>
                    </div>
                </div>
            </header>

            <!-- About Section -->
            <section class="mb-12 animate-slide-up">
                <div class="glassmorphism rounded-2xl p-8 shadow-xl">
                    <h2 class="text-3xl font-bold text-gray-800 mb-6 text-center">About Me</h2>
                    <p id="about" class="text-lg text-gray-700 leading-relaxed text-center">Loading...</p>
                </div>
            </section>

            <!-- Experience & Skills Grid -->
            <div class="grid md:grid-cols-2 gap-8 mb-12">
                <!-- Experience -->
                <div class="glassmorphism rounded-2xl p-8 shadow-xl animate-slide-up">
                    <h2 class="text-3xl font-bold text-gray-800 mb-6 flex items-center">
                        💼 Experience
                    </h2>
                    <div id="experiences" class="space-y-6">
                        <div class="animate-pulse">Loading experiences...</div>
                    </div>
                </div>

                <!-- Skills -->
                <div class="glassmorphism rounded-2xl p-8 shadow-xl animate-slide-up">
                    <h2 class="text-3xl font-bold text-gray-800 mb-6 flex items-center">
                        🛠️ Skills
                    </h2>
                    <div id="skills" class="space-y-4">
                        <div class="animate-pulse">Loading skills...</div>
                    </div>
                </div>
            </div>

            <!-- Education & Languages Grid -->
            <div class="grid md:grid-cols-2 gap-8 mb-12">
                <!-- Education -->
                <div class="glassmorphism rounded-2xl p-8 shadow-xl animate-slide-up">
                    <h2 class="text-3xl font-bold text-gray-800 mb-6 flex items-center">
                        🎓 Education
                    </h2>
                    <div id="education" class="space-y-4">
                        <div class="animate-pulse">Loading education...</div>
                    </div>
                </div>

                <!-- Languages -->
                <div class="glassmorphism rounded-2xl p-8 shadow-xl animate-slide-up">
                    <h2 class="text-3xl font-bold text-gray-800 mb-6 flex items-center">
                        🌍 Languages
                    </h2>
                    <div id="languages" class="space-y-3">
                        <div class="animate-pulse">Loading languages...</div>
                    </div>
                </div>
            </div>

            <!-- Action Buttons -->
            <div class="text-center animate-slide-up">
                <div class="glassmorphism rounded-2xl p-8 shadow-xl">
                    <div class="flex flex-wrap justify-center gap-4">
                        <a href="/admin" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors">
                            🔧 Admin Panel
                        </a>
                        <a href="/api/content/" class="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors">
                            📊 API Data
                        </a>
                        <a href="/health" class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors">
                            💓 Health Check
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Load CV data from API
        async function loadCVData() {
            try {
                const response = await fetch('/api/content/');
                const data = await response.json();
                
                // Personal Info
                document.getElementById('name').textContent = data.personalInfo.name;
                document.getElementById('title').textContent = data.personalInfo.title;
                document.getElementById('email').textContent = `📧 ${data.personalInfo.email}`;
                document.getElementById('phone').textContent = `📱 ${data.personalInfo.phone}`;
                document.getElementById('website').textContent = `🌐 ${data.personalInfo.website}`;
                document.getElementById('profileImage').src = data.personalInfo.profileImage;
                
                // About
                document.getElementById('about').textContent = data.aboutDescription.en || data.aboutDescription.es || 'About description not available';
                
                // Experiences
                const experiencesHtml = data.experiences.map(exp => `
                    <div class="border-l-4 border-blue-500 pl-4">
                        <h3 class="font-bold text-lg">${exp.title}</h3>
                        <p class="text-blue-600 font-semibold">${exp.company} • ${exp.location}</p>
                        <p class="text-sm text-gray-600 mb-2">${exp.period}</p>
                        <ul class="text-sm text-gray-700 space-y-1">
                            ${(exp.description.en || exp.description.es || []).map(desc => `<li>• ${desc}</li>`).join('')}
                        </ul>
                    </div>
                `).join('');
                document.getElementById('experiences').innerHTML = experiencesHtml;
                
                // Skills
                const skillsHtml = Object.entries(data.skills).map(([category, skills]) => `
                    <div>
                        <h4 class="font-semibold text-gray-800 capitalize mb-2">${category}:</h4>
                        <div class="flex flex-wrap gap-2">
                            ${skills.map(skill => `<span class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">${skill}</span>`).join('')}
                        </div>
                    </div>
                `).join('');
                document.getElementById('skills').innerHTML = skillsHtml;
                
                // Education
                const educationHtml = data.education.map(edu => `
                    <div class="border-l-4 border-green-500 pl-4">
                        <h3 class="font-bold">${edu.title}</h3>
                        <p class="text-green-600">${edu.institution}</p>
                        <p class="text-sm text-gray-600">${edu.year}</p>
                    </div>
                `).join('');
                document.getElementById('education').innerHTML = educationHtml;
                
                // Languages
                const languagesHtml = data.languages.map(lang => `
                    <div class="flex items-center justify-between">
                        <span class="font-semibold">${lang.name}</span>
                        <div class="flex items-center">
                            <span class="text-sm text-gray-600 mr-2">${lang.level}</span>
                            <div class="w-20 bg-gray-200 rounded-full h-2">
                                <div class="bg-blue-600 h-2 rounded-full" style="width: ${lang.proficiency}%"></div>
                            </div>
                        </div>
                    </div>
                `).join('');
                document.getElementById('languages').innerHTML = languagesHtml;
                
            } catch (error) {
                console.error('Error loading CV data:', error);
                document.getElementById('name').textContent = 'Error loading data';
            }
        }
        
        // Load data when page loads
        document.addEventListener('DOMContentLoaded', loadCVData);
    </script>
</body>
</html>'''

    # Admin page HTML
    admin_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel - CV Management</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 min-h-screen">
    <div class="container mx-auto py-8 px-4">
        <div class="bg-white rounded-lg shadow-lg p-8">
            <h1 class="text-3xl font-bold text-gray-800 mb-6">CV Admin Panel</h1>
            
            <div class="grid md:grid-cols-2 gap-6 mb-8">
                <div class="bg-blue-50 p-6 rounded-lg">
                    <h2 class="text-xl font-semibold mb-4">🏠 Quick Access</h2>
                    <div class="space-y-2">
                        <a href="/" class="block text-blue-600 hover:text-blue-800">← Back to CV</a>
                        <a href="/api/content/" class="block text-blue-600 hover:text-blue-800">📊 View Content API</a>
                        <a href="/health" class="block text-blue-600 hover:text-blue-800">💓 Health Check</a>
                    </div>
                </div>
                
                <div class="bg-green-50 p-6 rounded-lg">
                    <h2 class="text-xl font-semibold mb-4">📊 API Endpoints</h2>
                    <div class="space-y-2 text-sm">
                        <div><strong>GET</strong> /api/content/ - Get CV data</div>
                        <div><strong>PUT</strong> /api/content/ - Update CV data</div>
                        <div><strong>POST</strong> /api/import/cv-data - Import JSON</div>
                        <div><strong>GET</strong> /api/import/export - Export JSON</div>
                    </div>
                </div>
            </div>
            
            <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
                <h3 class="text-lg font-semibold text-yellow-800 mb-2">📝 Note</h3>
                <p class="text-yellow-700">
                    This is a basic admin interface. The full React admin panel with forms 
                    is available through the API endpoints above. You can use tools like 
                    Postman or curl to manage the CV content via the REST API.
                </p>
            </div>
        </div>
    </div>
</body>
</html>'''

    # Escribir archivos
    with open(f"{frontend_dir}/index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    
    with open(f"{frontend_dir}/admin.html", "w", encoding="utf-8") as f:
        f.write(admin_html)
    
    print("✅ Frontend HTML files created successfully!")
    print("📁 Files created:")
    print(f"  - {frontend_dir}/index.html")
    print(f"  - {frontend_dir}/admin.html")

if __name__ == "__main__":
    create_frontend_files()