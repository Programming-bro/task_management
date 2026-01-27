/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./templates/**/*.html/', // Template in main
    './**/templates/**/*.html/' // Template inside apps
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

