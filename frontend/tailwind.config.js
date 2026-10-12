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
        void: '#0B0F17',
        surface: '#111827',
        surfaceElevated: 'rgba(17, 24, 39, 0.75)',
        borderDark: '#1E293B',
        cyberCyan: '#06B6D4',
        cyberBlue: '#3B82F6',
        cyberPurple: '#8B5CF6',
        cyberEmerald: '#10B981',
        cyberAmber: '#F59E0B',
        cyberRed: '#EF4444',
        cyberPink: '#EC4899',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(6, 182, 212, 0.2), inset 0 0 5px rgba(6, 182, 212, 0.1)' },
          '100%': { boxShadow: '0 0 20px rgba(6, 182, 212, 0.6), inset 0 0 10px rgba(6, 182, 212, 0.3)' },
        }
      }
    },
  },
  plugins: [],
}
