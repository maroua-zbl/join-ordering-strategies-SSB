SELECT 
  d_year,
  s_city,
  p_brand1,
  SUM(lo_revenue - lo_supplycost) AS profit
FROM 
  date d,
  customer c,
  supplier s,
  part p,
  lineorder l
WHERE 
  l.lo_custkey = c.c_custkey
  AND l.lo_suppkey = s.s_suppkey
  AND l.lo_partkey = p.p_partkey
  AND l.lo_orderdate = d.d_datekey
  AND c.c_region = 'AMERICA'
  AND s.s_nation = 'UNITED STATES'
  AND (d.d_year = 1997
    OR d.d_year = 1998)
  AND p.p_category = 'MFGR#14'
GROUP BY 
  d_year,
  s_city,
  p_brand1
ORDER BY 
  d_year,
  s_city,
  p_brand1;
