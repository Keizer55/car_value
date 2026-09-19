"""Record the README / portfolio demo of the Streamlit app with Playwright.

Usage (app must already be running):
    streamlit run app/streamlit/app.py --server.headless true --server.port 8599
    python scripts/record-demo.py --url http://localhost:8599 --out <scratch dir>

Writes the raw .webm to --out (keep it out of the repo); see
dicetamer/docs/prompts/demo_capture_spec.md for the ffmpeg export steps.
"""

import argparse
import shutil
from pathlib import Path
import time

from playwright.sync_api import sync_playwright

VIEWPORT = {"width": 1280, "height": 800}

# Fake cursor (headless video has none) + hide Streamlit chrome.
INIT_SCRIPT = """
(() => {
  const css = `
    header, #MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] { visibility: hidden !important; }
    #demo-cursor { position: fixed; z-index: 2147483647; width: 22px; height: 30px;
      pointer-events: none; transform-origin: 0 0; transition: transform .1s;
      filter: drop-shadow(0 1px 2px rgba(0,0,0,.6)); }
    .demo-ripple { position: fixed; z-index: 2147483646; width: 40px; height: 40px;
      margin: -20px 0 0 -20px; border-radius: 50%; pointer-events: none;
      border: 3px solid #FF4B4B; animation: demo-ripple .5s ease-out forwards; }
    @keyframes demo-ripple { from { transform: scale(.3); opacity: 1 } to { transform: scale(1.4); opacity: 0 } }
  `;
  const install = () => {
    if (document.getElementById('demo-cursor')) return;
    const style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);
    const dot = document.createElement('div');
    dot.id = 'demo-cursor';
    // Classic arrow pointer; its tip (0,0) is the hotspot.
    dot.innerHTML = '<svg width="22" height="30" viewBox="0 0 22 30"><path d="M1 1 L1 23 L6.5 17.5 L10.5 27 L14 25.5 L10 16.5 L18 16.5 Z" fill="#fff" stroke="#000" stroke-width="1.5" stroke-linejoin="round"/></svg>';
    dot.style.left = '640px'; dot.style.top = '400px';
    document.body.appendChild(dot);
    window.addEventListener('mousemove', e => {
      dot.style.left = e.clientX + 'px'; dot.style.top = e.clientY + 'px';
    }, true);
    window.addEventListener('mousedown', e => {
      dot.style.transform = 'scale(.85)';
      const r = document.createElement('div');
      r.className = 'demo-ripple';
      r.style.left = e.clientX + 'px'; r.style.top = e.clientY + 'px';
      document.body.appendChild(r);
      setTimeout(() => r.remove(), 600);
    }, true);
    window.addEventListener('mouseup', () => { dot.style.transform = ''; }, true);
  };
  if (window.top !== window) return;  // only the main frame
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', install);
  else install();
})();
"""


def wait_idle(page, settle_ms=300):
    """Wait until Streamlit has finished rerunning."""
    page.wait_for_timeout(150)
    page.wait_for_selector('[data-testid="stStatusWidget"]', state="detached", timeout=60_000)
    page.wait_for_timeout(settle_ms)


def move_to(page, locator, dx=0.5, dy=0.5):
    box = locator.bounding_box()
    x, y = box["x"] + box["width"] * dx, box["y"] + box["height"] * dy
    page.mouse.move(x, y, steps=20)
    return x, y


def click(page, locator, **kw):
    move_to(page, locator, **kw)
    page.wait_for_timeout(120)
    page.mouse.down()
    page.mouse.up()


def pick(page, label, option):
    """Open a sidebar selectbox and choose an option by its visible text."""
    box = page.locator('[data-testid="stSidebar"] [data-testid="stSelectbox"]').filter(has_text=label)
    click(page, box.locator('[data-baseweb="select"]'), dx=0.6)
    page.wait_for_timeout(500)
    opt = page.locator('[role="option"]').filter(has_text=option).first
    click(page, opt, dx=0.3)
    wait_idle(page, 500)


def scroll_main(page, total, step=60, pause=30):
    for _ in range(int(abs(total) / step)):
        page.mouse.wheel(0, step if total > 0 else -step)
        page.wait_for_timeout(pause)


def run(url, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport=VIEWPORT,
            device_scale_factor=1,
            record_video_dir=str(out_dir),
            record_video_size=VIEWPORT,
        )
        context.add_init_script(INIT_SCRIPT)
        page = context.new_page()

        t0 = time.monotonic()
        page.goto(url)
        page.wait_for_selector('[data-testid="stSidebar"] [data-testid="stSelectbox"]', timeout=60_000)
        wait_idle(page, 500)
        # Decline the cookie dialog (no analytics); this lead-in is trimmed in export.
        decline = page.get_by_role("button", name="Decline")
        try:
            decline.wait_for(timeout=8_000)
            decline.click()
            page.wait_for_selector('[data-testid="stDialog"]', state="detached", timeout=10_000)
        except Exception:
            pass
        wait_idle(page, 300)
        page.mouse.move(640, 400)

        # 1. Land
        print(f"demo starts at {time.monotonic() - t0:.2f}s into raw.webm")
        page.wait_for_timeout(1200)
        page.mouse.move(700, 450, steps=10)
        page.wait_for_timeout(600)

        # 2. Fill in a SEAT León-like car: petrol, C-segment hatchback, 5 years, 75,000 km
        pick(page, "Fuel type", "Gasolina")
        pick(page, "Brand", "Seat")
        pick(page, "Segment", "C")
        pick(page, "Body type", "Hatchback")

        age = page.locator('[data-testid="stSidebar"] [data-testid="stSlider"]').filter(has_text="Age")
        click(page, age.locator('[role="slider"]'))
        for _ in range(3):  # default 2 -> 5
            page.keyboard.press("ArrowRight")
            page.wait_for_timeout(180)
        wait_idle(page, 400)

        click(page, page.locator('[data-testid="stSidebar"] [data-testid="stCheckbox"]').filter(has_text="Manual km input"), dx=0.08)
        wait_idle(page, 400)
        km = page.locator('[data-testid="stSidebar"] [data-testid="stNumberInput"] input')
        # The input appears below the sidebar fold: wheel-scroll the sidebar to it.
        page.mouse.move(150, 600, steps=10)
        for _ in range(6):
            page.mouse.wheel(0, 60)
            page.wait_for_timeout(40)
        page.wait_for_timeout(300)
        km.scroll_into_view_if_needed()
        click(page, km)
        km.select_text()
        page.keyboard.type("75000", delay=60)
        page.keyboard.press("Enter")
        wait_idle(page, 700)

        # 3. Predict
        click(page, page.get_by_role("button", name="Predict"))
        print(f"predict clicked at {time.monotonic() - t0:.2f}s")
        wait_idle(page, 300)
        page.wait_for_selector('[data-testid="stMetric"]', timeout=60_000)
        wait_idle(page, 800)
        print(f"results ready at {time.monotonic() - t0:.2f}s")

        # 4. Payoff: scroll through table, charts and KPIs
        page.mouse.move(760, 500, steps=15)
        page.wait_for_timeout(1500)
        for chunk, hold in [(420, 1600), (560, 1800), (560, 1800), (560, 2200)]:
            scroll_main(page, chunk)
            page.wait_for_timeout(hold)

        video = page.video
        context.close()
        browser.close()
        raw = Path(video.path())
        dest = out_dir / "raw.webm"
        shutil.move(raw, dest)
        print(dest)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://localhost:8599")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    run(a.url, Path(a.out))
