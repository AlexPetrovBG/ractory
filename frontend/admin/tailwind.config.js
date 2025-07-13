/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Primary brand color
        'primary': {
          DEFAULT: '#1951e3',
          '50': '#f4f6fe',
          '100': '#e8edfd',
          '200': '#d1dbfb',
          '300': '#aabef7',
          '400': '#799af1',
          '500': '#5476eb',
          '600': '#2e52e5',
          '700': '#1951e3',
          '800': '#1541b8',
          '900': '#143896',
          '950': '#0e234f',
        },
        // Dark mode colors
        'coal': {
          '50': '#f7f7f8',
          '100': '#edeef0',
          '200': '#d7d9dd',
          '300': '#b4b9c2',
          '400': '#8a92a2',
          '500': '#6d7686',
          '600': '#57606f',
          '700': '#4a535e',
          '800': '#393e48',
          '900': '#2b3138',
          '950': '#070f1a',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif']
      },
      borderRadius: {
        'sm': '0.25rem',
        DEFAULT: '0.475rem',
        'md': '0.5rem',
        'lg': '0.75rem',
        'xl': '1rem',
      },
      boxShadow: {
        'sm': '0 0.1rem 0.7rem 0 rgba(0, 0, 0, 0.05)',
        DEFAULT: '0 0.5rem 1.5rem 0.5rem rgba(0, 0, 0, 0.075)',
        'md': '0 0.5rem 2rem 1rem rgba(0, 0, 0, 0.1)',
        'lg': '0 1rem 3rem 1.5rem rgba(0, 0, 0, 0.1)',
      },
      transitionProperty: {
        'width': 'width',
        'height': 'height',
        'margin': 'margin',
      }
    },
  },
  plugins: [],
} 