import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const uiFilePath = path.join(__dirname, '../src/i18n/ui.ts');
const targetFile = process.argv[2] ? path.resolve(process.cwd(), process.argv[2]) : path.join(__dirname, '../src/components/pages/HomePage.astro');

console.log(`Starting Translation Automation Script...`);
console.log(`Target: ${targetFile}`);

if (!fs.existsSync(uiFilePath)) {
  console.error("ui.ts not found!");
  process.exit(1);
}

const uiContent = fs.readFileSync(uiFilePath, 'utf8');

// Regex parse `mr: { ... }` block
const mrBlockMatch = uiContent.match(/mr:\s*{([\s\S]*?)},\s*en:/);
if (!mrBlockMatch) {
  console.error("Could not find 'mr: { ... }' dictionary block in ui.ts");
  process.exit(1);
}

const mrText = mrBlockMatch[1];
const lineMatches = [...mrText.matchAll(/'([^']+)':\s*'([^']+)'/g)];

const dictionary = {};
// Sort by longest value first to prevent partial substrings from matching before longer strings
for (const m of lineMatches) {
  dictionary[m[1]] = m[2];
}
const sortedKeys = Object.keys(dictionary).sort((a, b) => dictionary[b].length - dictionary[a].length);

let code = fs.readFileSync(targetFile, 'utf8');

// Inject import statement if not exists
if (!code.includes("useTranslations") && code.includes("---")) {
  code = code.replace(
    /---\n([\s\S]*?)\n---/,
    `---\nimport { getLangFromUrl, useTranslations } from '../../i18n/utils';\n\nconst lang = getLangFromUrl(Astro.url);\nconst t = useTranslations(lang);\n$1\n---`
  );
  console.log("Injected useTranslations hook into Astro frontmatter.");
}

let replaceCount = 0;

for (const key of sortedKeys) {
  const value = dictionary[key];
  const escapedValue = value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  
  // 1. Exact inner HTML replacements (e.g. >योजना< to >{t('hero.title.schemes')}<)
  const innerHtmlRegex = new RegExp(`>\\s*${escapedValue}\\s*<`, 'g');
  code = code.replace(innerHtmlRegex, (match) => {
    replaceCount++;
    return `>{t('${key}')}<`;
  });

  // 2. Exact attribute replacements (e.g. placeholder="योजना शोधा..." to placeholder={t('search.placeholder')})
  const attrRegex = new RegExp(`="\\s*${escapedValue}\\s*"`, 'g');
  code = code.replace(attrRegex, (match) => {
    replaceCount++;
    return `={t('${key}')}`;
  });

  // 3. Trailing space/exact word replacements (when standalone outside tags, rare but happens)
  // For JSX single strings (e.g. 'योजना' to t('key'))
  const stringRegex = new RegExp(`'${escapedValue}'`, 'g');
  code = code.replace(stringRegex, (match) => {
    if (match.includes("t('")) return match; // skip if already wrapped
    replaceCount++;
    return `t('${key}')`;
  });
}

fs.writeFileSync(targetFile, code);
console.log(`Success! Replaced ${replaceCount} hardcoded Marathi strings with {t('key')} in ${path.basename(targetFile)}.`);
