import Civ5Save from '../../Civ5Save';

const fs = require('fs');
const path = require('path');

function getFileBlob(url) {
  return new Promise(function (resolve, reject) {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.responseType = 'blob';
    xhr.addEventListener('load', function() {
      resolve(xhr.response);
    });
    xhr.addEventListener('error', function() {
      reject(xhr.statusText);
    });
    xhr.send();
  });
}

test('Test creating Civ5Save instances from local save files', async () => {
  const resourceDir = path.join(__dirname, 'resources');
  let filenames = [];

  if (fs.existsSync(resourceDir)) {
    fs.readdirSync(resourceDir).forEach(filename => {
      if (filename.endsWith('.Civ5Save')) {
        filenames.push(filename);
      }
    });
  }

  for (let i = 0; i < filenames.length; i++) {
    let filename = filenames[i];
    try {
      let fileBlob = await getFileBlob(path.join(resourceDir, filename));
      await Civ5Save.fromFile(fileBlob);
    } catch (e) {
      e.message += ` (${filename})`;
      throw e;
    }
  }
}, 20000);
