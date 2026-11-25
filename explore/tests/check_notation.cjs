// Use the exact browser math engine, without introducing another npm dependency.
const {spawnSync}=require('node:child_process');
const {resolve}=require('node:path');
const katex=require('../../vendor/katex/katex.min.js');
const result=spawnSync('python3',['check_notation.py','--expressions'],{cwd:resolve(__dirname,'..'),encoding:'utf8',maxBuffer:20*1024*1024});
if(result.status!==0){process.stderr.write(result.stderr);process.exit(result.status||1);}
const {expressions,issues}=JSON.parse(result.stdout);const errors=issues.filter(issue=>issue.severity==='error');
for(const item of expressions){try{katex.renderToString(item.tex,{displayMode:item.display,throwOnError:true,trust:false,strict:'ignore',maxExpand:1000,maxSize:20});}catch(error){errors.push({...item,message:error.message});}}
for(const error of errors)console.error(`${error.path}:${error.line}: ${error.message}`);
console.log(`${expressions.length} authored equations checked with KaTeX; ${errors.length} errors.`);
process.exit(errors.length?1:0);
