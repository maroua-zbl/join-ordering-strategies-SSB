SELECT 
  SUM(lo_extendedprice * lo_discount) AS revenue
FROM 
  lineorder l,
  date d
WHERE 
  l.lo_orderdate = d.d_datekey
  AND d.d_weeknuminyear = 6
  AND d.d_year = 1994
  AND l.lo_discount BETWEEN 5 AND 7
  AND l.lo_quantity BETWEEN 26 AND 35;
