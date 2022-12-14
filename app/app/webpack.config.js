const path = require('path');
const CopyPlugin = require("copy-webpack-plugin");

module.exports = {
  mode: "development",
  entry: './src/index.tsx',
  output: {
    filename: 'index.js',
    path: path.resolve(__dirname, 'dist'),
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  plugins: [
    new CopyPlugin({
      patterns: [
        { from: "static", to: "./" }
      ],
    }),
  ],
};
