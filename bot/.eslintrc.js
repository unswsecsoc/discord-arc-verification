module.exports = {
  root: true,
  env: {
    node: true,
  },
  parser: "@typescript-eslint/parser",
  extends: [
    "plugin:@typescript-eslint/recommended"
  ],
  rules: {
    indent: ["error", 4],
    '@typescript-eslint/camelcase': 'off'
  }
}