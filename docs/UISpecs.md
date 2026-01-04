# UI Screens & Component Specifications

## Core Layout: "The Decision Workspace"
*   **Aesthetic**: Professional, high-contrast, "Bloomberg Terminal met Apple Design". Dark mode default for data density.
*   **Navigation**: Sidebar (Data Sources, Saved Scenarios, History). Main stage is the "Canvas".

## Screen 1: The "Smart Questions" Panel
*   **Location**: Right-hand panel, always accessible.
*   **Component**: `QuestionCard`
    *   **Headline**: The question text.
    *   **Tag**: "High Impact" (Red), "Efficiency" (Blue).
    *   **Interaction**: Hovering reveals *why* the AI generated this question (e.g., "Based on variance in column F").

## Screen 2: Scenario Builder
*   **Layout**: Split screen. Left = Controls; Right = Outcomes.
*   **Controls**:
    *   **Sliders**: For continuous variables (e.g., "Spend: +/- 10%").
    *   **Toggles**: For binary decisions (e.g., "Close Warehouse B?").
*   **Outcomes**:
    *   **Comparison View**: "Baseline" (Grey dashed line) vs. "Proposed" (Solid Green line).
    *   **Delta Badge**: "+$50k Savings" highlighted in green pill.

## Screen 3: The Decision Memo (Output)
*   **Header**: Title, Date, Author, **Confidence Badge**.
*   **Sections**:
    *   **BLUF**: 2-sentence summary.
    *   **Evidence**: 2 Charts (max) with "Source" links below them.
    *   **Trade-offs**: Bulleted list of what we lose (risk).
    *   **Assumption Log**: "We assumed X is true..." (Critical for trust).

## Trust Cues (The "Why")
1.  **Confidence Score**: Not just a % number, but a qualitative label ("High", "Medium", "Low Data").
2.  **Citations**: Clicking a data point in a sentence highlights the specific spreadsheet cell it came from.
3.  **"What We Don't Know"**: A dedicated section for missing data or high-variance assumptions.
