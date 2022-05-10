SELECT 
  SUM(lo_revenue),
  d_year,
  p_brand1
FROM 
  lineorder l,
  date d,
  part p,
  supplier s
WHERE 
  l.lo_orderdate = d.d_datekey
  AND l.lo_partkey = p.p_partkey
  AND l.lo_suppkey = s.s_suppkey
  AND p.p_brand1 = 'MFGR#2221'
  AND s.s_region = 'EUROPE'
GROUP BY 
  d_year,
  p_brand1
ORDER BY 
  d_year,
  p_brand1;
