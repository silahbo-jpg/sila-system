const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Define the domain structure
const DOMAIN_STRUCTURE = {
  'citizenship': {
    'api': ['citizenshipApi.ts'],
    'components': ['CitizenRequestForm.tsx', 'CitizenRequestList.tsx', 'CitizenRequestDetail.tsx'],
    'pages': ['CitizenRequestsPage.tsx', 'CitizenRequestDetailPage.tsx'],
    'types': ['index.ts'],
    'hooks': ['useCitizenRequests.ts', 'useCitizenRequest.ts'],
    'utils': ['citizenshipUtils.ts'],
  },
  'commercial': {
    'api': ['commercialApi.ts'],
    'components': ['BusinessForm.tsx', 'LicenseList.tsx', 'PaymentForm.tsx'],
    'pages': ['BusinessRegistrationPage.tsx', 'LicenseManagementPage.tsx'],
    'types': ['index.ts'],
  },
  'sanitation': {
    'api': ['sanitationApi.ts'],
    'components': ['InspectionForm.tsx', 'ReportList.tsx'],
    'pages': ['InspectionsPage.tsx', 'ReportsPage.tsx'],
  },
  'auth': {
    'components': ['LoginForm.tsx', 'RegisterForm.tsx', 'PasswordResetForm.tsx'],
    'pages': ['LoginPage.tsx', 'RegisterPage.tsx', 'ForgotPasswordPage.tsx'],
    'hooks': ['useAuth.ts', 'usePermissions.ts'],
  },
  'shared': {
    'components': ['ui/Button.tsx', 'ui/Input.tsx', 'ui/Table.tsx', 'layout/Header.tsx', 'layout/Sidebar.tsx'],
    'hooks': ['useForm.ts', 'useToast.ts'],
    'utils': ['api.ts', 'formatters.ts', 'validators.ts'],
  },
};

const SOURCE_DIR = path.join(__dirname, '..', 'src');
const TARGET_DIR = path.join(__dirname, '..', 'src', 'features');

// Create directory if it doesn't exist
function ensureDirectoryExistence(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

// Move file from source to destination
function moveFile(source, destination) {
  try {
    ensureDirectoryExistence(path.dirname(destination));
    
    // Check if source file exists
    if (!fs.existsSync(source)) {
      console.warn(`Source file does not exist: ${source}`);
      return false;
    }
    
    // Check if destination file already exists
    if (fs.existsSync(destination)) {
      console.warn(`Destination file already exists: ${destination}`);
      return false;
    }
    
    // Create the target directory if it doesn't exist
    ensureDirectoryExistence(path.dirname(destination));
    
    // Move the file
    fs.renameSync(source, destination);
    console.log(`Moved: ${source} -> ${destination}`);
    return true;
  } catch (error) {
    console.error(`Error moving file ${source} to ${destination}:`, error);
    return false;
  }
}

// Update import paths in a file
function updateImports(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Update relative imports
    content = content.replace(
      /from ['"](?:\.\.\/)*components\/([^'"]+)['"]/g,
      (match, p1) => {
        // Check if this is a shared component
        if (p1.startsWith('ui/') || p1.startsWith('layout/')) {
          return `from '@/shared/components/${p1}'`;
        }
        return match;
      }
    );
    
    // Update API imports
    content = content.replace(
      /from ['"](?:\.\.\/)*api\/([^'"]+)['"]/g,
      (match, p1) => {
        // Try to find which domain this API belongs to
        const domain = Object.keys(DOMAIN_STRUCTURE).find(domain => 
          DOMAIN_STRUCTURE[domain].api?.includes(p1)
        );
        return domain ? `from '@/features/${domain}/api/${p1}'` : match;
      }
    );
    
    // Update hooks imports
    content = content.replace(
      /from ['"](?:\.\.\/)*hooks\/([^'"]+)['"]/g,
      (match, p1) => {
        // Check if this is a shared hook
        if (['useForm', 'useToast', 'useApi'].includes(p1.replace('.ts', ''))) {
          return `from '@/shared/hooks/${p1}'`;
        }
        return match;
      }
    );
    
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Updated imports in: ${filePath}`);
    return true;
  } catch (error) {
    console.error(`Error updating imports in ${filePath}:`, error);
    return false;
  }
}

// Main function to organize files by domain
function organizeByDomain() {
  console.log('Starting to organize files by domain...');
  
  // Create the features directory if it doesn't exist
  ensureDirectoryExistence(TARGET_DIR);
  
  // Process each domain
  Object.entries(DOMAIN_STRUCTURE).forEach(([domain, structure]) => {
    console.log(`\nProcessing domain: ${domain}`);
    
    // Process each category in the domain
    Object.entries(structure).forEach(([category, files]) => {
      files.forEach(file => {
        // Skip if it's a directory pattern (like ui/Button)
        if (file.includes('/')) {
          return;
        }
        
        let sourcePath, targetPath;
        
        // Special handling for different file categories
        if (category === 'components' || category === 'pages') {
          // Look in components or pages directory
          sourcePath = path.join(SOURCE_DIR, category, file);
          targetPath = path.join(TARGET_DIR, domain, category, file);
        } else {
          // Look in the root src directory
          sourcePath = path.join(SOURCE_DIR, file);
          targetPath = path.join(TARGET_DIR, domain, category, file);
        }
        
        // Move the file if it exists
        if (fs.existsSync(sourcePath)) {
          if (moveFile(sourcePath, targetPath)) {
            // Update imports in the moved file
            updateImports(targetPath);
          }
        }
      });
    });
  });
  
  console.log('\nReorganization complete!');
  console.log('Please review the changes and update any remaining import paths manually.');
  console.log('You may need to run: npm run lint -- --fix');
}

// Run the script
organizeByDomain();

