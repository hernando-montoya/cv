import React from 'react';
import { Heart, Github, Linkedin, Mail } from 'lucide-react';
import { useLanguage } from './LanguageProvider';

const Footer = () => {
  const { t } = useLanguage();

  const socialLinks = [
    {
      icon: Github,
      href: '#',
      label: 'GitHub',
      color: 'hover:text-gray-900'
    },
    {
      icon: Linkedin,
      href: '#',
      label: 'LinkedIn',
      color: 'hover:text-blue-600'
    },
    {
      icon: Mail,
      href: 'mailto:h.montoya2004@gmail.com',
      label: 'Email',
      color: 'hover:text-red-600'
    }
  ];

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Main Footer Content */}
        <div className="py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Brand Section */}
            <div className="space-y-4">
              <h3 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                Hernando Montoya
              </h3>
              <p className="text-gray-400 leading-relaxed">
                Android Research & Development Engineer passionate about creating 
                innovative mobile solutions with cutting-edge technology.
              </p>
            </div>

            {/* Quick Links */}
            <div className="space-y-4">
              <h4 className="text-lg font-semibold text-white">Quick Links</h4>
              <nav className="flex flex-col space-y-2">
                {['about', 'experience', 'education', 'skills', 'contact'].map((item) => (
                  <button
                    key={item}
                    onClick={() => {
                      const element = document.getElementById(item);
                      if (element) {
                        element.scrollIntoView({ behavior: 'smooth' });
                      }
                    }}
                    className="text-gray-400 hover:text-blue-400 transition-colors duration-200 text-left capitalize"
                  >
                    {t(item)}
                  </button>
                ))}
              </nav>
            </div>

            {/* Social Links */}
            <div className="space-y-4">
              <h4 className="text-lg font-semibold text-white">Connect</h4>
              <div className="flex space-x-4">
                {socialLinks.map((social) => (
                  <a
                    key={social.label}
                    href={social.href}
                    className={`p-3 bg-gray-800 rounded-lg text-gray-400 ${social.color} transition-all duration-300 transform hover:scale-110 hover:bg-gray-700`}
                    aria-label={social.label}
                  >
                    <social.icon className="w-5 h-5" />
                  </a>
                ))}
              </div>
              <p className="text-gray-400 text-sm">
                Let's connect and build something amazing together!
              </p>
            </div>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-gray-800 py-8">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="flex items-center text-gray-400 text-sm">
              <span>© 2024 Hernando Montoya. Made with</span>
              <Heart className="w-4 h-4 mx-1 text-red-500" />
              <span>and React</span>
            </div>
            
            <div className="text-gray-400 text-sm">
              {t('footerText')}
            </div>

            <button
              onClick={scrollToTop}
              className="p-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-all duration-300 transform hover:scale-110"
              aria-label="Scroll to top"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 10l7-7m0 0l7 7m-7-7v18"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;