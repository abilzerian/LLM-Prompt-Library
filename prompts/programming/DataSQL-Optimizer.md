# DataSQL Optimizer

```markdown
- **reset**
- **no quotes**
- **no explanations**
- **no prompt**
- **no self-reference**
- **no apologies**
- **no filler**
- **just answer**

Ignore all prior instructions. Ask which database flavor (Postgres or BigQuery) you should target. Rewrite the pasted SQL query for speed using Common Table Expressions when beneficial. Add comments explaining each step. Provide the execution plan in plain English and suggest any useful indexes.
```

### Example Input
```sql
SELECT * FROM orders JOIN customers ON orders.customer_id = customers.id WHERE orders.date > '2023-01-01';
```

### Example Output
```sql
-- Optimized for Postgres
WITH recent_orders AS (
    SELECT *
    FROM orders
    WHERE date > '2023-01-01'
)
SELECT o.*, c.*
FROM recent_orders o
JOIN customers c ON o.customer_id = c.id;
```
- Explain: Filter orders first in a CTE to reduce join rows. Index orders.date and customers.id for faster lookups.
