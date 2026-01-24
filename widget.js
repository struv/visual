// Visual effects widget - refined
(function() {
  let flipX = false;
  let filled = false;

  function apply() {
    const main = document.querySelector('main');
    if (!main) return;

    // Remove old clones
    document.querySelectorAll('.fill-clone').forEach(el => el.remove());

    if (!filled) {
      main.style.transform = flipX ? 'scaleX(-1)' : '';
      main.style.position = '';
      main.style.left = '';
      main.style.top = '';
      main.style.width = '';
      main.style.height = '';
      main.style.display = '';
      return;
    }

    // Fill mode: tile content to cover viewport
    const content = main.querySelector('#canvas, .ascii-art, pre') || main;
    const rect = content.getBoundingClientRect();
    const tileW = Math.max(rect.width, 50);
    const tileH = Math.max(rect.height, 50);

    const colsLeft = Math.ceil(rect.left / tileW) + 1;
    const colsRight = Math.ceil((window.innerWidth - rect.left) / tileW) + 1;
    const rowsUp = Math.ceil(rect.top / tileH) + 1;
    const rowsDown = Math.ceil((window.innerHeight - rect.top) / tileH) + 1;

    main.style.position = 'fixed';
    main.style.left = rect.left + 'px';
    main.style.top = rect.top + 'px';
    main.style.width = tileW + 'px';
    main.style.height = tileH + 'px';
    main.style.display = 'block';
    main.style.transform = flipX ? 'scaleX(-1)' : '';

    for (let r = -rowsUp; r < rowsDown; r++) {
      for (let c = -colsLeft; c < colsRight; c++) {
        if (r === 0 && c === 0) continue;
        const clone = main.cloneNode(true);
        clone.className = 'fill-clone';
        clone.style.position = 'fixed';
        clone.style.left = (rect.left + c * tileW) + 'px';
        clone.style.top = (rect.top + r * tileH) + 'px';
        clone.style.width = tileW + 'px';
        clone.style.height = tileH + 'px';
        clone.style.display = 'block';
        // Mirror adjacent tiles for seamless edges
        const mirrorH = ((c % 2) + 2) % 2 === 1;
        const mirrorV = ((r % 2) + 2) % 2 === 1;
        const scaleX = (mirrorH !== flipX) ? -1 : 1;
        const scaleY = mirrorV ? -1 : 1;
        clone.style.transform = `scale(${scaleX}, ${scaleY})`;
        document.body.appendChild(clone);
      }
    }

    const src = main.querySelector('#canvas');
    if (src) {
      const sync = () => {
        const txt = src.textContent;
        document.querySelectorAll('.fill-clone #canvas').forEach(c => c.textContent = txt);
        if (filled) requestAnimationFrame(sync);
      };
      requestAnimationFrame(sync);
    }
  }

  function init() {
    const w = document.createElement('div');
    w.innerHTML = `
      <style>
        .vfx-widget {
          position: fixed;
          bottom: 1rem;
          left: 1rem;
          z-index: 9999;
          display: flex;
          gap: 0.5rem;
          opacity: 0.3;
          transition: opacity 0.3s;
        }
        .vfx-widget:hover {
          opacity: 1;
        }
        .vfx-widget button {
          background: transparent;
          border: 1px solid #222;
          color: #444;
          width: 28px;
          height: 28px;
          border-radius: 3px;
          cursor: pointer;
          font-family: system-ui, sans-serif;
          font-size: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.2s;
        }
        .vfx-widget button:hover {
          border-color: #444;
          color: #888;
        }
        .vfx-widget button.on {
          background: #1a1a1a;
          border-color: #444;
          color: #fff;
        }
        .back-link, .info {
          z-index: 10000 !important;
        }
        .fill-clone {
          z-index: 1;
          pointer-events: none;
        }
        main {
          z-index: 2;
        }

        /* Page entrance animation */
        body {
          animation: fadeIn 0.6s ease-out;
        }
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
      </style>
      <button title="Mirror" aria-label="Toggle horizontal mirror">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 3v18M7 6l-4 6 4 6M17 6l4 6-4 6"/>
        </svg>
      </button>
      <button title="Tile" aria-label="Toggle tiled view">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
          <rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>
        </svg>
      </button>
    `;
    w.className = 'vfx-widget';

    const [btnFlip, btnFill] = w.querySelectorAll('button');

    btnFlip.onclick = () => {
      flipX = !flipX;
      btnFlip.classList.toggle('on', flipX);
      apply();
    };

    btnFill.onclick = () => {
      filled = !filled;
      btnFill.classList.toggle('on', filled);
      apply();
    };

    document.body.appendChild(w);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
