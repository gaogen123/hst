-- 查看列的注释
SELECT
    a.attname AS 列名,
    d.description AS 列注释
FROM
    pg_class c
    JOIN pg_attribute a ON a.attrelid = c.oid
    LEFT JOIN pg_description d ON d.objoid = c.oid AND d.objsubid = a.attnum
WHERE
    c.relname = 'strategy_performance'
    AND a.attnum > 0
    AND NOT a.attisdropped;
