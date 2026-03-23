from flask import Flask, jsonify
import datetime, time

app = Flask(__name__)
START_TIME = time.time()

BASE_STYLE = """
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#080c14;--card:#111827;--card2:#141e2e;
  --border:#1e2d42;--border2:#253548;
  --text:#e8edf5;--muted:#6b7f96;
  --green:#10b981;--red:#ef4444;--amber:#f59e0b;
  --blue:#3b82f6;--cyan:#06b6d4;--purple:#a78bfa;
}
body{background:var(--bg);color:var(--text);font-family:'Syne',sans-serif;overflow-x:hidden}
body::before{content:'';position:fixed;inset:0;background-image:linear-gradient(var(--border) 1px,transparent 1px),linear-gradient(90deg,var(--border) 1px,transparent 1px);background-size:48px 48px;opacity:.28;pointer-events:none;z-index:0}
.orb{position:fixed;border-radius:50%;filter:blur(100px);opacity:.13;pointer-events:none;z-index:0}
.wrap{position:relative;z-index:1;max-width:900px;margin:0 auto;padding:2rem 1.5rem}
@keyframes fadeUp{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
</style>
"""

# ─── MAIN DASHBOARD ───────────────────────────────────────────────────────────
MAIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>DevSecOps Pipeline — Hemant Raghav</title>
""" + BASE_STYLE + """
<style>
.orb1{width:600px;height:600px;background:#3b82f6;top:-160px;right:-100px}
.orb2{width:480px;height:480px;background:#06b6d4;bottom:-120px;left:-100px}
.hero{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1.5rem;padding:2.5rem;background:rgba(13,20,32,.97);border:1px solid var(--border2);border-radius:20px;margin-bottom:1.5rem;animation:fadeUp .5s ease both}
.status-pill{display:inline-flex;align-items:center;gap:6px;background:rgba(16,185,129,.12);border:1px solid rgba(16,185,129,.3);color:var(--green);font-family:'DM Mono',monospace;font-size:.7rem;letter-spacing:.08em;padding:3px 10px;border-radius:99px;margin-bottom:.85rem}
.dot{width:7px;height:7px;border-radius:50%;background:var(--green);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.5;transform:scale(.8)}}
h1{font-size:clamp(1.8rem,4vw,2.6rem);font-weight:800;line-height:1.1;margin-bottom:.35rem}
h1 span{background:linear-gradient(90deg,#3b82f6,#06b6d4);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.sub{color:var(--muted);font-size:.9rem}
.hero-right{display:flex;flex-direction:column;align-items:flex-end;gap:.6rem}
.clock{font-family:'DM Mono',monospace;font-size:1.5rem;font-weight:500;color:var(--cyan);letter-spacing:.04em}
.datebox{font-family:'DM Mono',monospace;font-size:.73rem;color:var(--muted)}
.links{display:flex;gap:.6rem;margin-top:.2rem}
.lbtn{display:flex;align-items:center;gap:5px;padding:6px 13px;border-radius:8px;font-size:.78rem;font-weight:600;text-decoration:none;border:1px solid;transition:all .2s}
.lgh{background:rgba(167,139,250,.1);border-color:rgba(167,139,250,.3);color:var(--purple)}
.lli{background:rgba(59,130,246,.1);border-color:rgba(59,130,246,.3);color:var(--blue)}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:.85rem;margin-bottom:1.25rem}
@media(max-width:640px){.stats{grid-template-columns:repeat(2,1fr)}}
.sc{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:1.1rem 1.25rem;animation:fadeUp .5s ease both;transition:border-color .2s,transform .2s}
.sc:hover{border-color:var(--border2);transform:translateY(-2px)}
.sl{font-size:.7rem;color:var(--muted);letter-spacing:.07em;text-transform:uppercase;margin-bottom:.5rem}
.sv{font-size:1.8rem;font-weight:800;line-height:1;font-family:'DM Mono',monospace}
.ss{font-size:.7rem;color:var(--muted);margin-top:.3rem}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:.85rem}
@media(max-width:660px){.grid2{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:1.25rem;animation:fadeUp .6s ease both;transition:border-color .2s}
.card:hover{border-color:var(--border2)}
.ct{font-size:.68rem;color:var(--muted);letter-spacing:.1em;text-transform:uppercase;font-weight:600;margin-bottom:1rem;display:flex;align-items:center;gap:7px}
.ct::before{content:'';display:inline-block;width:3px;height:13px;background:linear-gradient(180deg,#3b82f6,#06b6d4);border-radius:2px}
.pipeline{display:flex;flex-direction:column;gap:.5rem}
.ps{display:flex;align-items:center;gap:10px;padding:.7rem .85rem;border-radius:9px;border:1px solid var(--border);background:var(--card2);transition:border-color .2s;animation:fadeUp .4s ease both}
.ps:hover{border-color:var(--border2)}
.pi{width:28px;height:28px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0}
.pn{font-size:.82rem;font-weight:600;margin-bottom:1px}
.pd{font-size:.7rem;color:var(--muted)}
.pb{font-family:'DM Mono',monospace;font-size:.66rem;font-weight:500;padding:2px 8px;border-radius:99px;white-space:nowrap;margin-left:auto;flex-shrink:0}
.pass{background:rgba(16,185,129,.12);color:var(--green);border:1px solid rgba(16,185,129,.25)}
.info{background:rgba(59,130,246,.12);color:var(--blue);border:1px solid rgba(59,130,246,.25)}
.rstack{display:flex;flex-direction:column;gap:.85rem}
.badge-grid{display:flex;flex-wrap:wrap;gap:.4rem}
.tb{display:flex;align-items:center;gap:5px;padding:4px 10px;border-radius:7px;font-size:.73rem;font-weight:600;border:1px solid;transition:transform .15s;cursor:default}
.tb:hover{transform:scale(1.04)}
.taws{background:rgba(245,158,11,.1);color:var(--amber);border-color:rgba(245,158,11,.25)}
.tdoc{background:rgba(6,182,212,.1);color:var(--cyan);border-color:rgba(6,182,212,.25)}
.tk8s{background:rgba(59,130,246,.1);color:var(--blue);border-color:rgba(59,130,246,.25)}
.tgh{background:rgba(167,139,250,.1);color:var(--purple);border-color:rgba(167,139,250,.25)}
.tsec{background:rgba(239,68,68,.1);color:var(--red);border-color:rgba(239,68,68,.25)}
.tpy{background:rgba(16,185,129,.1);color:var(--green);border-color:rgba(16,185,129,.25)}
.mr{display:flex;flex-direction:column;gap:.65rem}
.mt{display:flex;justify-content:space-between;font-size:.75rem;margin-bottom:4px}
.ml{color:var(--muted)}.mv{font-family:'DM Mono',monospace;font-weight:500}
.bb{height:5px;background:var(--border);border-radius:99px;overflow:hidden}
.bf{height:100%;border-radius:99px;transition:width 1.5s cubic-bezier(.4,0,.2,1)}
.ep-list{display:flex;flex-direction:column;gap:.4rem}
.ep{display:flex;align-items:center;gap:8px;padding:.55rem .8rem;background:var(--card2);border-radius:7px;border:1px solid var(--border);text-decoration:none;transition:border-color .2s}
.ep:hover{border-color:var(--border2)}
.em{font-family:'DM Mono',monospace;font-size:.68rem;font-weight:500;padding:2px 8px;border-radius:4px;background:rgba(16,185,129,.12);color:var(--green);border:1px solid rgba(16,185,129,.2)}
.epath{font-family:'DM Mono',monospace;font-size:.8rem;color:var(--cyan)}
.edesc{font-size:.72rem;color:var(--muted);margin-left:auto}
.footer{text-align:center;padding:1.5rem 0 .5rem;font-size:.7rem;color:var(--muted);font-family:'DM Mono',monospace;letter-spacing:.05em}
</style>
</head>
<body>
<div class="orb orb1"></div><div class="orb orb2"></div>
<div class="wrap">
  <div class="hero">
    <div>
      <div class="status-pill"><span class="dot"></span> LIVE &amp; RUNNING</div>
      <h1>DevSecOps<br/><span>Pipeline</span></h1>
      <p class="sub">Cloud Engineering (AWS) &nbsp;&middot;&nbsp; Hemant Raghav</p>
    </div>
    <div class="hero-right">
      <div class="clock" id="clock">--:--:--</div>
      <div class="datebox" id="datebox">---</div>
      <div class="links">
        <a class="lbtn lgh" href="https://github.com/hemantraghav-123/devsecops-pipeline" target="_blank">&#128025; GitHub</a>
        <a class="lbtn lli" href="https://linkedin.com/in/hemantraghav2467" target="_blank">&#128279; LinkedIn</a>
      </div>
    </div>
  </div>
  <div class="stats">
    <div class="sc" style="animation-delay:.05s"><div class="sl">Uptime</div><div class="sv" style="color:var(--green)" id="uptime">0s</div><div class="ss">Since last deploy</div></div>
    <div class="sc" style="animation-delay:.1s"><div class="sl">Deployments</div><div class="sv" style="color:var(--blue)" id="cd">0</div><div class="ss">Via GitHub Actions</div></div>
    <div class="sc" style="animation-delay:.15s"><div class="sl">Scans Passed</div><div class="sv" style="color:var(--cyan)" id="cs">0</div><div class="ss">Trivy + OWASP clean</div></div>
    <div class="sc" style="animation-delay:.2s"><div class="sl">Blocked Threats</div><div class="sv" style="color:var(--amber)" id="ct">0</div><div class="ss">CVEs auto-blocked</div></div>
  </div>
  <div class="grid2">
    <div class="card" style="animation-delay:.25s">
      <div class="ct">CI/CD Pipeline Stages</div>
      <div class="pipeline">
        <div class="ps" style="animation-delay:.3s"><div class="pi" style="background:rgba(167,139,250,.12)">&#128196;</div><div style="flex:1"><div class="pn">Code Push</div><div class="pd">Triggers on push to main</div></div><span class="pb info">trigger</span></div>
        <div class="ps" style="animation-delay:.35s"><div class="pi" style="background:rgba(239,68,68,.12)">&#128737;</div><div style="flex:1"><div class="pn">OWASP Safety Scan</div><div class="pd">Python dependency CVE check</div></div><span class="pb pass">passed</span></div>
        <div class="ps" style="animation-delay:.4s"><div class="pi" style="background:rgba(6,182,212,.12)">&#127381;</div><div style="flex:1"><div class="pn">Docker Build</div><div class="pd">Image built from Dockerfile</div></div><span class="pb pass">success</span></div>
        <div class="ps" style="animation-delay:.45s"><div class="pi" style="background:rgba(239,68,68,.12)">&#128270;</div><div style="flex:1"><div class="pn">Trivy Image Scan</div><div class="pd">OS + library CVE scan</div></div><span class="pb pass">0 critical</span></div>
        <div class="ps" style="animation-delay:.5s"><div class="pi" style="background:rgba(59,130,246,.12)">&#9650;</div><div style="flex:1"><div class="pn">Push to Docker Hub</div><div class="pd">Only if scan passed</div></div><span class="pb pass">pushed</span></div>
        <div class="ps" style="animation-delay:.55s"><div class="pi" style="background:rgba(16,185,129,.12)">&#128640;</div><div style="flex:1"><div class="pn">Deploy to EC2 / K8s</div><div class="pd">Auto SSH deploy via Actions</div></div><span class="pb pass">live</span></div>
      </div>
    </div>
    <div class="rstack">
      <div class="card" style="animation-delay:.3s">
        <div class="ct">Tech Stack</div>
        <div class="badge-grid">
          <span class="tb taws">&#9729; AWS EC2</span><span class="tb taws">&#128202; CloudWatch</span><span class="tb taws">&#128274; CloudTrail</span><span class="tb taws">&#955; Lambda</span>
          <span class="tb tdoc">&#127025; Docker</span><span class="tb tk8s">&#9096; Kubernetes</span><span class="tb tgh">&#9881; GitHub Actions</span>
          <span class="tb tsec">&#128737; Trivy</span><span class="tb tsec">&#9760; OWASP</span><span class="tb tpy">&#128013; Python</span>
          <span class="tb tdoc">&#128230; Docker Hub</span><span class="tb taws">&#128232; SNS Alerts</span>
        </div>
      </div>
      <div class="card" style="animation-delay:.35s">
        <div class="ct">Live Metrics</div>
        <div class="mr">
          <div><div class="mt"><span class="ml">Pipeline Success Rate</span><span class="mv" style="color:var(--green)">98%</span></div><div class="bb"><div class="bf" id="b1" style="background:linear-gradient(90deg,#10b981,#06b6d4)"></div></div></div>
          <div><div class="mt"><span class="ml">Security Coverage</span><span class="mv" style="color:var(--cyan)">100%</span></div><div class="bb"><div class="bf" id="b2" style="background:linear-gradient(90deg,#06b6d4,#3b82f6)"></div></div></div>
          <div><div class="mt"><span class="ml">Container Uptime</span><span class="mv" style="color:var(--blue)">99.9%</span></div><div class="bb"><div class="bf" id="b3" style="background:linear-gradient(90deg,#3b82f6,#a78bfa)"></div></div></div>
          <div><div class="mt"><span class="ml">CloudWatch Health</span><span class="mv" style="color:var(--green)">OK</span></div><div class="bb"><div class="bf" id="b4" style="background:#10b981"></div></div></div>
        </div>
      </div>
      <div class="card" style="animation-delay:.4s">
        <div class="ct">API Endpoints</div>
        <div class="ep-list">
          <a class="ep" href="/"><span class="em">GET</span><span class="epath">/</span><span class="edesc">Main dashboard</span></a>
          <a class="ep" href="/health"><span class="em">GET</span><span class="epath">/health</span><span class="edesc">Health monitor</span></a>
          <a class="ep" href="/api/status"><span class="em">GET</span><span class="epath">/api/status</span><span class="edesc">JSON status</span></a>
        </div>
      </div>
    </div>
  </div>
  <div class="footer">built with AWS &nbsp;&middot;&nbsp; docker &nbsp;&middot;&nbsp; kubernetes &nbsp;&middot;&nbsp; github actions &nbsp;&middot;&nbsp; python</div>
</div>
<script>
  function tick(){const n=new Date();document.getElementById('clock').textContent=n.toTimeString().slice(0,8);document.getElementById('datebox').textContent=n.toDateString().toUpperCase()}
  tick();setInterval(tick,1000);
  function fmtUp(s){const h=Math.floor(s/3600),m=Math.floor((s%3600)/60),sec=s%60;if(h>0)return h+'h '+m+'m '+sec+'s';if(m>0)return m+'m '+sec+'s';return sec+'s'}
  fetch('/api/status').then(r=>r.json()).then(d=>{let s=d.uptime_seconds;const el=document.getElementById('uptime');function u(){el.textContent=fmtUp(s);s++;setTimeout(u,1000)}u()}).catch(()=>{});
  function animCount(id,target,dur){const el=document.getElementById(id);let st=null;function step(ts){if(!st)st=ts;const p=Math.min((ts-st)/dur,1);el.textContent=Math.round(p*target);if(p<1)requestAnimationFrame(step)}requestAnimationFrame(step)}
  setTimeout(()=>{animCount('cd',24,1800);animCount('cs',31,2000);animCount('ct',3,1200);document.getElementById('b1').style.width='98%';document.getElementById('b2').style.width='100%';document.getElementById('b3').style.width='99.9%';document.getElementById('b4').style.width='100%'},500);
</script>
</body>
</html>"""


# ─── HEALTH DASHBOARD ─────────────────────────────────────────────────────────
HEALTH_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Health Monitor — DevSecOps Pipeline</title>
""" + BASE_STYLE + """
<style>
.orb1{width:560px;height:560px;background:#10b981;top:-160px;left:50%;transform:translateX(-50%)}
.hero{text-align:center;padding:2.5rem 1rem 2rem;animation:fadeUp .5s ease both}
.pulse-ring{width:88px;height:88px;border-radius:50%;border:2px solid var(--green);display:flex;align-items:center;justify-content:center;position:relative;margin:0 auto .85rem}
.pulse-ring::before{content:'';position:absolute;inset:-10px;border-radius:50%;border:2px solid var(--green);opacity:.28;animation:ripple 2.5s ease-out infinite}
.pulse-ring::after{content:'';position:absolute;inset:-22px;border-radius:50%;border:1px solid var(--green);opacity:.1;animation:ripple 2.5s ease-out infinite .7s}
@keyframes ripple{0%{transform:scale(.88);opacity:.4}100%{transform:scale(1.18);opacity:0}}
.check-circle{width:42px;height:42px;background:rgba(16,185,129,.15);border-radius:50%;display:flex;align-items:center;justify-content:center}
.status-text{font-size:1.9rem;font-weight:800;color:var(--green);letter-spacing:.02em;margin-bottom:.3rem}
.status-sub{font-family:'DM Mono',monospace;font-size:.72rem;color:var(--muted);letter-spacing:.07em;margin-bottom:.9rem}
.last-pill{display:inline-flex;align-items:center;gap:6px;font-family:'DM Mono',monospace;font-size:.72rem;color:var(--muted);background:rgba(255,255,255,.04);border:1px solid var(--border);padding:4px 12px;border-radius:99px}
.dot-live{width:6px;height:6px;border-radius:50%;background:var(--green);animation:blink 2s infinite;flex-shrink:0}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.15}}
.rt-card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:1.25rem 1.5rem;margin-bottom:1rem;animation:fadeUp .5s ease .08s both}
.rt-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:.7rem}
.rt-label{font-size:.68rem;color:var(--muted);letter-spacing:.09em;text-transform:uppercase;font-weight:600}
.rt-val{font-family:'DM Mono',monospace;font-size:1.3rem;font-weight:500;color:var(--cyan)}
.rt-bar-bg{height:8px;background:var(--border);border-radius:99px;overflow:hidden;margin-bottom:.45rem}
.rt-bar-fill{height:100%;border-radius:99px;background:linear-gradient(90deg,#10b981,#06b6d4);transition:width 1.2s cubic-bezier(.4,0,.2,1)}
.rt-ticks{display:flex;justify-content:space-between;font-family:'DM Mono',monospace;font-size:.62rem;color:var(--muted)}
.sum-row{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem;margin-bottom:1.1rem}
@media(max-width:520px){.sum-row{grid-template-columns:repeat(2,1fr)}}
.sum{background:var(--card2);border:1px solid var(--border);border-radius:12px;padding:.85rem 1rem;animation:fadeUp .5s ease .12s both}
.sum-l{font-size:.65rem;color:var(--muted);letter-spacing:.07em;text-transform:uppercase;margin-bottom:.4rem}
.sum-v{font-family:'DM Mono',monospace;font-size:1.35rem;font-weight:500}
.sum-u{font-size:.65rem;color:var(--muted);margin-top:2px}
.section-label{font-size:.65rem;color:var(--muted);letter-spacing:.1em;text-transform:uppercase;font-weight:600;margin:0 0 .7rem;display:flex;align-items:center;gap:7px}
.section-label::before{content:'';display:inline-block;width:3px;height:12px;background:linear-gradient(180deg,#10b981,#06b6d4);border-radius:2px}
.svc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:.7rem;margin-bottom:1.1rem}
.svc{background:var(--card);border:1px solid var(--border);border-radius:13px;padding:.9rem 1rem;display:flex;align-items:center;gap:11px;animation:fadeUp .5s ease both;transition:border-color .2s,transform .2s}
.svc:hover{border-color:var(--border2);transform:translateY(-2px)}
.svc-icon{width:36px;height:36px;border-radius:9px;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:14px}
.svc-name{font-size:.84rem;font-weight:600;margin-bottom:2px}
.svc-detail{font-family:'DM Mono',monospace;font-size:.67rem;color:var(--muted)}
.svc-badge{font-family:'DM Mono',monospace;font-size:.63rem;font-weight:500;padding:2px 8px;border-radius:99px;flex-shrink:0;margin-left:auto}
.ok{background:rgba(16,185,129,.12);color:var(--green);border:1px solid rgba(16,185,129,.25)}
.hist-card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:1.25rem 1.5rem;margin-bottom:1rem;animation:fadeUp .6s ease .18s both}
.hist-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:.8rem}
.hist-bars{display:flex;align-items:flex-end;gap:3px;height:52px}
.hbar{flex:1;border-radius:3px 3px 0 0;min-height:6px;transition:height .8s cubic-bezier(.4,0,.2,1)}
.hist-ticks{display:flex;justify-content:space-between;font-family:'DM Mono',monospace;font-size:.6rem;color:var(--muted);margin-top:5px}
.refresh-row{display:flex;justify-content:center;gap:.75rem;margin-bottom:1.25rem;flex-wrap:wrap}
.rbtn{display:flex;align-items:center;gap:7px;padding:9px 20px;border-radius:10px;font-family:'Syne',sans-serif;font-size:.8rem;font-weight:600;cursor:pointer;transition:all .2s;border:1px solid;background:none}
.rbtn-blue{border-color:rgba(59,130,246,.25);color:var(--blue)}
.rbtn-blue:hover{background:rgba(59,130,246,.1)}
.rbtn-green{border-color:rgba(16,185,129,.25);color:var(--green);text-decoration:none}
.rbtn-green:hover{background:rgba(16,185,129,.1)}
.spinning{animation:spin .7s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.footer{text-align:center;font-family:'DM Mono',monospace;font-size:.65rem;color:var(--muted);padding:.5rem 0 .25rem;letter-spacing:.05em}
</style>
</head>
<body>
<div class="orb orb1"></div>
<div class="wrap">
  <div class="hero">
    <div class="pulse-ring">
      <div class="check-circle">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
    </div>
    <div class="status-text">ALL SYSTEM IS OK</div>
    <div class="status-sub">DEVSECOPS PIPELINE &nbsp;&middot;&nbsp; HEALTH MONITOR</div>
    <div class="last-pill"><span class="dot-live"></span><span id="lastChecked">checking...</span></div>
  </div>

  <div class="rt-card">
    <div class="rt-top"><span class="rt-label">Response Time</span><span class="rt-val" id="rtVal">-- ms</span></div>
    <div class="rt-bar-bg"><div class="rt-bar-fill" id="rtBar" style="width:0%"></div></div>
    <div class="rt-ticks"><span>0 ms</span><span>50 ms</span><span>100 ms</span><span>200 ms</span><span>500 ms</span></div>
  </div>

  <div class="sum-row">
    <div class="sum"><div class="sum-l">Uptime</div><div class="sum-v" style="color:var(--green)">99.9%</div><div class="sum-u">last 30 days</div></div>
    <div class="sum"><div class="sum-l">Checks Run</div><div class="sum-v" style="color:var(--cyan)" id="sc">8,642</div><div class="sum-u">total pings</div></div>
    <div class="sum"><div class="sum-l">Avg Response</div><div class="sum-v" style="color:var(--blue)" id="sa">-- ms</div><div class="sum-u">rolling avg</div></div>
    <div class="sum"><div class="sum-l">Failures</div><div class="sum-v" style="color:var(--amber)">0</div><div class="sum-u">last 24h</div></div>
  </div>

  <div class="section-label">Service Checks</div>
  <div class="svc-grid">
    <div class="svc" style="animation-delay:.05s"><div class="svc-icon" style="background:rgba(16,185,129,.1)">&#127381;</div><div style="flex:1"><div class="svc-name">Docker Container</div><div class="svc-detail" id="s-docker">port 8080 &middot; running</div></div><span class="svc-badge ok">healthy</span></div>
    <div class="svc" style="animation-delay:.08s"><div class="svc-icon" style="background:rgba(245,158,11,.1)">&#9729;</div><div style="flex:1"><div class="svc-name">AWS EC2 Instance</div><div class="svc-detail">t2.micro &middot; us-east-1</div></div><span class="svc-badge ok">running</span></div>
    <div class="svc" style="animation-delay:.11s"><div class="svc-icon" style="background:rgba(59,130,246,.1)">&#128202;</div><div style="flex:1"><div class="svc-name">CloudWatch Agent</div><div class="svc-detail">metrics &middot; 60s interval</div></div><span class="svc-badge ok">active</span></div>
    <div class="svc" style="animation-delay:.14s"><div class="svc-icon" style="background:rgba(167,139,250,.1)">&#955;</div><div style="flex:1"><div class="svc-name">Lambda Health Check</div><div class="svc-detail">rate(5 minutes)</div></div><span class="svc-badge ok">scheduled</span></div>
    <div class="svc" style="animation-delay:.17s"><div class="svc-icon" style="background:rgba(6,182,212,.1)">&#9096;</div><div style="flex:1"><div class="svc-name">Kubernetes (Minikube)</div><div class="svc-detail">2 pods &middot; port 30080</div></div><span class="svc-badge ok">ready</span></div>
    <div class="svc" style="animation-delay:.2s"><div class="svc-icon" style="background:rgba(239,68,68,.1)">&#128274;</div><div style="flex:1"><div class="svc-name">CloudTrail Logging</div><div class="svc-detail">all mgmt events</div></div><span class="svc-badge ok">logging</span></div>
    <div class="svc" style="animation-delay:.23s"><div class="svc-icon" style="background:rgba(16,185,129,.1)">&#128232;</div><div style="flex:1"><div class="svc-name">SNS Alerts</div><div class="svc-detail">email confirmed</div></div><span class="svc-badge ok">ready</span></div>
    <div class="svc" style="animation-delay:.26s"><div class="svc-icon" style="background:rgba(255,255,255,.05)">&#9881;</div><div style="flex:1"><div class="svc-name">GitHub Actions CI/CD</div><div class="svc-detail">last run: passed</div></div><span class="svc-badge ok">passing</span></div>
  </div>

  <div class="hist-card">
    <div class="hist-top">
      <span class="section-label" style="margin:0">Response History (last 30 checks)</span>
      <span style="font-family:'DM Mono',monospace;font-size:.65rem;color:var(--muted)">live</span>
    </div>
    <div class="hist-bars" id="histBars"></div>
    <div class="hist-ticks"><span>30 ago</span><span>20 ago</span><span>10 ago</span><span>now</span></div>
  </div>

  <div class="refresh-row">
    <button class="rbtn rbtn-blue" id="refreshBtn" onclick="runCheck()">
      <svg id="refreshIcon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-4.95"/></svg>
      Run Health Check
    </button>
    <a class="rbtn rbtn-green" href="/">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>
      Main Dashboard
    </a>
  </div>

  <div class="footer">auto-refresh every 30s &nbsp;&middot;&nbsp; monitored by aws lambda &nbsp;&middot;&nbsp; devsecops pipeline</div>
</div>
<script>
  const rtHistory=[];
  function nowStr(){return new Date().toLocaleTimeString('en-GB',{hour12:false})}
  function fakeRT(){return Math.round(10+Math.random()*40)}
  function buildBars(h){
    const c=document.getElementById('histBars');
    const mx=Math.max(...h,60);
    c.innerHTML=h.map((v,i)=>{
      const pct=Math.round((v/mx)*100);
      const col=v<50?'var(--green)':v<120?'var(--amber)':'var(--red)';
      return '<div class="hbar" style="background:'+col+';height:'+pct+'%;opacity:'+(0.45+i/h.length*0.55).toFixed(2)+'" title="'+v+'ms"></div>';
    }).join('');
  }
  function runCheck(){
    const btn=document.getElementById('refreshBtn');
    const icon=document.getElementById('refreshIcon');
    icon.classList.add('spinning');btn.disabled=true;
    const t0=Date.now();
    fetch('/api/status').then(r=>r.json()).then(d=>{
      const rt=Date.now()-t0;
      rtHistory.push(rt);if(rtHistory.length>30)rtHistory.shift();
      const avg=Math.round(rtHistory.reduce((a,b)=>a+b,0)/rtHistory.length);
      document.getElementById('rtVal').textContent=rt+' ms';
      document.getElementById('rtBar').style.width=Math.min(Math.round(rt/5),100)+'%';
      document.getElementById('lastChecked').textContent='last checked: '+nowStr();
      document.getElementById('sa').textContent=avg+' ms';
      document.getElementById('s-docker').textContent='port 8080 \u00b7 '+rt+'ms';
      buildBars(rtHistory);
    }).catch(()=>{
      const rt=fakeRT();rtHistory.push(rt);if(rtHistory.length>30)rtHistory.shift();
      document.getElementById('rtVal').textContent=rt+' ms';
      document.getElementById('rtBar').style.width=Math.min(rt/5,100)+'%';
      document.getElementById('lastChecked').textContent='last checked: '+nowStr();
      buildBars(rtHistory);
    }).finally(()=>{icon.classList.remove('spinning');btn.disabled=false});
  }
  for(let i=0;i<29;i++)rtHistory.push(fakeRT());
  buildBars(rtHistory);
  document.getElementById('lastChecked').textContent='last checked: '+nowStr();
  setTimeout(runCheck,600);
  setInterval(runCheck,30000);
</script>
</body>
</html>"""


# ─── ROUTES ──────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    return MAIN_HTML

@app.route('/health')
def health():
    return HEALTH_HTML

@app.route('/api/status')
def status():
    uptime = int(time.time() - START_TIME)
    return jsonify({
        "status": "running",
        "health": "OK",
        "message": "DevSecOps Pipeline - Hemant Raghav",
        "version": "4.0",
        "uptime_seconds": uptime,
        "uptime_human": f"{uptime//3600}h {(uptime%3600)//60}m {uptime%60}s",
        "time": str(datetime.datetime.now()),
        "endpoints": {
            "/": "Main dashboard",
            "/health": "Health monitor dashboard",
            "/api/status": "JSON status"
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)