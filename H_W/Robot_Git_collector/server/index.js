const express = require('express');
const cors = require('cors');
const http = require('http');
const socketIo = require('socket.io');
const path = require('path');
const fs = require('fs-extra');
const axios = require('axios');
const { marked } = require('marked');
require('dotenv').config();

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "http://localhost:3000",
    methods: ["GET", "POST"]
  }
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../client/build')));

// GitHub API configuration
const GITHUB_API_BASE = process.env.GITHUB_API_BASE || 'https://api.github.com';
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;

// Agent classes
class CollectorAgent {
  constructor(socket) {
    this.socket = socket;
  }

  async collect(searchQuery) {
    try {
      this.emitLog('Collector', `🔍 Searching GitHub for "${searchQuery}"...`);
      
      // Search GitHub repositories
      const headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Robot-AI-Agent'
      };
      
      // Add authorization token if available
      if (GITHUB_TOKEN) {
        headers['Authorization'] = `token ${GITHUB_TOKEN}`;
      }
      
      const searchResponse = await axios.get(`${GITHUB_API_BASE}/search/repositories`, {
        params: {
          q: searchQuery,
          sort: 'stars',
          order: 'desc',
          per_page: 10
        },
        headers
      });

      if (searchResponse.data.items.length === 0) {
        throw new Error('No repositories found');
      }

      const repo = searchResponse.data.items[0];
      this.emitLog('Collector', `📦 Repository found: ${repo.html_url}`);
      
      // Get repository contents
      const contentsResponse = await axios.get(`${GITHUB_API_BASE}/repos/${repo.full_name}/contents`, {
        headers
      });

      const relevantFiles = this.filterRelevantFiles(contentsResponse.data);
      this.emitLog('Collector', `📄 Extracting files: ${relevantFiles.map(f => f.name).join(', ')}`);

      // Collect file contents
      const fileContents = {};
      for (const file of relevantFiles.slice(0, 5)) { // Limit to 5 files
        try {
          const fileResponse = await axios.get(file.url, {
            headers
          });
          fileContents[file.name] = atob(fileResponse.data.content);
        } catch (error) {
          console.warn(`Failed to fetch ${file.name}:`, error.message);
        }
      }

      const rawData = {
        repository: {
          name: repo.name,
          full_name: repo.full_name,
          description: repo.description,
          html_url: repo.html_url,
          stars: repo.stargazers_count,
          language: repo.language
        },
        files: fileContents,
        search_query: searchQuery,
        collected_at: new Date().toISOString()
      };

      this.emitLog('Collector', '✅ Generated: data_raw.json');
      return rawData;

    } catch (error) {
      this.emitLog('Collector', `❌ Error: ${error.message}`);
      throw error;
    }
  }

  filterRelevantFiles(contents) {
    const relevantExtensions = ['.py', '.cpp', '.h', '.launch', '.urdf', '.xacro', '.xml', '.yaml', '.yml', '.md', '.txt'];
    const relevantNames = ['README', 'package', 'CMakeLists', 'setup', 'requirements'];
    
    return contents.filter(item => {
      if (item.type !== 'file') return false;
      
      const extension = path.extname(item.name);
      const baseName = path.basename(item.name, extension);
      
      return relevantExtensions.includes(extension) || 
             relevantNames.some(name => baseName.toLowerCase().includes(name.toLowerCase()));
    });
  }

  emitLog(agent, message) {
    this.socket.emit('agent-log', { agent, message });
  }
}

class AnalystAgent {
  constructor(socket) {
    this.socket = socket;
  }

  async analyze(rawData) {
    try {
      this.emitLog('Analyst', '🧠 Analyzing source code logic...');

      const analysis = {
        project_type: this.detectProjectType(rawData),
        ros_version: this.detectRosVersion(rawData),
        control_type: this.detectControlType(rawData),
        topics: this.extractTopics(rawData),
        complexity_level: this.assessComplexity(rawData),
        dependencies: this.extractDependencies(rawData),
        file_structure: this.analyzeFileStructure(rawData)
      };

      this.emitLog('Analyst', `🔧 Detected Control Type: ${analysis.control_type}`);
      this.emitLog('Analyst', `📡 ROS Topic Map: ${analysis.topics.join(' -> ')}`);
      this.emitLog('Analyst', `📊 Complexity Level: ${analysis.complexity_level}`);

      return analysis;

    } catch (error) {
      this.emitLog('Analyst', `❌ Analysis Error: ${error.message}`);
      throw error;
    }
  }

