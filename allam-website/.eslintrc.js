module.exports = {
  parser: '@typescript-eslint/parser',
  extends: [
    'plugin:react/recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:prettier/recommended',
    'plugin:tailwindcss/recommended',
  ],
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },
  plugins: ['react', '@typescript-eslint', 'tailwindcss'],
  rules: {
    'tailwindcss/class-order': 'error',
    'react/react-in-jsx-scope': 'off', // Not needed with React 17+
    'prettier/prettier': 'error', // Show prettier errors as ESLint errors
  },
  settings: {
    react: {
      version: 'detect', // Automatically detect the react version
    },
  },
}
