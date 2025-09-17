import React, { useState, useEffect } from 'react';
import { Upload, Download, Database, AlertCircle, CheckCircle, Trash2, RefreshCw } from 'lucide-react';

const SimpleImport = () => {
  const [importStatus, setImportStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [cvStatus, setCvStatus] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('checking');

  // URL del backend de forma simple
  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8007';

  useEffect(() => {
    checkCvStatus();
    testConnection();
  }, []);

  const testConnection = async () => {
    setConnectionStatus('checking');
    try {
      console.log('🔗 Testing connection to:', backendUrl);
      const response = await fetch(`${backendUrl}/health`, { 
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        setConnectionStatus('connected');
        console.log('✅ Backend connection OK');
      } else {
        setConnectionStatus('error');
        console.log('❌ Backend responded with error:', response.status);
      }
    } catch (error) {
      setConnectionStatus('error');
      console.error('❌ Backend connection failed:', error);
    }
  };

  const checkCvStatus = async () => {
    try {
      console.log('📊 Checking CV status at:', `${backendUrl}/api/import/status`);
      const response = await fetch(`${backendUrl}/api/import/status`);
      const data = await response.json();
      setCvStatus(data);
      console.log('📊 CV Status:', data);
    } catch (error) {
      console.error('Error checking CV status:', error);
      setCvStatus({ initialized: false, error: error.message });
    }
  };

  const handleQuickInit = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      console.log('🚀 Quick init to:', `${backendUrl}/api/import/quick-init`);
      console.log('🔑 Token available:', !!token);
      
      const response = await fetch(`${backendUrl}/api/import/quick-init`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      console.log('📥 Quick init response status:', response.status);
      const data = await response.json();
      console.log('📥 Quick init response data:', data);
      
      if (response.ok) {
        setImportStatus({
          success: true,
          message: data.message,
          details: data.records_count
        });
        checkCvStatus();
        testConnection();
      } else {
        setImportStatus({
          success: false,
          message: data.detail || `Error HTTP ${response.status}: ${data.message || 'Error durante la inicialización'}`
        });
      }
    } catch (error) {
      console.error('❌ Quick init error:', error);
      setImportStatus({
        success: false,
        message: `Error de conexión: ${error.message}. Verifica que el backend esté accesible en ${backendUrl}`
      });
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/json') {
      setSelectedFile(file);
      setImportStatus(null);
    } else {
      setImportStatus({
        success: false,
        message: 'Por favor selecciona un archivo JSON válido'
      });
      setSelectedFile(null);
    }
  };

  const handleImportFile = async () => {
    if (!selectedFile) {
      setImportStatus({
        success: false,
        message: 'Por favor selecciona un archivo JSON'
      });
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const token = localStorage.getItem('token');
      console.log('📤 Importing file to:', `${backendUrl}/api/import/cv-data`);
      
      const response = await fetch(`${backendUrl}/api/import/cv-data`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      const data = await response.json();
      
      if (response.ok) {
        setImportStatus({
          success: true,
          message: data.message,
          details: data.records_count
        });
        checkCvStatus();
        testConnection();
      } else {
        setImportStatus({
          success: false,
          message: data.detail || `Error HTTP ${response.status}`
        });
      }
    } catch (error) {
      setImportStatus({
        success: false,
        message: `Error de conexión: ${error.message}`
      });
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${backendUrl}/api/import/export`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      const data = await response.json();
      
      if (response.ok) {
        const jsonString = JSON.stringify(data.data, null, 2);
        const blob = new Blob([jsonString], {
          type: 'application/json'
        });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `cv_data_export_${new Date().toISOString().slice(0, 10)}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        setImportStatus({
          success: true,
          message: `Datos exportados correctamente`
        });
      } else {
        setImportStatus({
          success: false,
          message: data.detail || `Error durante la exportación`
        });
      }
    } catch (error) {
      setImportStatus({
        success: false,
        message: `Error de conexión: ${error.message}`
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Connection Status */}
      <div className={`p-4 rounded-lg border ${
        connectionStatus === 'connected' 
          ? 'bg-green-50 border-green-200' 
          : connectionStatus === 'error'
          ? 'bg-red-50 border-red-200'
          : 'bg-yellow-50 border-yellow-200'
      }`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            {connectionStatus === 'connected' ? (
              <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
            ) : connectionStatus === 'error' ? (
              <AlertCircle className="h-5 w-5 text-red-600 mr-2" />
            ) : (
              <RefreshCw className="h-5 w-5 text-yellow-600 mr-2 animate-spin" />
            )}
            <div>
              <p className={`font-medium ${
                connectionStatus === 'connected' ? 'text-green-800' : 
                connectionStatus === 'error' ? 'text-red-800' : 'text-yellow-800'
              }`}>
                {connectionStatus === 'connected' ? 'Backend Conectado' : 
                 connectionStatus === 'error' ? 'Error de Conexión' : 'Verificando Conexión...'}
              </p>
              <p className={`text-sm ${
                connectionStatus === 'connected' ? 'text-green-600' : 
                connectionStatus === 'error' ? 'text-red-600' : 'text-yellow-600'
              }`}>
                URL: {backendUrl}
              </p>
            </div>
          </div>
          <button
            onClick={testConnection}
            className="text-sm px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 transition-colors"
          >
            Probar Conexión
          </button>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
          <Database className="h-5 w-5 mr-2 text-blue-600" />
          Gestión de Datos del CV
        </h2>

        {/* Status Display */}
        {cvStatus && (
          <div className={`p-4 rounded-lg mb-6 ${
            cvStatus.initialized 
              ? 'bg-green-50 border border-green-200' 
              : 'bg-yellow-50 border border-yellow-200'
          }`}>
            <div className="flex items-center">
              {cvStatus.initialized ? (
                <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
              ) : (
                <AlertCircle className="h-5 w-5 text-yellow-600 mr-2" />
              )}
              <div>
                <p className={`font-medium ${
                  cvStatus.initialized ? 'text-green-800' : 'text-yellow-800'
                }`}>
                  {cvStatus.message}
                </p>
                {cvStatus.records_count && (
                  <p className={`text-sm mt-1 ${
                    cvStatus.initialized ? 'text-green-600' : 'text-yellow-600'
                  }`}>
                    Experiencias: {cvStatus.records_count.experiences} | 
                    Educación: {cvStatus.records_count.education} | 
                    Idiomas: {cvStatus.records_count.languages}
                  </p>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Quick Initialize */}
        {!cvStatus?.initialized && (
          <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h3 className="font-medium text-blue-900 mb-2">Inicialización Rápida</h3>
            <p className="text-blue-700 text-sm mb-3">
              Inicializa la aplicación con datos predeterminados del CV de Hernando Montoya.
            </p>
            <button
              onClick={handleQuickInit}
              disabled={loading || connectionStatus !== 'connected'}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center"
            >
              <Database className="h-4 w-4 mr-2" />
              {loading ? 'Inicializando...' : 'Inicializar Datos'}
            </button>
          </div>
        )}

        {/* File Import */}
        <div className="mb-6">
          <h3 className="font-medium text-gray-900 mb-3">Importar desde Archivo JSON</h3>
          <div className="space-y-3">
            <div>
              <input
                type="file"
                accept=".json"
                onChange={handleFileSelect}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              />
              {selectedFile && (
                <p className="text-sm text-gray-600 mt-1">
                  Archivo seleccionado: {selectedFile.name}
                </p>
              )}
            </div>
            <button
              onClick={handleImportFile}
              disabled={loading || !selectedFile || connectionStatus !== 'connected'}
              className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50 flex items-center"
            >
              <Upload className="h-4 w-4 mr-2" />
              {loading ? 'Importando...' : 'Importar Datos'}
            </button>
          </div>
        </div>

        {/* Export and Management */}
        <div className="space-y-4">
          <h3 className="font-medium text-gray-900">Gestión de Datos</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <button
              onClick={handleExport}
              disabled={loading}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center justify-center"
            >
              <Download className="h-4 w-4 mr-2" />
              {loading ? 'Exportando...' : 'Exportar Datos'}
            </button>
          </div>
        </div>

        {/* Status Messages */}
        {importStatus && (
          <div className={`mt-4 p-4 rounded-lg ${
            importStatus.success 
              ? 'bg-green-50 border border-green-200' 
              : 'bg-red-50 border border-red-200'
          }`}>
            <div className="flex items-center">
              {importStatus.success ? (
                <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
              ) : (
                <AlertCircle className="h-5 w-5 text-red-600 mr-2" />
              )}
              <div>
                <p className={`font-medium ${
                  importStatus.success ? 'text-green-800' : 'text-red-800'
                }`}>
                  {importStatus.message}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SimpleImport;