import React, { useState, useEffect, useRef } from 'react';
import { 
  Search, 
  Cpu, 
  CheckCircle, 
  Settings, 
  FileText, 
  Code, 
  Play, 
  Terminal,
  Layers,
  Download,
  Loader2
} from 'lucide-react';
import io from 'socket.io-client';
import './App.css';

const AGENTS = [
  { id: 'collector', name: 'Collector Agent', icon: Search, color: 'text-blue-400', desc: 'GitHub API 수집 및 구조화' },
  { id: 'analyst', name: 'Analyst Agent', icon: Cpu, color: 'text-purple-400', desc: '알고리즘 분석 및 로직 추출' },
  { id: 'validator', name: 'Validator Agent', icon: CheckCircle, color: 'text-green-400', desc: '코드 검증 및 신뢰도 평가' },
  { id: 'engineer', name: 'Engineer Agent', icon: Settings, color: 'text-orange-400', desc: '시뮬레이션 환경 구성' }
];

const App = () => {
  const [socket, setSocket] = useState(null);
  const [activeStep, setActiveStep] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);
  const [logs, setLogs] = useState([]);
  const [searchQuery, setSearchQuery] = useState("ros2_diff_drive_controller");
  const [results, setResults] = useState({ rawData: null, analysis: null, validation: null, simulation: null });
  const [isConnected, setIsConnected] = useState(false);
  const logEndRef = useRef(null);

  useEffect(() => {
    // Initialize socket connection
    const newSocket = io('http://localhost:5000');
    setSocket(newSocket);

    newSocket.on('connect', () => {
      console.log('Connected to server');
      setIsConnected(true);
    });

    newSocket.on('disconnect', () => {
      console.log('Disconnected from server');
      setIsConnected(false);
    });

    newSocket.on('agent-log', (data) => {
      addLog(data.agent, data.message);
    });

    newSocket.on('step-update', (data) => {
      setActiveStep(data.step);
    });

    newSocket.on('pipeline-complete', (data) => {
      setResults(data);
      setIsProcessing(false);
      setActiveStep(4);
      addLog('System', '✅ Pipeline completed successfully!');
    });

    newSocket.on('pipeline-error', (data) => {
      addLog('System', `❌ Error: ${data.error}`);
      setIsProcessing(false);
      setActiveStep(0);
    });

    return () => newSocket.close();
  }, []);

  const addLog = (agent, message) => {
    setLogs(prev => [...prev, { 
      time: new Date().toLocaleTimeString(), 
      agent, 
      message,
      id: Date.now() + Math.random() 
    }]);
  };

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  const runPipeline = async () => {
    if (!socket || !isConnected || isProcessing) return;
    
    // Validate search query
    if (!searchQuery || searchQuery.trim() === '') {
      alert('검색어를 입력해주세요.');
      return;
    }
    
    setIsProcessing(true);
    setLogs([]);
    setActiveStep(0);
    setResults({ rawData: null, analysis: null, validation: null, simulation: null });

    socket.emit('run-pipeline', { searchQuery: searchQuery.trim() });
  };

  const downloadFile = (content, filename) => {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  const formatResults = () => {
    if (!results.analysis) return { json: null, markdown: null, sim: null };

    return {
      json: JSON.stringify({
        project: searchQuery,
        engine: results.analysis.ros_version || "Unknown",
        components: results.analysis.file_structure?.map(f => f.name) || [],
        control_type: results.analysis.control_type,
        complexity: results.analysis.complexity_level,
        reliability_score: results.validation?.reliability_score || 0
      }, null, 2),
      markdown: `# 🤖 ${searchQuery} 분석 결과

## 📊 프로젝트 정보
- **프로젝트 타입**: ${results.analysis.project_type}
- **ROS 버전**: ${results.analysis.ros_version}
- **제어 타입**: ${results.analysis.control_type}
- **복잡도**: ${results.analysis.complexity_level}

## 🔧 핵심 로직
- **ROS Topics**: ${results.analysis.topics?.join(' -> ') || 'N/A'}
- **의존성**: ${results.analysis.dependencies?.slice(0, 5).join(', ') || 'N/A'}

## ✅ 검증 결과
- **신뢰도 점수**: ${results.validation?.reliability_score || 0}/100
- **문법 검사**: ${results.validation?.syntax_check?.status || 'Unknown'}
- **보안 검사**: ${results.validation?.security_check?.status || 'Unknown'}

## 🚀 시뮬레이션
시뮬레이션 환경이 구성되었습니다. 아래 명령어를 실행하여 시뮬레이션을 시작하세요.`,
      sim: results.simulation?.ros_commands?.[0] || `ros2 launch ${searchQuery}_sim simulation.launch.py`
    };
  };

  const formattedResults = formatResults();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 p-8 font-sans">
      <header className="max-w-6xl mx-auto mb-10 flex justify-between items-end border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center gap-3">
            <Layers className="text-blue-500" /> Agri-Log Robot Agent Pipeline
          </h1>
          <p className="text-slate-400 mt-2">수집-분석-검증-시뮬레이션 자동화 시스템</p>
          <div className="flex items-center gap-2 mt-2">
            <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'} animate-pulse`}></div>
            <span className="text-xs text-slate-500">
              {isConnected ? '서버 연결됨' : '서버 연결 안됨'}
            </span>
          </div>
        </div>
        <div className="flex gap-4">
          <input 
            type="text" 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 w-64 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Search Keyword..."
            disabled={isProcessing}
          />
          <button 
            onClick={runPipeline}
            disabled={!isConnected || isProcessing}
            className={`flex items-center gap-2 px-6 py-2 rounded-lg font-semibold transition-all ${
              !isConnected || isProcessing ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-500 text-white'
            }`}
          >
            {isProcessing ? (
              <>
                <Loader2 size={18} className="animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <Play size={18} />
                Run Pipeline
              </>
            )}
          </button>
        </div>
      </header>

      <main className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Agents Panel */}
        <div className="lg:col-span-4 space-y-4">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Cpu size={20} className="text-blue-500" /> Active Agents
          </h2>
          {AGENTS.map((agent, index) => {
            const Icon = agent.icon;
            const isActive = activeStep === index;
            const isDone = activeStep > index;
            
            return (
              <div 
                key={agent.id}
                className={`p-4 rounded-xl border transition-all duration-500 ${
                  isActive ? 'bg-slate-900 border-blue-500 shadow-lg shadow-blue-900/20 scale-105' : 
                  isDone ? 'bg-slate-900/50 border-green-900/50 opacity-60' : 
                  'bg-slate-900/20 border-slate-800 opacity-40'
                }`}
              >
                <div className="flex items-center gap-4">
                  <div className={`p-2 rounded-lg ${isActive ? 'bg-blue-500/20' : 'bg-slate-800'}`}>
                    <Icon className={agent.color} size={24} />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-bold">{agent.name}</h3>
                    <p className="text-xs text-slate-500">{agent.desc}</p>
                  </div>
                  {isDone && <CheckCircle className="text-green-500" size={18} />}
                  {isActive && <div className="w-2 h-2 bg-blue-500 rounded-full animate-ping" />}
                </div>
              </div>
            );
          })}
        </div>

        {/* Main Content */}
        <div className="lg:col-span-8 space-y-6">
          <div className="bg-black rounded-xl border border-slate-800 overflow-hidden flex flex-col h-[400px]">
            <div className="bg-slate-900 px-4 py-2 border-b border-slate-800 flex items-center gap-2">
              <Terminal size={14} className="text-slate-400" />
              <span className="text-xs font-mono text-slate-400 uppercase tracking-widest">System Log Terminal</span>
            </div>
            <div className="p-4 font-mono text-sm overflow-y-auto flex-1 space-y-1">
              {logs.length === 0 && <div className="text-slate-700 italic">파이프라인을 실행하면 로그가 여기에 표시됩니다...</div>}
              {logs.map(log => (
                <div key={log.id} className="flex gap-3">
                  <span className="text-slate-600">[{log.time}]</span>
                  <span className={`font-bold w-20 ${
                    log.agent === 'Collector' ? 'text-blue-400' : 
                    log.agent === 'Analyst' ? 'text-purple-400' :
                    log.agent === 'Validator' ? 'text-green-400' : 
                    log.agent === 'Engineer' ? 'text-orange-400' :
                    log.agent === 'System' ? 'text-yellow-400' : 'text-slate-400'
                  }`}>
                    {log.agent}
                  </span>
                  <span className="text-slate-300">{log.message}</span>
                </div>
              ))}
              <div ref={logEndRef} />
            </div>
          </div>

          {/* Results */}
          {activeStep === 4 && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 animate-in fade-in slide-in-from-bottom-4 duration-700">
              <div className="bg-slate-900 p-5 rounded-xl border border-slate-800">
                <div className="flex justify-between items-center mb-3">
                  <h3 className="text-sm font-bold flex items-center gap-2"><FileText size={16} className="text-blue-400" /> Markdown Report</h3>
                  <button 
                    onClick={() => downloadFile(formattedResults.markdown, `${searchQuery}_report.md`)}
                    className="text-slate-500 hover:text-white transition-colors"
                  >
                    <Download size={14} />
                  </button>
                </div>
                <div className="text-xs text-slate-400 bg-slate-950 p-3 rounded border border-slate-800 whitespace-pre-wrap h-32 overflow-y-auto">
                  {formattedResults.markdown}
                </div>
              </div>
              <div className="bg-slate-900 p-5 rounded-xl border border-slate-800">
                <div className="flex justify-between items-center mb-3">
                  <h3 className="text-sm font-bold flex items-center gap-2"><Code size={16} className="text-purple-400" /> JSON Data (Agent Read)</h3>
                  <button 
                    onClick={() => downloadFile(formattedResults.json, `${searchQuery}_data.json`)}
                    className="text-slate-500 hover:text-white transition-colors"
                  >
                    <Download size={14} />
                  </button>
                </div>
                <pre className="text-[10px] text-purple-300 bg-slate-950 p-3 rounded border border-slate-800 h-32 overflow-y-auto">
                  {formattedResults.json}
                </pre>
              </div>
              <div className="md:col-span-2 bg-gradient-to-r from-orange-900/20 to-slate-900 p-5 rounded-xl border border-orange-900/30">
                <h3 className="text-sm font-bold flex items-center gap-2 mb-3 text-orange-400">
                  <Play size={16} /> Simulation Ready
                </h3>
                <div className="flex items-center gap-4 bg-black/50 p-3 rounded-lg border border-orange-500/20 font-mono text-xs">
                  <span className="text-orange-500">$</span>
                  <code className="text-slate-300 flex-1">{formattedResults.sim}</code>
                  <button 
                    onClick={() => navigator.clipboard.writeText(formattedResults.sim)}
                    className="text-[10px] bg-orange-600 px-2 py-1 rounded text-white hover:bg-orange-500 transition-colors"
                  >
                    Copy Command
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      <footer className="max-w-6xl mx-auto mt-12 text-center text-slate-600 text-xs border-t border-slate-900 pt-8">
        Designed for Robotics Learning Pipeline & Agri-Log Integration
      </footer>
    </div>
  );
};

export default App;
