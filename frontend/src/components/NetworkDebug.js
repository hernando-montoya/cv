import React, { useState } from 'react';
import { Wifi, CheckCircle, AlertTriangle, RefreshCw } from 'lucide-react';

const NetworkDebug = () => {
  const [networkResult, setNetworkResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || '';

  const runNetworkDebug = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${backendUrl}/api/network/debug`);
      const data = await response.json();
      
      setNetworkResult({
        success: response.ok,
        status: response.status,
        data: data
      });
      
    } catch (error) {
      setNetworkResult({
        success: false,
        error: error.message
      });
    } finally {
      setLoading(false);
    }
  };

  const renderConnectionTest = (url, result) => {
    if (!result) return null;
    
    const isOk = result.status === 'ok';
    return (
      <div className={`p-2 rounded border text-sm ${
        isOk ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
      }`}>
        <div className="flex items-center">
          {isOk ? (
            <CheckCircle className="h-3 w-3 text-green-600 mr-1" />
          ) : (
            <AlertTriangle className="h-3 w-3 text-red-600 mr-1" />
          )}
          <span className={`font-medium ${
            isOk ? 'text-green-800' : 'text-red-800'
          }`}>
            {url.split('@')[1]?.split('/')[0] || url}
          </span>
        </div>
        {result.message && (
          <p className={`text-xs mt-1 ${
            isOk ? 'text-green-600' : 'text-red-600'
          }`}>
            {result.message}
          </p>
        )}
        {result.ip && (
          <p className="text-xs text-gray-600 mt-1">IP: {result.ip}</p>
        )}
      </div>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
        <Wifi className="h-5 w-5 mr-2 text-blue-600" />
        Debug de Red y MongoDB
      </h2>

      <div className="mb-6">
        <button
          onClick={runNetworkDebug}
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50 flex items-center"
        >
          {loading ? <RefreshCw className="h-4 w-4 mr-2 animate-spin" /> : <Wifi className="h-4 w-4 mr-2" />}
          {loading ? 'Probando...' : 'Debug Red'}
        </button>
      </div>

      {networkResult && (
        <div className="space-y-6">
          <div className={`p-4 rounded ${
            networkResult.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
          }`}>
            <div className="flex items-center mb-2">
              {networkResult.success ? (
                <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
              ) : (
                <AlertTriangle className="h-5 w-5 text-red-600 mr-2" />
              )}
              <span className={`font-medium ${
                networkResult.success ? 'text-green-800' : 'text-red-800'
              }`}>
                Network Debug: {networkResult.status} - {networkResult.success ? 'OK' : 'ERROR'}
              </span>
            </div>
          </div>

          {networkResult.data && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Hostname Resolution */}
              <div>
                <h3 className="font-medium text-gray-800 mb-3">Resolución de Hostnames:</h3>
                <div className="space-y-2">
                  {Object.entries(networkResult.data.hostname_resolution || {}).map(([hostname, result]) => 
                    renderConnectionTest(hostname, result)
                  )}
                </div>
              </div>

              {/* Network Info */}
              <div>
                <h3 className="font-medium text-gray-800 mb-3">Info de Red:</h3>
                <div className="bg-gray-50 p-3 rounded text-sm">
                  {Object.entries(networkResult.data.network_info || {}).map(([key, value]) => (
                    <div key={key} className="mb-1">
                      <strong>{key}:</strong> {typeof value === 'string' ? value.substring(0, 50) + (value.length > 50 ? '...' : '') : JSON.stringify(value)}
                    </div>
                  ))}
                </div>
              </div>

              {/* MongoDB Connection Tests */}
              <div>
                <h3 className="font-medium text-gray-800 mb-3">Tests de MongoDB:</h3>
                <div className="space-y-2">
                  {Object.entries(networkResult.data.mongo_connection_tests || {}).map(([url, result]) => 
                    renderConnectionTest(url, result)
                  )}
                </div>
              </div>
            </div>
          )}

          {networkResult.error && (
            <div className="bg-red-50 border border-red-200 rounded p-4">
              <p className="text-red-800">Error: {networkResult.error}</p>
            </div>
          )}
        </div>
      )}

      <div className="mt-6 bg-blue-50 border border-blue-200 rounded p-4">
        <h4 className="font-medium text-blue-800 mb-2">Información:</h4>
        <p className="text-sm text-blue-700">
          Este debug verifica si el contenedor puede resolver hostnames como 'mongodb' y conectarse a MongoDB usando diferentes URLs.
          Si 'mongodb' no se resuelve, el problema es de configuración de red Docker.
        </p>
      </div>
    </div>
  );
};

export default NetworkDebug;