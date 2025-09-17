import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Badge } from './ui/badge';
import { 
  Plus, 
  Trash2, 
  Save, 
  Edit3, 
  User, 
  Briefcase, 
  GraduationCap, 
  Code, 
  Globe,
  Settings,
  Eye,
  EyeOff,
  Database,
  Wifi
} from 'lucide-react';
import { useToast } from '../hooks/use-toast';
import { useLanguage } from './LanguageProvider';
import ImportData from './ImportData';
import ConnectionDiagnostic from './ConnectionDiagnostic';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminPanel = ({ isVisible, onToggle }) => {
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const { toast } = useToast();
  const { language } = useLanguage();

  // Load content on component mount
  useEffect(() => {
    loadContent();
  }, []);

  const loadContent = async () => {
    try {
      const response = await fetch(`${API}/content/`);
      if (response.ok) {
        const data = await response.json();
        setContent(data);
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load content",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const saveContent = async (updatedContent) => {
    setSaving(true);
    try {
      const response = await fetch(`${API}/content/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedContent),
      });

      if (response.ok) {
        const newContent = await response.json();
        setContent(newContent);
        toast({
          title: "Success",
          description: "Content updated successfully!",
        });
      } else {
        throw new Error('Failed to save content');
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to save content",
        variant: "destructive",
      });
    } finally {
      setSaving(false);
    }
  };

  const updatePersonalInfo = (field, value) => {
    const updated = {
      ...content,
      personalInfo: {
        ...content.personalInfo,
        [field]: value
      }
    };
    setContent(updated);
  };

  const updateAboutDescription = (lang, value) => {
    const updated = {
      ...content,
      aboutDescription: {
        ...content.aboutDescription,
        [lang]: value
      }
    };
    setContent(updated);
  };

  const addExperience = () => {
    const newExp = {
      id: Date.now().toString(),
      title: '',
      company: '',
      location: '',
      period: '',
      period_es: '',
      period_fr: '',
      description: {
        en: [''],
        es: [''],
        fr: ['']
      }
    };
    
    const updated = {
      ...content,
      experiences: [...content.experiences, newExp]
    };
    setContent(updated);
  };

  const updateExperience = (index, field, value) => {
    const updated = { ...content };
    updated.experiences[index][field] = value;
    setContent(updated);
  };

  const deleteExperience = (index) => {
    const updated = {
      ...content,
      experiences: content.experiences.filter((_, i) => i !== index)
    };
    setContent(updated);
  };

  const addEducation = () => {
    const newEdu = {
      id: Date.now().toString(),
      title: '',
      institution: '',
      year: '',
      type: 'certification'
    };
    
    const updated = {
      ...content,
      education: [...content.education, newEdu]
    };
    setContent(updated);
  };

  const updateEducation = (index, field, value) => {
    const updated = { ...content };
    updated.education[index][field] = value;
    setContent(updated);
  };

  const deleteEducation = (index) => {
    const updated = {
      ...content,
      education: content.education.filter((_, i) => i !== index)
    };
    setContent(updated);
  };

  const updateSkills = (category, skills) => {
    const updated = {
      ...content,
      skills: {
        ...content.skills,
        [category]: skills.split(',').map(s => s.trim()).filter(s => s)
      }
    };
    setContent(updated);
  };

  const updateLanguage = (index, field, value) => {
    const updated = { ...content };
    updated.languages[index][field] = field === 'proficiency' ? parseInt(value) : value;
    setContent(updated);
  };

  if (!isVisible) {
    return null;
  }

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div className="bg-white p-8 rounded-lg">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-center">Loading content...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-6xl w-full max-h-[90vh] overflow-hidden">
        <div className="flex items-center justify-between p-6 border-b">
          <h2 className="text-2xl font-bold flex items-center">
            <Settings className="w-6 h-6 mr-2" />
            Content Manager
          </h2>
          <div className="flex space-x-2">
            <Button 
              onClick={() => saveContent(content)} 
              disabled={saving}
              className="bg-green-600 hover:bg-green-700"
            >
              <Save className="w-4 h-4 mr-2" />
              {saving ? 'Saving...' : 'Save All'}
            </Button>
            <Button onClick={onToggle} variant="outline">
              <EyeOff className="w-4 h-4 mr-2" />
              Close
            </Button>
          </div>
        </div>

        <div className="overflow-y-auto max-h-[calc(90vh-100px)]">
          <Tabs defaultValue="personal" className="p-6">
            <TabsList className="grid w-full grid-cols-7">
              <TabsTrigger value="personal" className="flex items-center">
                <User className="w-4 h-4 mr-2" />
                Personal
              </TabsTrigger>
              <TabsTrigger value="about" className="flex items-center">
                <User className="w-4 h-4 mr-2" />
                About
              </TabsTrigger>
              <TabsTrigger value="experience" className="flex items-center">
                <Briefcase className="w-4 h-4 mr-2" />
                Experience
              </TabsTrigger>
              <TabsTrigger value="education" className="flex items-center">
                <GraduationCap className="w-4 h-4 mr-2" />
                Education
              </TabsTrigger>
              <TabsTrigger value="skills" className="flex items-center">
                <Code className="w-4 h-4 mr-2" />
                Skills
              </TabsTrigger>
              <TabsTrigger value="languages" className="flex items-center">
                <Globe className="w-4 h-4 mr-2" />
                Languages
              </TabsTrigger>
              <TabsTrigger value="import" className="flex items-center">
                <Database className="w-4 h-4 mr-2" />
                Import
              </TabsTrigger>
            </TabsList>

            <TabsContent value="personal" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Personal Information</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-2">Name</label>
                      <Input
                        value={content?.personalInfo?.name || ''}
                        onChange={(e) => updatePersonalInfo('name', e.target.value)}
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-2">Title</label>
                      <Input
                        value={content?.personalInfo?.title || ''}
                        onChange={(e) => updatePersonalInfo('title', e.target.value)}
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-2">Email</label>
                      <Input
                        value={content?.personalInfo?.email || ''}
                        onChange={(e) => updatePersonalInfo('email', e.target.value)}
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-2">Phone</label>
                      <Input
                        value={content?.personalInfo?.phone || ''}
                        onChange={(e) => updatePersonalInfo('phone', e.target.value)}
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-2">Website</label>
                      <Input
                        value={content?.personalInfo?.website || ''}
                        onChange={(e) => updatePersonalInfo('website', e.target.value)}
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-2">Profile Image URL</label>
                      <Input
                        value={content?.personalInfo?.profileImage || ''}
                        onChange={(e) => updatePersonalInfo('profileImage', e.target.value)}
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="about" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>About Description</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {['en', 'es', 'fr'].map((lang) => (
                    <div key={lang}>
                      <label className="block text-sm font-medium mb-2">
                        {lang === 'en' ? 'English' : lang === 'es' ? 'Spanish' : 'French'}
                      </label>
                      <Textarea
                        value={content?.aboutDescription?.[lang] || ''}
                        onChange={(e) => updateAboutDescription(lang, e.target.value)}
                        rows={3}
                      />
                    </div>
                  ))}
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="experience" className="space-y-6">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold">Work Experience</h3>
                <Button onClick={addExperience} className="bg-blue-600 hover:bg-blue-700">
                  <Plus className="w-4 h-4 mr-2" />
                  Add Experience
                </Button>
              </div>

              {content?.experiences?.map((exp, index) => (
                <Card key={exp.id || index}>
                  <CardContent className="p-6 space-y-4">
                    <div className="flex justify-between items-start">
                      <h4 className="font-semibold">Experience #{index + 1}</h4>
                      <Button 
                        onClick={() => deleteExperience(index)}
                        variant="destructive"
                        size="sm"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium mb-2">Title</label>
                        <Input
                          value={exp.title}
                          onChange={(e) => updateExperience(index, 'title', e.target.value)}
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2">Company</label>
                        <Input
                          value={exp.company}
                          onChange={(e) => updateExperience(index, 'company', e.target.value)}
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2">Location</label>
                        <Input
                          value={exp.location}
                          onChange={(e) => updateExperience(index, 'location', e.target.value)}
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2">Period (EN)</label>
                        <Input
                          value={exp.period}
                          onChange={(e) => updateExperience(index, 'period', e.target.value)}
                          placeholder="2020 - Present"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-2">Description</label>
                      <p className="text-xs text-gray-500 mb-2">Separate each point with a new line</p>
                      {['en', 'es', 'fr'].map((lang) => (
                        <div key={lang} className="mb-3">
                          <label className="block text-xs font-medium mb-1">
                            {lang === 'en' ? 'English' : lang === 'es' ? 'Spanish' : 'French'}
                          </label>
                          <Textarea
                            value={exp.description?.[lang]?.join('\n') || ''}
                            onChange={(e) => {
                              const points = e.target.value.split('\n').filter(p => p.trim());
                              updateExperience(index, 'description', {
                                ...exp.description,
                                [lang]: points
                              });
                            }}
                            rows={4}
                          />
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </TabsContent>

            <TabsContent value="education" className="space-y-6">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold">Education & Certifications</h3>
                <Button onClick={addEducation} className="bg-blue-600 hover:bg-blue-700">
                  <Plus className="w-4 h-4 mr-2" />
                  Add Education
                </Button>
              </div>

              {content?.education?.map((edu, index) => (
                <Card key={edu.id || index}>
                  <CardContent className="p-6 space-y-4">
                    <div className="flex justify-between items-start">
                      <h4 className="font-semibold">Education #{index + 1}</h4>
                      <Button 
                        onClick={() => deleteEducation(index)}
                        variant="destructive"
                        size="sm"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium mb-2">Title</label>
                        <Input
                          value={edu.title}
                          onChange={(e) => updateEducation(index, 'title', e.target.value)}
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2">Institution</label>
                        <Input
                          value={edu.institution}
                          onChange={(e) => updateEducation(index, 'institution', e.target.value)}
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2">Year</label>
                        <Input
                          value={edu.year}
                          onChange={(e) => updateEducation(index, 'year', e.target.value)}
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2">Type</label>
                        <select
                          value={edu.type}
                          onChange={(e) => updateEducation(index, 'type', e.target.value)}
                          className="w-full p-2 border rounded-md"
                        >
                          <option value="degree">Degree</option>
                          <option value="certification">Certification</option>
                        </select>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </TabsContent>

            <TabsContent value="skills" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Technical Skills</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {Object.entries(content?.skills || {}).map(([category, skillList]) => (
                    <div key={category}>
                      <label className="block text-sm font-medium mb-2 capitalize">
                        {category}
                      </label>
                      <Input
                        value={skillList.join(', ')}
                        onChange={(e) => updateSkills(category, e.target.value)}
                        placeholder="Skill 1, Skill 2, Skill 3"
                      />
                      <p className="text-xs text-gray-500 mt-1">Separate skills with commas</p>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="languages" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Languages</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {content?.languages?.map((lang, index) => (
                    <div key={index} className="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 border rounded-lg">
                      <div>
                        <label className="block text-sm font-medium mb-2">Language</label>
                        <Input
                          value={lang.name}
                          onChange={(e) => updateLanguage(index, 'name', e.target.value)}
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2">Level</label>
                        <Input
                          value={lang.level}
                          onChange={(e) => updateLanguage(index, 'level', e.target.value)}
                          placeholder="e.g., Native, B2, Bilingual"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2">Proficiency (%)</label>
                        <Input
                          type="number"
                          min="0"
                          max="100"
                          value={lang.proficiency}
                          onChange={(e) => updateLanguage(index, 'proficiency', e.target.value)}
                        />
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="import" className="space-y-6">
              <ImportData />
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
};

export default AdminPanel;