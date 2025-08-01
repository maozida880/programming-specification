## **HIVE SQL 开发规范 (新人培训版)**

### **引言**

欢迎加入数据团队！在互联网行业，数据是驱动业务决策的核心。HIVE SQL 是我们与海量数据沟通的主要语言。一份高质量的SQL代码，不仅能保证计算结果的准确和高效，更能极大地提升团队协作效率和系统的可维护性。

本规范旨在帮助你建立起专业的SQL开发意识，养成良好的编程习惯。请在未来的每一次开发中，都严格遵守这些规范。**记住：代码首先是写给人看的，其次才是让机器执行的。**

---

### **一、命名规范 (Naming Conventions)**

清晰、统一的命名是代码可读性的基础。

#### **1.1 表命名**

表名应清晰地反映其在数据仓库中的分层、业务领域、数据内容和更新周期。

* **结构:** 层次\_业务域\_数据主题\_更新周期  
  * **层次:**  
    * ods: 操作数据层 (Operational Data Store)，原始数据，未经清洗转换。  
    * dwd: 明细数据层 (Data Warehouse Detail)，对ODS数据清洗、转换后的事实明细。  
    * dws: 汇总数据层 (Data Warehouse Summary)，按某个维度或主题轻度汇总。  
    * ads: 应用数据层 (Application Data Store)，面向具体业务应用或报表。  
    * dim: 维度层 (Dimension)，存储维度信息。  
    * tmp: 临时表，用于复杂计算的中间过程，通常以 tmp\_ 开头，并附带开发者标识和日期，如 tmp\_zhangsan\_20250801\_user\_active\_step1。  
  * **业务域:** 如 trade(交易), user(用户), log(日志), traffic(流量) 等。  
  * **数据主题:** 表的核心内容，如 order(订单), payment(支付), dau(日活)。  
  * **更新周期:**  
    * di: 日增量 (Daily Increment)。  
    * df: 日全量 (Daily Full)。  
    * wi/wf: 周增/全量。  
    * mi/mf: 月增/全量。  
    * hi/hf: 小时增/全量。  
* **示例:**  
  * dwd\_trade\_order\_detail\_di: 交易域的订单明细事实表，每日增量。  
  * dws\_user\_active\_device\_df: 用户域的日活设备汇总表，每日全量。  
  * dim\_user\_info\_mf: 用户维度信息表，每月全量快照。

#### **1.2 字段命名**

* **原则:** 使用小写字母和下划线 \_ (snake\_case)。  
* **规则:** 字段名应具备业务含义，做到见名知意。禁止使用 col1, a, b 等无意义的名称。  
* **布尔值:** 字段名建议使用 is\_ 或 has\_ 开头，如 is\_vip, has\_payment。  
* **统一性:** 同一含义的字段在不同表中应保持同名，如用户ID在所有表中都应命名为 user\_id。  
* **示例:**  
  * **推荐:** user\_id, order\_amount, payment\_time, is\_registered  
  * **禁止:** userId, orderamount, p\_time, reg\_flag

#### **1.3 别名命名**

* 表和子查询的别名应简洁并能体现其含义。  
* **示例:**  
  SQL  
  \-- 不推荐  
  SELECT a.id, b.name FROM user a JOIN user\_ext b ON a.id \= b.id;

  \-- 推荐  
  SELECT usr.user\_id, ext.user\_name  
  FROM dwd\_user\_info\_df AS usr  
  LEFT JOIN dwd\_user\_extra\_info\_df AS ext  
    ON usr.user\_id \= ext.user\_id;

---

### **二、注释规范 (Commenting Standards)**

注释的目的是解释代码的“为什么”，而不是“是什么”。

#### **2.1 脚本头注释**

每个独立的 .sql 脚本文件都必须包含头注释，说明脚本的用途、作者和修改历史。

* **格式:**  
  SQL  
  \-- \#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#  
  \-- @name: dws\_user\_daily\_active\_model\_df.sql  
  \-- @description: 用户日活设备型号汇总天表。用于统计不同设备型号的DAU。  
  \-- @author: 张三 (zhangsan)  
  \-- @create\_date: 2025-08-01  
  \-- @modify\_records:  
  \--   2025-08-02, 李四 (lisi), 增加了 xx 字段，修复了 xx 问题。  
  \-- \#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#