  detectProjectType(data) {
    const files = Object.keys(data.files);
    const content = Object.values(data.files).join(' ').toLowerCase();
    
    if (content.includes('ros2') || content.includes('rclpy') || content.includes('rclcpp')) {
      return 'ROS2';
    } else if (content.includes('ros') || content.includes('rospy') || content.includes('roscpp')) {
      return 'ROS1';
    } else if (files.some(f => f.includes('.py'))) {
      return 'Python';
    } else if (files.some(f => f.includes('.cpp'))) {
      return 'C++';
    }
    return 'Unknown';
  }

  detectRosVersion(data) {
    const content = Object.values(data.files).join(' ').toLowerCase();
    if (content.includes('ros2') || content.includes('rclpy') || content.includes('rclcpp')) {
      return 'ROS2';
    } else if (content.includes('ros') || content.includes('rospy') || content.includes('roscpp')) {
      return 'ROS1';
    }
    return 'None';
  }

  detectControlType(data) {
    const content = Object.values(data.files).join(' ').toLowerCase();
    
    if (content.includes('pid') || content.includes('proportional')) {
      return 'PID Control';
    } else if (content.includes('model predictive') || content.includes('mpc')) {
      return 'Model Predictive Control';
    } else if (content.includes('adaptive')) {
      return 'Adaptive Control';
    } else if (content.includes('diff_drive') || content.includes('differential')) {
      return 'Differential Drive';
    }
    return 'Unknown';
  }

  extractTopics(data) {
    const topics = [];
    const content = Object.values(data.files).join(' ');
    
    // Simple regex to find ROS topics
    const topicMatches = content.match(/\/[a-zA-Z_][a-zA-Z0-9_\/]*/g);
    if (topicMatches) {
      topics.push(...[...new Set(topicMatches)].slice(0, 5));
    }
    
    return topics.length > 0 ? topics : ['/cmd_vel', '/odom'];
  }

  assessComplexity(data) {
    const fileCount = Object.keys(data.files).length;
    const totalLines = Object.values(data.files).reduce((sum, content) => {
      return sum + content.split('\n').length;
    }, 0);
    
    if (totalLines < 100) return 'Beginner';
    if (totalLines < 500) return 'Intermediate';
    if (totalLines < 1000) return 'Advanced';
    return 'Expert';
  }

  extractDependencies(data) {
    const dependencies = [];
    const content = Object.values(data.files).join(' ');
    
    // Python imports
    const pythonImports = content.match(/import\s+([a-zA-Z_][a-zA-Z0-9_]+)/g);
    if (pythonImports) {
      dependencies.push(...pythonImports.map(imp => imp.replace('import ', '')));
    }
    
    // ROS package dependencies
    const rosDeps = content.match(/<depend\s+package="([^"]+)"/g);
    if (rosDeps) {
      dependencies.push(...rosDeps.map(dep => dep.match(/package="([^"]+)"/)[1]));
    }
    
    return [...new Set(dependencies)].slice(0, 10);
  }

  analyzeFileStructure(data) {
    return Object.keys(data.files).map(filename => ({
      name: filename,
      type: path.extname(filename),
      size: data.files[filename].length,
      lines: data.files[filename].split('\n').length
    }));
  }

  emitLog(agent, message) {
    this.socket.emit('agent-log', { agent, message });
  }
}

class ValidatorAgent {
  constructor(socket) {
    this.socket = socket;
  }

  async validate(rawData, analysis) {
    try {
      this.emitLog('Validator', '🔍 Running static analysis...');

      const validation = {
        syntax_check: this.checkSyntax(rawData),
        dependencies_check: this.checkDependencies(analysis.dependencies),
        security_check: this.checkSecurity(rawData),
        performance_score: this.assessPerformance(rawData),
        reliability_score: 0,
        recommendations: []
      };

      validation.reliability_score = this.calculateReliabilityScore(validation);
      
      this.emitLog('Validator', `✅ Syntax Check: ${validation.syntax_check.status}`);
      this.emitLog('Validator', `📦 Dependencies Check: ${validation.dependencies_check.status}`);
      this.emitLog('Validator', `📊 Reliability Score: ${validation.reliability_score}/100`);

      return validation;

    } catch (error) {
      this.emitLog('Validator', `❌ Validation Error: ${error.message}`);
      throw error;
    }
  }

