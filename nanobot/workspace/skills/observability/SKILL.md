# Observability Skill

You have access to system logs and can investigate errors.

## When user asks "What went wrong?" or "Check system health":

1. Check recent error logs using curl to VictoriaLogs API
2. Look for error messages mentioning:
   - "connection is closed" - database connection issue
   - "timeout" - service timeout
   - "500" - internal server error
3. Extract trace_id if available
4. Summarize findings:
   - What service failed
   - What error occurred
   - When it happened
   - Affected operations

## Response format:
- Be concise
- Use bullet points
- Include error message excerpt
- Mention affected components
