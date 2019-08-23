module.exports = {
  publicPath: '/geobrowser/',
  devServer: {
    port: 8081,
  },
  configureWebpack: {
    module: {
      rules: [
        {
          test: /\.(md|txt)$/,
          use: 'raw-loader',
        },
      ],
    },
  },
};
