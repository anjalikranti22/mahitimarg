import { ui, defaultLang } from './ui';

export function getLangFromUrl(url: URL) {
  const [, lang] = url.pathname.split('/');
  if (lang in ui) return lang as keyof typeof ui;
  return defaultLang;
}

export function useTranslations(lang: keyof typeof ui) {
  return function t(key: keyof typeof ui[typeof defaultLang]) {
    // Return translation if exists for the given language, fallback to default language if not
    return ui[lang][key] || ui[defaultLang][key];
  };
}

export function getRouteFromUrl(url: URL): string | undefined {
  const pathname = new URL(url).pathname;
  const parts = pathname.split('/');
  
  if (parts.length > 1 && parts[1] in ui) {
    // If it's a localized URL (e.g., /en/about), remove the /en
    return '/' + parts.slice(2).join('/');
  }
  
  // Otherwise, return original pathname
  return pathname;
}
