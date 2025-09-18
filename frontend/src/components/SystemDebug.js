import React, { useState } from 'react';
import { Play, CheckCircle, AlertTriangle, RefreshCw } from 'lucide-react';

const SystemDebug = () => {
  const [debugResult, setDebugResult] = useState(null);
  const [authResult, setAuthResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://192.168.1.18:8007';

  const runSystemDebug = async () => {
    setLoading(true);
    try {
      console.log('🔍 Running system debug...');
      const response = await fetch(`${backendUrl}/api/import/debug`);
      const data = await response.json();
      
      setDebugResult({
        success: response.ok,
        status: response.status,
        data: data
      });
      
      console.log('🔍 Debug result:', data);
    } catch (error) {
      setDebugResult({
        success: false,
        error: error.message
      });
    } finally {
      setLoading(false);
    }
  };

  const testAuth = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      console.log('🔑 Testing auth with token:', token ? 'Present' : 'Missing');
      
      const response = await fetch(`${backendUrl}/api/import/test-auth`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      const responseText = await response.text();
      let data;
      try {
        data = JSON.parse(responseText);
      } catch (e) {
        data = { raw_response: responseText, parse_error: e.message };
      }
      
      setAuthResult({
        success: response.ok,
        status: response.status,
        data: data
      });
      
      console.log('🔑 Auth result:', data);
    } catch (error) {
      setAuthResult({
        success: false,
        error: error.message
      });
    } finally {
      setLoading(false);
    }
  };

  const renderCheck = (check) => {
    if (!check) return null;
    
    const isOk = check.status === 'ok';
    return (
      <div className={`p-3 rounded border ${
        isOk ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
      }`}>
        <div className="flex items-center">
          {isOk ? (
            <CheckCircle className="h-4 w-4 text-green-600 mr-2" />
          ) : (
            <AlertTriangle className="h-4 w-4 text-red-600 mr-2" />
          )}
          <span className={`font-medium ${
            isOk ? 'text-green-800' : 'text-red-800'
          }`}>
            {isOk ? 'OK' : 'ERROR'}
          </span>
        </div>
        {check.message && (
          <p className={`text-sm mt-1 ${
            isOk ? 'text-green-600' : 'text-red-600'
          }`}>
            {check.message}
          </p>
        )}
        {Object.entries(check).filter(([key]) => !['status', 'message'].includes(key)).map(([key, value]) => (
          <p key={key} className="text-xs text-gray-600 mt-1">
            <strong>{key}:</strong> {JSON.stringify(value)}
          </p>
        ))}
      </div>
    );
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Diagnóstico del Sistema
        </h2>

        {/* Control buttons */}
        <div className="flex space-x-3 mb-6">
          <button
            onClick={runSystemDebug}
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50 flex items-center"
          >
            {loading ? <RefreshCw className="h-4 w-4 mr-2 animate-spin" /> : <Play className="h-4 w-4 mr-2" />}
            Debug Sistema
          </button>
          
          <button
            onClick={testAuth}
            disabled={loading}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:opacity-50 flex items-center"
          >
            {loading ? <RefreshCw className="h-4 w-4 mr-2 animate-spin" /> : <Play className="h-4 w-4 mr-2" />}
            Test Auth
          </button>
        </div>

        {/* System Debug Results */}
        {debugResult && (
          <div className="mb-6">
            <h3 className="font-medium text-gray-800 mb-3">Resultado Debug Sistema:</h3>
            
            <div className={`p-4 rounded mb-4 ${
              debugResult.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
            }`}>
              <div className="flex items-center mb-2">
                {debugResult.success ? (
                  <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
                ) : (
                  <AlertTriangle className="h-5 w-5 text-red-600 mr-2" />
                )}
                <span className={`font-medium ${
                  debugResult.success ? 'text-green-800' : 'text-red-800'
                }`}>
                  Status: {debugResult.status} - {debugResult.success ? 'OK' : 'ERROR'}
                </span>
              </div>
              
              {debugResult.error && (
                <p className="text-red-600 text-sm">{debugResult.error}</p>
              )}
            </div>

            {debugResult.data && debugResult.data.checks && (
              <div className="space-y-3">
                <h4 className="font-medium text-gray-700">Verificaciones del Sistema:</h4>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div>
                    <h5 className="text-sm font-medium text-gray-600 mb-2">Importaciones Python:</h5>
                    {renderCheck(debugResult.data.checks.imports)}
                  </div>
                  
                  <div>
                    <h5 className="text-sm font-medium text-gray-600 mb-2">Variables de Entorno:</h5>
                    {renderCheck(debugResult.data.checks.environment)}
                  </div>
                  
                  <div>
                    <h5 className="text-sm font-medium text-gray-600 mb-2">Base de Datos:</h5>
                    {renderCheck(debugResult.data.checks.database)}
                  </div>
                  
                  <div>
                    <h5 className="text-sm font-medium text-gray-600 mb-2">Colecciones:</h5>
                    {renderCheck(debugResult.data.checks.collections)}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Auth Test Results */}
        {authResult && (
          <div className="mb-6">
            <h3 className="font-medium text-gray-800 mb-3">Resultado Test Autenticación:</h3>
            
            <div className={`p-4 rounded ${
              authResult.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
            }`}>
              <div className="flex items-center mb-2">
                {authResult.success ? (
                  <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
                ) : (
                  <AlertTriangle className="h-5 w-5 text-red-600 mr-2" />
                )}
                <span className={`font-medium ${
                  authResult.success ? 'text-green-800' : 'text-red-800'
                }`}>
                  Auth Status: {authResult.status} - {authResult.success ? 'OK' : 'FAILED'}
                </span>
              </div>
              
              {authResult.data && (
                <pre className="text-xs bg-white p-2 rounded mt-2 overflow-auto">
                  {JSON.stringify(authResult.data, null, 2)}
                </pre>
              )}
              
              {authResult.error && (
                <p className="text-red-600 text-sm mt-2">{authResult.error}</p>
              )}
            </div>
          </div>
        )}

        {/* Instructions */}
        <div className="bg-blue-50 border border-blue-200 rounded p-4">
          <h4 className="font-medium text-blue-800 mb-2">Instrucciones:</h4>
          <ul className="text-sm text-blue-700 space-y-1">
            <li>1. <strong>Debug Sistema:</strong> Verifica importaciones, variables, MongoDB y colecciones</li>
            <li>2. <strong>Test Auth:</strong> Verifica que el token JWT funcione correctamente</li>
            <li>3. Si algún check falla, esa es la causa del error 500</li>
            <li>4. Si todo está OK, el problema puede estar en el procesamiento específico del archivo</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default SystemDebug;