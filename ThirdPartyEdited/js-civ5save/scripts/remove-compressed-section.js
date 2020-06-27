/*
 * This script takes a .Civ5Save input file and saves it to a new .Civ5Save
 * file with the compressed section of the file removed. The resulting output
 * file is much smaller and can be useful for testing although it is no longer
 * a valid Civilization V save.
 */

const fs = require('fs');

function main() {
  if (process.argv.length !== 4) {
    console.log(`USAGE: ${process.argv[0]} ${process.argv[1]} INPUT_FILE OUTPUT_FILE`);
    process.exit(1);
  }

  let inputFilename = process.argv[2];
  let outputFilename = process.argv[3];

  let inputFileData = fs.readFileSync(inputFilename);

  const COMPRESSED_SECTION_MARKER = '0100789c';
  let compressedSectionStart = inputFileData.indexOf(COMPRESSED_SECTION_MARKER, 'hex');

  if (compressedSectionStart === -1) {
    console.log('ERROR: compressed section not found');
    process.exit(1);

  } else {
    fs.writeFileSync(outputFilename, inputFileData.slice(0, compressedSectionStart));
  }
}

main();
