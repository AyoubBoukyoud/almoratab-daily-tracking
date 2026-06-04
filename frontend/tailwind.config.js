/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          gold: '#C9982A',
          'gold-light': '#E8BE5A',
          'gold-pale': '#F5EDD4',
          teal: '#1A4D4A',
          'teal-mid': '#246460',
          'teal-light': '#2E7D79',
          cream: '#FAF6EE',
          dark: '#0F2A28',
          text: '#1C2B2A',
          muted: '#6B8280',
          border: '#D4C5A0',
        }
      },
      fontFamily: {
        cairo: ['Cairo', 'sans-serif'],
        playfair: ['Playfair Display', 'serif'],
        lato: ['Lato', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
