# Database Schema

## Table: sales

| Column | Type | Description |
|--------|------|--------------|
| Row ID | BIGINT | Unique row identifier |
| Order ID | TEXT | Unique order identifier |
| Order Date | TEXT | Date order was placed |
| Ship Date | TEXT | Date order was shipped |
| Ship Mode | TEXT | Shipping method used |
| Customer ID | TEXT | Unique customer identifier |
| Customer Name | TEXT | Customer's full name |
| Segment | TEXT | Customer segment (Consumer/Corporate/Home Office) |
| Country | TEXT | Country |
| City | TEXT | City |
| State | TEXT | State |
| Postal Code | FLOAT | Postal/ZIP code |
| Region | TEXT | Sales region (West/East/Central/South) |
| Product ID | TEXT | Unique product identifier |
| Category | TEXT | Product category (Technology/Furniture/Office Supplies) |
| Sub-Category | TEXT | Product sub-category |
| Product Name | TEXT | Full product name |
| Sales | FLOAT | Sales amount |

## Sample Insights (Baseline)
- Total Sales: ~$2,261,536.78
- Top Category: Technology ($827,455.87)
- Top Region: West ($710,219.68)
- Top Customer: Sean Miller ($25,043.05)