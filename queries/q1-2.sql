SELECT 
  SUM(lo_extendedprice * lo_discount) AS revenue
FROM 
  lineorder l,
  date d
WHERE 
  l.lo_orderdate = d.d_datekey
  AND d.d_yearmonthnum = 199401
  AND l.lo_discount BETWEEN 4 AND 6
  AND l.lo_quantity BETWEEN 26 AND 35;
