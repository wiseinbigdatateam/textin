const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
	publicPath: 'http://0.0.0.0:8081/',
  outputDir: './dist/',

  chainWebpack: config => {
    config.optimization.splitChunks(false)

    config.plugin('BundleTracker').use(BundleTracker, [{filename: './webpack-stats.json'}])

    config.devServer.host('0.0.0.0').port(8081).https(false).headers({"Access-Control-Allow-Origin":["\*"]})
  },

  pages: {
    index: 'src/main.js'
  }
}
