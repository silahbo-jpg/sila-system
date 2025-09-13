# Frontend Reorganization Plan

This document outlines the new domain-driven structure for the frontend codebase.

## New Structure

```
src/
├── features/                    # Feature modules (domain-driven)
│   ├── auth/                   # Authentication module
│   │   ├── components/         # Auth-related components
│   │   ├── pages/              # Auth pages (login, register, etc.)
│   │   ├── hooks/              # Custom hooks for auth
│   │   └── types/              # TypeScript types/interfaces
│   │
│   ├── citizenship/            # Citizenship module
│   │   ├── api/                # API calls
│   │   ├── components/         # Reusable components
│   │   ├── pages/              # Page components
│   │   ├── hooks/              # Custom hooks
│   │   ├── types/              # TypeScript types
│   │   └── utils/              # Utility functions
│   │
│   ├── commercial/             # Commercial module
│   │   └── ...
│   │
│   └── shared/                 # Shared resources across domains
│       ├── components/         # Common UI components
│       ├── hooks/              # Shared hooks
│       └── utils/              # Shared utilities
│
├── app/                        # App configuration and routing
├── assets/                     # Static assets
└── styles/                     # Global styles
```

## Changes Made

1. **Domain Modules**
   - Each domain (auth, citizenship, commercial, etc.) is now self-contained
   - Related components, hooks, and utilities are colocated
   - Clear separation of concerns between domains

2. **Shared Resources**
   - Common UI components in `shared/components`
   - Shared hooks and utilities in their respective directories
   - TypeScript types defined close to where they're used

3. **API Layer**
   - API calls are colocated with their respective domains
   - Consistent API client configuration
   - Type-safe API responses

## How to Use the New Structure

1. **Adding a New Feature**
   - Create a new directory under `features/` for your domain
   - Follow the established pattern for components, pages, hooks, etc.
   - Keep related code together

2. **Sharing Code Between Domains**
   - For UI components: Add to `shared/components`
   - For utilities: Add to `shared/utils`
   - For hooks: Add to `shared/hooks`

3. **Importing**
   - Use absolute imports with `@/` prefix
   - Example: `import { Button } from '@/shared/components/ui/Button'`
   - Example: `import { useAuth } from '@/features/auth/hooks/useAuth'`

## Migration Steps

1. Run the reorganization script:
   ```bash
   node scripts/organize-by-domain.js
   ```

2. Review and fix any remaining import issues

3. Run the linter to catch any issues:
   ```bash
   npm run lint -- --fix
   ```

4. Test the application thoroughly to ensure everything works as expected

## Benefits

- **Better Organization**: Code is grouped by feature/domain
- **Improved Maintainability**: Easier to find and update related code
- **Enhanced Reusability**: Shared components are clearly identified
- **Clearer Boundaries**: Dependencies between domains are explicit
- **Easier Testing**: Related test files are colocated with their source

