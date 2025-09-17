import React, { useState, useEffect } from 'react';
import { RefreshCw, CheckCircle, AlertCircle, Info, Settings } from 'lucide-react';

const ConnectionDiagnostic = () => {
  const [diagnostics, setDiagnostics] = useState([]);
  const [testing, setTesting] = useState(false);
  const [envInfo, setEnvInfo] = useState({});
  const [error, setError] = useState(null);

  useEffect(() => {
    try {
      gatherEnvInfo();
      setTimeout(() => runDiagnostics(), 100);
    } catch (err) {
      setError(err.message);
      console.error('Error in ConnectionDiagnostic:', err);
    }
  }, []);

  const gatherEnvInfo = () => {
    try {
      const info = {
        // Intentar múltiples formas de obtener la URL del backend
        vite_env: (typeof import !== 'undefined' && import.meta && import.meta.env) ? import.meta.env.REACT_APP_BACKEND_URL : undefined,
        process_env: (typeof process !== 'undefined' && process.env) ? process.env.REACT_APP_BACKEND_URL : undefined,
        window_location: window.location.origin,
        expected_docker: 'http://backend:8001',
        expected_external: window.location.origin.replace(':8006', ':8007').replace(':3000', ':8007')
      };
      setEnvInfo(info);
    } catch (err) {
      console.error('Error gathering env info:', err);
      setEnvInfo({
        window_location: window.location.origin,
        expected_external: window.location.origin.replace(':8006', ':8007').replace(':3000', ':8007'),
        error: err.message
      });
    }
  };

  const testUrl = async (url, name) => {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000);

      const response = await fetch(`${url}/health`, {
        method: 'GET',
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json'
        }
      });

      clearTimeout(timeoutId);

      return {
        name,
        url,
        status: response.ok ? 'success' : 'error',
        code: response.status,
        message: response.ok ? 'Conectado correctamente' : `HTTP ${response.status}`
      };
    } catch (error) {
      return {
        name,
        url,
        status: 'error',
        message: error.name === 'AbortError' ? 'Timeout (5s)' : error.message
      };
    }
  };

  const runDiagnostics = async () => {
    setTesting(true);
    
    const urlsToTest = [
      { name: 'Variable de entorno actual', url: envInfo.vite_env || envInfo.process_env || 'No definida' },
      { name: 'Puerto 8007 (externo)', url: envInfo.expected_external },
      { name: 'Localhost:8007', url: 'http://localhost:8007' },
      { name: 'Backend interno Docker', url: 'http://backend:8001' }
    ].filter(item => item.url && item.url !== 'No definida');

    const results = [];
    for (const item of urlsToTest) {
      const result = await testUrl(item.url, item.name);
      results.push(result);
    }

    setDiagnostics(results);
    setTesting(false);
  };

  const getRecommendation = () => {
    const workingUrl = diagnostics.find(d => d.status === 'success');
    
    if (workingUrl) {
      return {
        type: 'success',
        message: `¡Conexión encontrada! URL que funciona: ${workingUrl.url}`,
        solution: `Para usar esta URL permanentemente, actualiza la variable REACT_APP_BACKEND_URL en el archivo .env del frontend.`
      };
    }

    return {
      type: 'error',
      message: 'No se encontró ninguna URL funcional',
      solution: `Verifica que:
      1. El contenedor backend esté corriendo (docker ps)
      2. El puerto 8007 esté mapeado correctamente
      3. El backend responda en /health`
    };
  };

  const recommendation = getRecommendation();

  return (
    <div className="bg-white rounded-lg shadow-sm border p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
        <Settings className="h-5 w-5 mr-2 text-blue-600" />
        Diagnóstico de Conexión Backend
      </h3>

      {/* Environment Info */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <h4 className="font-medium text-gray-800 mb-2">Información del Entorno</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
          <div><strong>URL actual:</strong> {envInfo.vite_env || envInfo.process_env || 'No definida'}</div>
          <div><strong>Origen ventana:</strong> {envInfo.window_location}</div>
          <div><strong>Esperado (externo):</strong> {envInfo.expected_external}</div>
          <div><strong>Esperado (Docker):</strong> {envInfo.expected_docker}</div>
        </div>
      </div>

      {/* Test Results */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-3">
          <h4 className="font-medium text-gray-800">Resultados de Pruebas</h4>
          <button
            onClick={runDiagnostics}
            disabled={testing}
            className="text-sm px-3 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200 disabled:opacity-50 flex items-center"
          >
            {testing ? <RefreshCw className="h-4 w-4 mr-1 animate-spin" /> : <RefreshCw className="h-4 w-4 mr-1" />}
            {testing ? 'Probando...' : 'Probar de nuevo'}
          </button>
        </div>

        <div className="space-y-2">
          {diagnostics.map((diagnostic, index) => (
            <div key={index} className={`p-3 rounded-lg border ${
              diagnostic.status === 'success' 
                ? 'bg-green-50 border-green-200' 
                : 'bg-red-50 border-red-200'
            }`}>
              <div className="flex items-center">
                {diagnostic.status === 'success' ? (
                  <CheckCircle className="h-4 w-4 text-green-600 mr-2" />
                ) : (
                  <AlertCircle className="h-4 w-4 text-red-600 mr-2" />
                )}
                <div className="flex-1">
                  <p className={`font-medium ${
                    diagnostic.status === 'success' ? 'text-green-800' : 'text-red-800'
                  }`}>
                    {diagnostic.name}
                  </p>
                  <p className={`text-sm ${
                    diagnostic.status === 'success' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {diagnostic.url} - {diagnostic.message}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recommendation */}
      <div className={`p-4 rounded-lg border ${
        recommendation.type === 'success' 
          ? 'bg-blue-50 border-blue-200' 
          : 'bg-yellow-50 border-yellow-200'
      }`}>
        <div className="flex items-start">
          <Info className={`h-5 w-5 mr-2 mt-0.5 ${
            recommendation.type === 'success' ? 'text-blue-600' : 'text-yellow-600'
          }`} />
          <div>
            <p className={`font-medium ${
              recommendation.type === 'success' ? 'text-blue-800' : 'text-yellow-800'
            }`}>
              {recommendation.message}
            </p>
            <p className={`text-sm mt-1 ${
              recommendation.type === 'success' ? 'text-blue-600' : 'text-yellow-600'
            }`}>
              {recommendation.solution}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConnectionDiagnostic;