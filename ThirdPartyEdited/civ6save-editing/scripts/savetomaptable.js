const fs = require("fs");
const stmj = require("../index.js").savetomapjson;
const verext = require("../index.js").verifyextension;

if (!(process.argv[2] && process.argv[3])) {
  console.log("# savetomaptable.js usage:");
  console.log("node savetomaptable.js [filename].Civ6save [htmlfilename]");
  console.log("# outputs an html file containing a table of tile data from a .Civ6Save file");
  process.exit();
}

const json = stmj(fs.readFileSync(process.argv[2]));

const headers = Object.keys(json.tiles[0]);
const header = headers.join("\n") + "\n";

const lines = json.tiles.map(o => {
  return Object.values(o).map(b => JSON.stringify(b)).join(" ") + "\n";
});

const file = `<table style="font-family: monospace;">${header}${lines.join('')}`;

fs.writeFileSync(verext(process.argv[3], ".html"), file);