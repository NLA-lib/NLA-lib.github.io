import React, {useEffect,useRef,useState} from 'react';
import {createRoot} from 'react-dom/client';
import {flushSync} from 'react-dom';
import {Avatar,BaseStyles,Button,Heading,Label,SegmentedControl,Select,Spinner,Textarea} from '@primer/react';
import {ThemeProvider} from '@primer/react/next';
import '@primer/primitives/dist/css/base/size/size.css';
import '@primer/primitives/dist/css/base/typography/typography.css';
import '@primer/primitives/dist/css/base/motion/motion.css';
import '@primer/primitives/dist/css/functional/size/size.css';
import '@primer/primitives/dist/css/functional/size/size-coarse.css';
import '@primer/primitives/dist/css/functional/size/size-fine.css';
import '@primer/primitives/dist/css/functional/typography/typography.css';
import '@primer/primitives/dist/css/functional/themes/light.css';
import './discussion.css';
const categories=[['comment','Comment'],['suggestion','Suggestion'],['mathematical-error','Potential error'],['reference-request','Reference request'],['formalization-request','Formalization request'],['generalization','Generalization']];
function avatarFor(name){const initials=name.trim().split(/\s+/).slice(0,2).map(word=>word[0]).join('').toUpperCase().replace(/[<>&"']/g,'');return 'data:image/svg+xml,'+encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64"><rect width="64" height="64" rx="32" fill="#e8edf3"/><text x="32" y="39" text-anchor="middle" font-family="sans-serif" font-size="22" fill="#44546b">'+initials+'</text></svg>');}
function readDraft(key){try{return localStorage.getItem(key)||'';}catch{return '';}}
function saveDraft(key,value){try{value?localStorage.setItem(key,value):localStorage.removeItem(key);}catch{}}
function Markdown({html,typeset}){const ref=useRef(null);useEffect(()=>{if(ref.current)typeset(ref.current);},[html,typeset]);return <div ref={ref} className="comment-markdown" dangerouslySetInnerHTML={{__html:html}}/>;}
function Composer({id,api,typeset,replyTo=null,onCancel,onSubmitted}){
 const key='nla-discussion-draft:'+id+(replyTo?':reply:'+replyTo:'');
 const [text,setText]=useState(()=>readDraft(key)),[kind,setKind]=useState('comment'),[mode,setMode]=useState(0),[preview,setPreview]=useState(''),[busy,setBusy]=useState(false),[error,setError]=useState('');
 useEffect(()=>saveDraft(key,text),[key,text]);
 async function showMode(index){setMode(index);setError('');if(index===1)try{setPreview((await api('feedback/preview',{body:text})).html);}catch(problem){setError(problem.message);}}
 async function submit(event){event.preventDefault();if(!text.trim()||busy)return;setBusy(true);setError('');try{await api('objects/'+id+'/feedback',{kind,body:text,parent_id:replyTo});setText('');saveDraft(key,'');setMode(0);setKind('comment');await onSubmitted();}catch(problem){setError(problem.message);}finally{setBusy(false);}}
 return <form className="comment-composer" onSubmit={submit} aria-label={replyTo?'Reply to this thread':'Add to the discussion'}>
  <div className="composer-toolbar"><SegmentedControl aria-label="Message editor" size="small" onChange={showMode}><SegmentedControl.Button selected={mode===0}>Write</SegmentedControl.Button><SegmentedControl.Button selected={mode===1}>Preview</SegmentedControl.Button></SegmentedControl>
  {!replyTo&&<Select aria-label="Contribution type" size="small" value={kind} onChange={event=>setKind(event.target.value)}>{categories.map(([value,name])=><Select.Option key={value} value={value}>{name}</Select.Option>)}</Select>}</div>
  <div className="composer-input">{mode===0?<Textarea block autoSize resize="vertical" aria-label="Message · Markdown and LaTeX" placeholder={replyTo?'Write a reply…':'Ask a question or add to the discussion…'} value={text} onChange={event=>setText(event.target.value)} rows={4} minHeight={112}/>:<div className="comment-preview" aria-label="Message preview">{preview?<Markdown html={preview} typeset={typeset}/>:<p className="muted">Nothing to preview.</p>}</div>}</div>
  {error&&<p role="alert" className="comment-error">{error}</p>}
  <div className="composer-footer"><span className="composer-hint">Markdown and LaTeX supported</span><span className="composer-buttons">{replyTo&&<Button size="small" variant="invisible" onClick={onCancel}>Cancel</Button>}<Button type="submit" variant="primary" size="small" disabled={busy||!text.trim()}>{busy?'Posting…':replyTo?'Reply':'Comment'}</Button></span></div>
 </form>;
}
function Discussion({id,api,typeset,onCount,initialData,onReport}){
 const [messages,setMessages]=useState(initialData?.items||[]),[cursor,setCursor]=useState(initialData?.next_cursor||null),[total,setTotal]=useState(initialData?.count||0),[loading,setLoading]=useState(!initialData),[error,setError]=useState(''),[replyTo,setReplyTo]=useState(null),[replyRoot,setReplyRoot]=useState(null),[hidden,setHidden]=useState(new Set());
 async function refresh(){try{const data=await api('objects/'+id+'/feedback');setMessages(data.items);setCursor(data.next_cursor);setTotal(data.count);onCount(data.count);setError('');}catch(problem){setError(problem.message);}finally{setLoading(false);}}
 useEffect(()=>{if(initialData)onCount(initialData.count);else refresh();},[id]);
 const children=new Map();for(const item of messages){const parent=item.parent_id||'';if(!children.has(parent))children.set(parent,[]);children.get(parent).push(item);}
 const cancel=()=>{setReplyTo(null);setReplyRoot(null);};const posted=async()=>{await refresh();cancel();};
 function message(item,root,depth=0){const replies=children.get(item.id)||[],actor=item.attribution?.actor||{display_name:'Local researcher',url:'/explore/people/local-researcher/'},owner=item.attribution?.responsible_person;return <React.Fragment key={item.id}><article className={'comment-message'+(depth?' comment-reply':'')} id={'comment-'+item.id}>
  <div className="message-avatar"><Avatar src={avatarFor(actor.display_name)} size={28} alt=""/></div><div className="message-content"><header className="message-header"><a className="message-author" href={actor.url}>{actor.display_name}</a>{actor.kind==='bot'&&<><Label>Bot</Label><span className="bot-owner">for <a href={owner.url}>{owner.display_name}</a></span></>}<time dateTime={item.created_at}>{new Date(item.created_at).toLocaleString(undefined,{month:'short',day:'numeric',hour:'numeric',minute:'2-digit'})}</time>{item.kind!=='comment'&&<Label>{categories.find(([key])=>key===item.kind)?.[1]||item.kind}</Label>}</header>
  <Markdown html={item.html} typeset={typeset}/><div className="message-actions"><Button size="small" variant="invisible" onClick={()=>{setReplyTo(item.id);setReplyRoot(root);}}>Reply</Button>{onReport&&<Button size="small" variant="invisible" onClick={()=>onReport(item.id)}>Report</Button>}{replies.length>0&&<Button size="small" variant="invisible" onClick={()=>setHidden(old=>{const next=new Set(old);next.has(item.id)?next.delete(item.id):next.add(item.id);return next;})}>{hidden.has(item.id)?'Show':'Hide'} replies ({replies.length})</Button>}</div></div></article>{!hidden.has(item.id)&&replies.map(reply=>message(reply,root,depth+1))}</React.Fragment>;}
 return <ThemeProvider colorMode="day" dayScheme="light"><BaseStyles className="primer-discussion"><div className="discussion-heading"><Heading as="h2">Discussion</Heading><span className="comment-total">{total}</span></div>
 {loading&&<div className="discussion-loading"><Spinner size="small"/><span>Loading discussion…</span></div>}{error&&<p role="alert" className="comment-error">{error}</p>}{!loading&&!messages.length&&!error&&<p className="discussion-empty">No comments yet. Start the conversation.</p>}
 <div className="comment-threads">{(children.get('')||[]).map(root=><section className="comment-thread" key={root.id} aria-label="Discussion thread">{message(root,root.id)}{replyRoot===root.id&&<div className="thread-composer"><Composer key={replyTo} id={id} api={api} typeset={typeset} replyTo={replyTo} onCancel={cancel} onSubmitted={posted}/></div>}</section>)}</div>
 {cursor&&<Button onClick={async()=>{try{const data=await api('objects/'+id+'/feedback?cursor='+encodeURIComponent(cursor));setMessages(old=>[...old,...data.items]);setCursor(data.next_cursor);setTotal(data.count);}catch(problem){setError(problem.message);}}}>Load more comments</Button>}
 {!replyTo&&<section className="new-comment"><Heading as="h3">Add a comment</Heading><Composer id={id} api={api} typeset={typeset} onSubmitted={posted}/></section>}</BaseStyles></ThemeProvider>;
}
export async function mountDiscussion(host,options){
 const shadow=host.attachShadow({mode:'open'});
 const loading=document.createElement('p');loading.textContent='Loading discussion…';loading.setAttribute('role','status');shadow.append(loading);
 const styles=['/explore/editor-assets/discussion.css','/explore/vendor/katex/katex.min.css'].map(href=>new Promise((resolve,reject)=>{const link=document.createElement('link');link.rel='stylesheet';link.href=href+'?v='+(options.assetVersion||'');link.onload=resolve;link.onerror=()=>reject(new Error('Could not load discussion styles. Reload to retry.'));shadow.append(link);}));
 const [initialData]=await Promise.all([options.api('objects/'+options.id+'/feedback'),...styles]);
 const target=document.createElement('div');target.dataset.colorMode='light';target.dataset.lightTheme='light';target.style.visibility='hidden';shadow.append(target);
 const root=createRoot(target);flushSync(()=>root.render(<Discussion {...options} initialData={initialData}/>));
 options.typeset(target);
 await document.fonts.ready;
 loading.remove();target.style.visibility='';
 return()=>root.unmount();
}
