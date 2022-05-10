SELECT 
  SUM(lo_extendedprice * lo_discount) AS revenue
FROM 
  lineorder l,
  date d
WHERE 
  l.lo_orderdate = d.d_datekey
  AND d.d_year = 1993
  AND l.lo_discount BETWEEN 1 AND 3
  AND l.lo_quantity < 25;