#### **2.2 行内注释**

对于复杂的业务逻辑、关键的计算步骤或容易引起误解的代码段，必须添加行内注释。

* **格式:** 使用 \-- 加一个空格。  
* **示例:**  
  SQL  
  SELECT  
      user\_id,  
      \-- GMV (Gross Merchandise Volume) \= 支付金额 \+ 余额支付金额  
      payment\_amount \+ balance\_amount AS gmv,  
      \-- 使用COALESCE处理支付时间为空的情况，默认当天最早时间  
      COALESCE(payment\_time, CONCAT(ds, ' 00:00:00')) AS final\_payment\_time  
  FROM dwd\_trade\_order\_detail\_di  
  WHERE ds \= '${bizdate}';

---

### **三、编码与格式规范 (Coding & Formatting Style)**

统一的格式是保证代码可读性的关键。

#### **3.1 关键字大小写**

* **规则:** HIVE SQL关键字、函数名、内置类型等全部使用 **大写**。  
* **示例:** SELECT, FROM, WHERE, GROUP BY, JOIN, ON, CASE WHEN, CAST, COUNT, SUM, STRING, BIGINT。

#### **3.2 缩进与换行**

* **缩进:** 使用 **2个或4个空格** 进行缩进（团队内统一）。  
* **换行:**  
  * SELECT 后的每个字段单独占一行，逗号放在字段前面。  
  * FROM, WHERE, GROUP BY, ORDER BY 等子句必须另起一行。  
  * 复杂的逻辑单元（如 CASE WHEN）应合理换行保持结构清晰。  
* **示例:**  
  **不规范的写法：**  
  SQL  
  select user\_id,count(distinct order\_id), sum(case when payment\_type\='alipay' then order\_amount else 0 end) as alipay\_amount from dwd\_trade\_order\_detail\_di where ds\='20250801' and order\_amount\>10 group by user\_id;

  **规范的写法：**  
  SQL  
  SELECT  
      user\_id  
    , COUNT(DISTINCT order\_id) AS order\_count  
    , SUM(  
          CASE  
              WHEN payment\_type \= 'alipay' THEN order\_amount  
              ELSE 0  
          END  
      ) AS alipay\_amount  
  FROM  
      dwd\_trade\_order\_detail\_di  
  WHERE  
      ds \= '20250801'  
      AND order\_amount \> 10  
  GROUP BY  
      user\_id;

---

### **四、核心SQL编写最佳实践 (Core SQL Best Practices)**

这是保证代码质量和性能的核心。

#### **4.1 SELECT 语句**

* **禁止使用 SELECT \*:** 必须明确写出所有需要的字段。  
  * **原因1 (性能):** SELECT \* 会读取所有列，即使你只需要其中几列，会造成不必要的I/O开销，尤其是在列式存储（如ORC, Parquet）中优势尽失。  
  * **原因2 (可维护性):** 当上游表结构发生变化（增减字段）时，SELECT \* 会导致下游代码报错或产生非预期的结果。  
* **示例:**  
  SQL  
  \-- 禁止  
  INSERT OVERWRITE TABLE dws\_user\_order\_summary  
  SELECT \* FROM dwd\_trade\_order\_detail\_di WHERE ds \= '${bizdate}';

  \-- 推荐  
  INSERT OVERWRITE TABLE dws\_user\_order\_summary  
  SELECT  
      user\_id  
    , order\_id  
    , order\_amount  
  FROM  
      dwd\_trade\_order\_detail\_di  
  WHERE  
      ds \= '${bizdate}';

#### **4.2 WHERE 语句**

* **分区过滤前置:** 如果表是分区表，必须在 WHERE 子句中 **第一时间** 加上分区过滤条件。  
  * **原因:** 这是HIVE性能优化的第一生命线。分区裁剪能让HIVE只扫描必要的分区目录，避免全表扫描，将计算量降低几个数量级。  
* **过滤条件前置:** 尽量将能过滤掉大量数据的条件写在 WHERE 子句中，而不是 JOIN 的 ON 之后或 HAVING 中。  
* **示例:**  
  SQL  
  \-- 必须在WHERE中带上分区 ds  
  SELECT  
      user\_id  
    , COUNT(1)  
  FROM  
      dwd\_user\_login\_log\_di  
  WHERE  
      ds \= '20250801' \-- 关键的分区过滤条件  
      AND os\_type \= 'iOS'  
  GROUP BY  
      user\_id;

#### **4.3 JOIN 语句**

* **明确JOIN类型:** 显式写出 INNER JOIN, LEFT JOIN, RIGHT JOIN。禁止只写 JOIN。  
* **JOIN顺序:** 在 LEFT JOIN 中，遵循“大表在右，小表在左”的原则。HIVE会将右表加载到内存中，流式读取左表进行匹配。  
* **JOIN条件:**  
  * JOIN的 ON 子句中只写关联条件。  
  * 过滤条件（非关联条件）写在后续的 WHERE 子句中。  
  * 确保关联键的数据类型完全一致，避免隐式类型转换带来的性能损耗。  
  * 注意处理关联键中的 NULL 值。ON a.key \= b.key 时，NULL 与任何值（包括 NULL）都不相等。如果需要关联 NULL，可以使用 ON a.key \<=\> b.key。  
* **示例:**  
  SQL  
  \-- user\_info 表较小, order 表较大  
  SELECT  
      usr.user\_name  
    , ord.order\_amount  
  FROM  
      dim\_user\_info\_mf AS usr \-- 小表在左  
  LEFT JOIN  
      dwd\_trade\_order\_detail\_di AS ord \-- 大表在右  
    ON usr.user\_id \= ord.user\_id AND ord.ds \= '20250801' \-- 错误：在ON中加入右表的过滤条件  
  WHERE  
      usr.ds \= '20250731';

  \-- 推荐的写法  
  SELECT  
      usr.user\_name  
    , ord.order\_amount  
  FROM  
      dim\_user\_info\_mf AS usr  
  LEFT JOIN  
      dwd\_trade\_order\_detail\_di AS ord  
    ON usr.user\_id \= ord.user\_id \-- ON 中只写关联键  
  WHERE  
      usr.ds \= '20250731'  
      AND ord.ds \= '20250801'; \-- 在WHERE中写过滤条件

#### **4.4 GROUP BY 语句**

* **COUNT(DISTINCT) 优化:** COUNT(DISTINCT col) 容易在数据量大、倾斜时产生单点瓶颈。可优化为两阶段聚合。  
* **示例:**  
  SQL  
  \-- 不推荐: 单个Reducer处理所有去重，压力巨大  
  SELECT  
      province  
    , COUNT(DISTINCT user\_id) AS dau  
  FROM  
      dwd\_user\_login\_log\_di  
  WHERE  
      ds \= '20250801'  
  GROUP BY  
      province;

  \-- 推荐: 两阶段聚合，打散压力  
  SELECT  
      province  
    , COUNT(user\_id) AS dau  
  FROM  
      (  
          SELECT  
              province  
            , user\_id  
          FROM  
              dwd\_user\_login\_log\_di  
          WHERE  
              ds \= '20250801'  
          GROUP BY \-- 第一阶段：先按所有维度和去重键GROUP BY，打散数据  
              province, user\_id  
      ) AS t  
  GROUP BY \-- 第二阶段：简单COUNT  
      province;

#### **4.5 UNION vs UNION ALL**

* **优先使用 UNION ALL:** UNION 会对结果集进行去重，带来一个额外的、耗费资源的 Sort 和 Distinct 操作。如果确认合并的两个结果集没有交集，或业务上允许重复，务必使用 UNION ALL。

#### **4.6 复杂逻辑拆解**

* 对于超过100行或者逻辑嵌套很深的SQL，强烈建议使用 WITH 子句 (CTE, Common Table Expressions) 或临时表来拆解。  
* **好处:**  
  * **可读性:** 逻辑层次清晰，易于理解和维护。  
  * **复用性:** 同一个中间结果可以被多次引用。  
  * **调试:** 可以单独执行某个CTE来验证中间结果。  
