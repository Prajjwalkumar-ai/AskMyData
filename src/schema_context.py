SCHEMA_CONTEXT = """
Table name: sales

Columns:
- "Row ID" (INTEGER) - unique row id
- "Order ID" (TEXT)
- "Order Date" (TEXT) - format: MM/DD/YYYY
- "Ship Date" (TEXT) - format: MM/DD/YYYY
- "Ship Mode" (TEXT)
- "Customer ID" (TEXT)
- "Customer Name" (TEXT)
- "Segment" (TEXT) - values: Consumer, Corporate, Home Office
- "Country" (TEXT)
- "City" (TEXT)
- "State" (TEXT)
- "Postal Code" (FLOAT)
- "Region" (TEXT) - values: West, East, Central, South
- "Product ID" (TEXT)
- "Category" (TEXT) - values: Technology, Furniture, Office Supplies
- "Sub-Category" (TEXT)
- "Product Name" (TEXT)
- "Sales" (FLOAT) - sales amount in dollars
"""