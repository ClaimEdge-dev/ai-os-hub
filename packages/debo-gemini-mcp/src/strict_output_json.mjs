// Strict, dependency-free JSON acceptance for the staged provider-output mapper.
// JSON.parse accepts repeated object keys silently. Scan the exact source text
// after its syntax check to refuse duplicate and escaped-equivalent keys.
// This code does NOT handle an API call or alter the deployed Worker.
const SPACE = c => c === ' ' || c === '\t' || c === '\r' || c === '\n';

function validUnicode(value) {
  for (let j=0;j<value.length;j++) {
    const n=value.charCodeAt(j);
    if (n>=0xd800 && n<=0xdbff) {
      const next=value.charCodeAt(++j);
      if (!(next>=0xdc00 && next<=0xdfff)) throw Error('unpaired surrogate');
    } else if (n>=0xdc00 && n<=0xdfff) throw Error('unpaired surrogate');
  }
}

export function parseUnambiguousJson(text, { maxChars = 32000 } = {}) {
  if (!Number.isSafeInteger(maxChars) || maxChars < 1 || maxChars > 48000 ||
      typeof text !== 'string' || text.length === 0 || text.length > maxChars) throw Error('bounded JSON string required');
  // First require valid JSON syntax. The scanner then checks extra restrictions
  // that vanilla JSON.parse does not enforce.
  const decoded = JSON.parse(text);
  let index=0;
  const spaces=()=>{ while(index<text.length && SPACE(text[index])) index++; };
  function quoted() {
    if (text[index] !== '"') throw Error('object key/string expected');
    const begin=index++;
    for (;;) {
      if (index>=text.length) throw Error('unterminated JSON string');
      const ch=text[index++];
      if (ch === '"') {
        const value=JSON.parse(text.slice(begin,index));
        validUnicode(value);
        return value;
      }
      // JSON.parse already validates the exact escape syntax; advancing past
      // the escape avoids confusing \" and \\ with a closing quote.
      if (ch === '\\') {
        if (index>=text.length) throw Error('trailing escape');
        const next=text[index++];
        if (next === 'u') index+=4;
      }
    }
  }
  function value(depth) {
    if (depth>32) throw Error('JSON nesting limit exceeded');
    spaces();
    const start=text[index];
    if (start === '{') {
      index++;spaces();
      const seen=new Set();
      if (text[index] === '}') {index++;return;}
      for (;;) {
        spaces();
        const key=quoted();
        if (seen.has(key)) throw Error('duplicate JSON key');
        seen.add(key);
        spaces();
        if (text[index++] !== ':') throw Error('missing JSON colon');
        value(depth+1);
        spaces();
        if(text[index] === '}') {index++;return;}
        if(text[index++] !== ',') throw Error('missing object separator');
      }
    }
    if (start === '[') {
      index++;spaces();
      if (text[index] === ']') {index++;return;}
      for (;;) {
        value(depth+1);
        spaces();
        if(text[index] === ']') {index++;return;}
        if(text[index++] !== ',') throw Error('missing array separator');
      }
    }
    if (start === '"') {quoted();return;}
    // Valid primitive syntax was already established by JSON.parse; stop at
    // the surrounding delimiter. This branch never decodes strings.
    while(index<text.length && !',}]'.includes(text[index]) && !SPACE(text[index])) index++;
  }
  value(0);spaces();
  if (index!==text.length) throw Error('trailing JSON content');
  return decoded;
}
