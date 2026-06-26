# Support Triage Prompt

Classify the support ticket and select the best specialist.

## Ticket

`{{message}}`

## Customer Tier

`{{customer_tier}}`

## Output Format

```json
{
  "route": "refund_specialist|billing_specialist|technical_specialist",
  "risk_level": "low|medium|high",
  "reason": "..."
}
```
