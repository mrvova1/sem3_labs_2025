// Простая логика редактора: сцены, группы, ассеты и экспорт.
// Не использует внешние библиотеки — все на "vanilla" JS.

(() => {
  // --- State ---
  const state = {
    assets: [], // {id,name,src,thumb}
    groups: [], // {id,name,music,sceneIds:[]}
    scenes: [], // {id,name,layers:[],dialogue:[] , thumbnail}
    currentSceneIndex: 0,
    selectedElem: null
  }

  // --- Utils ---
  const uid = (p = '') => Date.now().toString(36) + Math.random().toString(36).slice(2,6) + p
  const q = s => document.querySelector(s)
  const qa = s => Array.from(document.querySelectorAll(s))

  // --- Elements ---
  const assetsList = q('#assetsList')
  const assetUpload = q('#assetUpload')
  const addGroupBtn = q('#addGroupBtn')
  const groupsList = q('#groupsList')
  const scenesList = q('#scenesList')
  const newSceneBtn = q('#newScene')
  const dupSceneBtn = q('#dupScene')
  const delSceneBtn = q('#delScene')
  const prevSceneBtn = q('#prevScene')
  const nextSceneBtn = q('#nextScene')
  const stage = q('#stage')
  const layersList = q('#layersList')
  const dialogLines = q('#dialogLines')
  const addLineBtn = q('#addLineBtn')
  const currentSceneName = q('#currentSceneName')
  const exportBtn = q('#exportBtn')

  const selectedInfo = q('#selectedInfo')
  const propX = q('#propX')
  const propY = q('#propY')
  const propRot = q('#propRot')
  const propScale = q('#propScale')
  const propOpacity = q('#propOpacity')
  const bringForwardBtn = q('#bringForward')
  const sendBackwardBtn = q('#sendBackward')

  const groupNameInput = q('#groupNameInput')
  const groupMusicInput = q('#groupMusicInput')

  // --- Initial setup ---
  function init(){
    // create default group and scene
    const gId = uid('g')
    state.groups.push({id:gId,name:'Main',music:'',sceneIds:[]})
    createScene('Сцена 1')
    renderAll()
  }

  // --- Scenes & Groups ---
  function createScene(name = 'Untitled'){
    const s = {id:uid('s'),name, layers:[], dialogue:[]}
    state.scenes.push(s)
    // append to first group by default
    state.groups[0].sceneIds.push(s.id)
    state.currentSceneIndex = state.scenes.length - 1
    return s
  }

  function duplicateScene(index){
    const src = state.scenes[index]
    if(!src) return
    const copy = JSON.parse(JSON.stringify(src))
    copy.id = uid('s')
    copy.name = src.name + ' (copy)'
    // regenerate ids for layers
    copy.layers = copy.layers.map(l => ({...l, id: uid('l')}))
    state.scenes.splice(index+1,0,copy)
    state.currentSceneIndex = index+1
    // add to group
    state.groups[0].sceneIds.push(copy.id)
  }

  function removeScene(index){
    if(state.scenes.length<=1) return
    const s = state.scenes.splice(index,1)[0]
    state.groups.forEach(g=>{g.sceneIds = g.sceneIds.filter(id=>id!==s.id)})
    if(state.currentSceneIndex>=state.scenes.length) state.currentSceneIndex = state.scenes.length-1
  }

  // --- Assets ---
  assetUpload.addEventListener('change', async (e)=>{
    const files = Array.from(e.target.files)
    for(const f of files){
      const src = await fileToDataURL(f)
      const aid = uid('a')
      const asset = {id:aid,name:f.name,src}
      state.assets.push(asset)
    }
    renderAssets()
    e.target.value = ''
  })

  function fileToDataURL(file){
    return new Promise((res,rej)=>{
      const r = new FileReader()
      r.onload = ()=>res(r.result)
      r.onerror = rej
      r.readAsDataURL(file)
    })
  }

  function renderAssets(){
    assetsList.innerHTML = ''
    for(const a of state.assets){
      const div = document.createElement('div')
      div.className = 'asset'
      div.title = a.name
      const img = document.createElement('img')
      img.src = a.src
      img.draggable = false
      div.appendChild(img)

      // drag to stage
      div.addEventListener('pointerdown',(ev)=>{
        // create new placed item in center
        addLayerFromAsset(a, {x:stage.clientWidth/2 - 80, y: stage.clientHeight/2 - 120})
      })

      assetsList.appendChild(div)
    }
  }

  // --- Layers & placing items on stage ---
  function addLayerFromAsset(asset, pos={x:100,y:100}){
    const layerId = uid('l')
    const el = document.createElement('div')
    el.className = 'placed-item'
    el.dataset.layerId = layerId
    el.style.left = pos.x+'px'
    el.style.top = pos.y+'px'
    el.style.zIndex = 100 + (state.scenes[state.currentSceneIndex].layers.length)
    el.style.transform = 'translate(0,0) rotate(0deg) scale(1)'
    el.style.opacity = 1

    const img = document.createElement('img')
    img.src = asset.src
    img.style.maxWidth = '320px'
    img.style.maxHeight = '480px'
    img.draggable = false
    el.appendChild(img)

    // simple resize handle
    const h = document.createElement('div')
    h.className = 'handle'
    el.appendChild(h)

    // store metadata
    const layer = {
      id: layerId,
      type: 'image',
      assetId: asset.id,
      name: asset.name,
      position: {x: pos.x, y: pos.y},
      rotation: 0,
      scale: 1,
      flipX: false,
      flipY: false,
      opacity: 1,
      visible: true
    }

    // make draggable
    makeDraggable(el, layer)

    stage.appendChild(el)
    state.scenes[state.currentSceneIndex].layers.push(layer)
    renderLayersPanel()
  }

  function makeDraggable(el, layer){
    let down=false, sx=0, sy=0, ox=0, oy=0
    el.addEventListener('pointerdown', (e)=>{
      e.stopPropagation()
      down=true
      el.style.cursor='grabbing'
      sx=e.clientX; sy=e.clientY
      ox = parseFloat(el.style.left)
      oy = parseFloat(el.style.top)
      selectElement(el, layer)
      window.addEventListener('pointermove', onmove)
      window.addEventListener('pointerup', onup)
    })
    function onmove(e){
      if(!down) return
      const dx = e.clientX - sx
      const dy = e.clientY - sy
      const nx = ox + dx
      const ny = oy + dy
      el.style.left = nx + 'px'
      el.style.top = ny + 'px'
      // update model
      const s = state.scenes[state.currentSceneIndex]
      const L = s.layers.find(l=>l.id===layer.id)
      if(L){L.position.x = nx; L.position.y = ny}
      updatePropsPanelFromSelected()
    }
    function onup(e){
      down=false
      el.style.cursor='grab'
      window.removeEventListener('pointermove', onmove)
      window.removeEventListener('pointerup', onup)
    }

    // resize with handle
    const handle = el.querySelector('.handle')
    handle.addEventListener('pointerdown', (ev)=>{
      ev.stopPropagation()
      let startX = ev.clientX
      let startY = ev.clientY
      const initScale = layer.scale
      function move(ev2){
        const dy = ev2.clientY - startY
        const snew = Math.max(0.1, initScale + dy/200)
        el.style.transform = `scale(${snew}) rotate(${layer.rotation}deg)`
        layer.scale = snew
        const s = state.scenes[state.currentSceneIndex]
        const L = s.layers.find(l=>l.id===layer.id)
        if(L) L.scale = snew
        updatePropsPanelFromSelected()
      }
      function up(){
        window.removeEventListener('pointermove', move)
        window.removeEventListener('pointerup', up)
      }
      window.addEventListener('pointermove', move)
      window.addEventListener('pointerup', up)
    })
  }

  // --- Selection & Properties ---
  function selectElement(domEl, layer){
    // deselect prev
    if(state.selectedElem) state.selectedElem.classList.remove('selected')
    state.selectedElem = domEl
    domEl.classList.add('selected')
    selectedInfo.textContent = layer.name || layer.id
    propX.value = Math.round(layer.position.x)
    propY.value = Math.round(layer.position.y)
    propRot.value = Math.round(layer.rotation)
    propScale.value = layer.scale
    propOpacity.value = layer.opacity
  }

  function updatePropsPanelFromSelected(){
    if(!state.selectedElem) return
    const lid = state.selectedElem.dataset.layerId
    const s = state.scenes[state.currentSceneIndex]
    const L = s.layers.find(l=>l.id===lid)
    if(!L) return
    selectedInfo.textContent = L.name
    propX.value = Math.round(L.position.x)
    propY.value = Math.round(L.position.y)
    propRot.value = Math.round(L.rotation)
    propScale.value = L.scale
    propOpacity.value = L.opacity
  }

  propX.addEventListener('input', ()=>{
    if(!state.selectedElem) return
    const lid = state.selectedElem.dataset.layerId
    const s = state.scenes[state.currentSceneIndex]
    const L = s.layers.find(l=>l.id===lid)
    L.position.x = Number(propX.value)
    state.selectedElem.style.left = L.position.x + 'px'
  })
  propY.addEventListener('input', ()=>{
    if(!state.selectedElem) return
    const lid = state.selectedElem.dataset.layerId
    const s = state.scenes[state.currentSceneIndex]
    const L = s.layers.find(l=>l.id===lid)
    L.position.y = Number(propY.value)
    state.selectedElem.style.top = L.position.y + 'px'
  })
  propRot.addEventListener('input', ()=>{
    if(!state.selectedElem) return
    const v = Number(propRot.value)
    const lid = state.selectedElem.dataset.layerId
    const s = state.scenes[state.currentSceneIndex]
    const L = s.layers.find(l=>l.id===lid)
    L.rotation = v
    const sc = L.scale || 1
    state.selectedElem.style.transform = `scale(${sc}) rotate(${v}deg)`
  })
  propScale.addEventListener('input', ()=>{
    if(!state.selectedElem) return
    const v = Number(propScale.value)
    const lid = state.selectedElem.dataset.layerId
    const s = state.scenes[state.currentSceneIndex]
    const L = s.layers.find(l=>l.id===lid)
    L.scale = v
    state.selectedElem.style.transform = `scale(${v}) rotate(${L.rotation}deg)`
  })
  propOpacity.addEventListener('input', ()=>{
    if(!state.selectedElem) return
    const v = Number(propOpacity.value)
    const lid = state.selectedElem.dataset.layerId
    const s = state.scenes[state.currentSceneIndex]
    const L = s.layers.find(l=>l.id===lid)
    L.opacity = v
    state.selectedElem.style.opacity = v
  })

  bringForwardBtn.addEventListener('click', ()=>{
    if(!state.selectedElem) return
    const lid = state.selectedElem.dataset.layerId
    const s = state.scenes[state.currentSceneIndex]
    const L = s.layers.find(l=>l.id===lid)
    if(!L) return
    // increase zIndex by 1
    const z = parseInt(state.selectedElem.style.zIndex || 0)
    state.selectedElem.style.zIndex = z+1
  })
  sendBackwardBtn.addEventListener('click', ()=>{
    if(!state.selectedElem) return
    const z = parseInt(state.selectedElem.style.zIndex || 0)
    state.selectedElem.style.zIndex = Math.max(0,z-1)
  })

  // --- Layers panel rendering ---
  function renderLayersPanel(){
    layersList.innerHTML = ''
    const s = state.scenes[state.currentSceneIndex]
    s.layers.slice().reverse().forEach(l=>{
      const div = document.createElement('div')
      div.className = 'layer-item'
      const mini = document.createElement('div')
      mini.className = 'mini'
      const img = document.createElement('img')
      const asset = state.assets.find(a=>a.id===l.assetId)
      img.src = asset ? asset.src : ''
      mini.appendChild(img)
      div.appendChild(mini)
      const info = document.createElement('div')
      info.style.flex = '1'
      info.innerHTML = `<div style="font-size:13px">${l.name}</div><div class="small-muted">${l.type}</div>`
      div.appendChild(info)
      const visBtn = document.createElement('button')
      visBtn.className = 'layer-item-button'
      visBtn.textContent = l.visible ? '👁' : '🚫'
      visBtn.addEventListener('click',()=>{
        l.visible = !l.visible
        // find dom
        const dom = stage.querySelector(`[data-layer-id="${l.id}"]`)
        if(dom) dom.style.display = l.visible ? 'block' : 'none'
        renderLayersPanel()
      })
      div.appendChild(visBtn)
      layersList.appendChild(div)

      div.addEventListener('click', ()=>{
        const dom = stage.querySelector(`[data-layer-id="${l.id}"]`)
        if(dom) selectElement(dom,l)
      })
    })
  }

  // --- Dialogue editor ---
  addLineBtn.addEventListener('click', ()=>{
    const s = state.scenes[state.currentSceneIndex]
    const line = {id:uid('d'), speaker:'Narrator', text:''}
    s.dialogue.push(line)
    renderDialogue()
  })

  function renderDialogue(){
    dialogLines.innerHTML = ''
    const s = state.scenes[state.currentSceneIndex]
    for(const dl of s.dialogue){
      const row = document.createElement('div')
      row.className = 'dialog-line'
      const sp = document.createElement('input')
      sp.type='text'; sp.value = dl.speaker; sp.style.width='160px'
      sp.addEventListener('input',()=>{dl.speaker = sp.value})
      const ta = document.createElement('textarea')
      ta.value = dl.text
      ta.addEventListener('input',()=>{dl.text = ta.value})
      const del = document.createElement('button')
      del.className='btn small danger'
      del.textContent='Delete'
      del.addEventListener('click',()=>{ s.dialogue = s.dialogue.filter(x=>x.id!==dl.id); renderDialogue() })
      row.appendChild(sp)
      row.appendChild(ta)
      row.appendChild(del)
      dialogLines.appendChild(row)
    }
  }

  // --- Scenes UI ---
  function renderScenes(){
    scenesList.innerHTML = ''
    state.scenes.forEach((sc,i)=>{
      const div = document.createElement('div')
      div.className = 'asset'
      div.style.width = '72px'; div.style.height='56px'
      div.textContent = sc.name
      div.title = sc.name
      if(i===state.currentSceneIndex) div.style.outline = '2px solid rgba(124,92,255,0.35)'
      div.addEventListener('click', ()=>{state.currentSceneIndex = i; renderAll()})
      scenesList.appendChild(div)
    })
    currentSceneName.textContent = state.scenes[state.currentSceneIndex].name
  }

  newSceneBtn.addEventListener('click', ()=>{ createScene('Сцена '+(state.scenes.length+1)); renderAll() })
  dupSceneBtn.addEventListener('click', ()=>{ duplicateScene(state.currentSceneIndex); renderAll() })
  delSceneBtn.addEventListener('click', ()=>{ removeScene(state.currentSceneIndex); renderAll() })
  prevSceneBtn.addEventListener('click', ()=>{ state.currentSceneIndex = Math.max(0, state.currentSceneIndex-1); renderAll() })
  nextSceneBtn.addEventListener('click', ()=>{ state.currentSceneIndex = Math.min(state.scenes.length-1, state.currentSceneIndex+1); renderAll() })

  // --- Groups UI ---
  addGroupBtn.addEventListener('click', ()=>{
    const g = {id:uid('g'),name:'Group '+(state.groups.length+1),music:'',sceneIds:[]}
    state.groups.push(g)
    renderGroups()
  })
  function renderGroups(){
    groupsList.innerHTML = ''
    state.groups.forEach(g=>{
      const div = document.createElement('div')
      div.className = 'asset'
      div.style.width='100%'; div.style.height='44px'; div.style.display='flex'; div.style.alignItems='center'
      const title = document.createElement('div')
      title.style.flex='1'; title.textContent = g.name
      const btn = document.createElement('button')
      btn.className='btn small'
      btn.textContent='Select'
      btn.addEventListener('click', ()=>{
        groupNameInput.value = g.name
        groupMusicInput.value = g.music
        // quick assign: add current scene to this group if not present
        if(!g.sceneIds.includes(state.scenes[state.currentSceneIndex].id)) g.sceneIds.push(state.scenes[state.currentSceneIndex].id)
        alert('Сцена добавлена в группу "'+g.name+'"')
      })
      div.appendChild(title); div.appendChild(btn)
      groupsList.appendChild(div)
    })
  }

  // --- Export ---
  exportBtn.addEventListener('click', async ()=>{
    const exportJson = buildExportJson()
    // send to backend
    try{
      const res = await fetch('/export', {
        method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(exportJson)
      })
      if(!res.ok) throw new Error('Export failed')
      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = (exportJson.name || 'vnred_project') + '_vnred_export.txt'
      document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url)
    }catch(err){
      alert('Ошибка экспорта: '+err.message)
    }
  })

  function buildExportJson(){
    const data = {
      projectId: uid('project'),
      name: 'Название VNRed',
      version: '1.0',
      assets: state.assets.map(a=>({id:a.id,name:a.name,filename:null,thumbnail:null,src:a.src})),
      groups: state.groups.map(g=>({id:g.id,name:g.name,music:g.music || null,loop:false,scenes: g.sceneIds.map(sid => buildSceneForExport(state.scenes.find(s=>s.id===sid) || {}))})),
      scenes: state.scenes.map(s=>buildSceneForExport(s)),
      exportedAt: new Date().toISOString()
    }
    return data
  }
  function buildSceneForExport(scene){
    if(!scene) return null
    return {
      id: scene.id,
      name: scene.name,
      layers: scene.layers.map(l=>({id:l.id,type:l.type,assetId:l.assetId,zIndex:0,position:l.position,rotation:l.rotation,scale:l.scale,flipX:l.flipX,opacity:l.opacity,visible:l.visible})),
      dialogue: scene.dialogue.map(d=>({id:d.id,speaker:d.speaker,text:d.text,meta:{}})),
      meta:{duration:null}
    }
  }

  // --- Rendering everything ---
  function renderAll(){
    renderAssets(); renderGroups(); renderScenes(); renderStage(); renderLayersPanel(); renderDialogue(); renderGroups()
  }

  function renderStage(){
    stage.innerHTML = ''
    const s = state.scenes[state.currentSceneIndex]
    // render layers
    for(const l of s.layers){
      const asset = state.assets.find(a=>a.id===l.assetId)
      if(!asset) continue
      const el = document.createElement('div')
      el.className = 'placed-item'
      el.dataset.layerId = l.id
      el.style.left = (l.position.x||100)+'px'
      el.style.top = (l.position.y||100)+'px'
      el.style.zIndex = 100
      el.style.opacity = (l.opacity==null?1:l.opacity)
      el.style.transform = `scale(${l.scale||1}) rotate(${l.rotation||0}deg)`
      const img = document.createElement('img')
      img.src = asset.src
      img.style.maxWidth = '320px'
      img.style.maxHeight = '480px'
      img.draggable = false
      el.appendChild(img)
      const h = document.createElement('div'); h.className='handle'
      el.appendChild(h)
      makeDraggable(el, l)
      stage.appendChild(el)
    }
  }

  // --- Stage click deselect ---
  stage.addEventListener('pointerdown',(e)=>{ if(e.target===stage) { if(state.selectedElem) state.selectedElem.classList.remove('selected'); state.selectedElem=null; selectedInfo.textContent='None' } })

  // --- Init ---
  init()

})()