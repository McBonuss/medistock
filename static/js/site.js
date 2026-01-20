(async function() {
  const badge = document.getElementById('cartCount');
  if (!badge) return;
  try {
    const res = await fetch('/cart/count.json');
    if (!res.ok) return;
    const data = await res.json();
    badge.textContent = data.count;
  } catch (e) {
    // ignore
  }
})();
