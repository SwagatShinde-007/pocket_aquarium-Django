(() => {
  "use strict";

  const tank = document.getElementById("tank");
  const panel = document.getElementById("panel");
  const csrf = document.querySelector('meta[name="csrf-token"]').content;
  const fishCount = document.getElementById("fishCount");
  const mealCount = document.getElementById("mealCount");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const rand = (min, max) => Math.random() * (max - min) + min;
  const post = (url) =>
    fetch(url, { method: "POST", headers: { "X-CSRFToken": csrf } }).then((r) => {
      if (!r.ok) throw new Error("Request failed: " + r.status);
      return r.json();
    });

  /* ---------- Bubbles ---------- */
  const bubbles = document.getElementById("bubbles");
  if (!reduceMotion) {
    for (let i = 0; i < 24; i++) {
      const b = document.createElement("span");
      b.className = "bubble";
      b.style.setProperty("--x", rand(2, 98).toFixed(1) + "%");
      b.style.setProperty("--s", rand(6, 22).toFixed(0) + "px");
      b.style.setProperty("--d", rand(7, 16).toFixed(1) + "s");
      b.style.setProperty("--del", (-rand(0, 16)).toFixed(1) + "s");
      b.style.setProperty("--dx", rand(-50, 50).toFixed(0) + "px");
      bubbles.appendChild(b);
    }
  }

  /* ---------- Panel ---------- */
  const toggle = document.getElementById("panelToggle");
  toggle.addEventListener("click", () => {
    const collapsed = panel.classList.toggle("is-collapsed");
    toggle.textContent = collapsed ? "Show" : "Hide";
    toggle.setAttribute("aria-expanded", String(!collapsed));
  });

  // The slider says "slow -> fast" but the model stores seconds per crossing,
  // so the two are mirrored: seconds = 46 - slider.
  const speedUi = document.getElementById("speedUi");
  const speedReal = document.getElementById("speedReal");
  speedUi.value = 46 - Number(speedReal.value);
  speedUi.addEventListener("input", () => {
    speedReal.value = 46 - Number(speedUi.value);
  });

  /* ---------- Feeding ---------- */
  function burst(swimmer, fish) {
    fish.classList.remove("munch");
    void fish.offsetWidth; // restart the animation
    fish.classList.add("munch");

    const pop = document.createElement("span");
    pop.className = "pop";
    pop.textContent = "+1";
    pop.addEventListener("animationend", () => pop.remove());
    swimmer.appendChild(pop);

    for (let i = 0; i < 7; i++) {
      const c = document.createElement("span");
      c.className = "crumb";
      c.style.setProperty("--cx", rand(-40, 40).toFixed(0) + "px");
      c.style.setProperty("--cy", rand(-10, 46).toFixed(0) + "px");
      c.addEventListener("animationend", () => c.remove());
      swimmer.appendChild(c);
    }
  }

  tank.addEventListener("click", async (event) => {
    const fish = event.target.closest(".fish");
    if (!fish || fish.dataset.busy) return;
    fish.dataset.busy = "1";
    try {
      const data = await post(fish.dataset.feedUrl);
      const swimmer = fish.closest(".swimmer");
      swimmer.style.setProperty("--w", data.size + "px");
      swimmer.querySelector(".tag__level").textContent = data.level;

      const row = document.querySelector(`#roster li[data-id="${swimmer.dataset.id}"]`);
      if (row) {
        row.dataset.meals = data.meals;
        row.querySelector(".roster__level").textContent = data.level;
      }
      mealCount.textContent = Number(mealCount.textContent) + 1;
      burst(swimmer, fish);
    } catch (err) {
      console.error(err);
    } finally {
      delete fish.dataset.busy;
    }
  });

  /* ---------- Releasing fish ---------- */
  panel.addEventListener("click", async (event) => {
    const btn = event.target.closest(".release");
    if (!btn) return;
    const row = btn.closest("li");
    try {
      await post(btn.dataset.releaseUrl);
    } catch (err) {
      console.error(err);
      return;
    }

    const swimmer = tank.querySelector(`.swimmer[data-id="${row.dataset.id}"]`);
    if (swimmer) {
      swimmer.classList.add("leaving");
      setTimeout(() => swimmer.remove(), 850);
    }
    fishCount.textContent = Number(fishCount.textContent) - 1;
    mealCount.textContent = Math.max(0, Number(mealCount.textContent) - Number(row.dataset.meals || 0));

    const list = row.parentElement;
    row.remove();
    if (!list.children.length) {
      list.remove();
      const msg = document.createElement("p");
      msg.className = "empty";
      msg.textContent = "The tank is empty. Add your first fish from the panel.";
      tank.appendChild(msg);
    }
  });

  /* ---------- Welcome the newest fish ---------- */
  const params = new URLSearchParams(window.location.search);
  const newId = params.get("new");
  if (newId) {
    const swimmer = tank.querySelector(`.swimmer[data-id="${CSS.escape(newId)}"]`);
    if (swimmer) swimmer.classList.add("arrive");
    history.replaceState(null, "", window.location.pathname);
  }
})();
