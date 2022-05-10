SELECT 
  c_city,
  s_city,
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
  AND c.c_nation = 'UNITED STATES'
  AND s.s_nation = 'UNITED STATES'
  AND d.d_year >= 1992
  AND d.d_year <= 1997
GROUP BY 
  c_city,
  s_city,
  d_year
ORDER BY 
  d_year ASC, 
  revenue DESC;
