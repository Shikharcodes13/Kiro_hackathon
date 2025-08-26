/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'porsche-red': '#D5001C',
        'porsche-black': '#000000',
        'porsche-gray': '#F5F5F5',
        'porsche-dark-gray': '#333333',
        'autoagent-primary': '#1E40AF',
        'autoagent-secondary': '#3B82F6',
        'autoagent-accent': '#10B981',
      },
      fontFamily: {
        'porsche': ['Helvetica Neue', 'Arial', 'sans-serif'],
        'display': ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.6s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'typing': 'typing 3.5s steps(40, end), blink-caret .75s step-end infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        typing: {
          'from': { width: '0' },
          'to': { width: '100%' }
        },
        'blink-caret': {
          'from, to': { 'border-color': 'transparent' },
          '50%': { 'border-color': '#3B82F6' }
        }
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'hero-pattern': "linear-gradient(135deg, rgba(30, 64, 175, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%)",
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}