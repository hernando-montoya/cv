import React, { useState, useEffect } from 'react';
import { Upload, Download, Database, AlertCircle, CheckCircle, Trash2 } from 'lucide-react';

const ImportData = () => {
  const [importStatus, setImportStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [cvStatus, setCvStatus] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8007';

  useEffect(() => {
    checkCvStatus();
  }, []);

  const checkCvStatus = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/import/status`);
      const data = await response.json();
      setCvStatus(data);
    } catch (error) {
      console.error('Error checking CV status:', error);
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
        checkCvStatus(); // Refresh status
      } else {
        setImportStatus({
          success: false,
          message: data.detail || 'Error durante la importación'
        });
      }
    } catch (error) {
      setImportStatus({
        success: false,
        message: 'Error de conexión durante la importación'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleQuickInit = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${backendUrl}/api/import/quick-init`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      const data = await response.json();
      
      if (response.ok) {
        setImportStatus({
          success: true,
          message: data.message,
          details: data.records_count
        });
        checkCvStatus(); // Refresh status
      } else {
        setImportStatus({
          success: false,
          message: data.detail || 'Error durante la inicialización'
        });
      }
    } catch (error) {
      setImportStatus({
        success: false,
        message: 'Error de conexión durante la inicialización'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${backendUrl}/api/import/export`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const data = await response.json();
      
      if (response.ok) {
        // Download JSON file
        const blob = new Blob([JSON.stringify(data.data, null, 2)], {
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
          message: 'Datos exportados correctamente'
        });
      } else {
        setImportStatus({
          success: false,
          message: data.detail || 'Error durante la exportación'
        });
      }
    } catch (error) {
      setImportStatus({
        success: false,
        message: 'Error de conexión durante la exportación'
      });
    }
  };

  const handleClearData = async () => {
    if (!window.confirm('¿Estás seguro de que quieres eliminar todos los datos del CV? Esta acción no se puede deshacer.')) {
      return;
    }

    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${backendUrl}/api/import/cv-data`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const data = await response.json();
      
      if (response.ok) {
        setImportStatus({
          success: true,
          message: data.message
        });
        checkCvStatus(); // Refresh status
      } else {
        setImportStatus({
          success: false,
          message: data.detail || 'Error durante el borrado'
        });
      }
    } catch (error) {
      setImportStatus({
        success: false,
        message: 'Error de conexión durante el borrado'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
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
              disabled={loading}
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
              disabled={loading || !selectedFile}
              className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50 flex items-center"
            >
              <Upload className="h-4 w-4 mr-2" />
              {loading ? 'Importando...' : 'Importar Datos'}
            </button>
          </div>
        </div>

        {/* Export and Clear */}
        {cvStatus?.initialized && (
          <div className="flex space-x-3">
            <button
              onClick={handleExport}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center"
            >
              <Download className="h-4 w-4 mr-2" />
              Exportar Datos
            </button>
            
            <button
              onClick={handleClearData}
              disabled={loading}
              className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 disabled:opacity-50 flex items-center"
            >
              <Trash2 className="h-4 w-4 mr-2" />
              Borrar Todos los Datos
            </button>
          </div>
        )}

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
                {importStatus.details && (
                  <p className={`text-sm mt-1 ${
                    importStatus.success ? 'text-green-600' : 'text-red-600'
                  }`}>
                    Experiencias: {importStatus.details.experiences} | 
                    Educación: {importStatus.details.education} | 
                    Idiomas: {importStatus.details.languages}
                  </p>
                )}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Instructions */}
      <div className="bg-gray-50 rounded-lg p-4">
        <h3 className="font-medium text-gray-900 mb-2">Instrucciones</h3>
        <ul className="text-sm text-gray-600 space-y-1">
          <li>• <strong>Inicialización Rápida:</strong> Carga datos predeterminados para comenzar inmediatamente</li>
          <li>• <strong>Importar JSON:</strong> Sube un archivo cv_data.json personalizado</li>
          <li>• <strong>Exportar:</strong> Descarga los datos actuales como archivo JSON</li>
          <li>• <strong>Borrar:</strong> Elimina todos los datos para empezar de nuevo</li>
        </ul>
        <p className="text-xs text-gray-500 mt-2">
          Archivo de ejemplo disponible: cv_data.json
        </p>
      </div>
    </div>
  );
};

export default ImportData;