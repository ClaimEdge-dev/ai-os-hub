import { mkdir, open, readFile, writeFile, link, unlink } from 'node:fs/promises';
import { join } from 'node:path';
import { createHash, randomUUID } from 'node:crypto';
import { PolicyError } from './policy.mjs';
const sleep=(ms)=>new Promise(r=>setTimeout(r,ms));
export class LocalFixtureStore {
  // Only for a single shared local filesystem. NOT durable across Site instances.
  constructor(directory){this.directory=directory;}
  filename(project,key){const h=createHash('sha256').update(`${project}\0${key}`).digest('hex');return join(this.directory,h+'.json');}
  async read(project,key){try{return JSON.parse(await readFile(this.filename(project,key),'utf8'));}catch(e){if(e?.code==='ENOENT')return null;throw e;}}
  async withRequestLock(project,key,callback){
    await mkdir(this.directory,{recursive:true});
    const lockPath=this.filename(project,key)+'.lock';
    let handle;
    for(let attempt=0;attempt<50;attempt++){
      try{handle=await open(lockPath,'wx',0o600);break;}
      catch(e){if(e.code!=='EEXIST')throw e;await sleep(20);}
    }
    if(!handle)throw new PolicyError('LOCK_TIMEOUT','Request currently owned by another worker');
    try{return await callback();}finally{await handle.close();await unlink(lockPath);}
  }
  async put(project,key,receipt){
    const dest=this.filename(project,key),tmp=dest+'.'+randomUUID()+'.tmp';
    await writeFile(tmp,JSON.stringify(receipt)+'\n',{flag:'wx',mode:0o600});
    try{await link(tmp,dest);}catch(e){if(e.code==='EEXIST')throw new PolicyError('RECEIPT_CONFLICT','Receipt already exists');throw e;}finally{await unlink(tmp);}
    return this.read(project,key);
  }
}
