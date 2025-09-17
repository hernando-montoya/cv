import React, { useState, useEffect } from 'react';
import { RefreshCw, CheckCircle, AlertCircle, Info } from 'lucide-react';

const SimpleDebug = () => {
  const [backendStatus, setBackendStatus] = useState('checking');
  const [backendUrl, setBackendUrl] = useState('');
  const [testResults, setTestResults] = useState([]);
  const [testing, setTesting] = useState(false);

  useEffect(() => {
    // Obtener URL del backend de forma simple
    const url = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8007';
    setBackendUrl(url);
    testBackendConnection(url);
  }, []);

  const testBackendConnection = async (url) => {
    setTesting(true);
    const results = [];
    
    // URLs a probar
    const urlsToTest = [
      { name: 'Variable de entorno', url: url },
      { name: 'Puerto 8007 (externo)', url: window.location.origin.replace(':8006', ':8007').replace(':3000', ':8007') },
      { name: 'Backend Docker interno', url: 'http://backend:8001' },
      { name: 'Localhost:8007', url: 'http://localhost:8007' }
    ];

    for (const test of urlsToTest) {
      try {
        const response = await fetch(`${test.url}/health`, { 
          method: 'GET',
          timeout: 5000 
        });
        
        results.push({
          ...test,
          status: response.ok ? 'success' : 'error',
          message: response.ok ? 'Conectado' : `Error ${response.status}`
        });
        
        if (response.ok && backendStatus === 'checking') {
          setBackendStatus('connected');
        }
      } catch (error) {
        results.push({
          ...test,
          status: 'error',
          message: error.message || 'No accesible'
        });
      }
    }

    setTestResults(results);
    
    if (backendStatus === 'checking') {
      setBackendStatus('error');
    }
    
    setTesting(false);
  };

  const handleRetest = () => {
    setBackendStatus('checking');
    testBackendConnection(backendUrl);
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Diagnóstico de Conexión
        </h2>

        {/* Estado general */}
        <div className={`p-4 rounded-lg mb-6 ${
          backendStatus === 'connected' 
            ? 'bg-green-50 border border-green-200' 
            : backendStatus === 'error'
            ? 'bg-red-50 border border-red-200'
            : 'bg-yellow-50 border border-yellow-200'
        }`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              {backendStatus === 'connected' ? (
                <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
              ) : backendStatus === 'error' ? (
                <AlertCircle className="h-5 w-5 text-red-600 mr-2" />
              ) : (
                <RefreshCw className="h-5 w-5 text-yellow-600 mr-2 animate-spin" />
              )}
              <div>
                <p className={`font-medium ${
                  backendStatus === 'connected' ? 'text-green-800' : 
                  backendStatus === 'error' ? 'text-red-800' : 'text-yellow-800'
                }`}>
                  {backendStatus === 'connected' ? 'Backend Conectado' : 
                   backendStatus === 'error' ? 'Backend No Accesible' : 'Verificando...'}
                </p>
                <p className="text-sm text-gray-600">
                  URL configurada: {backendUrl}
                </p>
              </div>
            </div>
            <button
              onClick={handleRetest}
              disabled={testing}
              className="px-3 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200 disabled:opacity-50"
            >
              {testing ? 'Probando...' : 'Probar de nuevo'}
            </button>
          </div>
        </div>

        {/* Resultados de pruebas */}
        <div className="space-y-3">
          <h3 className="font-medium text-gray-800">Resultados de Pruebas:</h3>
          {testResults.map((result, index) => (
            <div key={index} className={`p-3 rounded border ${
              result.status === 'success' 
                ? 'bg-green-50 border-green-200' 
                : 'bg-red-50 border-red-200'
            }`}>
              <div className="flex items-center">
                {result.status === 'success' ? (
                  <CheckCircle className="h-4 w-4 text-green-600 mr-2" />
                ) : (
                  <AlertCircle className="h-4 w-4 text-red-600 mr-2" />
                )}
                <div>
                  <p className={`font-medium ${
                    result.status === 'success' ? 'text-green-800' : 'text-red-800'
                  }`}>
                    {result.name}
                  </p>
                  <p className={`text-sm ${
                    result.status === 'success' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {result.url} - {result.message}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Información del entorno */}
        <div className="mt-6 p-4 bg-gray-50 rounded">
          <h4 className="font-medium text-gray-800 mb-2">Información del Entorno:</h4>
          <div className="text-sm text-gray-600 space-y-1">
            <div><strong>Ubicación actual:</strong> {window.location.origin}</div>
            <div><strong>URL Backend configurada:</strong> {backendUrl}</div>
            <div><strong>Puerto esperado (externo):</strong> {window.location.origin.replace(':8006', ':8007')}</div>
          </div>
        </div>

        {/* Recomendaciones */}
        {backendStatus === 'error' && (
          <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded">
            <div className="flex items-start">
              <Info className="h-5 w-5 text-yellow-600 mr-2 mt-0.5" />
              <div>
                <p className="font-medium text-yellow-800">Recomendaciones:</p>
                <ul className="text-sm text-yellow-700 mt-1 space-y-1">
                  <li>• Verifica que el contenedor backend esté corriendo</li>
                  <li>• Confirma que el puerto 8007 esté mapeado</li>
                  <li>• Ejecuta: python3 fix_frontend_config.py</li>
                  <li>• O usa el stack portainer-corrected.yml</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SimpleDebug;