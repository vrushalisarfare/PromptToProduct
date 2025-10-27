#!/usr/bin/env node

const { program } = require('commander');
const { SpecValidator } = require('./spec-validator');
const { SpecParser } = require('./spec-parser');
const { TestGenerator } = require('./test-generator');
const fs = require('fs');
const path = require('path');

program
  .name('prompt-to-product')
  .description('Spec-Driven Development CLI for transforming prompts into products')
  .version('1.0.0');

program
  .command('init')
  .description('Initialize a new spec-driven project')
  .option('-n, --name <name>', 'Project name')
  .action((options) => {
    const projectName = options.name || 'my-project';
    console.log(`Initializing new spec-driven project: ${projectName}`);
    
    const projectDir = path.join(process.cwd(), projectName);
    
    if (fs.existsSync(projectDir)) {
      console.error(`Error: Directory ${projectName} already exists`);
      process.exit(1);
    }
    
    // Create project structure
    fs.mkdirSync(projectDir);
    fs.mkdirSync(path.join(projectDir, 'specs'));
    fs.mkdirSync(path.join(projectDir, 'src'));
    fs.mkdirSync(path.join(projectDir, 'tests'));
    
    // Copy template
    const templatePath = path.join(__dirname, '..', 'specs', 'TEMPLATE.md');
    const specPath = path.join(projectDir, 'specs', 'specification.md');
    
    if (fs.existsSync(templatePath)) {
      fs.copyFileSync(templatePath, specPath);
    } else {
      fs.writeFileSync(specPath, '# Specification\n\nWrite your specification here.');
    }
    
    // Create README
    fs.writeFileSync(
      path.join(projectDir, 'README.md'),
      `# ${projectName}\n\nSpec-driven development project.\n\n## Getting Started\n\n1. Edit \`specs/specification.md\` to define your requirements\n2. Run \`prompt-to-product validate\` to validate your spec\n3. Run \`prompt-to-product generate\` to generate tests\n4. Implement your code to pass the tests\n`
    );
    
    console.log(`✓ Project ${projectName} created successfully!`);
    console.log('\nNext steps:');
    console.log(`  cd ${projectName}`);
    console.log('  Edit specs/specification.md');
    console.log('  prompt-to-product validate');
  });

program
  .command('validate')
  .description('Validate a specification file')
  .argument('[file]', 'Specification file to validate', 'specs/specification.md')
  .action((file) => {
    console.log(`Validating specification: ${file}`);
    
    if (!fs.existsSync(file)) {
      console.error(`Error: File ${file} not found`);
      process.exit(1);
    }
    
    try {
      const validator = new SpecValidator();
      const content = fs.readFileSync(file, 'utf8');
      const result = validator.validate(content, file);
      
      if (result.valid) {
        console.log('✓ Specification is valid');
        if (result.warnings.length > 0) {
          console.log('\nWarnings:');
          result.warnings.forEach(warning => console.log(`  - ${warning}`));
        }
      } else {
        console.error('✗ Specification has errors:');
        result.errors.forEach(error => console.error(`  - ${error}`));
        process.exit(1);
      }
    } catch (error) {
      console.error(`Error validating specification: ${error.message}`);
      process.exit(1);
    }
  });

program
  .command('parse')
  .description('Parse a specification file and display structured output')
  .argument('[file]', 'Specification file to parse')
  .action((file) => {
    if (!file) {
      console.error('Error: Please specify a specification file');
      process.exit(1);
    }
    
    if (!fs.existsSync(file)) {
      console.error(`Error: File ${file} not found`);
      process.exit(1);
    }
    
    try {
      const parser = new SpecParser();
      const content = fs.readFileSync(file, 'utf8');
      const spec = parser.parse(content, file);
      
      console.log('Parsed Specification:');
      console.log(JSON.stringify(spec, null, 2));
    } catch (error) {
      console.error(`Error parsing specification: ${error.message}`);
      process.exit(1);
    }
  });

program
  .command('generate')
  .description('Generate test scaffolding from specification')
  .argument('[file]', 'Specification file')
  .option('-o, --output <dir>', 'Output directory for tests', 'tests')
  .action((file, options) => {
    if (!file) {
      console.error('Error: Please specify a specification file');
      process.exit(1);
    }
    
    if (!fs.existsSync(file)) {
      console.error(`Error: File ${file} not found`);
      process.exit(1);
    }
    
    try {
      const parser = new SpecParser();
      const generator = new TestGenerator();
      
      const content = fs.readFileSync(file, 'utf8');
      const spec = parser.parse(content, file);
      
      const tests = generator.generate(spec);
      
      if (!fs.existsSync(options.output)) {
        fs.mkdirSync(options.output, { recursive: true });
      }
      
      const outputFile = path.join(options.output, 'generated.test.js');
      fs.writeFileSync(outputFile, tests);
      
      console.log(`✓ Tests generated successfully: ${outputFile}`);
    } catch (error) {
      console.error(`Error generating tests: ${error.message}`);
      process.exit(1);
    }
  });

program
  .command('status')
  .description('Show status of requirements and test coverage')
  .action(() => {
    console.log('Spec-Driven Development Status:');
    console.log('This feature will show implementation progress vs specifications');
    // TODO: Implement status tracking
  });

program.parse();
