module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        // Angola flag colors for institutional identity
        angola: {
          red: '#D71A28',      // Official red from Angola flag
          black: '#000000',    // Official black from Angola flag  
          gold: '#FFD700',     // Official gold/yellow from Angola flag
          'red-dark': '#B71C1C', // Darker red for hover states
          'red-light': '#EF5350', // Lighter red for backgrounds
          'gold-dark': '#FFC107', // Darker gold for accents
          'gold-light': '#FFF9C4', // Light gold for subtle backgrounds
        },
        primary: {
          50: '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
          950: '#1e1b4b',
        },
        secondary: {
          50: '#f0fdfa',
          100: '#ccfbf1',
          200: '#99f6e4',
          300: '#5eead4',
          400: '#2dd4bf',
          500: '#14b8a6',
          600: '#0d9488',
          700: '#0f766e',
          800: '#115e59',
          900: '#134e4a',
          950: '#042f2e',
        },
      },
      spacing: {
        '72': '18rem',
        '84': '21rem',
        '96': '24rem',
        '128': '32rem',
      },
      fontFamily: {
        sans: [
          '-apple-system', 
          'BlinkMacSystemFont', 
          '"Segoe UI"', 
          'Roboto', 
          '"Helvetica Neue"', 
          'Arial', 
          'sans-serif',
        ],
      },
      boxShadow: {
        soft: '0 3px 10px rgba(0, 0, 0, 0.08)',
        card: '0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)',
      },
      maxWidth: {
        'container-sm': '640px',
        'container-md': '768px',
        'container-lg': '1024px',
        'container-xl': '1280px',
      },
      zIndex: {
        '-10': '-10',
        '-1': '-1',
        '60': '60',
        '70': '70',
      },
      transitionDuration: {
        '400': '400ms',
      },
    },
  },
  plugins: [],
};