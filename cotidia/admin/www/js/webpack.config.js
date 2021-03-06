/* eslint-env node */
/* eslint-disable object-shorthand */

const path = require('path')
const webpack = require('webpack')

module.exports = function webpackBootstrap (env) {
  env = env || 'production'

  process.env.NODE_ENV = env
  process.env.BABEL_ENV = env

  const plugins = [
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify(env),
    }),
  ]

  const devToolSettings = {
    'development': 'cheap-module-source-map',
    'production': 'source-map',
  }

  return {
    entry: [
      path.resolve(__dirname, 'src', 'index.js'),
    ],
    output: {
      path: path.resolve(__dirname, '..', '..', 'static', 'js'),
      filename: 'admin.js',
    },
    plugins: plugins,
    module: {
      rules: [
        {
          test: /\.js$/,
          include: path.resolve(__dirname, 'src'),
          use: [{
            loader: 'babel-loader',
          }],
        },
        {
          test: /\.css$/,
          use: [
            { loader: 'style-loader' },
            { loader: 'css-loader' },
          ],
        },
      ],

      // see https://github.com/webpack/webpack/issues/198#issuecomment-104688430
      noParse: [ /moment.js/ ],
    },
    devtool: devToolSettings[env] || false,
    devServer: {
      contentBase: path.resolve(__dirname, 'public'),
      inline: true,
      host: '0.0.0.0',
      port: 3300,
      historyApiFallback: true,
    },
  }
}
