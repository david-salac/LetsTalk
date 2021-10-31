module.exports = {
    devServer: {
        proxy: {
            '^/api': {
                target: 'http://web_service:8081',
                changeOrigin: true,
                logLevel: 'debug',
                pathRewrite: {
                    '^/api': '/api'
                }
            }
        }
    },

}