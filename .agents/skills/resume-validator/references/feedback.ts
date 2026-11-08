type Metric =
  | "human_readability"
  | "completeness"
  | "impact"
  | "consistency"
  | "ats_readiness";

export type ResumeFeedback = Array<{
  metric: Metric; // Locked metric name; return metrics in the union order above.
  score: number; // Integer from 1–100: 1 means severe problems; 100 means no material problems.
  feedback: Array<{
    // Findings for this metric; use an empty array when there are none.
    reason: string; // Specific evidence explaining the issue.
    score: number; // Integer from 1–99 deducted from the metric score.
    suggestion: string; // Actionable way to mitigate the issue.
  }>;
}>;
