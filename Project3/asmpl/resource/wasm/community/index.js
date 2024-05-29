const { readFileSync } = require("fs");

const run = async () => {
  const buffer = readFileSync("./test.wasm");
  const module = await WebAssembly.compile(buffer);
  const instance = await WebAssembly.instantiate(module, {
	console: {
		log: console.log
	}
  });
 instance.exports.main();
};

run();