* **示例:**  
  SQL  
  \-- 使用WITH子句拆解复杂逻辑  
  WITH paid\_orders AS (  
      \-- 步骤1: 筛选出已支付订单  
      SELECT  
          user\_id  
        , order\_id  
        , order\_amount  
      FROM  
          dwd\_trade\_order\_detail\_di  
      WHERE  
          ds \= '20250801'  
          AND is\_paid \= 1  
  ),  
  user\_with\_vip\_info AS (  
      \-- 步骤2: 关联用户信息，并打上VIP标记  
      SELECT  
          a.user\_id  
        , a.order\_id  
        , a.order\_amount  
        , b.is\_vip  
      FROM  
          paid\_orders AS a  
      LEFT JOIN  
          dim\_user\_info\_mf AS b  
        ON a.user\_id \= b.user\_id AND b.ds \= '20250731'  
  )  
  \-- 步骤3: 按VIP和非VIP用户进行最终聚合  
  SELECT  
      is\_vip  
    , COUNT(DISTINCT user\_id) AS user\_count  
    , SUM(order\_amount) AS total\_amount  
  FROM  
      user\_with\_vip\_info  
  GROUP BY  
      is\_vip;

---

### **五、性能调优核心 (Performance Tuning)**

除了遵循上述最佳实践，还需具备主动性能调优的意识。

#### **5.1 数据倾斜 (Data Skew)**

数据倾斜是HIVE任务最常见的性能杀手。表现为一个或少数几个Reducer任务迟迟无法完成。

* **识别:** 观察任务日志，发现大部分Reducer已完成，少数几个进度条卡在99%。  
* **常见原因:** JOIN 或 GROUP BY 的 key 中存在大量相同的“热点值”，如 NULL、-1 或某个爆款商品的ID。  
* **解决方案:**  
  1. **GROUP BY 倾斜:**  
     * 开启 hive.groupby.skewindata=true，HIVE会自动拆分任务。  
     * 手动处理：将热点 key 和非热点 key 分开处理，最后 UNION ALL。或给热点 key 拼接一个随机数打散，再二次聚合。  
  2. **JOIN 倾斜:**  
     * 过滤掉异常的“热点值”。  
     * 将倾斜的 key 单独拿出来处理，主流数据正常 JOIN，结果 UNION ALL。  
     * 使用 HIVE 的 MAPJOIN (适用于小表JOIN大表)。set hive.auto.convert.join=true;

#### **5.2 合理使用数据存储格式和压缩**

* **存储格式:** 新建的数仓表，推荐使用 **ORC** 或 **Parquet** 格式。它们是列式存储，支持高效压缩，并且在查询时只读取所需列，极大提升性能。禁止使用 TEXTFILE。  
* **压缩:** ORC默认使用 ZLIB，Parquet 默认使用 SNAPPY。通常无需手动更改。

#### **5.3 使用 EXPLAIN 分析执行计划**

在提交一个复杂任务前，使用 EXPLAIN 命令查看其执行计划。可以帮助你预判：

* 是否走了分区。  
* JOIN的类型和顺序是否合理。  
* 有几个MapReduce阶段。

SQL

EXPLAIN SELECT ... ;

---

### **六、开发流程与意识 (Development Process & Mindset)**

1. **需求理解:** 在动手写代码前，务必完全理解业务需求。不明确的地方，多问、多确认。  
2. **数据探查:** 了解源表的数据质量、数据量、分区情况、是否有异常值等。  
3. **开发与自测:**  
   * 先抽样少量数据进行逻辑开发和验证。  
   * 开发完成后，找几个边界case（如 NULL 值、0值、最大/最小值）进行自测。  
   * **核心指标核对:** 计算结果总和、总行数、关联率等，与已有数据或预期进行比对，确保逻辑正确。  
4. **代码评审 (Code Review):** 将你的代码提交给同事或导师进行评审。这是一个非常好的学习和发现问题的机会。  
5. **版本控制:** 所有SQL脚本必须纳入 **Git** 进行版本管理。

---

### **结语**

良好的规范和习惯是卓越工程师的基石。希望这份文档能成为你数据开发生涯的一个良好开端。在实践中不断学习、总结，你将成长为一名优秀的数据工程师。祝你工作顺利！
