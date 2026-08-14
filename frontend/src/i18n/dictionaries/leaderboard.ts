export const leaderboardEn = {
  leaderboard: {
    navLink: "Leaderboard",
    title: "Leaderboard",
    subtitle: "Your standing in the company and your department by completion rate",
    disabled: "The leaderboard hasn't been enabled by an administrator yet.",
    companyTitle: "Company-wide",
    departmentTitle: "In “{name}”",
    noDepartment: "You're not assigned to a department, so a department ranking isn't available.",
    you: "You",
    yourPlace: "Your place: {rank} of {total} ({percent}%)",
    empty: "No ranking data yet.",
  },
  consoleLeaderboard: {
    title: "Leaderboard",
    subtitle: "Public employee ranking by course completion rate",
    enabled: "Show employees the company and department leaderboard",
    enabledHint: "Off by default - this is an HR-sensitive topic, a public completion ranking can demotivate people who are behind. Employees only see the top 10 and their own place, never the full list.",
    saveFailed: "Failed to save settings",
  },
};

// Export only English version
export const leaderboard = leaderboardEn;