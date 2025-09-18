import React, { useState } from 'react';
import { Upload, Eye, AlertTriangle, CheckCircle } from 'lucide-react';

const ImportDebug = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState(null);
  const [importResult, setImportResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || '';

  const handleFileSelect = async (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/json') {
      setSelectedFile(file);
      
      // Leer el contenido del archivo para preview
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const content = JSON.parse(e.target.result);
          setFileContent(content);
        } catch (error) {
          setFileContent({ error: `Invalid JSON: ${error.message}` });
        }
      };
      reader.readAsText(file);
    } else {
      alert('Por favor selecciona un archivo JSON válido');
    }
  };

  const handleImport = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setImportResult(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const token = localStorage.getItem('token');
      console.log('🔑 Token:', token ? `${token.substring(0, 20)}...` : 'No token');
      console.log('📤 Importing to:', `${backendUrl}/api/import/cv-data`);
      
      const response = await fetch(`${backendUrl}/api/import/cv-data`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      console.log('📥 Response status:', response.status);
      console.log('📥 Response headers:', Object.fromEntries(response.headers.entries()));

      const responseText = await response.text();
      console.log('📥 Raw response:', responseText);

      let responseData;
      try {
        responseData = JSON.parse(responseText);
      } catch (e) {
        responseData = {
          success: false,
          raw_response: responseText,
          parse_error: e.message
        };
      }

      setImportResult({
        success: response.ok,
        status: response.status,
        data: responseData,
        raw_response: responseText
      });

    } catch (error) {
      console.error('❌ Import error:', error);
      setImportResult({
        success: false,
        error: error.message,
        type: 'fetch_error'
      });
    } finally {
      setLoading(false);
    }
  };

  const validateJsonStructure = (content) => {
    if (!content || content.error) return [];

    const requiredFields = ["personalInfo", "experiences", "education", "skills", "languages", "aboutDescription"];
    const missing = requiredFields.filter(field => !(field in content));
    
    return {
      valid: missing.length === 0,
      missing: missing,
      present: requiredFields.filter(field => field in content),
      extra: Object.keys(content).filter(key => !requiredFields.includes(key))
    };
  };

  const validation = fileContent ? validateJsonStructure(fileContent) : null;

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Debug de Importación JSON
        </h2>

        {/* File Selection */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Seleccionar archivo JSON:
          </label>
          <input
            type="file"
            accept=".json"
            onChange={handleFileSelect}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          {selectedFile && (
            <p className="text-sm text-gray-600 mt-1">
              Archivo: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)
            </p>
          )}
        </div>

        {/* File Content Preview */}
        {fileContent && (
          <div className="mb-6">
            <h3 className="font-medium text-gray-800 mb-2 flex items-center">
              <Eye className="h-4 w-4 mr-2" />
              Vista previa del archivo:
            </h3>
            
            {validation && (
              <div className={`p-3 rounded mb-3 ${
                validation.valid ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
              }`}>
                <div className="flex items-center">
                  {validation.valid ? (
                    <CheckCircle className="h-4 w-4 text-green-600 mr-2" />
                  ) : (
                    <AlertTriangle className="h-4 w-4 text-red-600 mr-2" />
                  )}
                  <span className={`font-medium ${
                    validation.valid ? 'text-green-800' : 'text-red-800'
                  }`}>
                    {validation.valid ? 'Estructura JSON válida' : 'Estructura JSON inválida'}
                  </span>
                </div>
                
                {validation.missing.length > 0 && (
                  <p className="text-sm text-red-600 mt-1">
                    Campos faltantes: {validation.missing.join(', ')}
                  </p>
                )}
                
                {validation.present.length > 0 && (
                  <p className="text-sm text-green-600 mt-1">
                    Campos presentes: {validation.present.join(', ')}
                  </p>
                )}
              </div>
            )}

            <pre className="bg-gray-50 p-3 rounded text-xs overflow-auto max-h-96">
              {JSON.stringify(fileContent, null, 2)}
            </pre>
          </div>
        )}

        {/* Import Button */}
        <div className="mb-6">
          <button
            onClick={handleImport}
            disabled={!selectedFile || loading || (validation && !validation.valid)}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
          >
            <Upload className="h-4 w-4 mr-2" />
            {loading ? 'Importando...' : 'Importar con Debug'}
          </button>
        </div>

        {/* Import Result */}
        {importResult && (
          <div className="space-y-4">
            <h3 className="font-medium text-gray-800">Resultado de la importación:</h3>
            
            <div className={`p-4 rounded border ${
              importResult.success ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
            }`}>
              <div className="flex items-center mb-2">
                {importResult.success ? (
                  <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
                ) : (
                  <AlertTriangle className="h-5 w-5 text-red-600 mr-2" />
                )}
                <span className={`font-medium ${
                  importResult.success ? 'text-green-800' : 'text-red-800'
                }`}>
                  {importResult.success ? 'Importación exitosa' : 'Error en importación'}
                </span>
              </div>

              <div className="text-sm space-y-2">
                <div><strong>Status:</strong> {importResult.status || 'N/A'}</div>
                
                {importResult.data && (
                  <div>
                    <strong>Respuesta JSON:</strong>
                    <pre className="bg-white p-2 rounded mt-1 overflow-auto">
                      {JSON.stringify(importResult.data, null, 2)}
                    </pre>
                  </div>
                )}

                {importResult.raw_response && (
                  <div>
                    <strong>Respuesta raw:</strong>
                    <pre className="bg-white p-2 rounded mt-1 overflow-auto text-xs">
                      {importResult.raw_response}
                    </pre>
                  </div>
                )}

                {importResult.error && (
                  <div className="text-red-600">
                    <strong>Error:</strong> {importResult.error}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ImportDebug;