const path = require('path');

const config = {
  entry: './src/Civ5Save.js',
  output: {
    filename: 'civ5save.js',
    // library and libraryTarget are necessary so this can be imported as a module
    library: 'Civ5Save',
    libraryTarget: 'umd',
    path: path.resolve(__dirname, 'dist')
  },
};

module.exports = (env, argv) => {
  if (argv.mode === 'production') {
    config.output.filename = 'civ5save.min.js';
  }

  return config;
};
