# -*- coding: utf-8 -*-
"""Generate web/assets/course-catalog.js from structured course rows."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "web" / "assets" / "course-catalog.js"

# Each row: code, English name, intro (no 简介 prefix), outline (syllabus content)
ROWS = [
    # 一、金融学
    ("FIN2010", "Financial Management", "财务管理基础，投融资、资本成本、现金流估值", "财务决策；货币时间价值；资本预算；资本结构；营运资金管理"),
    ("FIN2210", "Probability for Finance", "金融概率论，分布、期望、收敛、中心极限定理", "概率基础；随机变量；多元分布；条件期望；大数定律与中心极限定理"),
    ("FIN3030", "Financial Institutions and Markets", "金融机构与市场，银行、监管、金融市场运行", "金融体系；商业银行；金融市场；央行政策；影子银行；中国金融市场"),
    ("FIN3080", "Investment Analysis and Portfolio Management", "投资组合、股票估值、量化策略", "现金流估值；相对估值；组合理论；CAPM；因子模型；行为金融"),
    ("FIN3210", "Fintech Theory and Practice", "金融科技，大数据、区块链、AI在金融中应用", "数字信贷；另类数据；文本挖掘；支付；智能投顾；监管科技"),
    ("FIN3340", "Financial Innovations and Alternative Investment", "风投/私募股权，初创估值、退出机制", "VC/PE全流程；初创估值；投资条款；LBO；退出策略（IPO/并购）"),
    ("FIN4080", "Behavioral Finance", "行为金融，认知偏差、市场异象、投资者行为", "前景理论；过度自信；羊群效应；有限套利；行为资产定价"),
    ("FIN4110", "Options and Futures", "期权期货，衍生品定价、套利、对冲策略", "衍生品基础；远期期货；期权平价；二叉树；BS模型；对冲"),
    ("FIN4120", "Fixed Income Securities Analysis", "固定收益，债券定价、久期、利率风险", "债券定价；收益率；期限结构；久期与凸性；利率风险"),
    ("FIN4210", "Corporate Finance", "公司金融，资本结构、股利政策、资本预算", "投资决策；融资决策；MM定理；股利政策；并购基础"),
    ("FIN4220", "Advanced Corporate Finance", "高级公司金融，企业估值、并购、重组", "公司估值；相对估值；并购；资本结构优化；价值创造"),
    ("FIN4230", "Value Investing", "价值投资，安全边际、自由现金流、护城河", "价值投资原理；安全边际；自由现金流；财务健康；经济护城河"),
    ("FIN4231", "Asset Pricing", "资产定价，因子模型、消费定价、市场效率", "消费定价；因子模型；市场效率；行为定价；技术分析"),
    ("FMA4200", "Financial Data Analysis", "金融数据分析，回归、时间序列、风险管理", "统计方法；风险管理；波动率建模；投资组合分析"),
    ("FMA4800", "Financial Computation", "金融计算，蒙特卡洛、二叉树、数值定价", "随机模型；蒙特卡洛模拟；二叉树；数值偏微分方程"),
    ("RMS4060", "Risk Management with Derivatives", "衍生品风险管理，利率/信用/市场风险", "风险类型；衍生品对冲；利率风险；信用风险；市场风险"),
    # 二、经济学
    ("ECO2011", "Basic Microeconomics", "微观基础，供需、消费者、厂商、市场均衡", "供需；消费者理论；生产与成本；市场结构；均衡"),
    ("ECO2021", "Basic Macroeconomics", "宏观基础，GDP、通胀、失业、货币财政政策", "GDP；通胀失业；增长；金融市场；财政货币政策"),
    ("ECO3011", "Intermediate Microeconomic Theory", "中级微观，效用、生产、垄断、寡头", "偏好效用；生产与成本；完全竞争；垄断；寡头；一般均衡"),
    ("ECO3021", "Intermediate Macroeconomic Theory", "中级宏观，增长模型、经济周期、IS-LM", "索洛模型；内生增长；失业；货币；IS-LM；开放经济"),
    ("ECO3080", "Machine Learning for Business", "商业机器学习，监督/无监督学习、模型评估", "线性回归；分类；重抽样；正则化；树模型；神经网络；聚类"),
    ("ECO3090", "Machine Learning for Financial Economics", "金融机器学习，时序、信用风险、交易策略", "信用建模；时序预测；组合优化；文本数据；强化学习交易"),
    ("ECO3110", "Behavioral Economics", "行为经济学，前景理论、时间偏好、社会偏好", "时间偏好；风险偏好；前景理论；社会偏好；注意力与框架"),
    ("ECO3121", "Introductory Econometrics", "计量经济学，回归、假设检验、Stata实操", "回归模型；估计与推断；异方差；虚拟变量；时间序列"),
    ("ECO3160", "Game Theory and Business Strategy", "博弈论，纳什均衡、序贯博弈、议价", "占优策略；纳什均衡；序贯博弈；重复博弈；不完全信息；拍卖"),
    ("ECO3211", "Quantitative Methods for Policy Evaluation", "政策评估，DID、IV、RDD因果推断", "潜在结果；随机实验；双重差分；工具变量；断点回归"),
    ("ECO3410", "Economics of Money and Financial Institutions", "货币银行，央行、货币政策、金融体系", "货币与央行；货币供需；利率；货币政策；银行管理"),
    ("ECO3230", "Economic Analysis of Law and Human Behavior", "法与行为经济学（兼容占位）", "法律经济分析；行为视角；案例讨论"),
    ("ECO3430", "Public Finance", "公共财政，外部性、税收、社保、收入分配", "公共品；外部性；税收理论；社保；收入再分配"),
    ("ECO3480", "Industrial Organization and Public Policy", "产业组织，市场势力、反垄断、竞争政策", "市场势力；定价；广告；研发；网络经济；反垄断政策"),
    ("ECO3610", "International Trade", "国际贸易，比较优势、要素禀赋、贸易政策", "李嘉图模型；H-O模型；关税；贸易协定；离岸外包"),
    ("ECO3620", "Data Analysis and Macroeconomic Policies", "宏观政策数据分析，Excel/Python可视化", "宏观指标；人口与增长；经济周期；货币财政；全球化；AI与政策"),
    ("ECO3630", "International Finance", "国际金融，汇率、国际收支、资本流动", "国际收支；汇率决定；利率平价；宏观政策；固定/浮动汇率"),
    ("ECO3710", "China Economy", "中国经济，制度、增长、金融、创新、反腐", "改革制度；官僚治理；分权；市场化；国企；金融；创新；环境"),
    ("ECO4121", "Intermediate Econometrics", "高级计量，时间序列、ARMA、GARCH、VAR", "平稳序列；ARMA；预测；单位根；GARCH；VAR"),
    # 经济学（续）
    ("ECO3010", "Law, Economics and Society", "法与经济学，用经济学分析法律、犯罪、垄断、环境治理", "市场与社会治理；司法系统；犯罪与惩罚；管制经济学"),
    ("ECO3420", "Financial Economics", "金融经济学，投资、资产定价、无套利、衍生品基础", "现值与债券；衍生品定价；投资组合；CAPM；套利定价理论"),
    ("ECO3460", "ESG Fundamentals", "ESG基础，环境、社会、治理投资框架", "ESG定义与指标；可持续投资；风险管理；披露与合规"),
    ("ECO3470", "Labor Economics", "劳动经济学，劳动供给/需求、人力资本、歧视、移民", "劳动供需；人力资本；歧视；移民；委托代理问题"),
    ("ECO3650", "Development Economics", "发展经济学，增长理论、农业、城乡迁移、教育医疗", "发展理论；农业；城乡迁移；土地与劳动力；教育与基建"),
    ("ECO4001", "Environmental Economics and Policy", "环境经济学，污染、外部性、碳定价、可持续政策", "市场失灵；环境政策；成本收益分析；污染治理"),
    ("ECO4002", "Health Economics", "卫生经济学，医疗需求、保险、创新、医疗政策", "医疗需求；健康保险；医疗供给；创新与政策"),
    ("ECO4270/4280", "Thesis in Economics I/II", "经济学论文，独立研究、实证分析、写作答辩", "选题；文献；数据；实证；写作；答辩"),
    ("ECO4312/4313", "Directed Research in Economics", "经济学定向研究，导师指导下专题研究", "开题；文献；数据；实证；论文写作与展示"),
    # 三、会计学
    ("ACT2111", "Introductory Financial Accounting", "财务会计入门，报表、借贷、会计循环", "会计恒等式；报表编制；收入；资产；负债；所有者权益"),
    ("ACT2121", "Introductory Management Accounting", "管理会计，成本核算、本量利、预算、决策", "成本概念；分批/分步成本；本量利；作业成本法；预算；差异分析"),
    ("ACT3011", "Intermediate Financial Accounting", "中级财务会计，收入、租赁、所得税、养老金、每股收益", "概念框架；资产；租赁；收入；养老金；权益；所得税；EPS"),
    ("ACT3131", "Accounting Theory", "会计理论，信息不对称、有效市场、估值、契约理论", "信息不对称；披露；市场效率；估值；契约理论；会计新发展"),
    ("ACT3141", "Accounting Information Systems", "会计信息系统，业务流程、内控、金蝶系统、大数据", "AIS与ERP；收入/支出循环；金蝶系统；供应链云；区块链"),
    ("ACT3153", "Business and Company Law", "商法，合同、企业法、证券法、中国法", "私法；财产；合同；商业组织；并购；证券法"),
    ("ACT3154", "Business and Company Law II", "公司法与商法进阶，香港法、反贪、雇佣、公司治理", "香港法律制度；反贪；合同；侵权；雇佣；公司设立与治理"),
    ("ACT3181", "Credit Rating and Risk Management", "信用评级与风险管理，信用风险度量、案例", "信用风险；评级方法；会计信息与信贷决策；案例"),
    ("ACT3311", "Accounting Forecasting and Analysis", "会计预测与分析，盈余质量、破产预测、舞弊分析", "会计分析；Stata基础；盈余质量；破产预测；舞弊法务"),
    ("ACT3321", "Textual Analysis for Accounting and Finance", "文本分析，NLP、爬虫、情感分析、主题模型", "文本挖掘；数据处理；情感分析；爬虫；主题建模；生成式AI"),
    ("ACT4121", "Strategic Management Accounting", "战略管理会计，管理控制、转移定价、绩效", "管理控制系统；转移定价；绩效衡量；激励；公司治理"),
    ("ACT4131", "Auditing", "审计学，审计流程、内控、循环审计、审计报告", "审计基础；内控；风险评估；销售/采购/存货/薪酬循环；审计报告；道德"),
    ("ACT4213", "Financial Statement Analysis", "财务报表分析，估值、盈利、增长、现金流、AI基本面", "投资与估值；应计与现金流；风险；盈利与增长；预测估值；案例"),
    ("ACT4231", "Internal Auditing and Risk Management", "内部审计与风险管理，公司治理、风险识别、合规", "公司治理；风险识别评估；合规；反舞弊；反洗钱"),
    ("ACT4252", "Corporate Restructuring and Insolvency", "企业重组与破产，并购、估值、LBO、SPAC", "并购类型与动因；估值；融资；LBO；重组；破产；SPAC"),
    ("ACT4262", "China Taxation", "中国税制，个税、企业所得税、增值税、消费税、转让定价", "个税；企业所得税；增值税；消费税；财产行为税；转让定价"),
    ("ACT4263", "International Taxation", "国际税收，税收协定、转让定价、跨境筹划、反避税", "税收居民；税收协定；转让定价；并购税收；国际筹划；反避税"),
    ("ACT4311", "Data Mining for Accounting Analytics", "会计数据挖掘，Python、预测模型、文本分析、聚类", "R/Python；数据处理；预测模型；聚类；关联规则；文本分析"),
    ("ACT4321", "Accounting Database and Data Visualization", "会计数据库与可视化，SQL、Stata、Tableau", "数据清洗；SQL；Stata；Tableau可视化；描述/预测分析；AI可视化"),
    # 会计学（续）
    ("ACT4141", "Intro to Accounting Research", "会计研究导论，实证会计理论、研究方法", "会计实证文献；研究设计；理论与方法"),
    ("ACT4211", "Accounting for Financial Institutions", "金融机构会计，银行、券商、保险会计处理", "金融机构报表；金融工具；风险计量；监管资本"),
    ("ACT4212", "Accounting for Government & Non-Profit", "政府与非营利组织会计，预算、基金、收支核算", "政府会计；基金会计；非营利组织报表"),
    ("ACT4271", "Corporate Governance", "公司治理，代理问题、董事会、股权激励、ESG", "公司理论；代理问题；董事会；治理机制"),
    ("ACT4312/4313", "Directed Research in Accounting", "会计定向研究，学术专题、实证分析", "研究设计；数据与实证；论文写作"),
    # 四、金融工程/量化
    ("MAT1001", "Calculus I", "一元微积分，极限、导数、积分、微分方程", "极限连续；导数与微分；积分；微分方程基础"),
    ("MAT2040", "Linear Algebra", "线性代数，矩阵、向量空间、特征值、正交、SVD", "线性方程组；矩阵运算；向量空间；行列式；特征值；正交；SVD"),
    ("MAT3280", "Probability Theory", "概率论，测度、期望、大数定律、中心极限定理", "概率空间；随机变量；期望；独立性；大数定律；中心极限定理"),
    ("STA2001", "Probability and Statistics I", "概率统计I，分布、参数估计", "概率基础；分布；抽样；点估计；区间估计"),
    ("STA2002", "Probability and Statistics II", "概率统计II，假设检验、方差分析、回归", "假设检验；非参数检验；方差分析；线性回归"),
    ("STA3020", "Statistical Inference", "统计推断，充分统计量、似然、贝叶斯、假设检验", "数据压缩；点估计；假设检验；区间估计；贝叶斯推断"),
    ("STA4001", "Stochastic Process", "随机过程，马尔可夫链、泊松过程、布朗运动、排队论", "条件期望；离散/连续时间马尔可夫链；泊松过程；布朗运动；排队论"),
    ("STA4003", "Time Series", "时间序列，ARIMA、GARCH、预测、季节性", "平稳性；ARMA；ARIMA；预测；GARCH；季节性"),
    ("DDA3020", "Machine Learning", "机器学习，监督/无监督、神经网络、决策树", "线性回归；分类；树模型；神经网络；过拟合；聚类；PCA"),
    ("MAT4500", "Stochastics Differential Equations", "随机微分方程，伊藤公式、鞅、衍生品定价", "鞅；布朗运动；伊藤积分；伊藤公式；SDE；衍生品定价"),
    # 金融工程/量化（续）
    ("MAT1005", "Mathematics for Business & Economics", "商学数学，方程、线性规划、微积分、金融数学", "非线性方程；矩阵；线性规划；微分；积分；货币时间价值"),
    ("MAT2002", "Ordinary Differential Equation", "常微分方程，一阶/二阶方程、线性系统、定性分析", "一阶方程；线性系统；稳定性；相平面；应用"),
    ("MAT2050", "Mathematical Analysis", "数学分析，极限、连续、微分、积分、级数（严谨证明）", "序列极限；连续；微分；积分；级数；多元微积分"),
    ("MAT3004", "Abstract Algebra I", "抽象代数，群、环、域、同态、理想", "群论；子群；正规子群；环与域；多项式环"),
    ("MAT3006", "Real Analysis", "实分析，测度、勒贝格积分、可测函数、收敛", "勒贝格测度；可测函数；积分；收敛定理；有界变差"),
    ("MAT3007", "Optimization", "最优化，线性规划、单纯形法、对偶、非线性优化", "线性规划；对偶；单纯形法；整数规划；非线性优化"),
    ("MAT3010", "Calculus for Economic Analysis II", "经济分析微积分，多元、最优化、比较静态", "线性代数；拓扑与连续；多元函数；静态最优化；微分方程"),
    ("MAT3300", "Mathematical Modeling", "数学建模，优化、仿真、微分方程、图模型", "建模基础；数据拟合；仿真；优化；微分方程模型"),
    # 五、大数据/商业分析/MIS
    ("DMS2030", "Operations Management", "运营管理，流程、库存、供应链、质量管理", "运营战略；流程分析；库存管理；质量管理；供应链"),
    ("DMS3003", "Data Analytics and Decision Making", "数据分析与决策，回归、优化、模拟", "概率统计；线性回归；模型检验；仿真；线性/非线性优化"),
    ("MIS2051", "IT in Business Applications", "商业信息系统，数据库、SQL、数据挖掘、网络分析", "数据库；关系模型；SQL；数据挖掘；聚类；关联；文本挖掘"),
    ("MIS3011", "Advanced AI for Business", "高级商业AI，大模型、提示工程、AI项目全流程", "AI解决方案；生成式AI；LLM；线性/逻辑回归；深度学习；项目"),
    ("MKT3310", "Marketing Analytics", "营销分析，聚类、回归、分类、客户价值", "数据可视化；聚类；回归；分类；实验；定价优化"),
    ("MKT3320", "Digital Consumer Analytics", "数字消费者分析，RFM、逻辑回归、推荐系统、文本挖掘", "数据预处理；探索性分析；RFM；CLV；推荐系统；文本分析"),
    ("MKT3060", "Quantitative Marketing Methods", "量化营销，A/B测试、回归、DID、因果推断", "数据可视化；概率；A/B测试；回归；DID；RDD；工具变量"),
    # 五（续）
    ("CSC1001", "Introduction to Computer Science", "计算机科学导论，Python基础、编程、数据结构", "Python语法；函数；条件循环；列表；面向对象；基础算法"),
    ("CSC1002", "Computational Laboratory", "计算实验，Python实战、项目、AI辅助编程、GUI", "编程实战；AI辅助开发；小游戏项目；GUI；机器学习基础"),
    ("DMS3002", "Applied Probability & Stochastic Process", "应用概率与随机过程，马尔可夫链、泊松过程、排队论", "概率复习；条件期望；马尔可夫链；指数与泊松；连续时间马氏链；布朗运动"),
    ("DMS4312/4313", "Directed Research in Decision Science", "决策科学定向研究，优化、统计、运营模型研究", "模型构建；数据；实证；论文写作"),
    ("MIS2011", "AI for Business", "商业AI入门，机器学习、NLP、大模型、商业应用", "AI基础；数据处理；机器学习；深度学习；NLP；AI商业落地"),
    ("MIS3012", "LLMs in Business", "大模型商业应用，提示工程、AI Agent、生成式AI项目", "大模型原理；提示工程；微调；AI应用开发；安全与伦理"),
    # 六、国际商务/管理/营销
    ("MGT2020", "Principles of Management", "管理学原理，计划、组织、领导、控制", "管理职能；决策；战略；组织设计；领导；控制"),
    ("MGT3250", "International Business", "国际商务，全球化、进入模式、跨国公司、全球–本地平衡", "全球化；FDI；跨国企业；国际化战略；进入模式；全球vs本地"),
    ("MGT4250", "Cross-Cultural Communication and Negotiation", "跨文化沟通与谈判，文化差异、国际谈判、礼仪", "文化维度；跨文化谈判；国际商务礼仪；原则式谈判"),
    ("MKT2010", "Marketing Management", "营销管理，STP、4P、品牌、渠道、推广", "营销导论；市场调研；消费者行为；STP；4P策略"),
    ("MKT3020", "Consumer Behavior", "消费者行为，感知、学习、态度、群体、文化", "感知学习；动机；态度；决策；群体；社会阶层；文化"),
    ("MKT3030", "Integrated Marketing Communication", "整合营销传播，公关、数字媒体、内容策略", "IMC基础；公关；促销；媒体计划；数字媒体；内容策略"),
    ("MKT4110", "Strategic Brand Management", "战略品牌管理，品牌资产、定位、延伸", "品牌资产；品牌战略；定位；品牌个性；品牌延伸"),
    ("MKT4120", "Marketing Research", "营销调研，问卷、抽样、数据分析、报告", "研究设计；数据收集；问卷与抽样；描述与推断分析；回归"),
    # 六（续）管理
    ("MGT3010", "Organizational Behavior", "组织行为学，人格、动机、团队、权力、谈判、文化", "人格与动机；决策；团队；权力；冲突；结构与文化"),
    ("MGT3080", "Managing Social Ventures", "社会企业管理，社会创新、商业模式、社会影响力评估", "社会创业；机会识别；精益创业；融资；影响力衡量"),
    ("MGT3210", "Strategic Management", "战略管理，五力、资源观、竞争战略、公司战略", "内外部分析；竞争优势；多元化；并购；国际化；治理"),
    ("MGT3260", "Human Resource Management", "人力资源管理，招聘、培训、绩效、薪酬、员工关系", "工作分析；招聘甄选；培训；绩效管理；薪酬；离职与留存"),
    ("MGT3650", "AI in Strategic Management", "AI与战略管理，AI驱动决策、商业模式、组织转型", "AI战略；数据驱动决策；AI组织；提示工程；商业AI应用"),
    ("MGT3680", "New Venture Management", "创业与新企业管理，机会识别、市场调研、路演、财务预测", "创业思维；机会识别；市场调研；财务预测；路演"),
    ("MGT3780", "Quantitative Strategic Analysis", "定量战略分析，STATA、实证、企业战略量化", "战略量化；公司治理；多元化；并购；ESG；国际化"),
    ("MGT4020", "Case Study", "商业案例分析，战略、数字化转型、商业模式诊断", "分析框架；商业模式；蓝海战略；数字化转型；案例答辩"),
    ("MGT4030", "Business Presentation & Communication", "商务演讲与高效沟通，职场表达、面试、路演、汇报", "结构表达；非语言沟通；故事化；电梯演讲；路演；虚拟会议"),
    ("MGT4060", "Corporate Strategy", "公司战略，集团战略、并购、联盟、国际化", "公司战略框架；治理；多元化；并购；联盟；国际化战略"),
    ("MGT4080", "People Analytics", "人力分析，数据驱动HR、招聘算法、员工监控、绩效", "数据化HR；自动化招聘；数字监控；统计建模；数据挖掘"),
    ("MGT4130", "Organization Theory & Design", "组织理论与设计，结构、环境、网络、数字化组织", "组织理论；环境；间组织关系；国际化；数字化组织设计"),
    ("MGT4187", "Managerial Analytics", "管理分析，预测、聚类、资源配置、社交聆听、推荐系统", "商业预测；聚类分析；数据可视化；资源分配；推荐系统"),
    ("MGT4188", "Internship", "实习课程，企业实习、周报、导师评价、结项报告", "实习执行；周报；企业评价；最终报告"),
    ("MGT4210", "Decision Making & Negotiation", "决策与谈判，分配式/整合式谈判、权力、跨文化谈判", "决策偏差；谈判策略；分配谈判；整合谈判；跨文化谈判"),
    ("MGT4230", "Innovation & Entrepreneurship", "创新与创业，技术周期、创业流程、商业计划、融资", "创新理论；创业机会；商业模式；商业计划；融资"),
    ("MGT4310", "Advanced Strategic Management", "高级战略管理，学术前沿、IO、资源观、动态能力", "战略理论；产业组织；资源基础观；动态能力；公司治理"),
    ("MGT4320", "Advanced Global Business", "高级国际商务，跨国企业、全球价值链、创新、跨境并购", "IB研究前沿；跨境并购；全球战略；创新；数字经济"),
    ("MGT4321", "Social Problems & Sustainability Strategy", "社会问题与可持续战略，ESG、社会责任、可持续创新", "可持续框架；ESG；社会责任；战略创新；辩论与仿真"),
    ("MGT4560", "Business Sustainability & ESG", "商业可持续与利益相关者管理，ESG披露、责任投资", "利益相关者；CSR；ESG；可持续报告；合规与投资"),
    # 兼容旧推荐中出现的课程（简要）
    ("FIN3060", "Banking", "商业银行课程（兼容占位）", "商业银行运营；信贷；监管；风险管理"),
    ("FIN3330", "Alternative Investments", "另类投资（兼容占位）", "对冲基金；私募股权；大宗商品；不动产"),
    ("FIN4050", "Mergers and Acquisitions", "并购（兼容占位）", "并购估值；交易结构；尽职调查；整合"),
    ("MKT3050", "Global Marketing", "全球营销（兼容占位）", "全球市场进入；标准化与本地化；全球品牌"),
    ("MKT3080", "Strategic Media Planning", "战略媒体策划（兼容占位）", "媒体策略；投放；效果衡量"),
    ("STA3010", "Regression Analysis", "回归分析（兼容占位）", "线性回归；诊断；扩展模型"),
    ("SCM3010", "Supply Chain Management", "供应链管理（兼容占位）", "供应链战略；网络设计；协调"),
    ("SCM3020", "Demand and Inventory Planning", "需求与库存计划（兼容占位）", "需求预测；库存模型；补货策略"),
    ("SCM3030", "Strategic Procurement and Supply", "战略采购与供应（兼容占位）", "供应商管理；采购策略；合同"),
    ("LGS3010", "Logistics and Distribution Management", "物流与配送管理（兼容占位）", "运输；仓储；配送网络；最后一公里"),
]


def main():
    obj = {code: {"name": name, "intro": intro, "outline": outline} for code, name, intro, outline in ROWS}
    js = (
        "/* Generated by scripts/build_course_catalog.py — 课程简介与大纲来自 Student Information System */\n"
        "window.COURSE_CATALOG = "
        + json.dumps(obj, ensure_ascii=False, indent=2)
        + ";\n"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(js, encoding="utf-8")
    print(f"Wrote {OUT} ({len(obj)} courses)")


if __name__ == "__main__":
    main()
