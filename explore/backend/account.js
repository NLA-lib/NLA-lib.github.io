'use strict';
(async()=>{
 const host=document.getElementById('account');
 const node=(tag,text)=>{const element=document.createElement(tag);if(text!==undefined)element.textContent=text;return element;};
 async function read(path,payload,csrf){const response=await fetch(path,payload===undefined?{credentials:'same-origin',cache:'no-store'}:{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify(payload)});const data=await response.json();if(!response.ok)throw Object.assign(new Error(data.error||'Request failed.'),{status:response.status});return data;}
 try{
  const me=await read('/me');host.replaceChildren();host.removeAttribute('role');
  const identity=node('p','Signed in with ORCID '+me.profile.orcid+'. New accounts are contributors; sign-in does not grant editor trust.');host.append(identity);
  const form=node('form'),inputs={};
  for(const [key,label] of [['display_name','Display name'],['affiliation','Affiliation'],['bio','About you'],['interests','Research interests'],['website','Website · HTTPS']]){const wrapper=node('label',label),input=node(key==='bio'?'textarea':'input');input.name=key;input.value=me.profile[key]||'';if(key==='bio')input.rows=5;wrapper.append(input);form.append(wrapper);inputs[key]=input;}
  const save=node('button','Save profile');save.type='submit';form.append(save);const status=node('p');status.setAttribute('role','status');form.append(status);host.append(form);
  form.addEventListener('submit',async event=>{event.preventDefault();save.disabled=true;try{await read('/me/profile',Object.fromEntries(Object.entries(inputs).map(([key,input])=>[key,input.value])),me.csrf_token);status.textContent='Profile saved.';}catch(error){status.textContent=error.message;}finally{save.disabled=false;}});
  const profile=node('a','View public profile');profile.href=me.profile.url;host.append(profile);
  const logout=node('button','Sign out');logout.type='button';logout.className='text-button';logout.addEventListener('click',async()=>{try{await read('/auth/logout',{},me.csrf_token);location.reload();}catch(error){status.textContent=error.message;}});host.append(logout);
 }catch(error){host.replaceChildren(node('p',error.status===401?'Sign in to create or edit your researcher profile.':error.message));const link=node('a','Sign in with ORCID');link.href='/auth/login';host.append(link);}
})();
