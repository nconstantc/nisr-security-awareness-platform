import { pagesEn } from "./dictionaries/pages";
import { profileEn } from "./dictionaries/profile";
import { consoleCoreEn } from "./dictionaries/consoleCore";
import { consoleManageEn } from "./dictionaries/consoleManage";
import { badgesEn } from "./dictionaries/badges";
import { leaderboardEn } from "./dictionaries/leaderboard";
import type { Language } from "./translations";

const dictionaries = {
  en: { ...pagesEn, ...profileEn, ...consoleCoreEn, ...consoleManageEn, ...badgesEn, ...leaderboardEn },
};

export function getDictionary(language: Language) {
  return dictionaries[language] || dictionaries.en;
}

// Export default language
export const defaultLanguage: Language = "en";