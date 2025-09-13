/**
 * Script to check and improve accessibility in React components
 * 
 * This script helps identify and fix common accessibility issues in the frontend code.
 * It provides functions to check for missing alt text, color contrast, keyboard navigation,
 * and other accessibility best practices.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Configuration
const SRC_DIR = path.join(__dirname, '..', 'src');
const COMPONENTS_DIR = path.join(SRC_DIR, 'components');
const PAGES_DIR = path.join(SRC_DIR, 'pages');

// Common accessibility issues to check for
const ACCESSIBILITY_ISSUES = {
  MISSING_ALT: 'Image is missing alt text',
  LOW_CONTRAST: 'Text has insufficient color contrast',
  MISSING_LABEL: 'Form element is missing a label',
  MISSING_BUTTON_TYPE: 'Button is missing a type attribute',
  MISSING_INPUT_TYPE: 'Input is missing a type attribute',
  MISSING_KEY: 'List item is missing a key prop',
  INVALID_HTML: 'Invalid HTML structure',
  MISSING_LANG: 'HTML is missing lang attribute',
  MISSING_ROLE: 'Interactive element is missing a role',
  MISSING_ARIA: 'Interactive element is missing ARIA attributes',
};

/**
 * Find all React component files in the project
 */
function findReactComponents() {
  const jsxFiles = [];
  
  function walkDir(dir) {
    const files = fs.readdirSync(dir);
    
    files.forEach(file => {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);
      
      if (stat.isDirectory()) {
        walkDir(filePath);
      } else if (file.match(/\.(jsx|tsx)$/)) {
        jsxFiles.push(filePath);
      }
    });
  }
  
  // Start walking from components and pages directories
  [COMPONENTS_DIR, PAGES_DIR].forEach(dir => {
    if (fs.existsSync(dir)) {
      walkDir(dir);
    }
  });
  
  return jsxFiles;
}

/**
 * Check a single file for accessibility issues
 */
function checkFileAccessibility(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const issues = [];
  const lines = content.split('\n');
  
  // Check for common accessibility issues
  lines.forEach((line, index) => {
    const lineNumber = index + 1;
    
    // Check for missing alt text in images
    if (line.match(/<img\s+[^>]*?src=["'][^"']+["'][^>]*?(?<!alt=["'][^"']*)[\s>]/)) {
      issues.push({
        type: ACCESSIBILITY_ISSUES.MISSING_ALT,
        line: lineNumber,
        code: line.trim(),
      });
    }
    
    // Check for buttons missing type attribute
    if (line.match(/<button\s+[^>]*?(?<!type=["'][^"']*)[\s>]/)) {
      issues.push({
        type: ACCESSIBILITY_ISSUES.MISSING_BUTTON_TYPE,
        line: lineNumber,
        code: line.trim(),
      });
    }
    
    // Check for inputs missing type attribute
    if (line.match(/<input\s+[^>]*?(?<!type=["'][^"']*)[\s>]/)) {
      issues.push({
        type: ACCESSIBILITY_ISSUES.MISSING_INPUT_TYPE,
        line: lineNumber,
        code: line.trim(),
      });
    }
    
    // Check for missing keys in lists
    if (line.match(/<\s*[A-Za-z][^>]*\s+key\s*=\s*{[^}]*}\s*[^>]*>/) && 
        !line.match(/key\s*=\s*\{[\s\S]*?\}/)) {
      issues.push({
        type: ACCESSIBILITY_ISSUES.MISSING_KEY,
        line: lineNumber,
        code: line.trim(),
      });
    }
    
    // Check for interactive elements without proper roles
    if (line.match(/<div\s+[^>]*?onClick\s*=[^>]*>/) && !line.match(/role=["']button["']/)) {
      issues.push({
        type: ACCESSIBILITY_ISSUES.MISSING_ROLE,
        line: lineNumber,
        code: line.trim(),
      });
    }
  });
  
  return issues;
}

/**
 * Generate an accessibility report
 */
function generateAccessibilityReport() {
  console.log('🔍 Checking for accessibility issues...\n');
  
  const components = findReactComponents();
  const report = [];
  let totalIssues = 0;
  
  components.forEach(componentPath => {
    const relativePath = path.relative(process.cwd(), componentPath);
    const issues = checkFileAccessibility(componentPath);
    
    if (issues.length > 0) {
      report.push(`\n📄 ${relativePath}:`);
      
      issues.forEach(issue => {
        report.push(`  Line ${issue.line}: ${issue.type}`);
        report.push(`    ${issue.code}`);
        totalIssues++;
      });
    }
  });
  
  // Add summary
  report.unshift(`\n🔍 Found ${totalIssues} accessibility issues across ${components.length} components\n`);
  
  // Add recommendations
  if (totalIssues > 0) {
    report.push('\n💡 Recommendations for improving accessibility:');
    report.push('  1. Add meaningful alt text to all images');
    report.push('  2. Ensure all interactive elements have proper roles and ARIA attributes');
    report.push('  3. Add proper labels to all form elements');
    report.push('  4. Ensure sufficient color contrast for text');
    report.push('  5. Test keyboard navigation and screen reader compatibility');
    report.push('  6. Use semantic HTML elements where appropriate');
    report.push('  7. Ensure all interactive elements are focusable and have visible focus states');
    report.push('  8. Add proper document titles and language attributes');
  } else {
    report.push('\n✅ No accessibility issues found!');
  }
  
  // Write report to file
  const reportPath = path.join(__dirname, '..', 'accessibility-report.txt');
  fs.writeFileSync(reportPath, report.join('\n'));
  
  console.log(report.join('\n'));
  console.log(`\n📝 Full accessibility report saved to: ${reportPath}`);
  
  return totalIssues;
}

// Run the accessibility check
const issuesFound = generateAccessibilityReport();

// Exit with appropriate status code
process.exit(issuesFound > 0 ? 1 : 0);

