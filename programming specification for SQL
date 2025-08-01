-- 不推荐
    SELECT a.id, b.name FROM user a JOIN user_ext b ON a.id = b.id;

    -- 推荐
    SELECT usr.user_id, ext.user_name
    FROM dwd_user_info_df AS usr
    LEFT JOIN dwd_user_extra_info_df AS ext
      ON usr.user_id = ext.user_id;

-- ##################################################################
    -- @name: dws_user_daily_active_model_df.sql
    -- @description: 用户日活设备型号汇总天表。用于统计不同设备型号的DAU。
    -- @author: 张三 (zhangsan)
    -- @create_date: 2025-08-01
    -- @modify_records:
    --   2025-08-02, 李四 (lisi), 增加了 xx 字段，修复了 xx 问题。
    -- ##################################################################

SELECT
        user_id,
        -- GMV (Gross Merchandise Volume) = 支付金额 + 余额支付金额
        payment_amount + balance_amount AS gmv,
        -- 使用COALESCE处理支付时间为空的情况，默认当天最早时间
        COALESCE(payment_time, CONCAT(ds, ' 00:00:00')) AS final_payment_time
    FROM dwd_trade_order_detail_di
    WHERE ds = '${bizdate}';

select user_id,count(distinct order_id), sum(case when payment_type='alipay' then order_amount else 0 end) as alipay_amount from dwd_trade_order_detail_di where ds='20250801' and order_amount>10 group by user_id;

SELECT
        user_id
      , COUNT(DISTINCT order_id) AS order_count
      , SUM(
            CASE
                WHEN payment_type = 'alipay' THEN order_amount
                ELSE 0
            END
        ) AS alipay_amount
    FROM
        dwd_trade_order_detail_di
    WHERE
        ds = '20250801'
        AND order_amount > 10
    GROUP BY
        user_id;

-- 禁止
    INSERT OVERWRITE TABLE dws_user_order_summary
    SELECT * FROM dwd_trade_order_detail_di WHERE ds = '${bizdate}';

    -- 推荐
    INSERT OVERWRITE TABLE dws_user_order_summary
    SELECT
        user_id
      , order_id
      , order_amount
    FROM
        dwd_trade_order_detail_di
    WHERE
        ds = '${bizdate}';

-- 必须在WHERE中带上分区 ds
    SELECT
        user_id
      , COUNT(1)
    FROM
        dwd_user_login_log_di
    WHERE
        ds = '20250801' -- 关键的分区过滤条件
        AND os_type = 'iOS'
    GROUP BY
        user_id;

-- user_info 表较小, order 表较大
    SELECT
        usr.user_name
      , ord.order_amount
    FROM
        dim_user_info_mf AS usr -- 小表在左
    LEFT JOIN
        dwd_trade_order_detail_di AS ord -- 大表在右
      ON usr.user_id = ord.user_id AND ord.ds = '20250801' -- 错误：在ON中加入右表的过滤条件
    WHERE
        usr.ds = '20250731';


    -- 推荐的写法
    SELECT
        usr.user_name
      , ord.order_amount
    FROM
        dim_user_info_mf AS usr
    LEFT JOIN
        dwd_trade_order_detail_di AS ord
      ON usr.user_id = ord.user_id -- ON 中只写关联键
    WHERE
        usr.ds = '20250731'
        AND ord.ds = '20250801'; -- 在WHERE中写过滤条件

-- 不推荐: 单个Reducer处理所有去重，压力巨大
    SELECT
        province
      , COUNT(DISTINCT user_id) AS dau
    FROM
        dwd_user_login_log_di
    WHERE
        ds = '20250801'
    GROUP BY
        province;

    -- 推荐: 两阶段聚合，打散压力
    SELECT
        province
      , COUNT(user_id) AS dau
    FROM
        (
            SELECT
                province
              , user_id
            FROM
                dwd_user_login_log_di
            WHERE
                ds = '20250801'
            GROUP BY -- 第一阶段：先按所有维度和去重键GROUP BY，打散数据
                province, user_id
        ) AS t
    GROUP BY -- 第二阶段：简单COUNT
        province;

-- 使用WITH子句拆解复杂逻辑
    WITH paid_orders AS (
        -- 步骤1: 筛选出已支付订单
        SELECT
            user_id
          , order_id
          , order_amount
        FROM
            dwd_trade_order_detail_di
        WHERE
            ds = '20250801'
            AND is_paid = 1
    ),
    user_with_vip_info AS (
        -- 步骤2: 关联用户信息，并打上VIP标记
        SELECT
            a.user_id
          , a.order_id
          , a.order_amount
          , b.is_vip
        FROM
            paid_orders AS a
        LEFT JOIN
            dim_user_info_mf AS b
          ON a.user_id = b.user_id AND b.ds = '20250731'
    )
    -- 步骤3: 按VIP和非VIP用户进行最终聚合
    SELECT
        is_vip
      , COUNT(DISTINCT user_id) AS user_count
      , SUM(order_amount) AS total_amount
    FROM
        user_with_vip_info
    GROUP BY
        is_vip;

EXPLAIN SELECT ... ;
