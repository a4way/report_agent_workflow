# LangGraph Showcase – Synthetic Business CSV Pack

This folder contains synthetic CSV datasets tailored for a "CSV-to-Insights Copilot" built with LangGraph.

## Files
- customers.csv — customers with acquisition channels & demographics
- products.csv — product master data with cost & price
- orders.csv — order headers incl. status, device, payment, country
- order_items.csv — items per order with discount, tax & prices
- marketing_spend.csv — daily ad spend by channel & campaign
- web_analytics_daily.csv — daily sessions, users, transactions & revenue by channel

## Joining Keys
- orders.customer_id → customers.customer_id
- order_items.order_id → orders.order_id
- order_items.product_id → products.product_id
- web_analytics_daily.date/channel can be aligned to paid orders aggregated via customers.acquisition_channel

## KPI Hints
- Revenue = SUM(order_items.(net_price + tax_amount) * quantity) on paid orders
- AOV = Revenue / Transactions (orders count) for paid orders
- Conversion Rate (GA-style) = transactions / sessions
- ROAS = Revenue attributed to a channel / marketing_spend.spend (same channel/date window)
- CAC = (Sales + Marketing cost in period) / New customers in period
- Gross Margin = (Revenue - COGS) / Revenue, where COGS = SUM(products.unit_cost * quantity)

All data is synthetic and internally consistent enough for demos. 
