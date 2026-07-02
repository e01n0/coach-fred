#!/usr/bin/env node
/* Build whole-combo phrase entries for gen_voice.py.
   Extracts every FIXED token sequence the caller can produce from index.html
   (library combos, freestyle pool, focus setups, pyramid rungs, footwork
   drills), adds southpaw-flipped variants of directional sequences, and emits
   one phrases.json entry per (sequence x call style): a single natural
   utterance instead of stitched atoms. Slugs match what speak() derives at
   runtime: "seq-" + spoken atoms slugified and joined. Run, then render with
   gen_voice.py --styles seq --stitch. */
const fs = require("fs");
const vm = require("vm");

const src = fs.readFileSync(__dirname + "/index.html", "utf8");
function grab(name){
  const start = src.indexOf(`const ${name} = `);
  if(start < 0) throw new Error("not found: " + name);
  const open = src.indexOf("=", start) + 1;
  // find the matching end: first `];` or `};` at the original nesting level
  let depth = 0, i = open;
  for(; i < src.length; i++){
    const ch = src[i];
    if(ch === "[" || ch === "{") depth++;
    else if(ch === "]" || ch === "}"){ depth--; if(depth === 0){ i++; break; } }
  }
  return vm.runInNewContext("(" + src.slice(open, i).trim() + ")");
}

const PRESETS = grab("PRESETS");
const REAL_HEAD = grab("REAL_HEAD");
const REAL_BODY = grab("REAL_BODY");
const FOCUS_SETUPS = grab("FOCUS_SETUPS");
const PYRAMID = grab("PYRAMID");
const FOOT_DRILLS = grab("FOOT_DRILLS");
const SPEAK = grab("SPEAK");

const WORD = {1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight"};
const isDigit = t => Object.prototype.hasOwnProperty.call(SPEAK, t);
const slugify = s => String(s).toLowerCase().trim()
  .replace(/&/g,"and").replace(/['".,!?:;]/g,"")
  .replace(/[^a-z0-9]+/g,"-").replace(/^-+|-+$/g,"");

// spoken atoms (slug source — MUST mirror comboAtoms() in index.html) plus
// phrase units (text source: "both" pairs number+name into one unit, so the
// clip says "one jab, two cross" rather than "one, jab, two, cross")
function partsFor(tokens, style){
  const atoms = [], units = [];
  tokens.forEach(t=>{
    if(!isDigit(t)){ atoms.push(t); units.push(t); return; }
    const pure = /^[1-8]$/.test(t);
    if(style === "numbers"){ const a = pure ? t : SPEAK[t]; atoms.push(a); units.push(pure ? WORD[t] : SPEAK[t]); }
    else if(style === "names"){ atoms.push(SPEAK[t]); units.push(SPEAK[t]); }
    else { // both
      if(pure){ atoms.push(t, SPEAK[t]); units.push(WORD[t] + " " + SPEAK[t]); }
      else { atoms.push(SPEAK[t]); units.push(SPEAK[t]); }
    }
  });
  return {atoms, units};
}
// the text the whole clip should say: one connected phrase, emphasis last
function textFor(units){
  const s = units.join(", ") + "!";
  return s.charAt(0).toUpperCase() + s.slice(1);
}
const flip = tokens => tokens.map(t =>
  t.replace(/\b(left|right)\b/gi, m => m.toLowerCase() === "left" ? "right" : "left"));

// collect every fixed sequence (2+ tokens; single atoms already exist)
const seqs = [];
PRESETS.forEach(p => seqs.push(p[2]));
REAL_HEAD.forEach(c => seqs.push(c.t));
REAL_BODY.forEach(c => seqs.push(c.t));
Object.values(FOCUS_SETUPS).forEach(list => list.forEach(s => seqs.push(s)));
PYRAMID.forEach(s => seqs.push(s));
FOOT_DRILLS.forEach(s => seqs.push(s));
[["1","1"],["1","2"],["1","2","3"]].forEach(s => seqs.push(s));   // warm-up/burnout staples
const withFlips = [];
seqs.forEach(s => {
  withFlips.push(s);
  if(s.some(t => /\b(left|right)\b/i.test(t))) withFlips.push(flip(s));
});

const entries = [];
const seen = new Set();
for(const tokens of withFlips){
  if(tokens.length < 2) continue;
  for(const style of ["numbers","names","both"]){
    const {atoms, units} = partsFor(tokens, style);
    const slug = "seq-" + atoms.map(slugify).join("-");
    if(seen.has(slug)) continue;
    seen.add(slug);
    entries.push({slug, text: textFor(units), style: "seq"});
  }
}

// merge into phrases.json (idempotent)
const phrasesPath = __dirname + "/voice/phrases.json";
const phrases = JSON.parse(fs.readFileSync(phrasesPath, "utf8"));
const have = new Set(phrases.map(p => p.slug));
let added = 0;
for(const e of entries){ if(!have.has(e.slug)){ phrases.push(e); added++; } }
fs.writeFileSync(phrasesPath, JSON.stringify(phrases, null, 1) + "\n");
console.log(`sequences: ${entries.length} unique (${added} new) -> ${phrases.length} phrases total`);
console.log("sample:", entries.slice(0, 4).map(e => `${e.slug} = "${e.text}"`).join(" | "));
