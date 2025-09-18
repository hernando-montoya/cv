import React, { useState } from 'react';
import { RefreshCw, AlertTriangle, CheckCircle, Copy } from 'lucide-react';

const CorsDebug = () => {
  const [testResults, setTestResults] = useState([]);
  const [testing, setTesting] = useState(false);

  // Obtener la URL del backend
  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8007';

  const runCorsTests = async () => {
    setTesting(true);
    const results = [];

    // Test 1: Petición simple GET
    try {
      console.log('🧪 Testing simple GET request...');
      const response = await fetch(`${backendUrl}/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      results.push({
        test: 'GET /health',
        success: response.ok,
        status: response.status,
        details: response.ok ? await response.json() : await response.text()
      });
    } catch (error) {
      results.push({
        test: 'GET /health',
        success: false,
        status: 'ERROR',
        details: error.message
      });
    }

    // Test 2: Petición CORS preflight
    try {
      console.log('🧪 Testing CORS preflight...');
      const response = await fetch(`${backendUrl}/api/import/status`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      results.push({
        test: 'GET /api/import/status',
        success: response.ok,
        status: response.status,
        details: response.ok ? await response.json() : await response.text()
      });
    } catch (error) {
      results.push({
        test: 'GET /api/import/status',
        success: false,
        status: 'ERROR',
        details: error.message
      });
    }

    // Test 3: Petición POST (simulando login)
    try {
      console.log('🧪 Testing POST request...');
      const response = await fetch(`${backendUrl}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: 'test',
          password: 'test'
        })
      });
      
      results.push({
        test: 'POST /api/auth/login',
        success: response.status !== 0, // Cualquier respuesta del servidor es buena
        status: response.status,
        details: await response.text()
      });
    } catch (error) {
      results.push({
        test: 'POST /api/auth/login',
        success: false,
        status: 'ERROR',
        details: error.message
      });
    }

    setTestResults(results);
    setTesting(false);
  };

  const copyDebugInfo = () => {
    const debugInfo = {
      backendUrl,
      currentUrl: window.location.href,
      userAgent: navigator.userAgent,
      testResults,
      timestamp: new Date().toISOString()
    };
    
    navigator.clipboard.writeText(JSON.stringify(debugInfo, null, 2));
    alert('Información de debug copiada al portapapeles');
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Diagnóstico CORS y Conectividad
      </h3>

      {/* Información básica */}
      <div className="mb-6 p-4 bg-gray-50 rounded">
        <h4 className="font-medium text-gray-800 mb-2">Configuración Actual</h4>
        <div className="text-sm space-y-1">
          <div><strong>Frontend URL:</strong> {window.location.origin}</div>
          <div><strong>Backend URL:</strong> {backendUrl}</div>
          <div><strong>User Agent:</strong> {navigator.userAgent.substring(0, 100)}...</div>
        </div>
      </div>

      {/* Botón de test */}
      <div className="mb-6">
        <button
          onClick={runCorsTests}
          disabled={testing}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50 flex items-center"
        >
          {testing ? <RefreshCw className="h-4 w-4 mr-2 animate-spin" /> : <RefreshCw className="h-4 w-4 mr-2" />}
          {testing ? 'Probando...' : 'Ejecutar Tests CORS'}
        </button>
      </div>

      {/* Resultados */}
      {testResults.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="font-medium text-gray-800">Resultados:</h4>
            <button
              onClick={copyDebugInfo}
              className="text-sm bg-gray-100 px-3 py-1 rounded hover:bg-gray-200 flex items-center"
            >
              <Copy className="h-3 w-3 mr-1" />
              Copiar Debug
            </button>
          </div>
          
          {testResults.map((result, index) => (
            <div key={index} className={`p-3 rounded border ${
              result.success 
                ? 'bg-green-50 border-green-200' 
                : 'bg-red-50 border-red-200'
            }`}>
              <div className="flex items-start">
                {result.success ? (
                  <CheckCircle className="h-4 w-4 text-green-600 mr-2 mt-0.5" />
                ) : (
                  <AlertTriangle className="h-4 w-4 text-red-600 mr-2 mt-0.5" />
                )}
                <div className="flex-1">
                  <p className={`font-medium ${
                    result.success ? 'text-green-800' : 'text-red-800'
                  }`}>
                    {result.test} - Status: {result.status}
                  </p>
                  <pre className={`text-xs mt-1 ${
                    result.success ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {typeof result.details === 'object' 
                      ? JSON.stringify(result.details, null, 2)
                      : result.details}
                  </pre>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Instrucciones manuales */}
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded">
        <h4 className="font-medium text-blue-800 mb-2">Test Manual en Consola del Navegador:</h4>
        <div className="text-sm text-blue-700 space-y-2">
          <p>Abre la consola del navegador (F12) y ejecuta:</p>
          <pre className="bg-blue-100 p-2 rounded text-xs overflow-x-auto">
{`fetch('${backendUrl}/health')
  .then(r => r.json())
  .then(d => console.log('✅ Success:', d))
  .catch(e => console.log('❌ Error:', e));`}
          </pre>
          <p>Si esto falla, el problema es de red/CORS. Si funciona, el problema es del componente React.</p>
        </div>
      </div>
    </div>
  );
};

export default CorsDebug;