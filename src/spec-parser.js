const YAML = require('yaml');

class SpecParser {
  parse(content, filename) {
    const ext = filename.split('.').pop().toLowerCase();
    
    if (ext === 'yaml' || ext === 'yml') {
      return this.parseYAML(content);
    } else if (ext === 'md') {
      return this.parseMarkdown(content);
    } else {
      throw new Error(`Unsupported file format: ${ext}`);
    }
  }
  
  parseYAML(content) {
    try {
      return YAML.parse(content);
    } catch (error) {
      throw new Error(`Failed to parse YAML: ${error.message}`);
    }
  }
  
  parseMarkdown(content) {
    const spec = {
      name: '',
      description: '',
      requirements: {
        functional: [],
        non_functional: []
      },
      user_stories: [],
      test_cases: []
    };
    
    const lines = content.split('\n');
    let currentSection = '';
    let currentItem = null;
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      
      // Detect sections
      if (line.startsWith('## ')) {
        currentSection = line.substring(3).trim().toLowerCase();
        currentItem = null;
      }
      
      // Parse functional requirements
      if (currentSection.includes('functional requirement')) {
        const frMatch = line.match(/\*\*FR-(\d+)\*\*:\s*(.+)/);
        if (frMatch) {
          currentItem = {
            id: `FR-${frMatch[1]}`,
            description: frMatch[2],
            priority: 'medium',
            status: 'planned'
          };
          spec.requirements.functional.push(currentItem);
        }
        
        if (currentItem && line.includes('**Priority**:')) {
          const priority = line.split(':')[1].trim().toLowerCase().split('/')[0];
          currentItem.priority = priority;
        }
      }
      
      // Parse test cases
      if (currentSection.includes('test case')) {
        const tcMatch = line.match(/\*\*ID\*\*:\s*TC-(\d+)/);
        if (tcMatch) {
          currentItem = {
            id: `TC-${tcMatch[1]}`,
            description: '',
            steps: [],
            expected_result: ''
          };
          spec.test_cases.push(currentItem);
        }
        
        if (currentItem) {
          if (line.includes('**Description**:')) {
            currentItem.description = line.split(':').slice(1).join(':').trim();
          }
          if (line.includes('**Expected Result**:')) {
            currentItem.expected_result = line.split(':').slice(1).join(':').trim();
          }
        }
      }
    }
    
    return spec;
  }
}

module.exports = { SpecParser };
