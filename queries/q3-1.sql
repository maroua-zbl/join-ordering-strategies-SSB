SELECT 
  c_nation,
  s_nation,
  d_year,
  SUM(lo_revenue) AS revenue
FROM 
  customer c,
  lineorder l,
  supplier s,
  date d
WHERE 
  l.lo_custkey = c.c_custkey
  AND l.lo_suppkey = s.s_suppkey
  AND l.lo_orderdate = d.d_datekey
  AND c.c_region = 'ASIA'
  AND s.s_region = 'ASIA'
  AND d.d_year >= 1992
  AND d.d_year <= 1997
GROUP BY 
  c_nation,
  s_nation,
  d_year
ORDER BY 
  d_year ASC, 
  revenue DESC;
