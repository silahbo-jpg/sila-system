#!/usr/bin/env node
/**
 * Script institucional: Varre todos os arquivos .tsx, detecta imports quebrados e sugere correções
 * Uso: node scripts/check-broken-imports.js > broken-imports.log
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '../src/pages');
const VALID_EXTENSIONS = ['.tsx', '.ts', '.jsx', '.js'];

/** Recursivamente coleta todos os arquivos com extensões válidas */
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

/** Tenta sugerir caminhos alternativos com base no nome do import */
function suggestAlternatives(baseDir, importName) {
  const candidates = getAllFiles(baseDir)
    .filter(f => f.toLowerCase().includes(importName.toLowerCase()))
    .map(f => path.relative(baseDir, f));
  return candidates;
}

function checkImportsInFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split(/\r?\n/);
  const importRegex = /import\s+[^'";]+['"](\.[^'"]+)['"]/g;
  let result = [];
  lines.forEach((line, idx) => {
    let match;
    importRegex.lastIndex = 0;
    while ((match = importRegex.exec(line)) !== null) {
      const relImport = match[1];
      let importPath = relImport;
      // Resolve relativo ao arquivo
      let absImportPath = path.resolve(path.dirname(filePath), importPath);
      let found = false;
      for (const ext of VALID_EXTENSIONS) {
        if (fs.existsSync(absImportPath + ext)) { found = true; break; }
        if (fs.existsSync(absImportPath + '/index' + ext)) { found = true; break; }
      }
      if (!found) {
        // Sugestão de caminhos similares
        const importBase = path.basename(importPath).replace(/\.[^.]+$/, '');
        const alternatives = suggestAlternatives(ROOT, importBase);
        result.push({
          file: filePath,
          line: idx + 1,
          import: relImport,
          alternatives
        });
      }
    }
  });
  return result;
}

function main() {
  const files = getAllFiles(ROOT);
  let brokenImports = [];
  files.forEach(f => {
    brokenImports = brokenImports.concat(checkImportsInFile(f));
  });
  if (brokenImports.length === 0) {
    console.log('Nenhum import quebrado encontrado.');
    return;
  }
  console.log('IMPORTS QUEBRADOS ENCONTRADOS:\n');
  brokenImports.forEach(entry => {
    console.log(`Arquivo: ${entry.file}`);
    console.log(`Linha: ${entry.line}`);
    console.log(`Import quebrado: ${entry.import}`);
    if (entry.alternatives.length) {
      console.log('Sugestões automáticas:');
      entry.alternatives.forEach(s => console.log('  - ' + s));
    } else {
      console.log('Nenhuma sugestão automática encontrada.');
    }
    console.log('---');
  });
}

main();

