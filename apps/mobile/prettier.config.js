module.exports = {
  printWidth: 80,                 // fuerza saltos de línea en className largos
  tabWidth: 4,
  singleQuote: true,
  jsxSingleQuote: false,          // JSX sigue con comillas dobles (más común)
  trailingComma: 'es5',
  bracketSpacing: true,
  bracketSameLine: false,         // <Button ...\n> en vez de <Button ...>
  semi: true,                     // ; siempre (opcional)
  arrowParens: 'always',

  plugins: [require.resolve('prettier-plugin-tailwindcss')],
  tailwindAttributes: ['className'],
};
