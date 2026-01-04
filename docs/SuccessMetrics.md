# Success Metrics Dashboard

## North Star Metric
*   **Decisions Velocity**: Average time reduction per major decision workflow (Baseline: 4 hours -> Target: 30 mins).

## Key Performance Indicators (KPIs)

### Engagement
*   **Weekly Active Managers (WAM)**: Unique users who perform at least one query/analysis per week.
*   **Memo Generation Rate**: # of Decision Memos generated / Total Active Sessions.
*   **Query Complexity**: Average length/depth of user prompts (Proxy for trust; deeper questions = higher trust).

### Quality & Performance
*   **First-Pass Acceptance**: % of Decision Memos used with <10% manual edits by the user.
*   **Data Latency**: Time from "Data Upload" to "Ready for Analysis". Target: < 30 seconds for 10MB file.
*   **Hallucination Rate**: % of answers flagged as "Inaccurate" by users (measured via Thumbs Down feedback).

### Business Impact (Lagging)
*   **Adoption Speed**: Time for a new department (e.g., from Finance to Ops) to onboard 5+ users.
*   **NPS**: Net Promoter Score from internal stakeholders.

## Dashboard Layout (Mockup)
1.  **Top Row (Real-time)**: Active Users Now | Queries Today | Memos Generated Today
2.  **Middle Row (Trends)**:
    *   [Line Chart] Time-Saved per User (Weekly avg).
    *   [Bar Chart] Top Use Cases (Finance vs Ops vs Growth).
3.  **Bottom Row (Feedback)**:
    *   [List] Recent "Thumbs Down" feedback with user comments (for QA).
    *   [Gauge] System Uptime & API Latency.
