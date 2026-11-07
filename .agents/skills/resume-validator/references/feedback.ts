type Metric =
  | "impact"
  | "consistency"
  | "completeness"
  | "ats_readiness"
  | "human_readability";

export type ResumeFeedback = Array<{
  metric: Metric; // Locked metric name.
  score: number; // Integer from 1–100: 1 means severe problems; 100 means no material problems.
  feedback: Array<{
    // Findings for this metric; use an empty array when there are none.
    reason: string; // Specific evidence explaining the issue.
    priority: number; // Integer from 1–10, where 10 is most urgent.
    suggestion: string; // Actionable way to mitigate the issue.
  }>;
}>;