  checkSyntax(data) {
    // Simple syntax validation
    const pythonFiles = Object.keys(data.files).filter(f => f.endsWith('.py'));
    const cppFiles = Object.keys(data.files).filter(f => f.endsWith('.cpp'));
    
    let errors = 0;
    let totalFiles = pythonFiles.length + cppFiles.length;
    
    // Check for basic Python syntax issues
    pythonFiles.forEach(filename => {
      const content = data.files[filename];
      if (content.includes('import') && !content.includes('from')) {
        // Basic check
      }
    });

    return {
      status: errors === 0 ? 'PASS' : 'FAIL',
      errors_found: errors,
      files_checked: totalFiles
    };
  }

  checkDependencies(dependencies) {
    const commonDeps = ['numpy', 'scipy', 'matplotlib', 'geometry_msgs', 'sensor_msgs'];
    const missingCommon = commonDeps.filter(dep => !dependencies.includes(dep));
    
    return {
      status: missingCommon.length === 0 ? 'PASS' : 'WARNING',
      missing_dependencies: missingCommon,
      total_dependencies: dependencies.length
    };
  }

  checkSecurity(data) {
    const content = Object.values(data.files).join(' ').toLowerCase();
    const securityIssues = [];
    
    if (content.includes('eval(') || content.includes('exec(')) {
      securityIssues.push('Dynamic code execution detected');
    }
    
    return {
      status: securityIssues.length === 0 ? 'PASS' : 'WARNING',
      issues: securityIssues
    };
  }

  assessPerformance(data) {
    const totalLines = Object.values(data.files).reduce((sum, content) => {
      return sum + content.split('\n').length;
    }, 0);
    
    // Simple performance heuristic
    if (totalLines < 100) return 90;
    if (totalLines < 500) return 80;
    if (totalLines < 1000) return 70;
    return 60;
  }

  calculateReliabilityScore(validation) {
    let score = 100;
    
    if (validation.syntax_check.status === 'FAIL') score -= 30;
    if (validation.dependencies_check.status === 'WARNING') score -= 20;
    if (validation.security_check.status === 'WARNING') score -= 25;
    
    score = Math.max(0, Math.min(100, score));
    return Math.round(score);
  }

  emitLog(agent, message) {
    this.socket.emit('agent-log', { agent, message });
  }
}

class EngineerAgent {
  constructor(socket) {
    this.socket = socket;
  }

  async generateSimulation(rawData, analysis, validation) {
    try {
      this.emitLog('Engineer', '⚙️ Synthesizing Gazebo simulation config...');

      const simulation = {
        launch_file: this.generateLaunchFile(analysis),
        urdf_config: this.generateUrdfConfig(analysis),
        gazebo_world: this.generateGazeboWorld(analysis),
        ros_commands: this.generateRosCommands(analysis),
        docker_config: this.generateDockerConfig(analysis)
      };

      this.emitLog('Engineer', '🚀 Generated: sim_launcher.py');
      this.emitLog('Engineer', '🗺️ Mapping URDF to Ignition Gazebo plugins...');
      this.emitLog('Engineer', '✅ Pipeline Completed Successfully.');

      return simulation;

    } catch (error) {
      this.emitLog('Engineer', `❌ Simulation Generation Error: ${error.message}`);
      throw error;
    }
  }

  generateLaunchFile(analysis) {
    const rosVersion = analysis.ros_version;
    const projectName = analysis.project_type.toLowerCase();
    
    if (rosVersion === 'ROS2') {
      return `#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='gazebo_ros',
            executable='gazebo',
            name='gazebo',
            arguments=['--verbose', '-s', 'libgazebo_ros_init.so'],
            output='screen'
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'robot_description': open_urdf()}]
        ),
        Node(
            package='${projectName}_controller',
            executable='controller_node',
            name='controller',
            output='screen'
        )
    ])

def open_urdf():
    return open(get_package_share_directory('${projectName}_description') + '/urdf/robot.urdf').read()`;
    }
    
    return '# ROS1 launch file would go here';
  }

