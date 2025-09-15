from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
import uuid

class PersonalInfo(BaseModel):
    name: str
    title: str
    phone: str
    email: str
    website: str
    profileImage: str

class ExperienceItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    company: str
    location: str
    period: str
    period_es: Optional[str] = None
    period_fr: Optional[str] = None
    description: Dict[str, List[str]]

class EducationItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    institution: str
    year: str
    type: str

class SkillCategory(BaseModel):
    category: str
    skills: List[str]

class LanguageItem(BaseModel):
    name: str
    level: str
    proficiency: int

class ContentData(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    personalInfo: PersonalInfo
    experiences: List[ExperienceItem]
    education: List[EducationItem]
    skills: Dict[str, List[str]]
    languages: List[LanguageItem]
    aboutDescription: Dict[str, str]  # {lang: description}
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ContentUpdate(BaseModel):
    personalInfo: Optional[PersonalInfo] = None
    experiences: Optional[List[ExperienceItem]] = None
    education: Optional[List[EducationItem]] = None
    skills: Optional[Dict[str, List[str]]] = None
    languages: Optional[List[LanguageItem]] = None
    aboutDescription: Optional[Dict[str, str]] = None