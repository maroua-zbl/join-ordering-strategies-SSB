SELECT 
  d_year,
  s_nation,
  p_category,
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
  AND s.s_region = 'AMERICA'
  AND (d.d_year = 1997
    OR d.d_year = 1998)
  AND (p.p_mfgr = 'MFGR#1'
    OR p.p_mfgr = 'MFGR#2')
GROUP BY 
  d_year,
  s_nation,
  p_category
ORDER BY 
  d_year,
  s_nation,
  p_category;
