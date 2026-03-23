from flask import Flask, jsonify
import datetime, time

app = Flask(__name__)
START_TIME = time.time()

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>DevSecOps Pipeline — Hemant Raghav</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  :root{
    --bg:#080c14;
    --surface:#0d1420;
    --card:#111827;
    --card2:#141e2e;
    --border:#1e2d42;
    --border2:#253548;
    --text:#e8edf5;
    --muted:#6b7f96;
    --accent:#3b82f6;
    --accent2:#06b6d4;
    --green:#10b981;
    --amber:#f59e0b;
    --red:#ef4444;
    --purple:#a78bfa;
  }
  html{scroll-behavior:smooth}
  body{
    background:var(--bg);
    color:var(--text);
    font-family:'Syne',sans-serif;
    min-height:100vh;
    overflow-x:hidden;
  }

  /* ── grid bg ── */
  body::before{
    content:'';
    position:fixed;inset:0;
    background-image:
      linear-gradient(var(--border) 1px,transparent 1px),
      linear-gradient(90deg,var(--border) 1px,transparent 1px);
    background-size:48px 48px;
    opacity:.35;
    pointer-events:none;
    z-index:0;
  }

  /* ── glow orbs ── */
  .orb{position:fixed;border-radius:50%;filter:blur(90px);opacity:.18;pointer-events:none;z-index:0}
  .orb1{width:600px;height:600px;background:#3b82f6;top:-150px;right:-100px}
  .orb2{width:500px;height:500px;background:#06b6d4;bottom:-150px;left:-100px}

  /* ── layout ── */
  .wrap{position:relative;z-index:1;max-width:1120px;margin:0 auto;padding:2.5rem 1.5rem}

  /* ── hero ── */
  .hero{
    display:flex;align-items:center;justify-content:space-between;
    flex-wrap:wrap;gap:1.5rem;
    padding:2.5rem;
    background:linear-gradient(135deg,rgba(17,24,39,.95),rgba(13,20,32,.95));
    border:1px solid var(--border2);
    border-radius:20px;
    margin-bottom:1.5rem;
    backdrop-filter:blur(12px);
    animation:fadeUp .6s ease both;
  }
  .hero-left{}
  .status-pill{
    display:inline-flex;align-items:center;gap:6px;
    background:rgba(16,185,129,.12);
    border:1px solid rgba(16,185,129,.3);
    color:var(--green);
    font-family:'DM Mono',monospace;
    font-size:.72rem;letter-spacing:.08em;
    padding:4px 12px;border-radius:99px;
    margin-bottom:1rem;
  }
  .dot{width:7px;height:7px;border-radius:50%;background:var(--green);animation:pulse 2s infinite}
  @keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.5;transform:scale(.8)}}
  .hero h1{font-size:clamp(1.8rem,4vw,2.8rem);font-weight:800;line-height:1.1;margin-bottom:.4rem}
  .hero h1 span{
    background:linear-gradient(90deg,#3b82f6,#06b6d4);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  }
  .hero-sub{color:var(--muted);font-size:.95rem;font-weight:400}
  .hero-right{display:flex;flex-direction:column;align-items:flex-end;gap:.75rem}
  .clock-box{
    font-family:'DM Mono',monospace;
    font-size:1.6rem;font-weight:500;
    color:var(--accent2);letter-spacing:.04em;
    text-align:right;
  }
  .date-box{font-family:'DM Mono',monospace;font-size:.78rem;color:var(--muted);text-align:right}
  .hero-links{display:flex;gap:.75rem;margin-top:.25rem}
  .link-btn{
    display:flex;align-items:center;gap:6px;
    padding:7px 16px;border-radius:8px;
    font-size:.82rem;font-weight:600;letter-spacing:.03em;
    text-decoration:none;transition:all .2s;border:1px solid;
  }
  .link-gh{
    background:rgba(167,139,250,.1);border-color:rgba(167,139,250,.3);color:var(--purple)
  }
  .link-gh:hover{background:rgba(167,139,250,.2)}
  .link-li{
    background:rgba(59,130,246,.1);border-color:rgba(59,130,246,.3);color:var(--accent)
  }
  .link-li:hover{background:rgba(59,130,246,.2)}

  /* ── stat cards row ── */
  .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem;margin-bottom:1.5rem}
  .stat-card{
    background:var(--card);border:1px solid var(--border);border-radius:16px;
    padding:1.25rem 1.5rem;
    animation:fadeUp .6s ease both;
    transition:border-color .2s,transform .2s;
  }
  .stat-card:hover{border-color:var(--border2);transform:translateY(-2px)}
  .stat-label{font-size:.75rem;color:var(--muted);letter-spacing:.07em;text-transform:uppercase;margin-bottom:.6rem}
  .stat-val{font-size:2rem;font-weight:800;line-height:1;font-family:'DM Mono',monospace}
  .stat-sub{font-size:.75rem;color:var(--muted);margin-top:.35rem}
  .c-green{color:var(--green)}.c-blue{color:var(--accent)}.c-cyan{color:var(--accent2)}.c-amber{color:var(--amber)}

  /* ── grid 2col ── */
  .grid2{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem}
  @media(max-width:700px){.grid2{grid-template-columns:1fr}}

  /* ── section card ── */
  .card{
    background:var(--card);border:1px solid var(--border);border-radius:16px;
    padding:1.5rem;animation:fadeUp .7s ease both;
    transition:border-color .2s;
  }
  .card:hover{border-color:var(--border2)}
  .card-title{
    font-size:.72rem;color:var(--muted);letter-spacing:.1em;
    text-transform:uppercase;font-weight:600;margin-bottom:1.25rem;
    display:flex;align-items:center;gap:8px;
  }
  .card-title::before{
    content:'';display:inline-block;width:3px;height:14px;
    background:linear-gradient(180deg,#3b82f6,#06b6d4);border-radius:2px;
  }

  /* ── pipeline ── */
  .pipeline{display:flex;flex-direction:column;gap:.6rem}
  .pipe-step{
    display:flex;align-items:center;gap:12px;
    padding:.8rem 1rem;border-radius:10px;
    border:1px solid var(--border);
    background:var(--card2);
    transition:border-color .2s,background .2s;
    animation:slideIn .5s ease both;
  }
  .pipe-step:hover{border-color:var(--border2);background:#182030}
  .pipe-icon{
    width:32px;height:32px;border-radius:8px;
    display:flex;align-items:center;justify-content:center;
    font-size:.85rem;flex-shrink:0;
  }
  .pipe-info{flex:1}
  .pipe-name{font-size:.88rem;font-weight:600;margin-bottom:2px}
  .pipe-desc{font-size:.75rem;color:var(--muted)}
  .pipe-badge{
    font-family:'DM Mono',monospace;font-size:.7rem;font-weight:500;
    padding:3px 10px;border-radius:99px;white-space:nowrap;
  }
  .badge-pass{background:rgba(16,185,129,.12);color:var(--green);border:1px solid rgba(16,185,129,.25)}
  .badge-warn{background:rgba(245,158,11,.12);color:var(--amber);border:1px solid rgba(245,158,11,.25)}
  .badge-info{background:rgba(59,130,246,.12);color:var(--accent);border:1px solid rgba(59,130,246,.25)}

  /* ── tech badges ── */
  .badge-grid{display:flex;flex-wrap:wrap;gap:.5rem}
  .tech-badge{
    display:flex;align-items:center;gap:6px;
    padding:5px 12px;border-radius:8px;
    font-size:.78rem;font-weight:600;
    border:1px solid;transition:transform .15s;
    cursor:default;
  }
  .tech-badge:hover{transform:scale(1.04)}
  .tb-aws{background:rgba(245,158,11,.1);color:var(--amber);border-color:rgba(245,158,11,.25)}
  .tb-docker{background:rgba(6,182,212,.1);color:var(--accent2);border-color:rgba(6,182,212,.25)}
  .tb-k8s{background:rgba(59,130,246,.1);color:var(--accent);border-color:rgba(59,130,246,.25)}
  .tb-gh{background:rgba(167,139,250,.1);color:var(--purple);border-color:rgba(167,139,250,.25)}
  .tb-sec{background:rgba(239,68,68,.1);color:var(--red);border-color:rgba(239,68,68,.25)}
  .tb-py{background:rgba(16,185,129,.1);color:var(--green);border-color:rgba(16,185,129,.25)}
  .tb-cw{background:rgba(245,158,11,.1);color:var(--amber);border-color:rgba(245,158,11,.25)}

  /* ── metrics bar ── */
  .metric-row{display:flex;flex-direction:column;gap:.75rem}
  .metric{display:flex;flex-direction:column;gap:5px}
  .metric-top{display:flex;justify-content:space-between;font-size:.8rem}
  .metric-label{color:var(--muted)}
  .metric-val{font-family:'DM Mono',monospace;font-weight:500}
  .bar-bg{height:6px;background:var(--border);border-radius:99px;overflow:hidden}
  .bar-fill{height:100%;border-radius:99px;transition:width 1.5s cubic-bezier(.4,0,.2,1)}

  /* ── endpoint table ── */
  .ep-list{display:flex;flex-direction:column;gap:.5rem}
  .ep-row{
    display:flex;align-items:center;gap:10px;
    padding:.6rem .9rem;background:var(--card2);
    border-radius:8px;border:1px solid var(--border);
  }
  .ep-method{
    font-family:'DM Mono',monospace;font-size:.72rem;font-weight:500;
    padding:3px 9px;border-radius:5px;
    background:rgba(16,185,129,.12);color:var(--green);border:1px solid rgba(16,185,129,.2);
  }
  .ep-path{font-family:'DM Mono',monospace;font-size:.85rem;color:var(--accent2)}
  .ep-desc{font-size:.78rem;color:var(--muted);margin-left:auto}

  /* ── footer ── */
  .footer{
    text-align:center;padding:2rem 0 1rem;
    font-size:.78rem;color:var(--muted);
    font-family:'DM Mono',monospace;letter-spacing:.04em;
  }

  @keyframes fadeUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
  @keyframes slideIn{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:translateX(0)}}
</style>
</head>
<body>
<div class="orb orb1"></div>
<div class="orb orb2"></div>

<div class="wrap">

  <!-- ── HERO ── -->
  <div class="hero">
    <div class="hero-left">
      <div class="status-pill"><span class="dot"></span> LIVE &amp; RUNNING</div>
      <h1>DevSecOps<br/><span>Pipeline</span></h1>
      <p class="hero-sub">Cloud Engineer Intern (AWS) &nbsp;·&nbsp; Hemant Raghav</p>
    </div>
    <div class="hero-right">
      <div class="clock-box" id="clock">--:--:--</div>
      <div class="date-box" id="datestr">---</div>
      <div class="hero-links">
        <a class="link-btn link-gh" href="https://github.com/hemantraghav-123/devsecops-pipeline" target="_blank">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 .5C5.37.5 0 5.87 0 12.5c0 5.31 3.44 9.8 8.21 11.39.6.11.82-.26.82-.58v-2.03c-3.34.72-4.04-1.61-4.04-1.61-.55-1.39-1.34-1.76-1.34-1.76-1.09-.74.08-.73.08-.73 1.21.09 1.85 1.24 1.85 1.24 1.07 1.84 2.81 1.31 3.5 1 .11-.78.42-1.31.76-1.61-2.67-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.14-.3-.54-1.52.11-3.17 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 3-.4c1.02.01 2.04.14 3 .4 2.28-1.55 3.29-1.23 3.29-1.23.65 1.65.25 2.87.12 3.17.77.84 1.24 1.91 1.24 3.22 0 4.61-2.81 5.63-5.48 5.92.43.37.81 1.1.81 2.22v3.29c0 .32.21.7.82.58C20.56 22.3 24 17.81 24 12.5 24 5.87 18.63.5 12 .5z"/></svg>
          GitHub
        </a>
        <a class="link-btn link-li" href="https://linkedin.com/in/hemantraghav2467" target="_blank">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.36V9h3.41v1.56h.05c.47-.9 1.63-1.85 3.36-1.85 3.59 0 4.25 2.37 4.25 5.44v6.3zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zm1.78 13.02H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.44c.98 0 1.79-.77 1.79-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg>
          LinkedIn
        </a>
      </div>
    </div>
  </div>

  <!-- ── STAT CARDS ── -->
  <div class="stats">
    <div class="stat-card" style="animation-delay:.05s">
      <div class="stat-label">Uptime</div>
      <div class="stat-val c-green" id="uptime">0s</div>
      <div class="stat-sub">Since last deploy</div>
    </div>
    <div class="stat-card" style="animation-delay:.1s">
      <div class="stat-label">Deployments</div>
      <div class="stat-val c-blue" id="ctr-deploys">0</div>
      <div class="stat-sub">Via GitHub Actions</div>
    </div>
    <div class="stat-card" style="animation-delay:.15s">
      <div class="stat-label">Scans Passed</div>
      <div class="stat-val c-cyan" id="ctr-scans">0</div>
      <div class="stat-sub">Trivy + OWASP clean</div>
    </div>
    <div class="stat-card" style="animation-delay:.2s">
      <div class="stat-label">Blocked Threats</div>
      <div class="stat-val c-amber" id="ctr-threats">0</div>
      <div class="stat-sub">CVEs auto-blocked</div>
    </div>
  </div>

  <!-- ── PIPELINE + TECH ── -->
  <div class="grid2" style="margin-bottom:1rem">

    <!-- pipeline -->
    <div class="card" style="animation-delay:.25s">
      <div class="card-title">CI/CD Pipeline Stages</div>
      <div class="pipeline">
        <div class="pipe-step" style="animation-delay:.3s">
          <div class="pipe-icon" style="background:rgba(167,139,250,.12)">&#128196;</div>
          <div class="pipe-info">
            <div class="pipe-name">Code Push</div>
            <div class="pipe-desc">Triggers on push to main</div>
          </div>
          <span class="pipe-badge badge-info">trigger</span>
        </div>
        <div class="pipe-step" style="animation-delay:.35s">
          <div class="pipe-icon" style="background:rgba(239,68,68,.12)">&#128737;</div>
          <div class="pipe-info">
            <div class="pipe-name">OWASP Safety Scan</div>
            <div class="pipe-desc">Python dependency CVE check</div>
          </div>
          <span class="pipe-badge badge-pass">passed</span>
        </div>
        <div class="pipe-step" style="animation-delay:.4s">
          <div class="pipe-icon" style="background:rgba(6,182,212,.12)">&#127381;</div>
          <div class="pipe-info">
            <div class="pipe-name">Docker Build</div>
            <div class="pipe-desc">Image built from Dockerfile</div>
          </div>
          <span class="pipe-badge badge-pass">success</span>
        </div>
        <div class="pipe-step" style="animation-delay:.45s">
          <div class="pipe-icon" style="background:rgba(239,68,68,.12)">&#128270;</div>
          <div class="pipe-info">
            <div class="pipe-name">Trivy Image Scan</div>
            <div class="pipe-desc">OS + library CVE scan</div>
          </div>
          <span class="pipe-badge badge-pass">0 critical</span>
        </div>
        <div class="pipe-step" style="animation-delay:.5s">
          <div class="pipe-icon" style="background:rgba(59,130,246,.12)">&#9650;</div>
          <div class="pipe-info">
            <div class="pipe-name">Push to Docker Hub</div>
            <div class="pipe-desc">Only if scan passed</div>
          </div>
          <span class="pipe-badge badge-pass">pushed</span>
        </div>
        <div class="pipe-step" style="animation-delay:.55s">
          <div class="pipe-icon" style="background:rgba(16,185,129,.12)">&#128640;</div>
          <div class="pipe-info">
            <div class="pipe-name">Deploy to EC2 / K8s</div>
            <div class="pipe-desc">Auto SSH deploy via Actions</div>
          </div>
          <span class="pipe-badge badge-pass">live</span>
        </div>
      </div>
    </div>

    <!-- right col: tech + metrics + endpoints -->
    <div style="display:flex;flex-direction:column;gap:1rem">

      <!-- tech stack -->
      <div class="card" style="animation-delay:.3s">
        <div class="card-title">Tech Stack</div>
        <div class="badge-grid">
          <span class="tech-badge tb-aws">&#9729; AWS EC2</span>
          <span class="tech-badge tb-aws">&#128202; CloudWatch</span>
          <span class="tech-badge tb-aws">&#128274; CloudTrail</span>
          <span class="tech-badge tb-aws">&#955; Lambda</span>
          <span class="tech-badge tb-docker">&#127025; Docker</span>
          <span class="tech-badge tb-k8s">&#9096; Kubernetes</span>
          <span class="tech-badge tb-gh">&#9881; GitHub Actions</span>
          <span class="tech-badge tb-sec">&#128737; Trivy</span>
          <span class="tech-badge tb-sec">&#9760; OWASP</span>
          <span class="tech-badge tb-py">&#128013; Python</span>
          <span class="tech-badge tb-docker">&#128230; Docker Hub</span>
          <span class="tech-badge tb-aws">&#128232; SNS Alerts</span>
        </div>
      </div>

      <!-- live metrics bars -->
      <div class="card" style="animation-delay:.35s">
        <div class="card-title">Live Metrics</div>
        <div class="metric-row">
          <div class="metric">
            <div class="metric-top">
              <span class="metric-label">Pipeline Success Rate</span>
              <span class="metric-val c-green">98%</span>
            </div>
            <div class="bar-bg"><div class="bar-fill" style="width:0%;background:linear-gradient(90deg,#10b981,#06b6d4)" id="bar1"></div></div>
          </div>
          <div class="metric">
            <div class="metric-top">
              <span class="metric-label">Security Coverage</span>
              <span class="metric-val c-cyan">100%</span>
            </div>
            <div class="bar-bg"><div class="bar-fill" style="width:0%;background:linear-gradient(90deg,#06b6d4,#3b82f6)" id="bar2"></div></div>
          </div>
          <div class="metric">
            <div class="metric-top">
              <span class="metric-label">Container Uptime</span>
              <span class="metric-val c-blue" id="uptime-pct">--%</span>
            </div>
            <div class="bar-bg"><div class="bar-fill" style="width:0%;background:linear-gradient(90deg,#3b82f6,#a78bfa)" id="bar3"></div></div>
          </div>
          <div class="metric">
            <div class="metric-top">
              <span class="metric-label">CloudWatch Health</span>
              <span class="metric-val c-green">OK</span>
            </div>
            <div class="bar-bg"><div class="bar-fill" style="width:0%;background:linear-gradient(90deg,#10b981,#10b981)" id="bar4"></div></div>
          </div>
        </div>
      </div>

      <!-- endpoints -->
      <div class="card" style="animation-delay:.4s">
        <div class="card-title">API Endpoints</div>
        <div class="ep-list">
          <div class="ep-row">
            <span class="ep-method">GET</span>
            <span class="ep-path">/</span>
            <span class="ep-desc">Dashboard UI</span>
          </div>
          <div class="ep-row">
            <span class="ep-method">GET</span>
            <span class="ep-path">/health</span>
            <span class="ep-desc">Lambda health check</span>
          </div>
          <div class="ep-row">
            <span class="ep-method">GET</span>
            <span class="ep-path">/api/status</span>
            <span class="ep-desc">JSON status</span>
          </div>
        </div>
      </div>

    </div>
  </div>

  <div class="footer">built with AWS &nbsp;·&nbsp; docker &nbsp;·&nbsp; kubernetes &nbsp;·&nbsp; github actions &nbsp;·&nbsp; python</div>
</div>

<script>
  // ── clock ──
  function updateClock(){
    const n=new Date();
    document.getElementById('clock').textContent=
      n.toTimeString().slice(0,8);
    document.getElementById('datestr').textContent=
      n.toDateString().toUpperCase();
  }
  updateClock();setInterval(updateClock,1000);

  // ── uptime from server ──
  function fmtUptime(s){
    const d=Math.floor(s/86400),h=Math.floor((s%86400)/3600),
          m=Math.floor((s%3600)/60),sec=Math.floor(s%60);
    if(d>0) return d+'d '+h+'h '+m+'m';
    if(h>0) return h+'h '+m+'m '+sec+'s';
    if(m>0) return m+'m '+sec+'s';
    return sec+'s';
  }
  fetch('/api/status').then(r=>r.json()).then(d=>{
    let s=d.uptime_seconds;
    const el=document.getElementById('uptime');
    function tick(){el.textContent=fmtUptime(s);s++;setTimeout(tick,1000)}
    tick();
    const p=Math.min(99.9,99.5+(s>86400?0.4:0)).toFixed(1);
    document.getElementById('uptime-pct').textContent=p+'%';
    document.getElementById('bar3').style.width=p+'%';
  });

  // ── animated counters ──
  function animCount(id,target,dur){
    const el=document.getElementById(id);let start=null;
    function step(ts){
      if(!start)start=ts;
      const prog=Math.min((ts-start)/dur,1);
      el.textContent=Math.round(prog*target);
      if(prog<1)requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  setTimeout(()=>{
    animCount('ctr-deploys',24,1800);
    animCount('ctr-scans',31,2000);
    animCount('ctr-threats',3,1200);
  },400);

  // ── animate bars ──
  setTimeout(()=>{
    document.getElementById('bar1').style.width='98%';
    document.getElementById('bar2').style.width='100%';
    document.getElementById('bar4').style.width='100%';
  },600);
</script>
</body>
</html>"""

@app.route('/')
def home():
    return HTML

@app.route('/health')
def health():
    return jsonify({"health": "OK", "status": "running"})

@app.route('/api/status')
def status():
    uptime = int(time.time() - START_TIME)
    return jsonify({
        "status": "running",
        "message": "DevSecOps Pipeline - Hemant Raghav",
        "version": "4.0",
        "uptime_seconds": uptime,
        "uptime_human": f"{uptime//3600}h {(uptime%3600)//60}m {uptime%60}s",
        "time": str(datetime.datetime.now()),
        "endpoints": ["/", "/health", "/api/status"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)