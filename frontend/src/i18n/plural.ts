// English pluralization only
type EnForms = [one: string, many: string];

const FORMS: Record<string, { en: EnForms }> = {
  chapters: { en: ["chapter", "chapters"] },
  questions: { en: ["question", "questions"] },
  waves: { en: ["wave", "waves"] },
  days: { en: ["day", "days"] },
  employees: { en: ["employee", "employees"] },
  courses: { en: ["course", "courses"] },
  attempts: { en: ["attempt", "attempts"] },
};

export function pluralize(count: number, category: keyof typeof FORMS): string {
  const forms = FORMS[category];
  const word = count === 1 ? forms.en[0] : forms.en[1];
  return `${count} ${word}`;
}

export function getPluralWord(count: number, singular: string, plural: string): string {
  return count === 1 ? singular : plural;
}

export function getPluralRule(): (n: number) => number {
  return (n: number) => n === 1 ? 0 : 1;
}

export function getPluralForm(n: number, forms: string[]): string {
  const index = n === 1 ? 0 : 1;
  return forms[index] || forms[0];
}

export const pluralRules: Record<string, (n: number) => number> = {
  en: getPluralRule(),
};

export function getPlural(forms: string[], n: number): string {
  const rule = getPluralRule();
  return forms[rule(n)] || forms[0];
}