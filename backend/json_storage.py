"""
Simple JSON-based storage system for CV data
Eliminates MongoDB dependency - all data stored in JSON files
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import shutil
import uuid

class JSONStorage:
    def __init__(self, data_dir: str = "/app/data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.content_file = self.data_dir / "cv_content.json"
        self.backup_dir = self.data_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # Initialize with default data if file doesn't exist
        if not self.content_file.exists():
            self._create_default_content()
    
    def _create_default_content(self):
        """Create default CV content"""
        default_content = {
            "id": str(uuid.uuid4()),
            "personalInfo": {
                "name": "Hernando Montoya Oliveros",
                "title": "Android Research & Development Engineer",
                "phone": "06.23.70.58.66",
                "email": "h.montoya2004@gmail.com",
                "website": "hernandomontoya.net",
                "profileImage": "https://customer-assets.emergentagent.com/job_responsive-vita/artifacts/x21fq5wh_profil.png"
            },
            "experiences": [
                {
                    "id": str(uuid.uuid4()),
                    "title": "Android Research & Development Engineer",
                    "company": "ELTA System",
                    "location": "Ashdod, Israel",
                    "period": "2021 - Present",
                    "period_es": "2021 - Presente",
                    "period_fr": "2021 - Présent",
                    "description": {
                        "en": [
                            "Lead development of advanced Android applications for defense systems",
                            "Implement modern Android architecture patterns with MVVM and Clean Architecture",
                            "Integrate cutting-edge technologies including Jetpack Compose and Kotlin Coroutines",
                            "Collaborate with cross-functional teams to deliver high-quality mobile solutions"
                        ],
                        "es": [
                            "Lidero el desarrollo de aplicaciones Android avanzadas para sistemas de defensa",
                            "Implemento patrones de arquitectura Android modernos con MVVM y Clean Architecture",
                            "Integro tecnologías de vanguardia incluyendo Jetpack Compose y Kotlin Coroutines",
                            "Colaboro con equipos multifuncionales para entregar soluciones móviles de alta calidad"
                        ],
                        "fr": [
                            "Dirige le développement d'applications Android avancées pour les systèmes de défense",
                            "Implémente des modèles d'architecture Android modernes avec MVVM et Clean Architecture",
                            "Intègre des technologies de pointe incluant Jetpack Compose et Kotlin Coroutines",
                            "Collabore avec des équipes pluridisciplinaires pour livrer des solutions mobiles de haute qualité"
                        ]
                    }
                }
            ],
            "education": [
                {
                    "id": str(uuid.uuid4()),
                    "title": "Computer Science Engineering",
                    "institution": "Universidad Nacional de Colombia",
                    "year": "2005",
                    "type": "Bachelor's Degree"
                }
            ],
            "skills": {
                "languages": ["Kotlin", "Java", "Python", "JavaScript"],
                "android": ["Gradle", "Firebase", "Dagger2", "Dagger Hilt", "RxJava", "Coroutines", "Jetpack Compose"],
                "tools": ["Android Studio", "VS Code", "Git", "Bitrise", "Docker", "CI/CD"],
                "methodologies": ["MVVM", "UML", "Scrum", "Clean Architecture", "TDD"]
            },
            "languages": [
                {"name": "English", "level": "B2", "proficiency": 75},
                {"name": "Spanish", "level": "Native", "proficiency": 100},
                {"name": "French", "level": "Bilingual", "proficiency": 95}
            ],
            "aboutDescription": {
                "en": "Experienced Android developer with 13+ years in software development, specializing in modern Android development with Kotlin, Jetpack Compose, and cutting-edge mobile technologies. Passionate about creating innovative solutions that push the boundaries of mobile development.",
                "es": "Desarrollador Android experimentado con más de 13 años en desarrollo de software, especializado en desarrollo Android moderno con Kotlin, Jetpack Compose y tecnologías móviles de vanguardia. Apasionado por crear soluciones innovadoras que expanden los límites del desarrollo móvil.",
                "fr": "Développeur Android expérimenté avec plus de 13 ans en développement logiciel, spécialisé dans le développement Android moderne avec Kotlin, Jetpack Compose et les technologies mobiles de pointe. Passionné par la création de solutions innovantes qui repoussent les limites du développement mobile."
            },
            "updated_at": datetime.utcnow().isoformat()
        }
        
        self._save_content(default_content)
    
    def _save_content(self, content: Dict[str, Any]) -> None:
        """Save content to JSON file with backup"""
        try:
            # Create backup if file exists
            if self.content_file.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = self.backup_dir / f"cv_content_backup_{timestamp}.json"
                shutil.copy2(self.content_file, backup_file)
                
                # Keep only last 10 backups
                backups = sorted(self.backup_dir.glob("cv_content_backup_*.json"))
                if len(backups) > 10:
                    for old_backup in backups[:-10]:
                        old_backup.unlink()
            
            # Update timestamp
            content["updated_at"] = datetime.utcnow().isoformat()
            
            # Save content
            with open(self.content_file, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            raise Exception(f"Error saving content: {str(e)}")
    
    def load_content(self) -> Dict[str, Any]:
        """Load content from JSON file"""
        try:
            if not self.content_file.exists():
                self._create_default_content()
            
            with open(self.content_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            # If file is corrupted, create default content
            print(f"Warning: Error loading content ({e}), creating default content")
            self._create_default_content()
            return self.load_content()
    
    def update_content(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update specific fields in content"""
        current_content = self.load_content()
        
        # Update only provided fields
        for key, value in updates.items():
            if value is not None:
                current_content[key] = value
        
        self._save_content(current_content)
        return current_content
    
    def import_content(self, new_content: Dict[str, Any]) -> Dict[str, Any]:
        """Import complete content (for JSON import feature)"""
        # Validate basic structure
        required_fields = ["personalInfo", "experiences", "education", "skills", "languages", "aboutDescription"]
        for field in required_fields:
            if field not in new_content:
                raise ValueError(f"Missing required field: {field}")
        
        # Ensure ID and timestamp
        if "id" not in new_content:
            new_content["id"] = str(uuid.uuid4())
        
        self._save_content(new_content)
        return new_content
    
    def export_content(self) -> Dict[str, Any]:
        """Export current content"""
        return self.load_content()
    
    def get_backups(self) -> list:
        """Get list of available backups"""
        backups = sorted(self.backup_dir.glob("cv_content_backup_*.json"), reverse=True)
        return [backup.name for backup in backups]
    
    def restore_backup(self, backup_name: str) -> Dict[str, Any]:
        """Restore from backup"""
        backup_file = self.backup_dir / backup_name
        if not backup_file.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_name}")
        
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_content = json.load(f)
        
        self._save_content(backup_content)
        return backup_content

# Global storage instance
storage = JSONStorage()