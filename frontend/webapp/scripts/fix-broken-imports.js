#!/usr/bin/env node
/**
 * Script institucional: Corrige automaticamente imports quebrados sugeridos pelo check-broken-imports.js
 * Uso: node scripts/fix-broken-imports.js
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '../src/pages');
const VALID_EXTENSIONS = ['.tsx', '.ts', '.jsx', '.js'];

function getAllFiles(dir, files = []) {
  fs.readdirSync(dir).forEach(file => {
    const fullPath = path.join(dir, file);
    if (fs.statSync(fullPath).isDirectory()) {
      getAllFiles(fullPath, files);
    } else if (VALID_EXTENSIONS.includes(path.extname(fullPath))) {
      files.push(fullPath);
    }
  });
  return files;
}

function suggestAlternatives(baseDir, importName) {
  const candidates = getAllFiles(baseDir)
    .filter(f => f.toLowerCase().includes(importName.toLowerCase()))
    .map(f => path.relative(baseDir, f));
  return candidates;
}

function fixImportsInFile(filePath) {
  let content = fs.readFileSync(filePath, 'utf-8');
  let changed = false;
  const importRegex = /import\s+([^'";]+)['"](\.[^'"]+)['"]/g;
  let match;
  let matches = [];
  while ((match = importRegex.exec(content)) !== null) {
    matches.push({
      full: match[0],
      varPart: match[1],
      relImport: match[2],
      index: match.index
    });
  }
  for (const m of matches) {
    let absImportPath = path.resolve(path.dirname(filePath), m.relImport);
    let found = false;
    for (const ext of VALID_EXTENSIONS) {
      if (fs.existsSync(absImportPath + ext)) { found = true; break; }
      if (fs.existsSync(absImportPath + '/index' + ext)) { found = true; break; }
    }
    if (!found) {
      const importBase = path.basename(m.relImport).replace(/\.[^.]+$/, '');
      const alternatives = suggestAlternatives(ROOT, importBase);
      if (alternatives.length > 0) {
        // Escolhe a primeira sugestão
        const newImportRel = './' + path.relative(path.dirname(filePath), path.join(ROOT, alternatives[0])).replace(/\\/g, '/');
        const newImportLine = `import ${m.varPart}"${newImportRel.replace(/\.[^.]+$/, '')}"`;
        content = content.replace(m.full, newImportLine);
        changed = true;
        console.log(`Corrigido em ${filePath}: ${m.full} => ${newImportLine}`);
      }
    }
  }
  if (changed) {
    fs.writeFileSync(filePath, content, 'utf-8');
  }
}

function main() {
  const files = getAllFiles(ROOT);
  files.forEach(fixImportsInFile);
  console.log('Correção automática concluída. Revise os arquivos alterados antes de commitar.');
}

main();

