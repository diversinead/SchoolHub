/* Quiz progress persistence: saves DOM state on interaction, restores on load,
   clears only when resetQuiz() is invoked. */
(function () {
  var KEY = 'quiz_progress:' + location.pathname;
  var pending = false;

  function snap() {
    try {
      var s = {};
      var els = document.querySelectorAll('[id]');
      for (var i = 0; i < els.length; i++) {
        var e = els[i];
        var o = { c: e.className, st: e.style.cssText };
        if (!e.querySelector('[id]')) o.h = e.innerHTML;
        var tag = e.tagName;
        if (tag === 'TEXTAREA' || tag === 'INPUT' || tag === 'SELECT') o.v = e.value;
        if ('disabled' in e) o.d = e.disabled;
        s[e.id] = o;
      }
      localStorage.setItem(KEY, JSON.stringify(s));
    } catch (err) { /* ignore quota / privacy errors */ }
    pending = false;
  }

  function schedule() {
    if (pending) return;
    pending = true;
    setTimeout(snap, 100);
  }

  function restore() {
    var raw;
    try { raw = localStorage.getItem(KEY); } catch (e) { return; }
    if (!raw) return;
    var s;
    try { s = JSON.parse(raw); } catch (e) { return; }

    // Pass 1: class / style / value / disabled
    for (var id in s) {
      var el = document.getElementById(id);
      if (!el) continue;
      var o = s[id];
      if ('c' in o) el.className = o.c;
      if ('st' in o) el.style.cssText = o.st;
      if ('v' in o && 'value' in el) el.value = o.v;
      if ('d' in o && 'disabled' in el) el.disabled = o.d;
    }
    // Pass 2: innerHTML only on leaf elements (no descendant IDs)
    for (var id2 in s) {
      var el2 = document.getElementById(id2);
      if (!el2) continue;
      var o2 = s[id2];
      if ('h' in o2 && !el2.querySelector('[id]')) el2.innerHTML = o2.h;
    }

    // Re-sync common JS globals used by the bus_man / PE quiz scripts from DOM.
    // Guard on `=== 'number'` so we don't clobber vars that are maps (e.g. PE ch2's `answered = {}`).
    var ANSWERED_SEL = '.q-card.correct, .q-card.incorrect, .q-card.wrong, .q-card.revealed';
    var CORRECT_SEL = '.q-card.correct';
    try {
      if (typeof window.mcCorrectCount === 'number')
        window.mcCorrectCount = document.querySelectorAll('.answer-box.ans-correct').length;
      if (typeof window.totalAnswered === 'number')
        window.totalAnswered = document.querySelectorAll(ANSWERED_SEL).length;
      if (typeof window.correctCount === 'number')
        window.correctCount = document.querySelectorAll(CORRECT_SEL).length;
      if (typeof window.answered === 'number')
        window.answered = document.querySelectorAll(ANSWERED_SEL).length;
      // topic2_quiz* pattern: mcAnswered (total) + mcCorrect (right)
      if (typeof window.mcAnswered === 'number')
        window.mcAnswered = document.querySelectorAll(ANSWERED_SEL).length;
      if (typeof window.mcCorrect === 'number')
        window.mcCorrect = document.querySelectorAll(CORRECT_SEL).length;

      // bus_man pattern: mcAnswers tracks user state — re-populate .locked so
      // selectMC() won't let the user change an already-checked answer.
      if (typeof window.mcAnswers === 'object' && window.mcAnswers) {
        var groups = document.querySelectorAll('.mc-options[id]');
        for (var g = 0; g < groups.length; g++) {
          var grp = groups[g];
          if (!grp.querySelector('.mc-opt.disabled')) continue;
          window.mcAnswers[grp.id] = window.mcAnswers[grp.id] || {};
          window.mcAnswers[grp.id].locked = true;
          var sel = grp.querySelector('.mc-opt.selected');
          if (sel) {
            var opts = grp.querySelectorAll('.mc-opt');
            var L = ['A', 'B', 'C', 'D', 'E', 'F'];
            for (var k = 0; k < opts.length; k++) {
              if (opts[k] === sel) { window.mcAnswers[grp.id].selected = L[k]; break; }
            }
          }
        }
      }
    } catch (e) { /* best effort */ }
  }

  document.addEventListener('click', schedule, true);
  document.addEventListener('input', schedule, true);
  document.addEventListener('change', schedule, true);
  // Flush before unload so a click within the 100ms debounce isn't lost on close.
  window.addEventListener('pagehide', snap);
  window.addEventListener('beforeunload', snap);

  // Auto-assign stable IDs to elements we want to persist but that lack one,
  // so their state lands in the snapshot. Order-based IDs are stable as long
  // as the quiz HTML structure doesn't change between saves.
  function assignIds() {
    var targets = [
      ['textarea:not([id])', 'qp_ta_'],
      ['.eq-model:not([id])', 'qp_em_'],
      ['.eq-reveal-btn:not([id])', 'qp_erb_']
    ];
    for (var t = 0; t < targets.length; t++) {
      var els = document.querySelectorAll(targets[t][0]);
      for (var i = 0; i < els.length; i++) els[i].id = targets[t][1] + i;
    }
  }

  function init() {
    assignIds();
    restore();
    // Replace any page-defined resetQuiz with a version that also clears storage.
    window.resetQuiz = function () {
      if (!confirm('Reset the quiz? All your answers will be cleared.')) return;
      try { localStorage.removeItem(KEY); } catch (e) {}
      location.reload();
    };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
