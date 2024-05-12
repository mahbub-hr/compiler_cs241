const { readFileSync } = require("fs");

const run = async () => {
  const buffer = readFileSync("./new_hello.wasm");
  const module = await WebAssembly.compile(buffer);
  const instance = await WebAssembly.instantiate(module, {
	console: {
		log: console.log
	}
  });
 instance.exports.main();
};

run();