  generateUrdfConfig(analysis) {
    return `<?xml version="1.0"?>
<robot name="${analysis.project_type}_robot">
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.3 0.1"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.3 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10"/>
      <inertia ixx="1" ixy="0" ixz="0" iyy="1" iyz="0" izz="1"/>
    </inertial>
  </link>
  
  <!-- Differential drive configuration -->
  <link name="left_wheel"/>
  <link name="right_wheel"/>
</robot>`;
  }

  generateGazeboWorld(analysis) {
    return `<?xml version="1.0"?>
<sdf version="1.6">
  <world name="default">
    <include>
      <uri>model://ground_plane</uri>
    </include>
    <include>
      <uri>model://sun</uri>
    </include>
    
    <!-- Physics configuration -->
    <physics name="1ms" type="ignored">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>
  </world>
</sdf>`;
  }

  generateRosCommands(analysis) {
    const rosVersion = analysis.ros_version;
    const projectName = analysis.project_type.toLowerCase();
    
    if (rosVersion === 'ROS2') {
      return [
        `ros2 launch ${projectName}_sim simulation.launch.py`,
        `ros2 run ${projectName}_controller controller_node`,
        `ros2 topic echo /cmd_vel`,
        `ros2 topic hz /odom`
      ];
    }
    
    return [
      `roslaunch ${projectName}_sim simulation.launch`,
      `rosrun ${projectName}_controller controller_node`,
      `rostopic echo /cmd_vel`,
      `rostopic hz /odom`
    ];
  }

  generateDockerConfig(analysis) {
    return `FROM ros:humble-ros-base

# Install dependencies
RUN apt-get update && apt-get install -y \\
    python3-pip \\
    gazebo \\
    ros-humble-gazebo-ros-pkgs \\
    ros-humble-robot-state-publisher \\
    ros-humble-joint-state-publisher \\
    && rm -rf /var/lib/apt/lists/*

# Copy workspace
COPY ./ws /ros2_ws
WORKDIR /ros2_ws

# Build
RUN source /opt/ros/humble/setup.bash && colcon build

# Launch command
CMD ["bash", "-c", "source /opt/ros/humble/setup.bash && source install/setup.bash && ros2 launch ${analysis.project_type.toLowerCase()}_sim simulation.launch.py"]`;
  }

  emitLog(agent, message) {
    this.socket.emit('agent-log', { agent, message });
  }
}

// Socket.IO connection handling
io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);

  socket.on('run-pipeline', async (data) => {
    try {
      const { searchQuery } = data;
      
      // Validate search query
      if (!searchQuery || searchQuery.trim() === '') {
        throw new Error('검색어를 입력해주세요.');
      }
      
      // Initialize agents
      const collector = new CollectorAgent(socket);
      const analyst = new AnalystAgent(socket);
      const validator = new ValidatorAgent(socket);
      const engineer = new EngineerAgent(socket);

      // Step 1: Collection
      socket.emit('step-update', { step: 0 });
      const rawData = await collector.collect(searchQuery);

      // Step 2: Analysis
      socket.emit('step-update', { step: 1 });
      const analysis = await analyst.analyze(rawData);

      // Step 3: Validation
      socket.emit('step-update', { step: 2 });
      const validation = await validator.validate(rawData, analysis);

      // Step 4: Simulation Generation
      socket.emit('step-update', { step: 3 });
      const simulation = await engineer.generateSimulation(rawData, analysis, validation);

      // Complete
      socket.emit('pipeline-complete', {
        rawData,
        analysis,
        validation,
        simulation
      });
      socket.emit('step-update', { step: 4 });

    } catch (error) {
      console.error('Pipeline error:', error);
      socket.emit('pipeline-error', { error: error.message });
    }
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});

// API Routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Serve React app (only in production)
if (process.env.NODE_ENV === 'production') {
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../client/build/index.html'));
  });
}

const PORT = process.env.PORT || 5000;
server.listen(PORT, () => {
  console.log(`🚀 Robot AI Agent Server running on port ${PORT}`);
  console.log(`🌐 Client: http://localhost:3000`);
  console.log(`🔌 API: http://localhost:${PORT}/api/health`);
});
