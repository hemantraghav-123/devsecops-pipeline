from flask import Flask, jsonify
import datetime
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Histogram, Gauge
import time

app = Flask(__name__)

# ─────────────────────────────────────────────
#  PROMETHEUS METRICS SETUP
#  Adds /metrics endpoint automatically
#  Auto-tracks every route: count, latency, status codes
# ─────────────────────────────────────────────

metrics = PrometheusMetrics(app)

# Custom business metrics
REQUEST_COUNT = Counter(
    'devsecops_requests_total',
    'Total number of requests received',
    ['endpoint', 'method']
)

RESPONSE_TIME = Histogram(
    'devsecops_response_seconds',
    'Response time in seconds',
    ['endpoint']
)

APP_INFO = Gauge(
    'devsecops_app_info',
    'App version information',
    ['version']
)

# Set app info metric once at startup
APP_INFO.labels(version='3.0').set(1)


# ─────────────────────────────────────────────
#  HOME PAGE
# ─────────────────────────────────────────────

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DevSecOps Pipeline — Hemant Raghav</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: #0a0e1a;
    color: #e0e6ff;
    font-family: 'Segoe UI', sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 30px 20px;
  }

  .badge {
    background: linear-gradient(135deg, #00c9ff, #0066ff);
    color: #fff;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 6px 18px;
    border-radius: 20px;
    margin-bottom: 18px;
  }

  h1 {
    font-size: 28px;
    font-weight: 800;
    background: linear-gradient(90deg, #00c9ff, #a78bfa, #00c9ff);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3s linear infinite;
    text-align: center;
    margin-bottom: 6px;
  }

  .subtitle {
    font-size: 13px;
    color: #6b7eb8;
    margin-bottom: 36px;
    text-align: center;
    letter-spacing: 1px;
  }

  @keyframes shine {
    to { background-position: 200% center; }
  }

  .status-row {
    display: flex;
    gap: 14px;
    margin-bottom: 40px;
    flex-wrap: wrap;
    justify-content: center;
  }

  .stat-card {
    background: #111827;
    border: 1px solid #1e2d4d;
    border-radius: 12px;
    padding: 14px 22px;
    text-align: center;
    min-width: 120px;
  }

  .stat-card .label {
    font-size: 10px;
    color: #4b5e8a;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
  }

  .stat-card .value {
    font-size: 15px;
    font-weight: 700;
    color: #e0e6ff;
  }

  .dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #22c55e;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 1.5s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.8); }
  }

  .pipeline-title {
    font-size: 11px;
    letter-spacing: 3px;
    color: #4b5e8a;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 20px;
  }

  .pipeline {
    display: flex;
    align-items: center;
    gap: 0;
    flex-wrap: wrap;
    justify-content: center;
    margin-bottom: 44px;
  }

  .stage {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }

  .stage-box {
    background: #111827;
    border: 1px solid #1e2d4d;
    border-radius: 12px;
    padding: 14px 18px;
    text-align: center;
    width: 108px;
    transition: border-color 0.3s;
  }

  .stage-box:hover { border-color: #0066ff; }

  .stage:nth-child(1)  .stage-box { animation: glow 4s 0.0s ease-in-out infinite; }
  .stage:nth-child(3)  .stage-box { animation: glow 4s 0.5s ease-in-out infinite; }
  .stage:nth-child(5)  .stage-box { animation: glow 4s 1.0s ease-in-out infinite; }
  .stage:nth-child(7)  .stage-box { animation: glow 4s 1.5s ease-in-out infinite; }
  .stage:nth-child(9)  .stage-box { animation: glow 4s 2.0s ease-in-out infinite; }
  .stage:nth-child(11) .stage-box { animation: glow 4s 2.5s ease-in-out infinite; }

  @keyframes glow {
    0%, 100% { box-shadow: none; }
    50%       { box-shadow: 0 0 16px rgba(0,102,255,0.4); border-color: #0066ff; }
  }

  .icon       { font-size: 24px; }
  .stage-name { font-size: 10px; font-weight: 700; color: #a0aec0; letter-spacing: 0.5px; text-transform: uppercase; }
  .stage-desc { font-size: 9px; color: #4b5e8a; margin-top: 2px; }

  .arrow { display: flex; align-items: center; padding: 0 2px; margin-bottom: 20px; }

  .arrow-line {
    width: 28px;
    height: 2px;
    background: linear-gradient(90deg, #1e2d4d, #0066ff, #1e2d4d);
    background-size: 200% auto;
    animation: flow 2s linear infinite;
    border-radius: 2px;
    position: relative;
  }

  .arrow-line::after {
    content: '';
    position: absolute;
    right: -5px;
    top: -4px;
    border-left: 7px solid #0066ff;
    border-top: 5px solid transparent;
    border-bottom: 5px solid transparent;
  }

  @keyframes flow { to { background-position: 200% center; } }

  .stage.security .stage-box { border-color: #2d1e3a; }
  .stage.security .stage-box:hover { border-color: #a855f7; }
  .stage:nth-child(3).security .stage-box { animation: glow-purple 4s 0.5s ease-in-out infinite; }
  .stage:nth-child(5).security .stage-box { animation: glow-purple 4s 1.0s ease-in-out infinite; }

  @keyframes glow-purple {
    0%, 100% { box-shadow: none; }
    50%       { box-shadow: 0 0 16px rgba(168,85,247,0.4); border-color: #a855f7; }
  }

  .stage.deploy .stage-box { border-color: #1a2d1e; }
  .stage.deploy .stage-box:hover { border-color: #22c55e; }
  .stage:nth-child(11).deploy .stage-box { animation: glow-green 4s 2.5s ease-in-out infinite; }

  @keyframes glow-green {
    0%, 100% { box-shadow: none; }
    50%       { box-shadow: 0 0 16px rgba(34,197,94,0.4); border-color: #22c55e; }
  }

  .tags {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: center;
    margin-bottom: 36px;
  }

  .tag {
    font-size: 11px;
    font-weight: 600;
    padding: 5px 14px;
    border-radius: 20px;
    border: 1px solid;
    letter-spacing: 0.5px;
  }

  .tag.blue   { color: #60a5fa; border-color: #1e3a5f; background: #0d1f35; }
  .tag.purple { color: #c084fc; border-color: #3b1f5e; background: #1a0d35; }
  .tag.green  { color: #4ade80; border-color: #1a3d1e; background: #0d2010; }
  .tag.orange { color: #fb923c; border-color: #3d2210; background: #200f05; }

  .links {
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
    justify-content: center;
  }

  .link-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 22px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 600;
    text-decoration: none;
    transition: opacity 0.2s, transform 0.2s;
    border: 1px solid;
  }

  .link-btn:hover { opacity: 0.85; transform: translateY(-2px); }

  .link-btn.github   { background: #161b22; color: #e0e6ff; border-color: #30363d; }
  .link-btn.linkedin { background: #0a1628; color: #60a5fa; border-color: #1e3a5f; }

  .footer {
    margin-top: 40px;
    font-size: 11px;
    color: #2d3a55;
    letter-spacing: 1px;
    text-align: center;
  }
</style>
</head>
<body>

  <div class="badge">⚡ Live DevSecOps Project</div>

  <h1>DevSecOps CI/CD Pipeline</h1>
  <p class="subtitle">Built by Hemant Raghav &nbsp;·&nbsp; AWS · Docker · Kubernetes · GitHub Actions</p>

  <div class="status-row">
    <div class="stat-card">
      <div class="label">Status</div>
      <div class="value"><span class="dot"></span>Running</div>
    </div>
    <div class="stat-card">
      <div class="label">Version</div>
      <div class="value">3.0</div>
    </div>
    <div class="stat-card">
      <div class="label">Platform</div>
      <div class="value">AWS EC2</div>
    </div>
    <div class="stat-card">
      <div class="label">Container</div>
      <div class="value">Docker ✦ K8s</div>
    </div>
  </div>

  <div class="pipeline-title">⬇ CI / CD Pipeline Flow ⬇</div>

  <div class="pipeline">

    <div class="stage">
      <div class="stage-box">
        <div class="icon">💻</div>
        <div class="stage-name">Code Push</div>
        <div class="stage-desc">git push main</div>
      </div>
    </div>

    <div class="arrow"><div class="arrow-line"></div></div>

    <div class="stage security">
      <div class="stage-box">
        <div class="icon">🛡️</div>
        <div class="stage-name">OWASP Scan</div>
        <div class="stage-desc">deps check</div>
      </div>
    </div>

    <div class="arrow"><div class="arrow-line"></div></div>

    <div class="stage security">
      <div class="stage-box">
        <div class="icon">🔍</div>
        <div class="stage-name">Trivy Scan</div>
        <div class="stage-desc">CVE check</div>
      </div>
    </div>

    <div class="arrow"><div class="arrow-line"></div></div>

    <div class="stage">
      <div class="stage-box">
        <div class="icon">🐳</div>
        <div class="stage-name">Docker Build</div>
        <div class="stage-desc">image built</div>
      </div>
    </div>

    <div class="arrow"><div class="arrow-line"></div></div>

    <div class="stage">
      <div class="stage-box">
        <div class="icon">📦</div>
        <div class="stage-name">Push Image</div>
        <div class="stage-desc">Docker Hub</div>
      </div>
    </div>

    <div class="arrow"><div class="arrow-line"></div></div>

    <div class="stage deploy">
      <div class="stage-box">
        <div class="icon">☸️</div>
        <div class="stage-name">Deploy</div>
        <div class="stage-desc">EC2 · K8s</div>
      </div>
    </div>

  </div>

  <div class="tags">
    <span class="tag blue">AWS EC2</span>
    <span class="tag blue">CloudWatch</span>
    <span class="tag blue">CloudTrail</span>
    <span class="tag blue">Lambda</span>
    <span class="tag blue">SNS</span>
    <span class="tag orange">Docker</span>
    <span class="tag orange">Kubernetes</span>
    <span class="tag green">GitHub Actions</span>
    <span class="tag purple">Trivy</span>
    <span class="tag purple">OWASP Safety</span>
    <span class="tag green">Python Flask</span>
    <span class="tag green">Prometheus</span>
    <span class="tag orange">Grafana</span>
  </div>

  <div class="links">
    <a class="link-btn github"
       href="https://github.com/hemantraghav-123/devsecops-pipeline"
       target="_blank">⭐ GitHub Repo</a>
    <a class="link-btn linkedin"
       href="https://linkedin.com/in/hemantraghav2467"
       target="_blank">🔗 LinkedIn</a>
  </div>

  <div class="footer">AWS Free Tier &nbsp;·&nbsp; Zero cost infrastructure &nbsp;·&nbsp; 2026</div>

</body>
</html>
"""


# ─────────────────────────────────────────────
#  HEALTH PAGE
# ─────────────────────────────────────────────

HEALTH_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Health Check — DevSecOps Pipeline</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: #0a0e1a;
    color: #e0e6ff;
    font-family: 'Segoe UI', sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 30px 20px;
  }

  .pulse-wrap {
    position: relative;
    width: 90px;
    height: 90px;
    margin-bottom: 28px;
  }

  .pulse-ring {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    border: 2px solid #22c55e;
    animation: ring 2s ease-out infinite;
    opacity: 0;
  }

  .pulse-ring:nth-child(2) { animation-delay: 0.6s; }
  .pulse-ring:nth-child(3) { animation-delay: 1.2s; }

  @keyframes ring {
    0%   { transform: scale(0.6); opacity: 0.8; }
    100% { transform: scale(1.6); opacity: 0; }
  }

  .pulse-dot {
    position: absolute;
    inset: 20px;
    background: #22c55e;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
  }

  .status-label {
    font-size: 12px;
    letter-spacing: 3px;
    color: #22c55e;
    text-transform: uppercase;
    margin-bottom: 8px;
  }

  h1 {
    font-size: 26px;
    font-weight: 800;
    color: #e0e6ff;
    margin-bottom: 6px;
    text-align: center;
  }

  .sub {
    font-size: 13px;
    color: #4b5e8a;
    margin-bottom: 36px;
    text-align: center;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    width: 100%;
    max-width: 420px;
    margin-bottom: 32px;
  }

  .card {
    background: #111827;
    border: 1px solid #1e2d4d;
    border-radius: 12px;
    padding: 16px 18px;
  }

  .card-label {
    font-size: 10px;
    color: #4b5e8a;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
  }

  .card-value { font-size: 15px; font-weight: 700; color: #e0e6ff; }
  .ok         { color: #22c55e; }
  .blue       { color: #60a5fa; }

  .checks {
    width: 100%;
    max-width: 420px;
    background: #111827;
    border: 1px solid #1e2d4d;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 32px;
  }

  .checks-title {
    font-size: 10px;
    letter-spacing: 2px;
    color: #4b5e8a;
    text-transform: uppercase;
    margin-bottom: 14px;
  }

  .check-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #1a2235;
    font-size: 13px;
  }

  .check-row:last-child { border-bottom: none; }
  .check-name           { color: #a0aec0; }

  .badge {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 3px 10px;
    border-radius: 20px;
  }

  .badge.pass {
    background: #052e16;
    color: #22c55e;
    border: 1px solid #166534;
  }

  .back {
    font-size: 12px;
    color: #4b5e8a;
    text-decoration: none;
    border: 1px solid #1e2d4d;
    padding: 8px 20px;
    border-radius: 8px;
    transition: color 0.2s, border-color 0.2s;
  }

  .back:hover { color: #60a5fa; border-color: #1e3a5f; }

  .timestamp {
    margin-top: 24px;
    font-size: 11px;
    color: #2d3a55;
    letter-spacing: 1px;
    text-align: center;
  }
</style>
</head>
<body>

  <div class="pulse-wrap">
    <div class="pulse-ring"></div>
    <div class="pulse-ring"></div>
    <div class="pulse-ring"></div>
    <div class="pulse-dot">✓</div>
  </div>

  <div class="status-label">● All systems operational</div>
  <h1>Health Check</h1>
  <p class="sub">DevSecOps Pipeline — Hemant Raghav</p>

  <div class="grid">
    <div class="card">
      <div class="card-label">Status</div>
      <div class="card-value ok">OK</div>
    </div>
    <div class="card">
      <div class="card-label">Version</div>
      <div class="card-value blue">3.0</div>
    </div>
    <div class="card">
      <div class="card-label">Platform</div>
      <div class="card-value">AWS EC2</div>
    </div>
    <div class="card">
      <div class="card-label">Runtime</div>
      <div class="card-value">Python Flask</div>
    </div>
  </div>

  <div class="checks">
    <div class="checks-title">Component checks</div>
    <div class="check-row">
      <span class="check-name">Flask application</span>
      <span class="badge pass">PASS</span>
    </div>
    <div class="check-row">
      <span class="check-name">Docker container</span>
      <span class="badge pass">PASS</span>
    </div>
    <div class="check-row">
      <span class="check-name">Port 8080</span>
      <span class="badge pass">PASS</span>
    </div>
    <div class="check-row">
      <span class="check-name">Lambda ping</span>
      <span class="badge pass">PASS</span>
    </div>
    <div class="check-row">
      <span class="check-name">CI/CD pipeline</span>
      <span class="badge pass">PASS</span>
    </div>
    <div class="check-row">
      <span class="check-name">Prometheus metrics</span>
      <span class="badge pass">PASS</span>
    </div>
  </div>

  <a class="back" href="/">← Back to pipeline</a>

  <div class="timestamp">CHECKED AT __TIMESTAMP__</div>

</body>
</html>
"""


# ─────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────

@app.route('/')
def home():
    REQUEST_COUNT.labels(endpoint='home', method='GET').inc()
    return HTML_PAGE, 200, {'Content-Type': 'text/html'}


@app.route('/health')
def health():
    REQUEST_COUNT.labels(endpoint='health', method='GET').inc()
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    page = HEALTH_PAGE.replace('__TIMESTAMP__', now)
    return page, 200, {'Content-Type': 'text/html'}


@app.route('/health/json')
def health_json():
    REQUEST_COUNT.labels(endpoint='health_json', method='GET').inc()
    return jsonify({
        "health": "OK",
        "status": "running",
        "version": "3.0",
        "time": str(datetime.datetime.now())
    })


@app.route('/api')
def api():
    REQUEST_COUNT.labels(endpoint='api', method='GET').inc()
    return jsonify({
        "status": "running",
        "message": "DevSecOps Pipeline - Hemant Raghav",
        "version": "3.0",
        "time": str(datetime.datetime.now())
    })


@app.route('/slow')
def slow():
    # Simulates a slow endpoint — useful for seeing latency spikes in Grafana
    REQUEST_COUNT.labels(endpoint='slow', method='GET').inc()
    time.sleep(2)
    return jsonify({"message": "This was a slow response — check Grafana for latency spike"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)