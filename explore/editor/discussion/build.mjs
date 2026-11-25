import {build} from 'esbuild';
import {fileURLToPath} from 'node:url';
import {dirname, resolve} from 'node:path';
const root = dirname(fileURLToPath(import.meta.url));
await build({absWorkingDir:root,entryPoints:['discussion.jsx'],bundle:true,minify:true,format:'esm',target:['es2022'],outfile:resolve(root,'../discussion.js'),define:{'process.env.NODE_ENV':'"production"'},legalComments:'linked',jsx:'automatic'});
