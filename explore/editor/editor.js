'use strict';
(async () => {
  const assetVersion = document.currentScript ? new URL(document.currentScript.src).searchParams.get('v') || '' : '';
  const hosted = !['127.0.0.1', 'localhost'].includes(location.hostname);
  let apiRoot = '/explore/editor-api/', role = null, publishing = false;
  if (hosted) {
    try {
      const response = await fetch('/explore/collaboration-config.json', {cache:'no-cache'});
      const config = await response.json();
      if (!config.enabled || config.apiOrigin !== 'https://api.nla-lib.org') return;
      apiRoot = config.apiOrigin + '/editor-api/';
    } catch { return; }
  }
  const signInUrl=()=> 'https://api.nla-lib.org/auth/login?return_to='+encodeURIComponent(location.pathname+location.search+location.hash);
  let session, currentPerson, reactionOptions = [], readOnlyLibrary = false;
  async function api(path, payload) {
    const response = await fetch(apiRoot + path, payload === undefined ? {cache: 'no-store', credentials:'include'} : {
      method: 'POST', credentials:'include', headers: {'Content-Type': 'application/json', [hosted?'X-CSRF-Token':'X-Editor-Session']: session}, body: JSON.stringify(payload)
    });
    const result = await response.json();
    if (response.status === 401 && payload !== undefined && hosted) {
      const view=modal('Sign in to contribute'); const link=signInLink('Sign in with ORCID');view.content.append(node('p','Your text stays in this window. Sign in in a new tab, then choose Continue here and retry your submission.'),link);link.target='_blank';link.rel='noopener';
      button('Continue here',guarded(view,async()=>{const bootstrap=await api('bootstrap');if(!bootstrap.person)throw new Error('Complete ORCID sign-in in the other tab first.');session=bootstrap.session;currentPerson=bootstrap.person;role=bootstrap.role;publishing=bootstrap.publishing;view.clean();view.dialog.close();}),view.content);
    }
    if (!response.ok) throw new Error(result.error || 'The request failed. Your text remains in the editor.');
    return result;
  }
  function node(tag, text, className) {
    const element = document.createElement(tag);
    if (text !== undefined) element.textContent = text;
    if (className) element.className = className;
    return element;
  }
  function signInLink(label) {
    const link=node('a',label);link.href=signInUrl();
    link.addEventListener('click',()=>{link.href=signInUrl();});return link;
  }
  function button(label, action, parent, className) {
    const element = node('button', label, className); element.type = 'button';
    element.addEventListener('click', action); if (parent) parent.append(element); return element;
  }
  function field(label, value, parent, multiline = false) {
    const wrapper = node('label', label, 'editor-field');
    const input = node(multiline ? 'textarea' : 'input'); input.value = value || '';
    if (multiline) input.rows = 8;
    wrapper.append(input); parent.append(wrapper); return input;
  }
  function proofRequired(object) {return object.statement_kind==='result' && (!object.evidence?.declaration || object.evidence.admission_reported);}
  function leanLinkNotice(object) {
    const linked=!!object.evidence?.declaration;
    return node('p',linked?'Linked Lean statement.':'No linked Lean statement.','editor-notice');
  }
  function typeset(parent) {
    const errors=[];
    for (const element of parent.querySelectorAll('.math')) {
      if(element.querySelector('.katex'))continue;
      if(window.katex){const source=element.textContent;const options={displayMode:element.classList.contains('display'),trust:false,maxExpand:1000,maxSize:20};
        try{window.katex.render(source,element,{...options,throwOnError:true});}
        catch(error){errors.push(error.message);window.katex.render(source,element,{...options,throwOnError:false});}
      }
    }
    return errors;
  }

  const pageActivity = new Map();
  let sequence = 0;
  function modal(title, wide = false) {
    const dialog = node('dialog', undefined, 'editor-dialog' + (wide ? ' editor-wide' : ''));
    const top = node('div', undefined, 'editor-dialog-heading');
    const heading = node('h2', title); heading.id = 'editor-heading-' + (++sequence);
    dialog.setAttribute('aria-labelledby', heading.id);
    top.append(heading); dialog.append(top);
    const status = node('p', '', 'editor-message'); status.setAttribute('role', 'status');
    const content = node('div'); dialog.append(content, status);
    let dirty = false;
    const close = () => {
      if (dirty && !window.confirm('Close without saving your latest changes?')) return;
      dialog.close();
    };
    button('Close', close, top);
    dialog.addEventListener('cancel', event => { event.preventDefault(); close(); });
    dialog.addEventListener('input', () => { dirty = true; });
    dialog.addEventListener('close', () => dialog.remove());
    const mathTitle=/\$([^$\n]+)\$/g;let cursor=0,match;heading.replaceChildren();
    while((match=mathTitle.exec(title))){heading.append(document.createTextNode(title.slice(cursor,match.index)));const span=node('span',match[1],'math');heading.append(span);cursor=mathTitle.lastIndex;}
    heading.append(document.createTextNode(title.slice(cursor)));typeset(heading);
    document.body.append(dialog); dialog.showModal();
    return {dialog, content, status, clean: () => {dirty = false;}, dirty: () => {dirty = true; dialog.dispatchEvent(new Event('editorchange'));}};
  }
  document.addEventListener('click',async event=>{
    const link=event.target.closest('a.reference-bibtex');
    if(!link || event.button!==0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey)return;
    event.preventDefault();
    const view=modal('BibTeX');
    try {
      const response=await fetch(link.href);
      if(!response.ok)throw new Error('Could not load this reference. Please try again.');
      const source=await response.text();
      const text=field('BibTeX citation',source,view.content,true);text.readOnly=true;text.rows=12;
      const actions=node('div',undefined,'editor-actions');view.content.append(actions);
      button('Copy BibTeX',async()=>{
        try{await navigator.clipboard.writeText(source);view.status.textContent='BibTeX copied.';}
        catch{text.focus();text.select();view.status.textContent='Select and copy the BibTeX text above.';}
      },actions);
      text.focus();text.select();
    }catch(error){view.status.textContent=error.message;}
  });
  function download(value, name) {
    const url = URL.createObjectURL(new Blob([JSON.stringify(value, null, 2) + '\n'], {type: 'application/json'}));
    const link = node('a'); link.href = url; link.download = name; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  function guarded(view, action) {
    return async () => {
      view.status.textContent = 'Working…';
      try { await action(); } catch (error) { view.status.textContent = error.message; }
    };
  }
  async function openEditor(id, options = {}) {
    const fresh = options.fresh;
    let state = fresh ? {object: {id, type: 'statement', title: 'New statement', body_markdown: '', statement_kind: 'result', proofs: [], evidence: {type: 'local'}}, revision: null} : await api('objects/' + id);
    if(state.object.type==='reference')return openReferenceEditor(id,options,state);
    let obj = structuredClone(options.restore || state.draft?.object || state.object);
    let draftRevision = state.draft?.draft_revision || null;
    let staleDraft = !!state.draft && state.draft.base_revision !== state.revision && !options.restore;
    const isPage = obj.type === 'page';
    const view = modal((fresh ? 'Add statement' : isPage ? 'Edit page' : 'Edit statement') + ' · ' + obj.title, true);
    view.content.append(node('p', hosted ? 'Drafts are private. Submit your change for editorial review; the published page updates after acceptance and repository checks.' : 'Local workspace · changes are stored on this computer and are not published.', 'editor-notice'));
    if(fresh)view.content.append(node('p','A Lean link is optional. Results need an external natural-language proof link when no Lean proof is linked. Definitions and conjectures do not require proofs.','editor-notice'));
    if (state.draft) view.content.append(node('p', state.draft.base_revision === state.revision ? 'Your saved draft has been restored.' : 'A draft from an older revision was restored. Compare carefully before saving; the current revision is the new base.', 'editor-status'));
    if (staleDraft) button('I have compared this draft; use the latest revision as its base', () => {
      staleDraft = false; view.status.textContent = 'The latest revision is now the explicit base for your draft.';
    }, view.content);
    if (state.used_by?.length) view.content.append(node('p', 'Appears in: ' + state.used_by.map(item => item.title).join(', '), 'editor-notice'));
    const tabs = node('div', undefined, 'editor-actions');
    const form = node('div'); const preview = node('section', undefined, 'editor-preview'); preview.hidden = false;
    const previewStatus=node('p','','editor-preview-message');previewStatus.setAttribute('role','status');preview.append(previewStatus);
    const diff = node('pre', undefined, 'editor-diff'); diff.hidden = true;
    const title = !isPage ? field('Title', obj.title, form) : null;
    let kind, body;
    const proofInputs = [], referenceInputs = [];
    if (!isPage) {
      const label = node('label', 'Statement kind', 'editor-field'); kind = node('select');
      kind.setAttribute('aria-label', 'Statement kind');
      for (const value of ['result', 'conjecture', 'definition']) { const option = node('option', value); option.value = value; kind.append(option); }
      kind.value = obj.statement_kind; kind.disabled = !!obj.evidence.declaration; label.append(kind); form.append(label);
      body = field('Statement · Markdown and LaTeX', obj.body_markdown, form, true); body.rows = 14;
      const proofHeading=node('h3','Proof references');form.append(proofHeading);
      const updateProofLabel=()=>{proofHeading.textContent='Proof references'+(proofRequired({...obj,statement_kind:kind.value})?' · required':' · optional');};
      kind.addEventListener('change',updateProofLabel);updateProofLabel();
      form.append(node('p', 'Link to a natural-language proof hosted elsewhere, with a version or location if available. A link does not establish that the argument is correct or Lean-verified.', 'editor-notice'));
      const proofs = node('div'); form.append(proofs);
      const addProof = (proof = {}) => {
        const row = node('fieldset'); row.append(node('legend', 'External proof'));
        const inputs = {label: field('Reference label', proof.label, row), url: field('HTTPS link', proof.url, row), locator: field('Version and location (e.g. v2, Theorem 3.1)', proof.locator, row)};
        proofInputs.push({row, inputs}); button('Remove reference', () => {row.remove(); view.dirty();}, row); proofs.append(row);
      };
      for (const proof of obj.proofs) addProof(proof);
      button('Add proof reference', () => {addProof(); view.dirty();}, form);
      form.append(node('h3', 'References'));
      const bibliography = await api('references');
      const inherited = state.reference_links?.inherited || [];
      if (inherited.length) form.append(node('p', 'From the Lean source: ' + inherited.map(citation => citation.key + (citation.locator ? ', ' + citation.locator : '')).join('; '), 'editor-notice'));
      const references = node('div'); form.append(references);
      const addReference = citation => {
        const row = node('div', undefined, 'editor-reference-row');
        const label = node('label', 'Shared reference', 'editor-field'); const select = node('select'); select.setAttribute('aria-label', 'Shared reference');
        const empty = node('option', 'Choose a reference'); empty.value = ''; select.append(empty);
        for (const reference of bibliography.references) {const option = node('option', reference.key + ' — ' + reference.text); option.value = reference.key; select.append(option);}
        select.value = citation?.key || ''; label.append(select); row.append(label);
        const locator = field('Location (theorem, section, page, version)', citation?.locator || '', row);
        button('Remove reference', () => {row.remove(); view.dirty();}, row);
        referenceInputs.push({row, select, locator}); references.append(row);
      };
      for (const citation of obj.references || state.reference_links?.editorial || []) addReference(citation);
      button('Add shared reference', () => {addReference(); view.dirty();}, form);

    } else {
      body = field('Page Markdown', options.restore ? (options.document || options.restore.document_markdown || state.document_markdown) : (state.draft?.document_markdown || state.draft?.object.document_markdown || state.document_markdown), form, true);
      body.rows = 28;
      const add = node('div', undefined, 'editor-actions'); form.append(add);
      const insert = sid => {
        body.setRangeText('\n\n{{ statement:' + sid + ' }}\n\n', body.selectionStart, body.selectionEnd, 'end');
        body.dispatchEvent(new Event('input', {bubbles: true})); body.focus();
      };
      button('Add statement', () => openEditor(crypto.randomUUID(), {fresh: true, onCreated: insert}).catch(error => {view.status.textContent = error.message;}), add);
      button('Insert statement', guarded(view, async () => {
        const picker = modal('Insert statement'); const search = field('Search statement titles', '', picker.content);
        const select = node('select'); select.setAttribute('aria-label', 'Statement'); picker.content.append(select);
        const load = async () => {
          const result = await api('objects?type=statement&limit=100&q=' + encodeURIComponent(search.value));
          select.replaceChildren();
          for (const item of result.objects) {const option = node('option', item.title); option.value = item.id; select.append(option);}
        };
        let timer; search.addEventListener('input', () => {clearTimeout(timer); timer = setTimeout(() => load().catch(error => {picker.status.textContent = error.message;}), 200);});
        await load();
        button('Insert', () => {if (select.value) {insert(select.value); picker.dialog.close();}}, picker.content);
        view.status.textContent = '';
      }), add);
    }
    form.append(node('p', 'Notation: vectors/matrices \\mathbf{x}, \\mathbf{A}; transpose ^{\\mathsf{T}}; Hermitian transpose ^{\\mathsf{H}}.', 'editor-notice'));
    function fields() {
      if (isPage) return {document_markdown: body.value};
      return {title: title.value, body_markdown: body.value, statement_kind: kind.value, references: referenceInputs.filter(item => item.row.isConnected && item.select.value).map(item => ({key: item.select.value, locator: item.locator.value})), proofs: proofInputs.filter(item => item.row.isConnected).map(item => Object.fromEntries(Object.entries(item.inputs).map(([key, input]) => [key, input.value])))};
    }
    const panes = node('div', undefined, 'editor-panes editor-split'); panes.append(form, diff, preview);
    preview.setAttribute('aria-label','Live preview');
    let currentMode = 'edit', previewRequest = 0;
    const show = async mode => {
      currentMode = mode;
      form.hidden = mode === 'diff'; preview.hidden = false; diff.hidden = mode !== 'diff';
      panes.classList.add('editor-split');
      for (const control of tabs.children) control.setAttribute('aria-pressed', String(control.dataset.mode === mode));
      const request = ++previewRequest;
      const result = await api(fresh ? 'preview' : 'objects/' + id + '/preview', {fields: fields()});
      if (request !== previewRequest || mode !== currentMode) return;
      preview.innerHTML = result.html;if(!isPage)preview.append(leanLinkNotice(obj)); const errors=typeset(preview); diff.textContent = result.diff; previewStatus.textContent = [...(result.diagnostics||[]).map(issue=>'Line '+issue.line+': '+issue.message),...errors].join(' ');preview.append(previewStatus);if(view.status.textContent==='Working…')view.status.textContent='';
    };
    let previewTimer;
    form.addEventListener('input', () => {
      clearTimeout(previewTimer); previewTimer = setTimeout(()=>show(currentMode).catch(error=>{previewStatus.textContent=error.message;preview.append(previewStatus);}), 400);
    });
    view.dialog.addEventListener('close', () => clearTimeout(previewTimer));
    for (const [label, mode] of [['Edit', 'edit'], ['Changes', 'diff']]) {
      const control = button(label, guarded(view, () => show(mode)), tabs); control.dataset.mode = mode; control.setAttribute('aria-pressed', String(mode === 'edit'));
    }
    view.content.append(tabs, panes);
    const explanation = field('Explanation of this change', options.restore ? 'Restore content from an earlier revision.' : '', view.content, true); explanation.rows = 2;
    const actions = node('div', undefined, 'editor-actions'); view.content.append(actions);
    if (!fresh) button('Save draft', guarded(view, async () => {
      if (staleDraft) throw new Error('Compare the older draft with Changes, then explicitly choose the latest revision as its base.');
      const saved = await api('objects/' + id + '/draft', {base_revision: state.revision, draft_revision: draftRevision, fields: fields()}); draftRevision = saved.draft_revision;
      view.clean(); view.status.textContent = hosted ? 'Private draft saved. No revision or Git commit created.' : 'Draft saved locally. No revision or Git commit created.';
    }), actions);
    let proposalKey = crypto.randomUUID();
    function proposal() {
      return {idempotency_key: proposalKey, explanation: explanation.value, changes: [{operation: fresh ? 'create_statement' : 'update_' + obj.type, id, base_revision: state.revision, fields: fields()}]};
    }
    view.dialog.addEventListener('input', () => {proposalKey = crypto.randomUUID();});
    view.dialog.addEventListener('editorchange', () => {proposalKey = crypto.randomUUID();});
    button('Export proposal', () => {
      if (staleDraft) {view.status.textContent = 'Compare and reconcile this older draft before exporting.'; return;}
      if (explanation.value.trim().length < 3) {view.status.textContent = 'Add a short explanation before exporting.'; return;}
      download(proposal(), 'nla-proposal-' + id + '.json'); view.status.textContent = 'Structured proposal exported. Nothing published.';
    }, actions);
    button(hosted ? 'Submit for review' : 'Save local revision', guarded(view, async () => {
      if (staleDraft) throw new Error('Compare the older draft with Changes, then explicitly choose the latest revision as its base.');
      const submitted=fields();
      if(fresh && !submitted.body_markdown.trim())throw new Error('Write the statement before submitting.');
      if(proofRequired({...obj,...submitted}) && !submitted.proofs?.some(proof=>proof.url.startsWith('https://')))throw new Error('Add a link to an external natural-language proof under Proof references. Definitions and conjectures are exempt.');
      if(!window.katex)throw new Error('Math validation is unavailable. Save a draft and reload before submitting a revision.');
      const checked=await api(fresh?'preview':'objects/'+id+'/preview',{fields:fields()});
      if(checked.diagnostics?.some(issue=>issue.severity==='error'))throw new Error('Fix the mathematical delimiters or braces before submitting. You can save a draft.');
      const mathCheck=node('div');mathCheck.innerHTML=checked.html;const mathErrors=typeset(mathCheck);
      if(mathErrors.length)throw new Error('Fix the LaTeX before saving a revision: '+mathErrors[0]);
      const result = await api('proposals', proposal());
      if (!hosted) {state.revision = result.revisions[id]; state.object = {...obj, ...fields()};}
      draftRevision = null;
      view.clean(); view.status.textContent = hosted ? 'Submitted for review. Published content stays unchanged until accepted. Find this submission in My contributions.' : 'Revision saved locally. Close the editor to see it on this preview.';
      if (hosted) button('View submission', () => showProposal(result.id), view.content, 'editor-footer-link');
      if (fresh && !hosted) {options.onCreated?.(id); view.dialog.close(); return;}
      proposalKey = crypto.randomUUID();
    }), actions, 'editor-primary');
    show('edit').catch(error => {view.status.textContent=error.message;});
    if (!fresh) button('History', () => openHistory(id).catch(error => {view.status.textContent = error.message;}), actions);
    view.dialog.addEventListener('close', () => {
      if (!document.querySelector('dialog[open]')) location.reload();
    });
  }
  async function openReferenceEditor(id, options = {}, suppliedState = null) {
    const fresh=!id;
    const state=suppliedState || (fresh?{revision:null,draft:null,object:{bibtex:'@misc{NewReference,\n  author = {},\n  title = {},\n  year = {}\n}\n'}}:await api('objects/'+id));
    const view=modal(fresh?'Add reference':'Edit reference · '+state.object.evidence.reference_key,true);
    view.content.append(node('p','Edit the BibTeX entry. Existing citation keys stay fixed. Drafts are private; accepted changes update the shared bibliography.','editor-notice'));
    const source=field('BibTeX',options.restore?.bibtex || state.draft?.object.bibtex || state.object.bibtex,view.content,true);source.rows=20;
    const pane=node('div',undefined,'editor-panes editor-split');pane.append(source.parentElement);
    const right=node('section',undefined,'editor-preview');right.setAttribute('aria-label','Live preview');pane.append(right);view.content.append(pane);
    const diff=node('pre','', 'editor-diff');const changes=node('details');changes.append(node('summary','Source changes'),diff);view.content.append(changes);
    const explanation=field('Explanation of this change','',view.content,true);
    let draftRevision=state.draft?.draft_revision || null,key=crypto.randomUUID(),timer,sequence=0;
    let stale=!!state.draft && state.draft.base_revision!==state.revision && !options.restore;
    if(stale){view.content.append(node('p','This draft predates the published reference. Compare Source changes before using the latest version as its base.','editor-notice'));button('I have compared this draft with the latest reference',()=>{stale=false;view.status.textContent='The latest published version is now the explicit base.';},view.content);}
    view.dialog.addEventListener('input',()=>{key=crypto.randomUUID();});
    const fields=()=>({bibtex:source.value});
    async function update(){const request=++sequence;try{const result=await api(fresh?'references/preview':'objects/'+id+'/preview',{fields:fields()});if(request!==sequence)return;right.innerHTML=result.html;typeset(right);diff.textContent=result.diff;return result;}catch(error){if(request===sequence)right.textContent=error.message;throw error;}}
    source.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(()=>update().catch(()=>{}),400);});
    view.dialog.addEventListener('close',()=>clearTimeout(timer));update().catch(()=>{});
    const actions=node('div',undefined,'editor-actions');view.content.append(actions);
    if(!fresh)button('Save draft',guarded(view,async()=>{if(stale)throw new Error('Compare the older draft with the current reference first.');const result=await api('objects/'+id+'/draft',{base_revision:state.revision,fields:fields(),draft_revision:draftRevision});draftRevision=result.draft_revision;view.clean();view.status.textContent='Private draft saved.';}),actions);
    button('Submit for review',guarded(view,async()=>{if(stale)throw new Error('Compare the older draft with the current reference first.');const checked=await update();const objectId=fresh?checked.id:id;
      const result=await api('proposals',{idempotency_key:key,explanation:explanation.value,changes:[{operation:fresh?'create_reference':'update_reference',id:objectId,base_revision:state.revision,fields:fields()}]});
      view.clean();view.status.textContent='Submitted for review. The published bibliography is unchanged until accepted.';button('View submission',()=>showProposal(result.id),view.content,'editor-footer-link');
    }),actions,'editor-primary');
    if(!fresh)button('History',()=>openHistory(id),actions);
  }
  async function reportContent(id, commentId = null) {
    const view=modal('Report content');const reason=field('Reason for this report','',view.content,true);
    button('Send report',guarded(view,async()=>{await api('objects/'+id+'/report',{comment_id:commentId,reason:reason.value});view.clean();view.status.textContent='Report sent to the moderators.';}),view.content);
  }
  async function moderation() {
    const view=modal('Moderation reports',true),data=await api('moderation');
    if(!data.items.length)view.content.append(node('p','No reports.'));
    for(const report of data.items){const row=node('article',undefined,'profile-activity');row.append(node('h3',report.title),node('p',report.reason),node('p',report.status,'editor-notice'));
      if(report.status==='open')for(const [action,label] of [['dismiss','Dismiss report'],...(report.comment_id?[['hide_comment','Remove comment']]:[])])button(label,guarded(view,async()=>{await api('moderation/resolve',{id:report.id,action});view.status.textContent='Report resolved. Original content remains in the moderation audit.';}),row,'editor-footer-link');
      view.content.append(row);
    }
  }
  async function contributions(review = false) {
    const view=modal(review ? 'Editorial review' : 'My contributions', true);
    let cursor=null;
    const list=node('div');view.content.append(list);
    const more=button('Load older contributions',guarded(view,load),view.content);
    async function load() {
      const data=await api((review?'review':'proposals')+(cursor?'?cursor='+encodeURIComponent(cursor):''));
      if (!data.items.length && !list.children.length) list.append(node('p','No contributions yet.'));
      for (const item of data.items) {
        const row=node('article',undefined,'profile-activity');
        button(item.explanation,()=>showProposal(item.id),row,'editor-footer-link');
        row.append(node('p',item.status.replaceAll('_',' ')+' · '+item.attribution.actor.display_name,'editor-notice'));list.append(row);
      }
      cursor=data.next_cursor;more.hidden=!cursor;
    }
    await load();
  }
  async function showProposal(id) {
    const data=await api('proposals/'+id),view=modal('Contribution · '+data.explanation,true);
    view.content.append(node('p',data.status.replaceAll('_',' '),'editor-status'));
    const credit=node('p','Submitted by ');credit.append(profileLink(data.attribution.actor));view.content.append(credit);
    for (const item of data.objects) {
      const revision=await api('objects/'+item.id+'?revision='+item.revision);
      view.content.append(node('h3',item.title));
      const rendered=node('div',undefined,'editor-preview');rendered.innerHTML=revision.html;typeset(rendered);if(revision.object.type==='statement')rendered.append(leanLinkNotice(revision.object));view.content.append(rendered);
      const changes=node('details');changes.append(node('summary','Source changes'));
      const diff=node('pre',revision.diff || revision.document_markdown,'editor-diff');changes.append(diff);view.content.append(changes);
    }
    if(data.review_message)view.content.append(node('p','Reviewer: '+data.review_message));
    if(data.pull_request){const link=node('a','View publication checks on GitHub');link.href=data.pull_request.url;view.content.append(link);}
    if(['trusted_editor','admin'].includes(role)) {
      const message=field('Review note','',view.content,true);
      if(['submitted','changes_requested'].includes(data.status)) {
        for(const [decision,label] of [['approve','Approve'],['request_changes','Request changes'],['reject','Reject']]) {
          button(label,guarded(view,async()=>{await api('proposals/'+id+'/review',{decision,message:message.value});view.clean();view.dialog.close();await showProposal(id);}),view.content,'editor-footer-link');
        }
      }
      if(['approved','awaiting_checks'].includes(data.status)) {
        if(!publishing)view.content.append(node('p','Approved and saved. Publication becomes available when the GitHub App is connected.','editor-notice'));
        else button(data.status==='approved'?'Start publication':'Check and publish',guarded(view,async()=>{const result=await api('proposals/'+id+'/publish',{});view.status.textContent=result.status==='published'?'Published to Git. The site is rebuilding.':'The publication pull request is ready. Wait for its checks, then choose Check and publish.';}),view.content,'editor-primary');
      }
    }
  }
  async function openHistory(id) {
    const history = await api('objects/' + id + '/history'); const view = modal('Revision history', true);
    const list = node('ol'); view.content.append(list);
    for (const revision of [...history.revisions].reverse()) {
      const row = node('li'); row.append(node('p', revision.explanation), node('small', revision.created_at ? new Date(revision.created_at).toLocaleString() : 'Published source'));
      if(revision.attribution){const credit=node('p',undefined,'editor-notice');credit.append(profileLink(revision.attribution.actor));if(revision.attribution.actor.kind==='bot')credit.append(node('span',' · Bot · Responsible person: '),profileLink(revision.attribution.responsible_person));row.append(credit);}
      const link = node('a', 'Permanent revision link'); const url = new URL(location.href); url.searchParams.set('editor-object', id); url.searchParams.set('revision', revision.id); link.href = url; row.append(link);
      button('View revision', guarded(view, async () => {
        const item = await api('objects/' + id + '?revision=' + encodeURIComponent(revision.id));
        const detail = modal('Revision · ' + item.object.title, true); detail.content.innerHTML = item.html; typeset(detail.content);
        detail.content.prepend(node('p', (hosted ? 'Revision · ' : 'Immutable local revision · ') + revision.id, 'editor-notice'));
        if (!readOnlyLibrary) button('Restore as a new revision', () => openEditor(id, {restore: item.object, document: item.document_markdown}).catch(error => {detail.status.textContent = error.message;}), detail.content);
        view.status.textContent = '';
      }), row); list.append(row);
    }
    view.content.append(node('p', hosted ? 'Published revisions remain in Git. Proposed revisions are visible to their contributor and editors. Restore an earlier version by submitting it as a new change.' : 'Revision links require this local database. Published Git history will be connected in the publication phase.', 'editor-notice'));
  }
  function reactionBar(id, readOnly = false) {
    const bar = node('span', undefined, 'editor-reactions');
    bar.setAttribute('role', 'group'); bar.setAttribute('aria-label', 'Reactions');
    let reactions = [];
    const emojiImage = emoji => {
      const icon = node('img'); icon.alt = ''; icon.width = 20; icon.height = 20; icon.draggable = false;
      const code = [...emoji].filter(char => char.codePointAt(0) !== 0xfe0f).map(char => char.codePointAt(0).toString(16)).join('-');
      icon.src = '/explore/editor-assets/emoji/' + code + '.svg'; return icon;
    };
    const report = message => {const status = node('span', message, 'editor-reaction-error'); status.setAttribute('role', 'status'); bar.append(status);};
    const toggle = async emoji => {
      const selected = reactions.some(reaction => reaction.emoji === emoji && reaction.reacted);
      const result = await api('objects/' + id + '/reaction', {emoji, active: !selected});
      document.dispatchEvent(new CustomEvent('editor-reactions-changed', {detail: {id, reactions: result.reactions}}));
    };
    const draw = () => {
      bar.replaceChildren();
      for (const reaction of reactions) {
        const chip = readOnly ? node('span', undefined, 'editor-reaction-chip editor-reaction-readonly') : button(reaction.emoji + ' ' + reaction.count, async () => {try {await toggle(reaction.emoji);} catch (error) {report(error.message);}}, null, 'editor-reaction-chip');
        bar.append(chip);
        if(readOnly)chip.setAttribute('role','img');
        chip.setAttribute('aria-label', reaction.emoji + ' ' + reaction.label + ', ' + reaction.count + ' reaction');
        if(!readOnly)chip.setAttribute('aria-pressed', String(reaction.reacted));
        chip.title = readOnly ? reaction.label + ' · Open the statement to react' : (reaction.reacted ? 'You reacted. Click to remove: ' : 'React: ') + reaction.label;
        chip.replaceChildren(emojiImage(reaction.emoji), node('span', String(reaction.count)));
      }
      bar.hidden=readOnly&&!reactions.length;
      if(readOnly)return;
      const add = button('☺ +', () => {
        const picker = modal('Add a reaction'); picker.dialog.classList.add('editor-emoji-dialog');
        const grid = node('div', undefined, 'editor-emoji-grid'); picker.content.append(grid);
        const credit = node('p', undefined, 'editor-notice');
        const artwork = node('a', 'Twemoji'); artwork.href = 'https://github.com/twitter/twemoji';
        const license = node('a', 'CC BY 4.0'); license.href = 'https://creativecommons.org/licenses/by/4.0/';
        credit.append(artwork, ' by Twitter and contributors · ', license); picker.content.append(credit);
        for (const option of reactionOptions) {
          const choice = button(option.emoji, guarded(picker, async () => {await toggle(option.emoji); picker.dialog.close();}), grid, 'editor-emoji-option');
          choice.setAttribute('aria-label', 'React with ' + option.emoji + ' · ' + option.label);
          choice.setAttribute('aria-pressed', String(reactions.some(reaction => reaction.emoji === option.emoji)));
          choice.title = option.label;
          const icon = emojiImage(option.emoji); icon.width = 28; icon.height = 28; choice.replaceChildren(icon);
        }
      }, bar, 'editor-reaction-add');
      add.setAttribute('aria-label', 'Add reaction'); add.title = 'Add a reaction';
      add.replaceChildren(emojiImage('🙂'), node('span', '+'));
    };
    const changed = event => {
      if (!bar.isConnected) {document.removeEventListener('editor-reactions-changed', changed); return;}
      if (event.detail.id === id) {reactions = event.detail.reactions; draw();}
    };
    document.addEventListener('editor-reactions-changed', changed);
    draw();
    (pageActivity.get(id) || api('objects/' + id + '/reaction')).then(result => {reactions = result.reactions; draw();}).catch(error => report(error.message));
    return bar;
  }
  const discussionPanels = new Map();
  function discussionIcon(count) {
    const wrapper = node('span', undefined, 'discussion-icon-label');
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 24 24'); svg.setAttribute('width', '18'); svg.setAttribute('height', '18'); svg.setAttribute('aria-hidden', 'true');
    const path = document.createElementNS(svg.namespaceURI, 'path'); path.setAttribute('d', 'M4 4h16v12H9l-5 4V4Z');
    path.setAttribute('fill', 'none'); path.setAttribute('stroke', 'currentColor'); path.setAttribute('stroke-width', '1.6'); svg.append(path);
    wrapper.append(svg, node('span', String(count))); return wrapper;
  }
  function updateDiscussionCount(control, id, count) {
    control.replaceChildren(discussionIcon(count));
    control.setAttribute('aria-label', 'Discussion, ' + count + (count === 1 ? ' message' : ' messages'));
    control.title = count + (count === 1 ? ' message in the discussion' : ' messages in the discussion');
    control.dataset.discussionObject = id;
  }
  let discussionModule;
  async function openDiscussion(id, options = {}) {
    if (discussionPanels.has(id)) return discussionPanels.get(id);
    const host = node('section', undefined, 'editor-discussion'); host.id = 'discussion';
    host.dataset.discussionFor = id; discussionPanels.set(id, host);
    const main=document.querySelector('main');const reactions=main.querySelector('.theorem-reaction-slot') || (main.dataset.editorStatement?main.querySelector('.page-reactions'):null);
    if(reactions)reactions.after(host);else main.append(host);
    host.textContent = 'Loading discussion…';
    try {
      discussionModule ||= import('/explore/editor-assets/discussion.js?v='+assetVersion);
      const {mountDiscussion} = await discussionModule; host.textContent = '';
      await mountDiscussion(host, {id, api, typeset, assetVersion, onReport: hosted ? commentId => reportContent(id,commentId) : null, onCount: count => document.dispatchEvent(new CustomEvent('editor-discussion-changed', {detail: {id, count}}))});
    } catch (error) {const message=node('p','Discussion could not load. '+error.message);(host.shadowRoot||host).replaceChildren(message);}
    if (options.scroll || location.hash === '#discussion') host.scrollIntoView({block: 'start'});
    return host;
  }
  async function queue() {
    const view = modal('Suggestions & issues'); const data = await api('feedback');
    button('Export for research / Lean review', () => download({schema_version: 1, purpose: 'Human review; no automatic Lean updates', items: data.items}, 'nla-research-feedback.json'), view.content);
    const filter = node('select'); filter.setAttribute('aria-label', 'Feedback type');
    for (const value of ['all', 'suggestion', 'mathematical-error', 'reference-request', 'formalization-request', 'generalization', 'comment']) {const option = node('option', value.replaceAll('-', ' ')); option.value = value; filter.append(option);}
    const list = node('div'); view.content.append(filter, list);
    const show = () => {
      list.replaceChildren();
      for (const item of data.items.filter(item => filter.value === 'all' || item.kind === filter.value)) {
        const row = node('article', undefined, 'editor-feedback'); row.append(node('strong', item.kind.replaceAll('-', ' ')), node('h3', item.title), node('p', item.body));
        button('Open page', guarded(view, async () => {const state = await api('objects/' + item.object_id); location.assign(state.url + '#discussion');}), row); list.append(row);
      }
      if (!list.children.length) list.append(node('p', 'No local feedback of this type yet. Use Discuss on any page or statement.'));
    }; filter.addEventListener('change', show); show();
    const more = button('Load older feedback', guarded(view, async () => {
      const next = await api('feedback?cursor=' + data.next_cursor); data.items.push(...next.items); data.next_cursor = next.next_cursor; more.hidden = !data.next_cursor; show(); view.status.textContent = '';
    }), view.content); more.hidden = !data.next_cursor;
  }
  function profileLink(person) {
    const link = node('a', person.display_name); link.href = person.url; return link;
  }
  async function editProfile() {
    const view = modal('Edit profile');
    const inputs = {};
    for (const [key,label] of [['display_name','Display name'],['affiliation','Affiliation'],['bio','About'],['interests','Research interests'],['website','Website · HTTPS'],...(!hosted ? [['orcid','ORCID iD · unverified in this prototype']] : [])]) inputs[key]=field(label,currentPerson[key],view.content,key==='bio');
    button('Save profile',guarded(view,async()=>{currentPerson=await api('me/profile',Object.fromEntries(Object.entries(inputs).map(([key,input])=>[key,input.value])));view.status.textContent='Profile saved.';await renderProfile(currentPerson.id);}),view.content);
  }
  async function botSettings() {
    const view=modal('Your bots');
    view.content.append(node('p','Bots have their own names and profiles. Your profile remains responsible for their activity. Tokens grant only the actions you select.','editor-notice'));
    const list=node('div');view.content.append(list);
    async function refresh(){list.replaceChildren();for(const item of (await api('bots')).bots){const row=node('p');row.append(profileLink(item.bot),node('span',' · '+item.scopes.join(', ')+(item.revoked?' · Revoked':'')));if(!item.revoked)button('Revoke token',guarded(view,async()=>{await api('bots/'+item.token_id+'/revoke',{});await refresh();view.status.textContent='Token revoked.';}),row);list.append(row);}}
    await refresh();
    view.content.append(node('h3','Register a bot'));const name=field('Bot name','',view.content);const bio=field('What will this bot do?','',view.content,true);const scopes=node('fieldset');scopes.append(node('legend','Allowed actions'));const checks=[];
    for(const [value,label] of [['proposals','Propose content revisions'],['feedback','Comment and suggest'],['reactions','React']]){const row=node('label',label,'bot-scope');const check=node('input');check.type='checkbox';check.value=value;row.prepend(check);scopes.append(row);checks.push(check);}view.content.append(scopes);
    button('Create bot and token',guarded(view,async()=>{const result=await api('bots',{display_name:name.value,bio:bio.value,scopes:checks.filter(check=>check.checked).map(check=>check.value)});await refresh();const box=node('div',undefined,'bot-token');box.append(node('p','Copy this token now. It is shown only once; the database stores only its hash.'));const token=field('API token',result.token,box);token.readOnly=true;button('Copy token',guarded(view,async()=>{await navigator.clipboard.writeText(result.token);view.status.textContent='Token copied.';}),box);view.content.append(box);view.status.textContent='Bot registered. Never put the token in a URL or public source file.';}),view.content);
  }
  async function showNotifications() {
    const view=modal('Notifications');const list=node('div');view.content.append(list);let cursor=0;
    const load=async()=>{const data=await api('notifications?cursor='+cursor);for(const item of data.items){const row=node('article',undefined,'profile-activity');row.append(profileLink(item.actor),node('span',' · '+(item.kind==='comment'?'Commented on ':'Updated ')));const link=node('a',item.title);link.href=item.url+(item.kind==='comment'?'#discussion':'');row.append(link,node('p',new Date(item.created_at).toLocaleString(),'editor-notice'));if(!item.read_at)button('Mark read',guarded(view,async()=>{await api('notifications/read',{id:item.id});row.querySelector('button').remove();view.status.textContent='Marked read.';}),row);list.append(row);}if(!data.items.length&&!cursor)list.append(node('p','No notifications yet. Follow a result to receive activity updates. Your own and your bots’ activity won’t notify you.'));cursor=data.next_cursor;more.hidden=cursor===null;};
    const more=button('Load older notifications',guarded(view,load),view.content);await load();
  }
  async function renderProfile(id) {
    const host=document.getElementById('profile-content');if(!host)return;
    const data=await api('profiles/'+id), person=data.profile;host.replaceChildren();document.querySelector('.page-title').textContent=person.display_name;
    if(person.kind==='bot'){const owner=(await api('profiles/'+person.owner_id)).profile;const label=node('p','Bot · Responsible person: ','profile-kind');label.append(profileLink(owner));host.append(label);}
    else host.append(node('p',person.affiliation||'Researcher','profile-kind'));
    if(person.bio)host.append(node('p',person.bio,'profile-bio'));if(person.interests)host.append(node('p','Research interests: '+person.interests));
    if(person.website){const link=node('a','Website');link.href=person.website;link.rel='noopener noreferrer';host.append(link);}
    if(person.orcid)host.append(node('p','ORCID: '+person.orcid+(hosted?' · Authenticated ORCID iD':' · unverified in this prototype'),'editor-notice'));
    if(id===currentPerson?.id){const tools=node('div',undefined,'profile-actions');button('Edit profile',editProfile,tools,'editor-footer-link');button('Manage bots',botSettings,tools,'editor-footer-link');button('Notifications',showNotifications,tools,'editor-footer-link');host.append(tools);}
    if(data.bots.length){host.append(node('h2','Bots'));const list=node('ul');for(const bot of data.bots){const row=node('li');row.append(profileLink(bot),node('span',' · Bot'));list.append(row);}host.append(list);}
    host.append(node('h2','Contributions'));if(person.kind==='person')host.append(node('p','Includes contributions by this person and their bots.','editor-notice'));
    const activity=node('div');host.append(activity);let cursor=data.next_cursor;
    const draw=items=>{for(const item of items){const row=node('article',undefined,'profile-activity');const link=node('a',item.title);link.href=item.url+(item.kind==='comment'?'#discussion':'');row.append(profileLink(item.actor),node('span',item.actor.kind==='bot'?' · Bot · ':' · '),node('span',item.kind==='comment'?'Commented on ':'Revised '),link,node('p',new Date(item.created_at).toLocaleString(),'editor-notice'));if(item.excerpt_html){const excerpt=node('div',undefined,'profile-excerpt');excerpt.innerHTML=item.excerpt_html;row.append(excerpt);typeset(excerpt);}activity.append(row);}};draw(data.activities);if(!data.activities.length)activity.append(node('p','No contributions yet.'));
    const more=button('Load older contributions',async()=>{const next=await api('profiles/'+id+'?cursor='+cursor);draw(next.activities);cursor=next.next_cursor;more.hidden=cursor===null;},host);more.hidden=cursor===null;
    if(data.reactions.length){host.append(node('h2','Reactions'));const list=node('ul');for(const item of data.reactions){const row=node('li'),link=node('a',item.title);link.href=item.url;const icon=node('img');icon.alt=item.emoji;icon.width=18;icon.height=18;const code=[...item.emoji].filter(char=>char.codePointAt(0)!==0xfe0f).map(char=>char.codePointAt(0).toString(16)).join('-');icon.src='/explore/editor-assets/emoji/'+code+'.svg';row.append(icon,node('span',' '),link,node('span',' · '),profileLink(item.actor));list.append(row);}host.append(list);}
    if(id===currentPerson?.id){const inbox=await api('notifications');host.append(node('h2','Notifications · private'));host.append(node('p',inbox.unread+' unread'));for(const item of inbox.items.slice(0,5)){const row=node('p'),link=node('a',item.title);link.href=item.url+'#discussion';row.append(profileLink(item.actor),node('span',' · '+(item.kind==='comment'?'Commented on ':'Updated ')),link);host.append(row);}button('Open notification inbox',showNotifications,host,'editor-footer-link');const workspace=await api('me/workspace');for(const [key,title] of [['drafts','Your drafts · private'],['following','Following · private']]){host.append(node('h2',title));const list=node('ul');for(const item of workspace[key]){const row=node('li'),link=node('a',item.title);link.href=item.url;row.append(link);list.append(row);}host.append(list.children.length?list:node('p',key==='drafts'?'No saved drafts.':'Follow a result or join a discussion to track it here.'));}}
  }
  try {
    const bootstrap = await api('bootstrap'); session = bootstrap.session; currentPerson = bootstrap.person; reactionOptions = bootstrap.reaction_options;role=bootstrap.role;publishing=bootstrap.publishing;
    const main = document.querySelector('main'); if (!main) return; readOnlyLibrary = !!main.dataset.editorReadonly;
    const addStatement=async()=>{
      if(hosted && !currentPerson){const view=modal('Sign in to add a statement');view.content.append(signInLink('Sign in with ORCID'));return;}
      return openEditor(crypto.randomUUID(),{fresh:true});
    };
    const footer = document.querySelector('.site-footer-links') || document.querySelector('footer');
    if (footer) {
      if (currentPerson) {
        const me = profileLink(currentPerson); me.textContent='My profile'; footer.append(me);
        const notifications=button('Notifications', showNotifications, footer, 'editor-footer-link');
        api('notifications').then(data=>{notifications.textContent='Notifications'+(data.unread?' ('+data.unread+')':'');}).catch(()=>{});
        if (hosted) {
          button('Sign out',async()=>{const response=await fetch('https://api.nla-lib.org/auth/logout',{method:'POST',credentials:'include',headers:{'Content-Type':'application/json','X-CSRF-Token':session},body:'{}'});if(response.ok)location.reload();},footer,'editor-footer-link');
          if(['moderator','admin'].includes(role))button('Moderation reports',moderation,footer,'editor-footer-link');
          button('My contributions', () => contributions(false), footer, 'editor-footer-link');
          if (['trusted_editor','admin'].includes(role)) button('Review contributions', () => contributions(true), footer, 'editor-footer-link');
        } else button('Research feedback', queue, footer, 'editor-footer-link');
      } else if (hosted) {
        const signin=signInLink('Sign in with ORCID');footer.append(signin);
      }
      if (!hosted) footer.parentElement.append(node('p', 'Local preview · changes are saved on this computer', 'editor-preview-status'));
    }
    if(hosted && main.dataset.community !== undefined) {
      const profile=new URLSearchParams(location.search).get('profile') || currentPerson?.id;
      if(profile) main.dataset.profileId=profile;
      else document.getElementById('profile-content').textContent='Sign in with ORCID to manage your profile, drafts, contributions and bots.';
    }
    if(hosted && bootstrap.features?.includes('bibliography-editing') && location.pathname.replace(/\/$/,'')==='/explore/references'){
      const registry=await api('objects?type=reference&limit=100');let entries=[...registry.objects],cursor=registry.next_cursor;
      while(cursor){const next=await api('objects?type=reference&limit=100&cursor='+encodeURIComponent(cursor));entries.push(...next.objects);cursor=next.next_cursor;}
      const byKey=new Map(entries.map(item=>[item.reference_key,item.id]));
      for(const row of main.querySelectorAll('[data-reference-id]')){const id=byKey.get(row.dataset.referenceId);if(!id)continue;const tools=node('span',undefined,'reference-actions');button('Edit',()=>openReferenceEditor(id).catch(error=>{const view=modal('Reference editor');view.status.textContent=error.message;}),tools,'editor-footer-link');button('History',()=>openHistory(id),tools,'editor-footer-link');row.append(tools);}
      const heading=main.querySelector('.page-heading');if(heading)button('Add reference',()=>openReferenceEditor(null),heading,'editor-footer-link');
    }
    if(main.dataset.profileId) await renderProfile(main.dataset.profileId);
    const objectId = main.dataset.editorPage || main.dataset.editorStatement;
    const label = main.dataset.editorPage ? 'page' : 'statement';
    const heading = main.querySelector('.page-heading');
    if (objectId && heading) {
      const tools = node('details', undefined, 'page-tools');
      const summary = node('summary', '⋯'); summary.setAttribute('aria-label', 'Page actions');
      const menu = node('div', undefined, 'page-tools-menu');
      const action = callback => async () => {tools.open = false; try {await callback();} catch (problem) {const view = modal('Could not open'); view.status.textContent = problem.message;}};
      if (!readOnlyLibrary) {
        button('Edit ' + label, action(() => openEditor(objectId)), menu);
        button('Revision history', action(() => openHistory(objectId)), menu);
      }
      const follow=button('Follow',action(async()=>{const data=await api('objects/'+objectId+'/follow',{active:follow.dataset.following!=='true'});follow.dataset.following=String(data.following);follow.textContent=data.following?'Unfollow':'Follow';}),menu);
      api('objects/'+objectId+'/follow').then(data=>{follow.dataset.following=String(data.following);follow.textContent=data.following?'Unfollow':'Follow';});
      if(hosted)button('Report a problem',action(()=>reportContent(objectId)),menu);
      button('Add statement', action(addStatement), menu);
      button('Copy page link', action(async () => {await navigator.clipboard.writeText(location.origin + location.pathname);}), menu);
      tools.append(summary, menu); heading.append(tools);
      document.addEventListener('click', event => {if (!tools.contains(event.target)) tools.open = false;});
      document.addEventListener('keydown', event => {if (event.key === 'Escape') tools.open = false;});
    }
    if (!(objectId && heading) && footer) button('Add statement',()=>addStatement().catch(error=>{const view=modal('Could not open editor');view.status.textContent=error.message;}),footer,'editor-footer-link');
    const ids=[...new Set([...main.querySelectorAll('[data-statement-id]')].map(card=>card.dataset.statementId).concat(objectId?[objectId]:[]))];
    for(let offset=0;offset<ids.length;offset+=150){const group=ids.slice(offset,offset+150),batch=api('activity?ids='+group.join(','));for(const id of group)pageActivity.set(id,batch.then(data=>data.objects[id]));}
    for (const overview of main.querySelectorAll('[data-statement-id]')) {
      const meta = overview.querySelector('.statement-overview-meta');
      if (meta) meta.prepend(reactionBar(overview.dataset.statementId, true));
    }
    for (const slot of main.querySelectorAll('[data-reaction-object]')) slot.append(reactionBar(slot.dataset.reactionObject));
    if (objectId && !main.querySelector('[data-reaction-object]') && heading) {
      const reactions = node('div', undefined, 'page-reactions'); reactions.append(reactionBar(objectId)); heading.after(reactions);
    }
    for (const count of main.querySelectorAll('[data-discussion-count]')) {
      const sid = count.dataset.discussionCount;
      (pageActivity.get(sid) || api('objects/' + sid + '/feedback?summary=1')).then(data => {updateDiscussionCount(count, sid, data.count); count.hidden = false;}).catch(() => {});
    }
    document.addEventListener('editor-discussion-changed', event => {
      for (const count of document.querySelectorAll('[data-discussion-count]')) if (count.dataset.discussionCount === event.detail.id) {updateDiscussionCount(count, event.detail.id, event.detail.count); count.hidden = false;}
    });
    if (objectId && hosted && !currentPerson) {const notice=node('p','Sign in with ORCID to comment, react or propose an edit.','editor-notice');const link=signInLink('Sign in');notice.append(' ',link);heading?.after(notice);}
    if (objectId) openDiscussion(objectId).catch(error => console.error('Discussion:', error));
    const query = new URLSearchParams(location.search); const id = query.get('editor-object');
    if (id && query.get('revision')) {
      const state = await api('objects/' + encodeURIComponent(id) + '?revision=' + encodeURIComponent(query.get('revision')));
      const view = modal('Revision · ' + state.object.title, true); view.content.innerHTML = state.html; typeset(view.content);
      view.content.prepend(node('p', (hosted ? 'Revision · ' : 'Immutable local revision · ') + query.get('revision'), 'editor-notice'));
      if (!readOnlyLibrary) button('Restore as a new revision', () => openEditor(id, {restore: state.object, document: state.document_markdown}), view.content);
    }
    window.addEventListener('beforeunload', event => {if (document.querySelector('dialog[open] textarea')) {event.preventDefault(); event.returnValue = '';}});
  } catch (error) {
    if (hosted) {
      const footer=document.querySelector('.site-footer-links') || document.querySelector('footer');
      if (footer) {const link=node('a','Account · Sign in with ORCID');link.href='https://api.nla-lib.org/account';footer.append(link);}
    }
    console.error('Collaboration:', error);
  }
})();
