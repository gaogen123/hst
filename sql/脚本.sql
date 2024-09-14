-- 查看交易情况
select *
from strategy_performance
where strategy_name='黄金坑策略'
order by backtest_time desc
;


-- 查看所有回测每个策略的表现
SELECT
       backtest_time as 回测时间,
       strategy_name as 策略,
       sum(累计正收益) AS 最终累计正收益,
       sum(累计负收益) AS 最终累计负收益,
       sum(总收益)     AS 最终总收益,
       COUNT(CASE WHEN 收益 > 0 THEN 1 END) AS                                     正收益次数,
       COUNT(CASE WHEN 收益 < 0 THEN 1 END) AS                                     负收益次数,
       count(收益)                          as                                     总次数,
       ROUND(COUNT(CASE WHEN 收益 > 0 THEN 1 END)::numeric / count(收益) * 100, 2) 胜率
FROM strategy_performance
GROUP BY  strategy_name,backtest_time
order by 回测时间,策略,胜率 desc
;

-- 最近一次回测所有策略的表现
WITH latest_backtest AS (
    SELECT
        MAX(backtest_time) AS max_backtest_time,
        strategy_name
    FROM strategy_performance
    group by strategy_name
)
SELECT
    a1.backtest_time as 回测时间,
    a1.strategy_name AS 策略,
    SUM(a1.累计正收益) AS 最终累计正收益,
    SUM(a1.累计负收益) AS 最终累计负收益,
    SUM(a1.总收益) AS 最终总收益,
    COUNT(CASE WHEN a1.收益 > 0 THEN 1 END) AS 正收益次数,
    COUNT(CASE WHEN a1.收益 < 0 THEN 1 END) AS 负收益次数,
    COUNT(a1.收益) AS 总次数,
    ROUND(COUNT(CASE WHEN a1.收益 > 0 THEN 1 END)::numeric / COUNT(a1.收益) * 100, 2) AS 胜率
FROM strategy_performance a1
join latest_backtest a2
on  a1.backtest_time = a2.max_backtest_time
and a1.strategy_name=a2.strategy_name
GROUP BY a1.backtest_time ,a1.strategy_name
order by 回测时间,策略,胜率 desc
;

-- 今日发出买入信号股票
WITH latest_backtest AS (
    SELECT
        MAX(backtest_time) AS max_backtest_time,
        strategy_name
    FROM strategy_performance
    group by strategy_name
)
SELECT
    *
FROM strategy_performance a1
join latest_backtest a2
on a1.backtest_time=a2.max_backtest_time
and a1.strategy_name=a2.strategy_name
WHERE
    type = '买入'
    AND DATE(a1.trigger_time) = CURRENT_DATE
ORDER BY
    a1.strategy_name,
    a1.trigger_time;


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
