// Prüft alle Varianten über eine Parametermatrix: node packaging/tests/check_all.js
// Lädt den DOM-freien Geometriekern direkt aus der HTML-Datei.
const fs = require('fs'), path = require('path'), vm = require('vm');
const html = fs.readFileSync(path.join(__dirname, '..', 'rahmenbox-generator.html'), 'utf8');
const src = html.split('<script>')[1].split('</script>')[0];
const mod = { exports: {} };
vm.runInNewContext(src, { module: mod, console, Math, Date, JSON, Infinity, Uint8Array, Uint16Array, Int32Array, Map, Set, Array, Object, Number, isFinite });
const C = mod.exports;
let failed = 0, n = 0;
for (const variant of Object.keys(C.VARIANTS))
  for (const [X, Y, Z, w, t] of [[60, 80, 35, 10, 0.3], [90, 90, 90, 15, 0.45], [20, 25, 10, 8, 0.1], [90, 30, 60, 10, 0.15], [40, 90, 20, 12, 0.3], [50, 50, 50, 20, 0.3]])
    for (const tuck of [true, false]) {
      const O = C.build({ variant, X, Y, Z, w, t, gsm: 200, tuck });
      const fails = C.verify(O).filter(r => r.lvl === 'fail');
      n++;
      if (fails.length) { failed++; console.log('FAIL', variant, X, Y, Z, w, t, tuck, fails.map(f => f.label + ': ' + f.detail).join(' | ')); }
    }
const O = C.build({ variant: 'windrad', X: 40, Y: 50, Z: 25, w: 8, t: 0.3, gsm: 200, tuck: true });
const N = C.nest(O, { W: 297, H: 210, margin: 5, spacing: 2 });
if (N.n < 3) { failed++; console.log('FAIL Nesting A4: erwartet ≥ 3, erhalten', N.n); }
console.log(`${n} Konfigurationen geprüft, ${failed} Fehler; Nesting A4: ${N.n} Stück (${N.method})`);
process.exit(failed ? 1 : 0);
