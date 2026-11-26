/* Definition previews for explicit mathematical links; never guess a term's meaning. */
const cache=new Map();
let owner=null,box=null,opening,closing,request=0;
const element=(tag,text)=>{const node=document.createElement(tag);if(text!==undefined)node.textContent=text;return node;};
function destination(link){
  if(!link?.closest('main'))return null;
  const url=new URL(link.href,location.href);
  if(url.origin!==location.origin)return null;
  if(link.matches('.lean-definition-link'))return url;
  if(!link.closest('.explorer-statement-label,.page-heading,.statement-expanded-activity') && /^\/explore\/(statements|library\/declarations)\//.test(url.pathname))return url;
  return null;
}
function close(){
  clearTimeout(opening);clearTimeout(closing);request++;
  if(owner){owner.removeAttribute('aria-controls');owner.removeAttribute('aria-expanded');if(owner.dataset.definitionTitle){owner.title=owner.dataset.definitionTitle;delete owner.dataset.definitionTitle;}}
  box?.remove();box=null;owner=null;
}
function scheduleClose(){clearTimeout(opening);clearTimeout(closing);closing=setTimeout(()=>{if(!box?.matches(':hover')&&!box?.contains(document.activeElement)&&document.activeElement!==owner)close();},160);}
function position(){
  if(!box||!owner)return;
  const rect=owner.getBoundingClientRect(),width=box.offsetWidth,height=box.offsetHeight;
  const left=Math.max(12,Math.min(rect.left,innerWidth-width-12));
  const below=rect.bottom+8,above=rect.top-height-8;
  box.style.left=left+'px';box.style.top=Math.max(12,below+height<innerHeight-12?below:above>=12?above:innerHeight-height-12)+'px';
}
function safeCopy(source,budget={left:10000}){
  if(budget.left<=0)return document.createTextNode('');
  if(source.nodeType===Node.TEXT_NODE){const text=source.textContent.slice(0,budget.left);budget.left-=text.length;return document.createTextNode(text);}
  if(source.nodeType!==Node.ELEMENT_NODE)return document.createTextNode('');
  if(source.matches('script,style,iframe,object,form,button,.theorem-reaction-slot,.theorem-kind,.editor-status,.statement-verification'))return document.createTextNode('');
  const allowed=new Set(['P','UL','OL','LI','SPAN','STRONG','EM','CODE','PRE','A','BR','BLOCKQUOTE','CITE','H2','H3']);
  const node=allowed.has(source.tagName)?element(source.tagName.toLowerCase()):document.createDocumentFragment();
  if(source.matches('.math')){node.className='math'+(source.classList.contains('display')?' display':'');}
  if(source.tagName==='A'){
    const href=new URL(source.getAttribute('href')||'',source.baseURI);
    if(['https:','http:'].includes(href.protocol)){node.href=href.href;node.rel='noopener noreferrer';}
  }
  for(const child of source.childNodes)node.append(safeCopy(child,budget));
  return node;
}
async function read(url){
  const key=url.href;
  if(!cache.has(key)){
    const pending=(async()=>{
      const response=await fetch(url.href,{credentials:'same-origin'});
      if(!response.ok)throw new Error('Definition preview unavailable.');
      const source=await response.text();if(source.length>2000000)throw new Error('Open the definition to read its full text.');
      const doc=new DOMParser().parseFromString(source,'text/html');
      const base=doc.createElement('base');base.href=url.href;doc.head.prepend(base);
      const main=doc.querySelector('main');if(!main)throw new Error('Definition preview unavailable.');
      let target=null;if(url.hash)try{target=doc.getElementById(decodeURIComponent(url.hash.slice(1)));}catch{}
      const statement=target?.closest('.explorer-card')||target||main.querySelector('.theorem-statement');
      const readable=statement || [...main.children].find(node=>node.matches('p:not(.eyebrow)')&&!node.querySelector('a'));
      const formal=main.querySelector('.theorem-formal pre')||main.querySelector('pre');
      if(!readable&&!formal)throw new Error('Open the definition to read its full text.');
      return {title:main.querySelector('h1')?.textContent||'Definition',readable,formal};
    })();
    cache.set(key,pending);pending.catch(()=>cache.delete(key));
    if(cache.size>40)cache.delete(cache.keys().next().value);
  }
  return cache.get(key);
}
function typeset(container){
  if(!window.katex)return;
  for(const math of container.querySelectorAll('.math'))window.katex.render(math.textContent,math,{displayMode:math.classList.contains('display'),throwOnError:false,trust:false,maxExpand:1000,maxSize:20});
}
async function open(link,url){
  if(owner===link&&box){clearTimeout(closing);return;}
  close();owner=link;const serial=++request;
  box=element('aside');box.className='definition-preview';box.id='definition-preview';box.setAttribute('role','dialog');box.setAttribute('aria-label','Definition preview');
  const heading=element('div');heading.className='definition-preview-heading';const title=element('h3','Definition');
  const dismiss=element('button','×');dismiss.type='button';dismiss.className='definition-preview-close';dismiss.setAttribute('aria-label','Close definition preview');dismiss.addEventListener('click',close);heading.append(title,dismiss);
  const content=element('div','Loading definition…');content.className='definition-preview-content';
  const footer=element('p');footer.className='definition-preview-footer';const full=element('a','Open definition');full.href=url.href;footer.append(full);box.append(heading,content,footer);
  if(link.title){link.dataset.definitionTitle=link.title;link.removeAttribute('title');}
  link.setAttribute('aria-controls',box.id);link.setAttribute('aria-expanded','true');
  box.addEventListener('pointerenter',()=>clearTimeout(closing));box.addEventListener('pointerleave',scheduleClose);box.addEventListener('focusout',scheduleClose);
  document.body.append(box);position();
  try{
    const data=await read(url);if(serial!==request||owner!==link)return;
    title.textContent=data.title;content.replaceChildren();
    if(data.readable)content.append(safeCopy(data.readable));
    if(data.formal&&!data.readable?.contains(data.formal))content.append(safeCopy(data.formal,{left:6000}));
    typeset(content);position();
  }catch(error){if(serial===request&&box){content.textContent=error.message;position();}}
}
function schedule(link){
  const url=destination(link);if(!url)return;
  clearTimeout(opening);clearTimeout(closing);opening=setTimeout(()=>open(link,url),180);
}
document.addEventListener('pointerover',event=>{if(event.pointerType==='touch')return;const link=event.target.closest('a');if(link&&!link.contains(event.relatedTarget))schedule(link);});
document.addEventListener('pointerout',event=>{const link=event.target.closest('a');if(link&&link===owner&&!link.contains(event.relatedTarget))scheduleClose();else if(destination(link))clearTimeout(opening);});
document.addEventListener('focusin',event=>{if(event.target.matches('a')){const url=destination(event.target);if(url)open(event.target,url);}});
document.addEventListener('focusout',event=>{if(event.target===owner)scheduleClose();});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&box){event.preventDefault();close();}});
function reposition(){if(!owner||!box)return;const rect=owner.getBoundingClientRect();if(rect.bottom<0||rect.top>innerHeight)close();else position();}
window.addEventListener('resize',reposition);window.addEventListener('scroll',event=>{if(box&&!box.contains(event.target))reposition();},true);
