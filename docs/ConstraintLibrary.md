# Constraint Library: The "Guardrails"

## 1. Financial Constraints
| Constraint | Type | Definition & Logic |
| :--- | :--- | :--- |
| **Budget Cap** | Hard | Cannot approve spend > 10% above allocated line item without CFO override. |
| **EBITDA Floor** | Hard | Any decision reducing EBITDA below 15% margin triggers an automatic warning. |
| **Hiring Lag** | Soft | Assume 45 days from "Job Posted" to "Employee Start Date". Costs don't hit immediately. |
| **Payment Terms** | Soft | Standard is Net-30. Extending to Net-60 requires Vendor Management approval. |

## 2. Operational Constraints
| Constraint | Type | Definition & Logic |
| :--- | :--- | :--- |
| **Warehouse Capacity**| Hard | Utilization cannot exceed 90% (safety hazard + efficiency drop). |
| **Fleet Limits** | Hard | Max driving hours = 11 hours/day (DOT regulations). |
| **Lead Time** | Hard | Supplier X requires 6 weeks lead time. Orders placed today arrive in Q3. |
| **Labor Mix** | Soft | Ratio of Full-time to Contractor should ideally stay 70/30. |

## 3. Compliance & Risk Constraints
| Constraint | Type | Definition & Logic |
| :--- | :--- | :--- |
| **GDPR/PII** | Hard | Marketing lists cannot be exported to personal emails. |
| **Brand Safety** | Hard | No ad spend on platforms flagged as "high risk" (gambling, adult). |
| **Contract Min** | Hard | We have a committed minimum spend of \$50k/month with AWS. Don't optimize below this. |
