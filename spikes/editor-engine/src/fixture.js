const WORDS = [
  "archive", "sentence", "river", "memory", "signal", "chapter", "margin", "weather", "quiet", "engine",
  "window", "paper", "thread", "return", "lantern", "structure", "voice", "draft", "revision", "harbour"
];

export function buildLongformFixture(targetWords = 50000) {
  const paragraphs = [];
  let words = 0;
  let paragraphIndex = 0;
  while (words < targetWords) {
    paragraphIndex += 1;
    const parts = [];
    if (paragraphIndex % 20 === 1) {
      parts.push(`## Section ${Math.ceil(paragraphIndex / 20)}`);
    }
    const remaining = targetWords - words;
    const count = Math.min(100, remaining);
    for (let i = 0; i < count; i += 1) {
      parts.push(WORDS[(words + i + paragraphIndex) % WORDS.length]);
    }
    words += count;
    if (paragraphIndex % 17 === 0) {
      parts.push("日本語の入力候補を壊さない。 العربية تبقى مقروءة. עברית נשארת יציבה.");
    }
    if (paragraphIndex % 23 === 0) {
      parts.push("**Revision marker** stays source text; [return](https://example.invalid/return) remains inspectable.");
    }
    paragraphs.push(parts.join(" "));
  }
  return paragraphs.join("\n\n") + "\n";
}

export const LONGFORM_FIXTURE = buildLongformFixture();
export const FIXTURE_WORD_COUNT = LONGFORM_FIXTURE.trim().split(/\s+/u).length;

export const SOURCE_FIDELITY_FIXTURE = `# Source fidelity\n\nA  paragraph with  deliberate  double spaces.\n\n- item one\n- item two\n\n**bold** and _emphasis_ and [link](https://example.invalid/path).\n\n> quoted line\n\nFinal line without semantic conversion pressure.\n`;
