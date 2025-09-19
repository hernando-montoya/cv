#!/bin/bash

# Script para arreglar el frontend INMEDIATAMENTE
echo "🚀 ARREGLANDO FRONTEND - APLICACIÓN INMEDIATA"
echo "=============================================="

CONTAINER_NAME="cv_app"

# Verificar si el contenedor existe
if ! docker ps --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
    echo "❌ Contenedor $CONTAINER_NAME no encontrado"
    echo "💡 Contenedores disponibles:"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    exit 1
fi

echo "✅ Contenedor $CONTAINER_NAME encontrado"

# Recrear archivos HTML directamente en el contenedor
echo "📝 Creando nuevo frontend..."

# Crear index.html completo directamente en el contenedor
docker exec $CONTAINER_NAME /bin/bash -c 'python3 -c "
import os
frontend_dir = \"/app/frontend_build\"
os.makedirs(frontend_dir, exist_ok=True)

# HTML principal con diseño profesional
index_html = \"\"\"<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Hernando Montoya Oliveros - Android Developer</title>
    <script src=\"https://cdn.tailwindcss.com\"></script>
    <script src=\"https://unpkg.com/lucide@latest/dist/umd/lucide.js\"></script>
    <style>
        @import url(\"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap\");
        body { font-family: \"Inter\", sans-serif; }
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
    </style>
</head>
<body class=\"bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50\">
    <!-- Navigation -->
    <nav class=\"fixed top-0 left-0 right-0 z-50 glassmorphism\">
        <div class=\"max-w-7xl mx-auto px-4 sm:px-6 lg:px-8\">
            <div class=\"flex justify-between items-center h-16\">
                <div class=\"font-bold text-xl text-gray-800\">HM</div>
                <div class=\"hidden md:flex space-x-8\">
                    <a href=\"#home\" class=\"text-gray-700 hover:text-blue-600 transition-colors\">Home</a>
                    <a href=\"#about\" class=\"text-gray-700 hover:text-blue-600 transition-colors\">About</a>
                    <a href=\"#experience\" class=\"text-gray-700 hover:text-blue-600 transition-colors\">Experience</a>
                    <a href=\"#skills\" class=\"text-gray-700 hover:text-blue-600 transition-colors\">Skills</a>
                </div>
                <a href=\"/admin\" class=\"px-4 py-2 bg-gray-800 text-white rounded-full hover:bg-gray-700 transition-colors\">Admin</a>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id=\"home\" class=\"min-h-screen flex items-center justify-center relative overflow-hidden pt-16\">
        <div class=\"absolute inset-0\">
            <div class=\"absolute -top-40 -right-40 w-80 h-80 bg-blue-200 rounded-full opacity-20 animate-pulse\"></div>
            <div class=\"absolute -bottom-40 -left-40 w-96 h-96 bg-indigo-200 rounded-full opacity-20 animate-pulse\"></div>
        </div>
        
        <div class=\"max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10\">
            <div class=\"grid grid-cols-1 lg:grid-cols-2 gap-12 items-center\">
                <div class=\"space-y-8\">
                    <div class=\"space-y-4\">
                        <h1 class=\"text-5xl sm:text-6xl lg:text-7xl font-bold text-gray-900 leading-tight\">
                            <span class=\"block\" id=\"firstName\">Hernando</span>
                            <span class=\"block gradient-text\" id=\"lastName\">Montoya Oliveros</span>
                        </h1>
                        <h2 class=\"text-xl sm:text-2xl text-gray-600 font-medium\" id=\"jobTitle\">
                            Android Research & Development Engineer
                        </h2>
                        <p class=\"text-lg text-gray-500 max-w-2xl leading-relaxed\" id=\"heroDescription\">
                            Experienced Android developer specializing in modern development with Kotlin and Jetpack Compose
                        </p>
                    </div>
                    
                    <div class=\"flex flex-wrap gap-6 text-sm text-gray-600\">
                        <div class=\"flex items-center space-x-2\">
                            <i data-lucide=\"mail\" class=\"w-4 h-4\"></i>
                            <span id=\"email\">h.montoya2004@gmail.com</span>
                        </div>
                        <div class=\"flex items-center space-x-2\">
                            <i data-lucide=\"phone\" class=\"w-4 h-4\"></i>
                            <span id=\"phone\">06.23.70.58.66</span>
                        </div>
                        <div class=\"flex items-center space-x-2\">
                            <i data-lucide=\"globe\" class=\"w-4 h-4\"></i>
                            <span id=\"website\">hernandomontoya.net</span>
                        </div>
                    </div>
                    
                    <div class=\"flex flex-wrap gap-4\">
                        <button class=\"bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-full font-semibold transition-all transform hover:scale-105 shadow-lg\">
                            Get In Touch
                        </button>
                        <a href=\"/api/import/export\" class=\"border-2 border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white px-8 py-3 rounded-full font-semibold transition-all\">
                            Download CV
                        </a>
                    </div>
                </div>
                
                <div class=\"flex justify-center animate-float\">
                    <div class=\"relative\">
                        <div class=\"w-80 h-80 glassmorphism rounded-full p-4\">
                            <img id=\"profileImage\" 
                                 src=\"https://customer-assets.emergentagent.com/job_responsive-vita/artifacts/x21fq5wh_profil.png\"
                                 alt=\"Profile\"
                                 class=\"w-full h-full object-cover rounded-full\">
                        </div>
                        <div class=\"absolute -top-4 -right-4 w-24 h-24 bg-blue-500 rounded-full opacity-20 animate-pulse\"></div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id=\"about\" class=\"py-20 bg-white/30\">
        <div class=\"max-w-4xl mx-auto px-4 text-center\">
            <div class=\"glassmorphism rounded-3xl p-12\">
                <h2 class=\"text-4xl font-bold text-gray-900 mb-8\">About Me</h2>
                <p id=\"aboutText\" class=\"text-xl text-gray-700 leading-relaxed mb-8\">
                    Experienced Android developer with 13+ years in software development, specializing in modern Android development with Kotlin, Jetpack Compose, and cutting-edge mobile technologies.
                </p>
                <div class=\"grid grid-cols-1 md:grid-cols-3 gap-8\">
                    <div class=\"text-center\">
                        <div class=\"w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4\">
                            <i data-lucide=\"code\" class=\"w-8 h-8 text-blue-600\"></i>
                        </div>
                        <h3 class=\"font-semibold text-gray-900 mb-2\">13+ Years</h3>
                        <p class=\"text-gray-600\">Development Experience</p>
                    </div>
                    <div class=\"text-center\">
                        <div class=\"w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4\">
                            <i data-lucide=\"smartphone\" class=\"w-8 h-8 text-green-600\"></i>
                        </div>
                        <h3 class=\"font-semibold text-gray-900 mb-2\">Android Expert</h3>
                        <p class=\"text-gray-600\">Kotlin & Jetpack Compose</p>
                    </div>
                    <div class=\"text-center\">
                        <div class=\"w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4\">
                            <i data-lucide=\"globe\" class=\"w-8 h-8 text-purple-600\"></i>
                        </div>
                        <h3 class=\"font-semibold text-gray-900 mb-2\">International</h3>
                        <p class=\"text-gray-600\">Multi-language Projects</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Experience Section -->
    <section id=\"experience\" class=\"py-20\">
        <div class=\"max-w-6xl mx-auto px-4\">
            <h2 class=\"text-4xl font-bold text-center text-gray-900 mb-16\">Experience</h2>
            <div id=\"experienceList\" class=\"space-y-8\">
                <div class=\"glassmorphism rounded-2xl p-8\">
                    <div class=\"flex flex-col md:flex-row md:items-center md:justify-between mb-4\">
                        <div>
                            <h3 class=\"text-2xl font-bold text-gray-900 mb-2\">Android Research & Development Engineer</h3>
                            <p class=\"text-xl text-blue-600 font-semibold\">ELTA System</p>
                            <p class=\"text-gray-600\">Ashdod, Israel</p>
                        </div>
                        <span class=\"bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-semibold\">
                            2021 - Present
                        </span>
                    </div>
                    <ul class=\"space-y-2 text-gray-700\">
                        <li class=\"flex items-start\"><span class=\"text-blue-500 mr-2\">▸</span>Lead development of advanced Android applications for defense systems</li>
                        <li class=\"flex items-start\"><span class=\"text-blue-500 mr-2\">▸</span>Implement modern Android architecture patterns with MVVM and Clean Architecture</li>
                        <li class=\"flex items-start\"><span class=\"text-blue-500 mr-2\">▸</span>Integrate cutting-edge technologies including Jetpack Compose and Kotlin Coroutines</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <!-- Skills Section -->
    <section id=\"skills\" class=\"py-20 bg-white/30\">
        <div class=\"max-w-6xl mx-auto px-4\">
            <h2 class=\"text-4xl font-bold text-center text-gray-900 mb-16\">Skills & Technologies</h2>
            <div class=\"grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8\">
                <div class=\"glassmorphism rounded-2xl p-6 text-center\">
                    <h3 class=\"text-xl font-bold text-gray-900 mb-4\">Languages</h3>
                    <div class=\"flex flex-wrap gap-2 justify-center\">
                        <span class=\"bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm\">Kotlin</span>
                        <span class=\"bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm\">Java</span>
                        <span class=\"bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm\">Python</span>
                    </div>
                </div>
                <div class=\"glassmorphism rounded-2xl p-6 text-center\">
                    <h3 class=\"text-xl font-bold text-gray-900 mb-4\">Android</h3>
                    <div class=\"flex flex-wrap gap-2 justify-center\">
                        <span class=\"bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm\">Jetpack Compose</span>
                        <span class=\"bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm\">Coroutines</span>
                        <span class=\"bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm\">MVVM</span>
                    </div>
                </div>
                <div class=\"glassmorphism rounded-2xl p-6 text-center\">
                    <h3 class=\"text-xl font-bold text-gray-900 mb-4\">Tools</h3>
                    <div class=\"flex flex-wrap gap-2 justify-center\">
                        <span class=\"bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm\">Android Studio</span>
                        <span class=\"bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm\">Git</span>
                        <span class=\"bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm\">Docker</span>
                    </div>
                </div>
                <div class=\"glassmorphism rounded-2xl p-6 text-center\">
                    <h3 class=\"text-xl font-bold text-gray-900 mb-4\">Methodologies</h3>
                    <div class=\"flex flex-wrap gap-2 justify-center\">
                        <span class=\"bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm\">Scrum</span>
                        <span class=\"bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm\">TDD</span>
                        <span class=\"bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm\">Clean Code</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section class=\"py-20\">
        <div class=\"max-w-4xl mx-auto px-4 text-center\">
            <div class=\"glassmorphism rounded-3xl p-12\">
                <h2 class=\"text-4xl font-bold text-gray-900 mb-8\">Let\"s Work Together</h2>
                <p class=\"text-xl text-gray-700 mb-8\">Ready to create something amazing?</p>
                <div class=\"flex flex-wrap justify-center gap-4\">
                    <a href=\"mailto:h.montoya2004@gmail.com\" class=\"bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-full font-semibold transition-all\">
                        Send Email
                    </a>
                    <a href=\"/admin\" class=\"border-2 border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white px-8 py-3 rounded-full font-semibold transition-all\">
                        Admin Panel
                    </a>
                </div>
            </div>
        </div>
    </section>

    <footer class=\"bg-gray-900 text-white py-12\">
        <div class=\"max-w-6xl mx-auto px-4 text-center\">
            <p>&copy; 2025 Hernando Montoya Oliveros. All rights reserved.</p>
            <div class=\"flex justify-center space-x-6 mt-4\">
                <a href=\"/health\" class=\"text-gray-400 hover:text-white transition-colors\">Health Check</a>
                <a href=\"/api/content/\" class=\"text-gray-400 hover:text-white transition-colors\">API</a>
                <a href=\"/admin\" class=\"text-gray-400 hover:text-white transition-colors\">Admin</a>
            </div>
        </div>
    </footer>

    <script>
        document.addEventListener(\"DOMContentLoaded\", function() {
            lucide.createIcons();
            loadCVData();
        });

        async function loadCVData() {
            try {
                const response = await fetch(\"/api/content/\");
                const data = await response.json();
                
                const nameParts = data.personalInfo.name.split(\" \");
                document.getElementById(\"firstName\").textContent = nameParts[0];
                document.getElementById(\"lastName\").textContent = nameParts.slice(1).join(\" \");
                document.getElementById(\"jobTitle\").textContent = data.personalInfo.title;
                document.getElementById(\"email\").textContent = data.personalInfo.email;
                document.getElementById(\"phone\").textContent = data.personalInfo.phone;
                document.getElementById(\"website\").textContent = data.personalInfo.website;
                document.getElementById(\"profileImage\").src = data.personalInfo.profileImage;
                document.getElementById(\"aboutText\").textContent = data.aboutDescription.en || data.aboutDescription.es;
                
                lucide.createIcons();
            } catch (error) {
                console.error(\"Error loading CV data:\", error);
            }
        }
    </script>
</body>
</html>\"\"\"

with open(f\"{frontend_dir}/index.html\", \"w\", encoding=\"utf-8\") as f:
    f.write(index_html)

print(\"✅ Nuevo frontend creado!\")
"'

# Crear admin.html también
docker exec $CONTAINER_NAME /bin/bash -c 'echo "<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Admin Panel - CV Management</title>
    <script src=\"https://cdn.tailwindcss.com\"></script>
</head>
<body class=\"bg-gray-50 min-h-screen\">
    <header class=\"bg-white shadow-sm border-b\">
        <div class=\"max-w-7xl mx-auto px-4 sm:px-6 lg:px-8\">
            <div class=\"flex justify-between items-center h-16\">
                <h1 class=\"text-2xl font-bold text-gray-900\">CV Admin Panel</h1>
                <a href=\"/\" class=\"bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700\">Back to CV</a>
            </div>
        </div>
    </header>
    <div class=\"max-w-7xl mx-auto px-4 py-8\">
        <div class=\"bg-white rounded-lg shadow p-8\">
            <h2 class=\"text-xl font-semibold mb-6\">Content Management</h2>
            <div class=\"grid md:grid-cols-2 gap-6\">
                <div class=\"bg-blue-50 p-6 rounded-lg\">
                    <h3 class=\"text-lg font-semibold mb-4\">Quick Access</h3>
                    <div class=\"space-y-2\">
                        <a href=\"/\" class=\"block text-blue-600 hover:text-blue-800\">← Back to CV</a>
                        <a href=\"/api/content/\" class=\"block text-blue-600 hover:text-blue-800\">📊 View Content API</a>
                        <a href=\"/health\" class=\"block text-blue-600 hover:text-blue-800\">💓 Health Check</a>
                        <a href=\"/api/import/export\" class=\"block text-blue-600 hover:text-blue-800\">💾 Export Data</a>
                    </div>
                </div>
                <div class=\"bg-green-50 p-6 rounded-lg\">
                    <h3 class=\"text-lg font-semibold mb-4\">API Endpoints</h3>
                    <div class=\"space-y-2 text-sm\">
                        <div><strong>GET</strong> /api/content/ - Get CV data</div>
                        <div><strong>PUT</strong> /api/content/ - Update CV data</div>
                        <div><strong>POST</strong> /api/import/cv-data - Import JSON</div>
                        <div><strong>GET</strong> /api/import/export - Export JSON</div>
                    </div>
                </div>
            </div>
            <div class=\"mt-8 bg-yellow-50 border border-yellow-200 rounded-lg p-6\">
                <h3 class=\"text-lg font-semibold text-yellow-800 mb-2\">Admin Panel</h3>
                <p class=\"text-yellow-700\">
                    Full admin panel with forms is available through the API endpoints. 
                    Use the API to manage CV content programmatically.
                </p>
            </div>
        </div>
    </div>
</body>
</html>" > /app/frontend_build/admin.html'

echo "✅ Frontend actualizado en el contenedor"
echo "🌐 Prueba tu CV en: http://tu-servidor:8006"
echo "🔧 Admin Panel en: http://tu-servidor:8006/admin"
echo ""
echo "🔄 Si aún no ves cambios, espera 30 segundos y recarga la página"