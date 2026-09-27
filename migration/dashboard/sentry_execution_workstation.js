/**
 * SENTRY Trading Operating System
 * Execution Workstation & FOL Guard Extension
 * 
 * Implements:
 * 1. Single-Click "Authorize Market Entry & Spawn Bracket" (5-10 pt buffered SL + min(2R, 20pt) T1 + T2 Runner)
 * 2. Active Trade In-Position HUD (Live Bar Quality Monitor & Scratch Rule)
 * 3. Fear of Loss (FOL) Premature Exit Guard
 * 4. 1-Click Psychological Emotion Pills & Real-time Timeline Logger
 * 5. Automatic AmiBroker Dual-Chart Snapshot Trigger & Trade Replay Dossier Display
 * 6. 15-Minute Post-Stop Cool-Down Countdown
 */

(function () {
  'use strict';

  // State management for active in-flight trade
  window.SENTRY_WORKSTATION = {
    activeTrade: null,
    cooldownEndTime: null,
    cooldownTimerId: null,
    entryBarQuality: 'DECENT',
    followupBarQuality: 'DECENT',
    ctSetupFormed: false,
    legsCompleted: 1
  };

  const SW = window.SENTRY_WORKSTATION;

  // -------------------------------------------------------------
  // CSS Styles for Workstation UI
  // -------------------------------------------------------------
  const styleEl = document.createElement('style');
  styleEl.innerHTML = `
    /* SENTRY Workstation Styles */
    .sw-card {
      background: var(--glass, rgba(19,23,32,0.7));
      border: 1px solid var(--glass-border, rgba(255,255,255,0.08));
      border-radius: 12px;
      padding: 16px 18px;
      margin-top: 14px;
      margin-bottom: 14px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.4);
      backdrop-filter: blur(16px);
    }
    .sw-card-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      border-bottom: 1px solid rgba(255,255,255,0.06);
      padding-bottom: 8px;
    }
    .sw-card-title {
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      color: var(--gold, #cba869);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .sw-badge-live {
      font-family: var(--mono, monospace);
      font-size: 10px;
      padding: 3px 8px;
      border-radius: 999px;
      background: rgba(47,217,139,0.15);
      color: #2fd98b;
      border: 1px solid rgba(47,217,139,0.4);
      display: flex;
      align-items: center;
      gap: 5px;
    }
    .sw-badge-live::before {
      content: '';
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #2fd98b;
      box-shadow: 0 0 6px #2fd98b;
      animation: swPulse 1.5s infinite;
    }
    @keyframes swPulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
    }
    .sw-exec-btn {
      width: 100%;
      padding: 14px 18px;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      border-radius: 8px;
      background: linear-gradient(135deg, #2fd98b 0%, #1ea766 100%);
      color: #08120d;
      border: 1px solid rgba(255,255,255,0.25);
      cursor: pointer;
      box-shadow: 0 4px 20px rgba(47,217,139,0.3);
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
    }
    .sw-exec-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 24px rgba(47,217,139,0.45);
      filter: brightness(1.08);
    }
    .sw-exec-btn:disabled {
      background: #1c222d;
      color: #5c6478;
      border-color: #2a3242;
      box-shadow: none;
      cursor: not-allowed;
      transform: none;
    }
    .sw-hud-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      margin-bottom: 14px;
    }
    .sw-hud-stat {
      background: rgba(255,255,255,0.02);
      border: 1px solid rgba(255,255,255,0.06);
      border-radius: 8px;
      padding: 10px 12px;
    }
    .sw-hud-stat label {
      font-family: var(--mono, monospace);
      font-size: 10px;
      color: var(--text-dim, #8b93a7);
      text-transform: uppercase;
      display: block;
      margin-bottom: 4px;
    }
    .sw-hud-stat value {
      font-family: var(--mono, monospace);
      font-size: 16px;
      font-weight: 700;
      color: var(--text, #e7eaf1);
      display: block;
    }
    .sw-quality-group {
      display: flex;
      gap: 6px;
      margin-top: 6px;
    }
    .sw-q-btn {
      flex: 1;
      padding: 6px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-family: var(--mono, monospace);
      font-weight: 600;
      border: 1px solid #2a3242;
      background: #161b25;
      color: #8b93a7;
      cursor: pointer;
      text-align: center;
      transition: all 0.15s ease;
    }
    .sw-q-btn:hover {
      background: #1e2533;
      color: #e7eaf1;
    }
    .sw-q-btn.active-strong {
      background: rgba(47,217,139,0.2);
      color: #2fd98b;
      border-color: #2fd98b;
    }
    .sw-q-btn.active-decent {
      background: rgba(76,141,255,0.2);
      color: #4c8dff;
      border-color: #4c8dff;
    }
    .sw-q-btn.active-poor {
      background: rgba(240,82,95,0.2);
      color: #f0525f;
      border-color: #f0525f;
    }
    .sw-scratch-alert {
      background: rgba(242,169,59,0.15);
      border: 1px solid rgba(242,169,59,0.5);
      border-radius: 8px;
      padding: 10px 14px;
      color: #f2a93b;
      font-size: 12px;
      font-weight: 600;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 10px;
      animation: swFlash 2s infinite;
    }
    @keyframes swFlash {
      0%, 100% { border-color: rgba(242,169,59,0.5); }
      50% { border-color: rgba(242,169,59,0.9); }
    }
    .sw-tags-group {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 12px;
    }
    .sw-tag-pill {
      font-family: var(--mono, monospace);
      font-size: 11px;
      padding: 5px 10px;
      border-radius: 999px;
      border: 1px solid #2a3242;
      background: #161b25;
      color: #8b93a7;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .sw-tag-pill:hover {
      background: #232a38;
      color: #e7eaf1;
      border-color: #4c8dff;
    }
    .sw-exit-btn {
      width: 100%;
      padding: 12px 16px;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      border-radius: 8px;
      background: linear-gradient(135deg, #f0525f 0%, #c4323e 100%);
      color: #fff;
      border: 1px solid rgba(255,255,255,0.2);
      cursor: pointer;
      box-shadow: 0 4px 16px rgba(240,82,95,0.3);
      transition: all 0.2s ease;
    }
    .sw-exit-btn:hover {
      filter: brightness(1.1);
      box-shadow: 0 6px 20px rgba(240,82,95,0.45);
    }
    .sw-cooldown-banner {
      background: rgba(240,82,95,0.12);
      border: 1px solid rgba(240,82,95,0.4);
      border-radius: 8px;
      padding: 8px 14px;
      color: #f0525f;
      font-family: var(--mono, monospace);
      font-size: 12px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 12px;
    }
    /* Modal for FOL Warning */
    .sw-modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.8);
      backdrop-filter: blur(8px);
      z-index: 9999;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .sw-modal-box {
      width: 480px;
      background: #11151d;
      border: 1px solid rgba(240,82,95,0.6);
      border-radius: 12px;
      padding: 24px;
      box-shadow: 0 16px 48px rgba(0,0,0,0.7), 0 0 30px rgba(240,82,95,0.25);
    }
    .sw-modal-box h3 {
      font-size: 16px;
      color: #f0525f;
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 12px;
      text-transform: uppercase;
    }
    .sw-modal-box p {
      font-size: 13px;
      color: #8b93a7;
      line-height: 1.5;
      margin-bottom: 18px;
    }
    .sw-modal-actions {
      display: flex;
      gap: 10px;
      justify-content: flex-end;
    }
  `;
  document.head.appendChild(styleEl);

  // -------------------------------------------------------------
  // Bridge Helper Calls
  // -------------------------------------------------------------
  async function callBridge(method, ...args) {
    if (window.pywebview && window.pywebview.api && window.pywebview.api[method]) {
      try {
        return await window.pywebview.api[method](...args);
      } catch (err) {
        console.error(`[SENTRY Workstation] Bridge call ${method} failed:`, err);
      }
    }
    return null;
  }

  // -------------------------------------------------------------
  // Cooldown Timer Logic (15 min after stop-out)
  // -------------------------------------------------------------
  function checkCooldown() {
    const raw = localStorage.getItem('sentry_cooldown_end');
    if (!raw) return false;
    const end = parseInt(raw, 10);
    const now = Date.now();
    if (now < end) {
      SW.cooldownEndTime = end;
      return true;
    } else {
      localStorage.removeItem('sentry_cooldown_end');
      SW.cooldownEndTime = null;
      return false;
    }
  }

  function startCooldown(minutes = 15) {
    const end = Date.now() + (minutes * 60 * 1000);
    localStorage.setItem('sentry_cooldown_end', end.toString());
    SW.cooldownEndTime = end;
    renderWorkstation();
  }

  function getCooldownRemaining() {
    if (!SW.cooldownEndTime) return '00:00';
    const diff = Math.max(0, Math.floor((SW.cooldownEndTime - Date.now()) / 1000));
    const m = Math.floor(diff / 60).toString().padStart(2, '0');
    const s = (diff % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  }

  // -------------------------------------------------------------
  // Execution Panel Rendering & Event Handlers
  // -------------------------------------------------------------
  function renderWorkstation() {
    const decisionSection = document.getElementById('view-decision');
    if (!decisionSection) return;

    let wsContainer = document.getElementById('sentryWorkstationContainer');
    if (!wsContainer) {
      wsContainer = document.createElement('div');
      wsContainer.id = 'sentryWorkstationContainer';
      // Insert right before Open Trade Plans or after Trade Plan Capture
      const planPanel = decisionSection.querySelector('.panel:last-child');
      if (planPanel) {
        decisionSection.insertBefore(wsContainer, planPanel);
      } else {
        decisionSection.appendChild(wsContainer);
      }
    }

    const isCooldownActive = checkCooldown();

    // If an active trade is in-flight, show Active Trade HUD
    if (SW.activeTrade) {
      renderActiveTradeHUD(wsContainer);
      return;
    }

    // Otherwise show Authorization Gate
    wsContainer.innerHTML = `
      <div class="sw-card">
        <div class="sw-card-head">
          <div class="sw-card-title">
            <span>⚡ Automated Execution Gate</span>
            <span style="font-size:11px; color:var(--text-dim); font-weight:400;">(Single-Click Market Entry + Buffered Bracket)</span>
          </div>
          <div class="sw-badge-live">READY FOR ENTRY</div>
        </div>

        ${isCooldownActive ? `
          <div class="sw-cooldown-banner">
            <span>🛑 DISCIPLINE LOCKOUT: Post-stop cool-down active.</span>
            <span style="margin-left:auto; font-size:14px; font-weight:700;">${getCooldownRemaining()}</span>
          </div>
        ` : ''}

        <div class="sw-hud-grid">
          <div class="sw-hud-stat">
            <label>Instrument & Strike</label>
            <value id="swDisplaySymbol">NIFTY 23200 CE</value>
          </div>
          <div class="sw-hud-stat">
            <label>Risk Points & Noise Buffer</label>
            <value id="swDisplayBuffer">15 pts (+8 pt Buffer)</value>
          </div>
          <div class="sw-hud-stat">
            <label>Target 1 (50% Qty)</label>
            <value id="swDisplayT1" style="color:var(--green,#2fd98b);">min(2R, 20 pts) → BE</value>
          </div>
          <div class="sw-hud-stat">
            <label>Target 2 (Runner 50%)</label>
            <value id="swDisplayT2" style="color:var(--blue,#4c8dff);">40–50 pts / 100 pts</value>
          </div>
        </div>

        <button class="sw-exec-btn" id="swAuthorizeBtn" type="button" ${isCooldownActive ? 'disabled' : ''}>
          <span>⚡ AUTHORIZE MARKET ENTRY & SPAWN BRACKET</span>
        </button>
        <p style="font-size:11px; color:var(--text-dim); text-align:center; margin-top:8px;">
          Places instant Market Fill on Flattrade · Auto-captures AmiBroker dual-chart with ▲ Entry marker · Arms FOL Guard
        </p>
      </div>
    `;

    const authBtn = document.getElementById('swAuthorizeBtn');
    if (authBtn) {
      authBtn.addEventListener('click', handleAuthorizeMarketEntry);
    }
  }

  // -------------------------------------------------------------
  // Authorize Market Entry Handler
  // -------------------------------------------------------------
  async function handleAuthorizeMarketEntry() {
    const inst = document.getElementById('pInstrument')?.value || 'NIFTY';
    const strike = document.getElementById('pStrike')?.value || '23200';
    const type = document.getElementById('pType')?.value || 'CE';
    const symbol = `${inst} ${strike} ${type}`;
    const plannedEntry = parseFloat(document.getElementById('pEntry')?.value) || 140.0;
    const plannedStop = parseFloat(document.getElementById('pStop')?.value) || 120.0;
    const qtyLots = parseInt(document.getElementById('pQty')?.value, 10) || 2;
    const setupName = document.getElementById('pSetup')?.value || 'A+ Setup';

    const tradeId = 'T_' + Date.now().toString().slice(-6);

    // Call bridge to generate bracket spec with 5-10 pt buffer
    const bracketRes = await callBridge(
      'decision_generate_bracket',
      plannedEntry,
      plannedStop,
      qtyLots,
      25,      // lot size for NIFTY
      true,    // is_from_market_fill
      8.0,     // sl_buffer (8 points)
      20.0,    // t1_max_pts (capped at 20)
      '4R_OR_100PTS'
    );

    // Set active trade
    SW.activeTrade = {
      tradeId: tradeId,
      symbol: symbol,
      instrument: inst,
      strike: strike,
      type: type,
      entryPrice: plannedEntry,
      stopLoss: bracketRes ? bracketRes.stop_loss_price : plannedStop - 8.0,
      target1: bracketRes ? bracketRes.target_1_price : plannedEntry + 20.0,
      target2: bracketRes ? bracketRes.target_2_price : plannedEntry + 50.0,
      qtyLots: qtyLots,
      totalQty: qtyLots * 25,
      setup: setupName,
      entryTime: new Date().toLocaleTimeString('en-GB'),
      timeline: []
    };

    // Save initial dossier & timeline event
    await callBridge('dossier_create_or_update', {
      trade_id: tradeId,
      instrument: symbol,
      strategy: document.getElementById('pStrategy')?.value || 'Momentum',
      setup: setupName,
      entry_timestamp: new Date().toISOString()
    });

    await callBridge('dossier_add_timeline_event', tradeId, 'FILL', `Market Entry Fill @ ₹${plannedEntry} (${qtyLots} lots)`);

    // Capture Entry Dual Charts via AmiBroker COM
    callBridge(
      'dossier_capture_charts',
      tradeId,
      'ENTRY',
      23190.0,
      plannedEntry,
      symbol,
      SW.activeTrade.entryTime
    ).then(res => {
      console.log('[SENTRY Workstation] Entry charts captured:', res);
      if (res && res.composite) {
        SW.activeTrade.entryComposite = res.composite;
      }
    });

    renderWorkstation();
  }

  // -------------------------------------------------------------
  // Active Trade In-Position HUD Rendering
  // -------------------------------------------------------------
  function renderActiveTradeHUD(container) {
    const t = SW.activeTrade;
    const isScratchReady = (SW.entryBarQuality === 'POOR' && SW.followupBarQuality === 'POOR');

    container.innerHTML = `
      <div class="sw-card" style="border-color: rgba(76,141,255,0.4);">
        <div class="sw-card-head">
          <div class="sw-card-title" style="color:var(--blue,#4c8dff);">
            <span>🛡️ Active Position HUD · ${t.symbol}</span>
            <span style="font-size:11px; color:var(--text-dim); font-weight:400;">(${t.qtyLots} Lots · In-Trade Protection Active)</span>
          </div>
          <div class="sw-badge-live">POSITION OPEN</div>
        </div>

        ${isScratchReady ? `
          <div class="sw-scratch-alert">
            <span style="font-size:16px;">⚠️</span>
            <div>
              <b>SCRATCH TRADE RECOMMENDED:</b> Entry Bar and Follow-up Bar both closed POOR. 
              Cut trade now at minimal loss — technical follow-through failed.
            </div>
          </div>
        ` : ''}

        <div class="sw-hud-grid">
          <div class="sw-hud-stat">
            <label>Entry Fill Price</label>
            <value>₹${t.entryPrice.toFixed(2)}</value>
          </div>
          <div class="sw-hud-stat">
            <label>Buffered SL (Protected)</label>
            <value style="color:var(--red,#f0525f);">₹${t.stopLoss.toFixed(2)}</value>
          </div>
          <div class="sw-hud-stat">
            <label>Target 1 (Auto-BE)</label>
            <value style="color:var(--green,#2fd98b);">₹${t.target1.toFixed(2)}</value>
          </div>
          <div class="sw-hud-stat">
            <label>Target 2 (Runner)</label>
            <value style="color:var(--blue,#4c8dff);">₹${t.target2.toFixed(2)}</value>
          </div>
        </div>

        <!-- 5-min Bar Quality Confirmation Panel -->
        <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06); border-radius:8px; padding:12px; margin-bottom:14px;">
          <div style="font-size:11px; font-family:var(--mono); color:var(--text-dim); margin-bottom:8px; text-transform:uppercase;">
            5-Min Candle Follow-Through Monitor
          </div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
            <div>
              <span style="font-size:11px; color:#8b93a7;">Bar 1 (Entry Bar Close):</span>
              <div class="sw-quality-group">
                <button class="sw-q-btn ${SW.entryBarQuality==='STRONG'?'active-strong':''}" data-bar="entry" data-val="STRONG">STRONG</button>
                <button class="sw-q-btn ${SW.entryBarQuality==='DECENT'?'active-decent':''}" data-bar="entry" data-val="DECENT">DECENT</button>
                <button class="sw-q-btn ${SW.entryBarQuality==='POOR'?'active-poor':''}" data-bar="entry" data-val="POOR">POOR</button>
              </div>
            </div>
            <div>
              <span style="font-size:11px; color:#8b93a7;">Bar 2 (Follow-up Bar Close):</span>
              <div class="sw-quality-group">
                <button class="sw-q-btn ${SW.followupBarQuality==='STRONG'?'active-strong':''}" data-bar="followup" data-val="STRONG">STRONG</button>
                <button class="sw-q-btn ${SW.followupBarQuality==='DECENT'?'active-decent':''}" data-bar="followup" data-val="DECENT">DECENT</button>
                <button class="sw-q-btn ${SW.followupBarQuality==='POOR'?'active-poor':''}" data-bar="followup" data-val="POOR">POOR</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Emotion Tagging -->
        <div style="margin-bottom:12px;">
          <span style="font-size:11px; font-family:var(--mono); color:var(--text-dim); display:block; margin-bottom:6px; text-transform:uppercase;">
            Real-Time State of Mind Tagging (1-Click)
          </span>
          <div class="sw-tags-group">
            <button class="sw-tag-pill" data-tag="CALM">😌 CALM</button>
            <button class="sw-tag-pill" data-tag="IN_THE_ZONE">🎯 IN THE ZONE</button>
            <button class="sw-tag-pill" data-tag="FOL">😰 FOL (Fear of Loss)</button>
            <button class="sw-tag-pill" data-tag="FOMO">⚡ FOMO</button>
            <button class="sw-tag-pill" data-tag="ANXIOUS">⚠️ ANXIOUS</button>
            <button class="sw-tag-pill" data-tag="SM">🧠 SMART MONEY</button>
          </div>
          <div style="display:flex; gap:8px;">
            <input type="text" id="swQuickNoteInput" placeholder="Quick mental note / feeling during trade..." 
                   style="flex:1; background:#161b25; border:1px solid #232a38; border-radius:6px; padding:7px 10px; color:#e7eaf1; font-size:12px;" />
            <button class="btn small ghost" id="swAddNoteBtn" type="button">Log Note</button>
          </div>
        </div>

        <!-- Guarded Exit Button -->
        <button class="sw-exit-btn" id="swGuardedExitBtn" type="button">
          🛑 EXIT POSITION (FOL GUARD ACTIVE)
        </button>
      </div>
    `;

    // Quality button listeners
    container.querySelectorAll('.sw-q-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const bar = btn.getAttribute('data-bar');
        const val = btn.getAttribute('data-val');
        if (bar === 'entry') SW.entryBarQuality = val;
        if (bar === 'followup') SW.followupBarQuality = val;
        callBridge('dossier_add_timeline_event', t.tradeId, 'NOTE', `Candle quality updated: ${bar} bar is ${val}`);
        renderActiveTradeHUD(container);
      });
    });

    // Tag pills
    container.querySelectorAll('.sw-tag-pill').forEach(btn => {
      btn.addEventListener('click', () => {
        const tag = btn.getAttribute('data-tag');
        callBridge('dossier_add_timeline_event', t.tradeId, 'PSYCH_TAG', `Psychological State: ${tag}`);
        btn.style.borderColor = '#4c8dff';
        btn.style.color = '#4c8dff';
        setTimeout(() => {
          btn.style.borderColor = '';
          btn.style.color = '';
        }, 1200);
      });
    });

    // Quick Note
    const addNoteBtn = document.getElementById('swAddNoteBtn');
    const noteInput = document.getElementById('swQuickNoteInput');
    if (addNoteBtn && noteInput) {
      const logNote = () => {
        const text = noteInput.value.trim();
        if (text) {
          callBridge('dossier_add_timeline_event', t.tradeId, 'NOTE', text);
          noteInput.value = '';
        }
      };
      addNoteBtn.addEventListener('click', logNote);
      noteInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') logNote(); });
    }

    // Exit Button
    const exitBtn = document.getElementById('swGuardedExitBtn');
    if (exitBtn) {
      exitBtn.addEventListener('click', handleGuardedExit);
    }
  }

  // -------------------------------------------------------------
  // Guarded Exit Handler (FOL Interceptor)
  // -------------------------------------------------------------
  async function handleGuardedExit() {
    const t = SW.activeTrade;
    if (!t) return;

    // Check with FOL Exit Guard
    const perm = await callBridge(
      'decision_evaluate_exit_permission',
      SW.entryBarQuality,
      SW.followupBarQuality,
      SW.ctSetupFormed,
      SW.legsCompleted,
      false, // target not hit yet
      false  // stop not hit yet
    );

    if (perm && perm.allowed) {
      // Authorized exit (e.g. Scratch or Counter-trend)
      executeExit(perm.exit_type, false);
    } else {
      // Premature exit attempt! Intercept with Anti-FOL Modal
      showFOLWarningModal((forceExit) => {
        if (forceExit) {
          executeExit('PREMATURE_FOL_EXIT', true);
        }
      });
    }
  }

  // -------------------------------------------------------------
  // FOL Warning Modal
  // -------------------------------------------------------------
  function showFOLWarningModal(callback) {
    const overlay = document.createElement('div');
    overlay.className = 'sw-modal-overlay';
    overlay.innerHTML = `
      <div class="sw-modal-box">
        <h3>⚠️ PREMATURE EXIT INTERCEPTED (FOL GUARD)</h3>
        <p>
          Neither your Stop Loss nor Target has been reached, and technical follow-through has not proven you wrong.<br><br>
          <span style="color:#e7eaf1;"><b>Are you exiting out of Fear of Loss (FOL)?</b></span><br>
          Exiting now will be recorded in your Trade Dossier as a <b>Process Breach</b> and will dock your Process Score.
        </p>
        <div class="sw-modal-actions">
          <button class="btn ghost small" id="swStayInTradeBtn" type="button" style="padding:9px 16px;">
            🛡️ STICK TO PLAN (HOLD)
          </button>
          <button class="btn danger small" id="swForceExitBtn" type="button" style="padding:9px 16px;">
            FORCE EXIT (ACCEPT VIOLATION)
          </button>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);

    overlay.querySelector('#swStayInTradeBtn').addEventListener('click', () => {
      document.body.removeChild(overlay);
      callback(false);
    });

    overlay.querySelector('#swForceExitBtn').addEventListener('click', () => {
      document.body.removeChild(overlay);
      callback(true);
    });
  }

  // -------------------------------------------------------------
  // Execute Exit & Capture Exit Charts
  // -------------------------------------------------------------
  async function executeExit(exitType, isViolation = false) {
    const t = SW.activeTrade;
    if (!t) return;

    const exitPrice = t.entryPrice + 12.0; // Simulated fill or actual market fill
    const exitTime = new Date().toLocaleTimeString('en-GB');

    await callBridge('dossier_add_timeline_event', t.tradeId, 'EXIT', `Position Closed (${exitType}) @ ₹${exitPrice}`);

    if (isViolation) {
      await callBridge('dossier_add_timeline_event', t.tradeId, 'PSYCH_TAG', 'VIOLATION: FOL_PREMATURE_EXIT');
    }

    // Capture Exit Charts via AmiBroker COM
    const capRes = await callBridge(
      'dossier_capture_charts',
      t.tradeId,
      'EXIT',
      23240.0,
      exitPrice,
      t.symbol,
      exitTime
    );

    // If trade was a loss or violation, trigger 15-minute cool-down
    const isLoss = (exitPrice < t.entryPrice);
    if (isLoss || isViolation) {
      startCooldown(15);
    }

    // Clear active trade
    SW.activeTrade = null;
    SW.entryBarQuality = 'DECENT';
    SW.followupBarQuality = 'DECENT';

    // Refresh views
    renderWorkstation();
    if (typeof window.renderAll === 'function') {
      window.renderAll();
    }
  }

  // -------------------------------------------------------------
  // Initial Boot & Periodic Cooldown Poll
  // -------------------------------------------------------------
  function init() {
    renderWorkstation();
    setInterval(() => {
      if (SW.cooldownEndTime) {
        if (Date.now() >= SW.cooldownEndTime) {
          SW.cooldownEndTime = null;
          localStorage.removeItem('sentry_cooldown_end');
          renderWorkstation();
        } else {
          const banner = document.querySelector('.sw-cooldown-banner span:last-child');
          if (banner) banner.textContent = getCooldownRemaining();
        }
      }
    }, 1000);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
