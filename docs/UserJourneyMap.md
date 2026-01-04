# User Journey Map: From Data to Decision

## Phase 1: Ingest & Health Check
**User Goal**: "I want to make sure my data is clean before I trust the AI."

1.  **Action**: User drags & drops `Q3_Budget_Final.csv` into the upload zone.
2.  **System Response**:
    *   Scans for anomalies (e.g., "Row 45 has a negative value for 'Revenue'").
    *   Displays **Data Health Score**: 92/100.
3.  **Trust Cue**: "3 anomalies found and auto-corrected. [View Log]" (Transparency).

## Phase 2: Exploration & "Smart Questions"
**User Goal**: "I don't know exactly what to ask to find the hidden risks."

1.  **Action**: User views the dashboard.
2.  **System Response**: Presents 3 "Smart Questions" based on the data:
    *   *Ranked #1*: "Why is the Northeast region 15% below margin target?" (High Impact).
    *   *Ranked #2*: "Compare Q3 marketing spend vs. Q2."
3.  **User Choice**: Clicks Question #1.

## Phase 3: Scenario Building
**User Goal**: "I need to prove my recommendation is robust."

1.  **Action**: User opens "Scenario Builder".
2.  **UI Interaction**:
    *   Adjusts **"Hiring Freeze"** slider to "ON".
    *   Adjusts **"Marketing Spend"** slider to "-10%".
3.  **System Response**: Real-time update of the "EBITDA Projection" chart (Baseline vs. Scenario A).
    *   Visual: Diverging line chart showing the saved cash flow.

## Phase 4: Decision Memo & Export
**User Goal**: "I need something I can email to the CFO in 5 minutes."

1.  **Action**: User clicks "Generate Decision Memo".
2.  **System Response**: Creates a 1-pager.
3.  **Key Elements**:
    *   **Recommendation**: "Implement hiring freeze immediately."
    *   **Confidence Score**: "High (85%) - based on historical attrition rates."
    *   **Unknowns**: "Analysis assumes Q4 sales remain flat." (Honesty).
4.  **Action**: User clicks "Export to PDF".
