/* Optional hosted account controls. Local editing has its own session adapter. */
'use strict';
(async()=>{
 if(['127.0.0.1','localhost'].includes(location.hostname))return;
 const footer=document.querySelector('.site-footer-links') || document.querySelector('footer');if(!footer)return;
 let config;
 try{const response=await fetch('/explore/collaboration-config.json',{cache:'no-cache'});if(!response.ok)return;config=await response.json();}catch{return;}
 if(!config.enabled)return;
 const origin=new URL(config.apiOrigin);
 if(origin.protocol!=='https:'||origin.origin!=='https://api.nla-lib.org')return;
 const login='/auth/login?return_to='+encodeURIComponent(location.pathname+location.search+location.hash);
 const host=document.createElement('span');host.className='collaboration-account';
 const link=(label,path)=>{const item=document.createElement('a');item.textContent=label;item.href=origin.origin+path;return item;};
 try{
  const response=await fetch(origin.origin+'/me',{credentials:'include',cache:'no-store',signal:AbortSignal.timeout(6000)});
  if(response.status===401){host.append(link('Sign in with ORCID',login));}
  else{
   const me=await response.json();if(!response.ok)throw new Error('Sign-in unavailable');
   host.append(link(me.profile.display_name+' · My profile','/account'));
   const logout=document.createElement('button');logout.type='button';logout.textContent='Sign out';
   logout.addEventListener('click',async()=>{logout.disabled=true;try{const result=await fetch(origin.origin+'/auth/logout',{method:'POST',credentials:'include',headers:{'Content-Type':'application/json','X-CSRF-Token':me.csrf_token},body:'{}'});if(!result.ok)throw new Error();host.replaceChildren(link('Sign in with ORCID',login));}catch{logout.disabled=false;logout.textContent='Retry sign out';}});
   host.append(logout);
  }
 }catch{host.append(link('Sign-in service','/account'));}
 footer.append(host);
})();
