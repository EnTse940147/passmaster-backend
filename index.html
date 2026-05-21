<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PassMaster</title>
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,sans-serif;background:#060606;color:#e0e0e0;min-height:100vh}
nav{position:sticky;top:0;z-index:100;background:rgba(6,6,6,.95);border-bottom:1px solid #181818}
.nw{max-width:1060px;margin:0 auto;padding:0 16px;display:flex;align-items:center;height:52px;gap:8px;flex-wrap:wrap}
.logo{font-weight:900;font-size:18px;cursor:pointer;white-space:nowrap}
.nb{background:none;border:none;color:#666;cursor:pointer;padding:5px 9px;border-radius:6px;font-size:13px;font-weight:500}
.nb.on{color:#fff;background:#1a1a1a}
#app{max-width:900px;margin:0 auto;padding:16px}
.hero{text-align:center;padding:50px 0 36px}
.htag{display:inline-block;background:#0a2918;color:#4ade80;border:1px solid #14532d;border-radius:20px;padding:4px 14px;font-size:13px;font-weight:600;margin-bottom:12px}
.htitle{font-size:clamp(40px,10vw,76px);font-weight:900;letter-spacing:-3px;background:linear-gradient(135deg,#fff 35%,#4ade80);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:12px}
.hdesc{color:#888;font-size:15px;line-height:1.8;margin-bottom:24px}
.card{background:#0d0d0d;border:1px solid #1c1c1c;border-radius:14px;padding:20px;margin-bottom:20px}
.stag{background:#0a2918;color:#4ade80;border:1px solid #14532d;border-radius:20px;padding:5px 14px;font-size:13px;font-weight:700}
.sdesc{color:#555;font-size:13px;margin-top:8px;margin-bottom:16px}
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}
.tab{background:none;border:1px solid #222;color:#666;cursor:pointer;padding:6px 14px;border-radius:8px;font-size:13px;font-weight:600}
.tab.on{background:#1a1a1a;color:#4ade80;border-color:#4ade80}
.field{margin-bottom:14px}
.field label{display:block;font-size:13px;color:#666;font-weight:600;margin-bottom:5px}
.inp{background:#0a0a0a;border:1px solid #222;border-radius:10px;padding:12px 15px;color:#e0e0e0;font-size:16px;outline:none;width:100%}
.pww{position:relative}
.pwi{background:#0a0a0a;border:1px solid #222;border-radius:10px;padding:12px 44px 12px 15px;color:#e0e0e0;font-size:16px;outline:none;width:100%}
.pwb{position:absolute;right:10px;top:50%;transform:translateY(-50%);background:none;border:none;color:#666;cursor:pointer;font-size:16px;padding:4px}
.btn{background:linear-gradient(135deg,#16a34a,#15803d);color:#fff;border:none;border-radius:10px;padding:13px;font-size:16px;font-weight:700;cursor:pointer;width:100%;margin-top:4px}
.btn:disabled{opacity:0.6;cursor:not-allowed}
.bto{background:none;border:1px solid #333;color:#ccc;width:auto;padding:10px 18px;font-size:14px;border-radius:10px;cursor:pointer}
.err{background:#1f0a0a;border:1px solid #7f1d1d;border-radius:8px;padding:10px 14px;color:#fca5a5;font-size:14px;margin-bottom:12px}
.info{background:#0a1f2a;border:1px solid #164e63;border-radius:8px;padding:10px 14px;color:#7dd3fc;font-size:13px;margin-bottom:12px}
.scard{background:#0a0a0a;border:1px solid #14532d;border-radius:12px;padding:18px;margin-top:16px}
.stitle{color:#4ade80;font-weight:700;margin-bottom:12px}
.pimg{width:100%;max-height:320px;object-fit:contain;border-radius:8px;background:#111;display:block;margin-bottom:10px}
.rmeta{display:flex;gap:12px;font-size:12px;color:#4ade80;margin-bottom:12px;flex-wrap:wrap}
.dlg{display:flex;gap:10px;flex-wrap:wrap}
.dlg a{flex:1;min-width:120px;text-decoration:none}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;margin-top:4px}
.pc{background:#0d0d0d;border:1px solid;border-radius:12px;padding:16px;cursor:pointer;display:flex;flex-direction:column;gap:5px}
.fg{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}
.fc{background:#111;border:1px solid #1a1a1a;border-radius:12px;padding:16px}
.faq{background:#0d0d0d;border:1px solid #1a1a1a;border-radius:10px;padding:14px 16px;cursor:pointer;margin-bottom:8px}
.faqq{display:flex;justify-content:space-between;font-weight:600;font-size:14px;align-items:center}
.faqa{color:#777;font-size:13px;margin-top:10px;line-height:1.7;display:none}
.step{display:flex;gap:12px;align-items:flex-start;background:#0d0d0d;border:1px solid #1a1a1a;border-radius:12px;padding:16px;margin-bottom:10px}
.stn{width:30px;height:30px;background:linear-gradient(135deg,#16a34a,#15803d);border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;flex-shrink:0;font-size:14px}
h2{font-size:22px;font-weight:800;margin-bottom:18px;letter-spacing:-0.5px}
footer{background:#040404;border-top:1px solid #111;margin-top:40px;padding:36px 16px 0}
.fw{max-width:900px;margin:0 auto;display:flex;justify-content:space-between;flex-wrap:wrap;gap:24px;padding-bottom:24px}
.fl{font-weight:800;font-size:16px;margin-bottom:6px}
.fct{font-weight:700;font-size:13px;color:#ccc;margin-bottom:8px}
.flk{background:none;border:none;color:#444;cursor:pointer;font-size:13px;display:block;padding:2px 0;text-align:left}
.fb{text-align:center;color:#222;font-size:12px;padding:14px;border-top:1px solid #111}
.hidden{display:none}
.sec{padding:36px 0}
.ts-wrap{margin-bottom:14px}
</style>
</head>
<body>
<nav>
  <div class="nw">
    <div class="logo" onclick="go('home')">🔐 PassMaster</div>
    <button class="nb on" id="nb-home" onclick="go('home')">首頁</button>
    <button class="nb" id="nb-risu" onclick="go('risu')">Risu</button>
    <button class="nb" id="nb-myppt" onclick="go('myppt')">MyPPT</button>
    <button class="nb" id="nb-lurl" onclick="go('lurl')">Lurl</button>
    <button class="nb" id="nb-imgus" onclick="go('imgus')">Imgus</button>
    <button class="nb" id="nb-ppt" onclick="go('ppt')">PPt.cc</button>
    <button class="nb" id="nb-help" onclick="go('help')">使用教學</button>
    <button class="nb" id="nb-about" onclick="go('about')">關於我們</button>
  </div>
</nav>
<div id="app"></div>
<footer>
  <div class="fw">
    <div><div class="fl">🔐 PassMaster</div><div style="color:#444;font-size:13px">短網址檔案備份工具</div></div>
    <div style="display:flex;gap:32px;flex-wrap:wrap">
      <div>
        <div class="fct">服務</div>
        <button class="flk" onclick="go('risu')">Risu</button>
        <button class="flk" onclick="go('myppt')">MyPPT</button>
        <button class="flk" onclick="go('lurl')">Lurl</button>
        <button class="flk" onclick="go('imgus')">Imgus</button>
        <button class="flk" onclick="go('ppt')">PPt.cc</button>
      </div>
      <div>
        <div class="fct">快速連結</div>
        <button class="flk" onclick="go('home')">首頁</button>
        <button class="flk" onclick="go('help')">使用教學</button>
        <button class="flk" onclick="go('about')">關於我們</button>
      </div>
    </div>
  </div>
  <div class="fb">© PassMaster. All rights reserved.</div>
</footer>
<script>
const TURNSTILE_SITE_KEY = "0x4AAAAAADTd3BcMtgTk1iPO";
const CORS_PROXIES = [
  "https://corsproxy.io/?url=",
  "https://api.allorigins.win/raw?url=",
  "https://thingproxy.freeboard.io/fetch/",
];
const PLATS = [
  {id:"risu", name:"Risu", color:"#ff6b6b", domain:"risu.io"},
  {id:"myppt",name:"MyPPT",color:"#4ecdc4",domain:"myppt.cc"},
  {id:"lurl", name:"Lurl", color:"#45b7d1",domain:"lurl.cc"},
  {id:"imgus",name:"Imgus",color:"#96ceb4",domain:"imgus.net"},
  {id:"ppt",  name:"PPt.cc",color:"#ffd93d",domain:"ppt.cc"},
  {id:"mork", name:"Mork", color:"#c084fc",domain:"mork.cc",off:true},
];
let tab = "smart";

// 從瀏覽器直接抓頁面，用 CORS proxy 中轉
async function fetchPage(url) {
  for (const proxy of CORS_PROXIES) {
    try {
      const res = await fetch(proxy + encodeURIComponent(url), {
        headers: { "User-Agent": "Mozilla/5.0" },
        signal: AbortSignal.timeout(15000),
      });
      if (res.ok) {
        const text = await res.text();
        if (text && text.length > 100 && !text.includes("just a moment")) {
          return text;
        }
      }
    } catch(e) { continue; }
  }
  return null;
}

async function postForm(action, data, referer) {
  const body = new URLSearchParams(data).toString();
  for (const proxy of CORS_PROXIES) {
    try {
      const res = await fetch(proxy + encodeURIComponent(action), {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "Referer": referer,
        },
        body,
        signal: AbortSignal.timeout(15000),
      });
      if (res.ok) {
        const text = await res.text();
        if (text && text.length > 100) return text;
      }
    } catch(e) { continue; }
  }
  return null;
}

function makeAbsolute(src, base) {
  if (!src) return "";
  if (src.startsWith("http")) return src;
  try {
    const b = new URL(base);
    if (src.startsWith("//")) return b.protocol + src;
    if (src.startsWith("/")) return b.origin + src;
    return new URL(src, base).href;
  } catch { return src; }
}

function extractMedia(html, baseUrl) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, "text/html");

  // 影片
  const video = doc.querySelector("video");
  if (video) {
    const src = video.src || video.querySelector("source")?.src;
    if (src && !src.startsWith("blob:")) return {type:"video", url: makeAbsolute(src, baseUrl)};
  }

  // 音檔
  const audio = doc.querySelector("audio");
  if (audio) {
    const src = audio.src || audio.querySelector("source")?.src;
    if (src) return {type:"audio", url: makeAbsolute(src, baseUrl)};
  }

  // script 裡找媒體 URL
  for (const script of doc.querySelectorAll("script")) {
    const text = script.textContent || "";
    const m = text.match(/["'](https?:\/\/[^"']+\.(mp4|m3u8|jpg|jpeg|png|gif|webp|mp3|ogg)(\?[^"']*)?)['"]/);
    if (m) {
      const ext = m[2].toLowerCase();
      const t = ["mp4","m3u8"].includes(ext) ? "video" : ["mp3","ogg"].includes(ext) ? "audio" : "image";
      return {type: t, url: m[1]};
    }
  }

  // og:image
  const og = doc.querySelector('meta[property="og:image"]');
  if (og?.content && !og.content.includes("logo") && !og.content.includes("placeholder")) {
    return {type:"image", url: makeAbsolute(og.content, baseUrl)};
  }

  // data-src
  for (const img of doc.querySelectorAll("img[data-src]")) {
    const src = img.dataset.src;
    if (src && !["logo","icon","avatar","favicon"].some(x=>src.toLowerCase().includes(x))) {
      return {type:"image", url: makeAbsolute(src, baseUrl)};
    }
  }

  // img
  for (const img of doc.querySelectorAll("img")) {
    const src = img.src || img.getAttribute("src");
    if (src && src.startsWith("http") && !["logo","icon","avatar","favicon","banner","placeholder"].some(x=>src.toLowerCase().includes(x))) {
      return {type:"image", url: src};
    }
  }

  // a href 媒體連結
  for (const a of doc.querySelectorAll("a[href]")) {
    const href = a.href;
    const m = href.match(/\.(mp4|jpg|jpeg|png|gif|webp|mp3|ogg)(\?|$)/i);
    if (m) {
      const ext = m[1].toLowerCase();
      const t = ext==="mp4" ? "video" : ["mp3","ogg"].includes(ext) ? "audio" : "image";
      return {type: t, url: href};
    }
  }

  return null;
}

function needsPassword(html) {
  return html.toLowerCase().includes('type="password"') || html.toLowerCase().includes("type='password'");
}

function findForm(html, pageUrl) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, "text/html");
  const form = doc.querySelector("form");
  if (!form) return null;
  let action = form.getAttribute("action") || pageUrl;
  if (!action.startsWith("http")) {
    try { action = new URL(action, pageUrl).href; } catch {}
  }
  const data = {};
  for (const inp of form.querySelectorAll("input")) {
    const name = inp.getAttribute("name");
    if (name) data[name] = inp.value || "";
  }
  return {action, data, method: (form.getAttribute("method")||"post").toLowerCase()};
}

function guessFilename(url, type) {
  try {
    const path = new URL(url).pathname;
    const name = path.split("/").pop();
    if (name && name.includes(".")) return name;
    const ext = {image:"jpg",video:"mp4",audio:"mp3"}[type]||"bin";
    return "backup_" + (name||"file") + "." + ext;
  } catch { return "backup." + (type||"bin"); }
}

function getTurnstileToken() {
  const el = document.querySelector('[name="cf-turnstile-response"]');
  return el ? el.value : "";
}
function resetTurnstile() {
  if (window.turnstile) window.turnstile.reset();
}
function initTurnstile() {
  setTimeout(() => {
    const container = document.getElementById("turnstile-container");
    if (container && window.turnstile) {
      container.innerHTML = "";
      window.turnstile.render(container, {sitekey: TURNSTILE_SITE_KEY, theme:"dark"});
    }
  }, 200);
}

function go(page) {
  document.querySelectorAll(".nb").forEach(b=>b.classList.remove("on"));
  const nb = document.getElementById("nb-"+page);
  if(nb) nb.classList.add("on");
  const app = document.getElementById("app");

  if(page==="help"){
    app.innerHTML=`<div style="padding:30px 0 50px">
      <h2>使用教學</h2>
      ${[["1","貼上連結","將短網址貼入輸入欄位，系統自動辨識平台。"],
         ["2","輸入密碼","如有密碼保護，請填入密碼。"],
         ["3","完成驗證","點選「我不是機器人」完成人機驗證。"],
         ["4","開始備份","點擊查詢，系統從您的瀏覽器直接抓取內容。"],
         ["5","下載備份","完成後預覽並下載檔案。"]
        ].map(([n,t,d])=>`<div class="step"><div class="stn">${n}</div><div><b>${t}</b><div style="color:#777;font-size:14px;margin-top:3px">${d}</div></div></div>`).join("")}
    </div>`;
    return;
  }
  if(page==="about"){
    app.innerHTML=`<div style="padding:30px 0 50px"><h2>關於我們</h2><p style="color:#888;line-height:1.8;max-width:600px">PassMaster 是一款專為短網址檔案備份設計的線上工具，支援 Risu、MyPPT、Lurl、Imgus、PPt.cc 等主流平台。本工具僅供個人備份使用。</p></div>`;
    return;
  }
  const pp = PLATS.find(p=>p.id===page);
  if(pp){
    app.innerHTML=`<div style="padding:30px 0 50px"><h2 style="color:${pp.color}">${pp.name} 備份</h2><div class="card">${tool(pp.id)}</div></div>`;
    initTurnstile();
    return;
  }

  app.innerHTML=`
  <div class="hero">
    <div class="htag">短網址檔案備份工具</div>
    <div class="htitle">PassMaster</div>
    <div class="hdesc">整合 Risu、MyPPT、Lurl、Imgus、PPt.cc<br>在連結過期前安全備份您的圖片、影片與音檔</div>
    <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
      <button class="btn" style="width:auto;padding:11px 22px" onclick="document.getElementById('ts').scrollIntoView({behavior:'smooth'})">🚀 立即備份</button>
      <button class="bto" onclick="go('help')">📖 使用教學</button>
    </div>
  </div>
  <div id="ts" class="card">
    <div class="stag">⚡ Smart 智慧模式</div>
    <div class="sdesc">貼上任意短網址，自動辨識平台並備份</div>
    <div class="tabs" id="tabs">${renderTabs()}</div>
    <div id="ta">${tool(null)}</div>
  </div>
  <div class="sec">
    <h2>支援平台</h2>
    <div class="pgrid">
      ${PLATS.map(p=>`<div class="pc" style="border-color:${p.color}44;opacity:${p.off?.5:1}" onclick="${p.off?'':(`go('${p.id}')`)}">
        <div style="width:9px;height:9px;border-radius:50%;background:${p.color}"></div>
        <div style="font-weight:700;font-size:15px">${p.name}</div>
        <div style="color:#555;font-size:12px">${p.domain}</div>
        ${p.off?`<span style="font-size:12px;color:#444">暫無服務</span>`:`<span style="font-size:13px;font-weight:600;color:${p.color}">前往備份 →</span>`}
      </div>`).join("")}
    </div>
  </div>
  <div style="background:#0a0a0a;padding:36px 16px;margin:0 -16px">
    <div style="max-width:900px;margin:0 auto">
      <h2>功能特色</h2>
      <div class="fg">
        ${[["🌐","多平台支援","整合五大短網址平台"],["⚡","智慧辨識","自動辨識平台"],["📁","多種格式","圖片影片音檔全支援"],["🔐","密碼保護","支援密碼保護連結"],["🛡","人機驗證","防止濫用保護服務"],["💸","完全免費","所有功能免費"]].map(([i,t,d])=>`<div class="fc"><div style="font-size:26px;margin-bottom:8px">${i}</div><div style="font-weight:700">${t}</div><div style="color:#555;font-size:13px;margin-top:4px">${d}</div></div>`).join("")}
      </div>
    </div>
  </div>
  <div class="sec">
    <h2>常見問題</h2>
    ${[["PassMaster 是什麼？","一款短網址檔案備份工具，在連結過期前幫您保存圖片、影片和音檔。"],
       ["為什麼備份失敗？","可能原因：連結已過期、密碼錯誤、或來源平台暫時無法連線。"],
       ["支援哪些格式？","JPG、PNG、GIF、WebP、MP4、MP3、OGG 等常見格式。"],
       ["為什麼需要人機驗證？","防止機器人濫用服務，保護平台穩定運作。"]
      ].map(([q,a],i)=>`<div class="faq" onclick="tfaq(${i})"><div class="faqq"><span>${q}</span><span id="fa${i}">▾</span></div><div class="faqa" id="faa${i}">${a}</div></div>`).join("")}
  </div>`;
  initTurnstile();
}

function renderTabs(){
  return ["smart",...PLATS.filter(p=>!p.off).map(p=>p.id)].map(id=>{
    const p=PLATS.find(x=>x.id===id);
    const on=tab===id;
    const style=on&&p?`style="color:${p.color};border-color:${p.color}"`:"";
    return `<button class="tab${on?' on':''}" ${style} onclick="setTab('${id}')">${id==="smart"?"⚡ Smart":p?.name}</button>`;
  }).join("");
}

function setTab(id){
  tab=id;
  const el=document.getElementById("tabs");
  if(el) el.innerHTML=renderTabs();
  const ta=document.getElementById("ta");
  if(ta){ ta.innerHTML=tool(id==="smart"?null:id); initTurnstile(); }
}

function tool(pid){
  const p=PLATS.find(x=>x.id===pid);
  if(p?.off) return `<div style="text-align:center;padding:40px;color:#666"><div style="font-size:36px">🚧</div><div style="margin-top:8px">此平台目前暫無服務</div></div>`;
  const badge=p?`<div style="display:flex;align-items:center;gap:8px;border:1px solid ${p.color}66;background:${p.color}11;border-radius:8px;padding:8px 14px;margin-bottom:14px"><span style="color:${p.color};font-weight:700">${p.name}</span><span style="color:#666;font-size:13px">· ${p.domain}</span></div>`:"";
  const ph=p?`輸入 ${p.name} 短網址...`:"貼上任意短網址，自動辨識平台...";
  return `${badge}
  <div class="field"><label>短網址連結</label><input class="inp" id="ui" type="url" placeholder="${ph}" autocomplete="off" autocorrect="off" autocapitalize="off" onkeydown="if(event.key==='Enter')doFetch()"></div>
  <div class="field"><label>密碼（選填）</label><div class="pww"><input class="pwi" id="pi" type="password" placeholder="如連結有密碼保護，請輸入密碼" autocomplete="off" autocorrect="off" autocapitalize="off"><button class="pwb" id="ptb" onclick="tpw()" type="button">👁</button></div></div>
  <div class="ts-wrap"><div id="turnstile-container"></div></div>
  <div class="err hidden" id="eb"></div>
  <button class="btn" id="fb" onclick="doFetch()">🔍 開始備份查詢</button>
  <div id="rb"></div>`;
}

function tpw(){
  const i=document.getElementById("pi");
  const b=document.getElementById("ptb");
  if(!i)return;
  i.type=i.type==="password"?"text":"password";
  b.textContent=i.type==="password"?"👁":"🙈";
}

function tfaq(i){
  const a=document.getElementById("faa"+i);
  const arr=document.getElementById("fa"+i);
  if(!a)return;
  const open=a.style.display==="block";
  a.style.display=open?"none":"block";
  arr.style.transform=open?"none":"rotate(180deg)";
}

async function doFetch(){
  const ui=document.getElementById("ui");
  const pi=document.getElementById("pi");
  const eb=document.getElementById("eb");
  const rb=document.getElementById("rb");
  const fb=document.getElementById("fb");
  if(!ui||!eb||!rb||!fb)return;

  const url=ui.value.trim();
  const pw=pi?pi.value.trim():"";
  const token=getTurnstileToken();

  if(!url){eb.textContent="⚠️ 請輸入短網址連結";eb.classList.remove("hidden");return;}
  if(!token){eb.textContent="⚠️ 請先完成人機驗證";eb.classList.remove("hidden");return;}

  eb.classList.add("hidden");
  rb.innerHTML="";
  fb.textContent="🔄 查詢中，請稍候...";
  fb.disabled=true;

  try {
    // 第一次抓頁面
    let html = await fetchPage(url);
    if (!html) {
      throw new Error("無法連線到目標網站，請稍後再試");
    }

    // 需要密碼就提交表單
    if (needsPassword(html)) {
      if (!pw) throw new Error("此連結需要密碼，請輸入密碼後再試");
      const formInfo = findForm(html, url);
      if (formInfo) {
        // 填入密碼
        for (const key of Object.keys(formInfo.data)) {
          if (["pass","pw","password","pwd","secret"].some(x=>key.toLowerCase().includes(x))) {
            formInfo.data[key] = pw;
          }
        }
        html = await postForm(formInfo.action, formInfo.data, url);
        if (!html) throw new Error("密碼提交失敗，請稍後再試");
      }
    }

    // 解析媒體
    const media = extractMedia(html, url);
    fb.textContent="🔍 開始備份查詢";
    fb.disabled=false;
    resetTurnstile();

    if (!media) {
      eb.textContent="⚠️ 查無媒體內容，連結可能已過期或密碼錯誤";
      eb.classList.remove("hidden");
      return;
    }

    const filename = guessFilename(media.url, media.type);
    const proxy = `https://images.weserv.nl/?url=${encodeURIComponent(media.url)}`;
    let mediaHtml = "";
    if(media.type==="image") mediaHtml=`<img class="pimg" src="${media.url}" onerror="this.src='${proxy}'" alt="預覽">`;
    else if(media.type==="video") mediaHtml=`<video class="pimg" src="${media.url}" controls></video>`;
    else if(media.type==="audio") mediaHtml=`<audio src="${media.url}" controls style="width:100%;margin-bottom:10px"></audio>`;

    rb.innerHTML=`<div class="scard">
      <div class="stitle">✅ 備份成功</div>
      ${mediaHtml}
      <div class="rmeta"><span>📄 ${filename}</span></div>
      <div class="dlg">
        <a href="${media.url}" download="${filename}" target="_blank"><button class="btn" style="background:linear-gradient(135deg,#059669,#047857)">⬇ 下載檔案</button></a>
        <a href="${media.url}" target="_blank" style="flex:1;min-width:110px"><button class="bto" style="width:100%">🔗 開啟連結</button></a>
      </div>
    </div>`;

  } catch(e) {
    fb.textContent="🔍 開始備份查詢";
    fb.disabled=false;
    resetTurnstile();
    eb.textContent="⚠️ " + e.message;
    eb.classList.remove("hidden");
  }
}

go("home");
</script>
</body>
</html>
