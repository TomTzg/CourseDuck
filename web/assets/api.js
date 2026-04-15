// CourseDuck API client (prototype)
// - Default base: same-origin `/api`
// - Provides mock fallbacks when backend is absent

export const API_BASE = "/api";

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function nowIso() {
  return new Date().toISOString();
}

function safeJsonParse(text) {
  try { return JSON.parse(text); } catch { return null; }
}

function ensureArray(input) {
  return Array.isArray(input) ? input : [];
}

function pickItems(payload) {
  if (Array.isArray(payload)) return payload;
  if (!payload || typeof payload !== "object") return [];
  return ensureArray(payload.items ?? payload.data ?? payload.list ?? payload.results);
}

function hasAnyListField(payload) {
  return Boolean(
    payload &&
    typeof payload === "object" &&
    ("items" in payload || "data" in payload || "list" in payload || "results" in payload)
  );
}

const CAREER_PROFILES = {
  career_ib_analyst: {
    skills: ["企业估值", "财务建模", "并购重组", "尽职调查", "投融资方案设计", "财报分析"],
    courses: [
      "FIN2010 Financial Management",
      "FIN3080 Investment Analysis and Portfolio Management",
      "FIN4210 Corporate Finance",
      "FIN4220 Advanced Corporate Finance",
      "FIN4050 Mergers and Acquisitions",
      "ACT4213 Financial Statement Analysis",
      "FIN4230 Value Investing",
    ],
  },
  career_securities_trader: {
    skills: ["金融市场交易", "衍生品操作", "风险控制", "投资组合管理", "行情研判"],
    courses: [
      "FIN3080 Investment Analysis and Portfolio Management",
      "FIN4110 Options and Futures",
      "FIN3030 Financial Institutions and Markets",
      "RMS4060 Risk Management with Derivatives",
      "FIN4080 Behavioral Finance",
      "FIN4120 Fixed Income Securities Analysis",
    ],
  },
  career_bank_mt: {
    skills: ["商业银行运营", "信贷管理", "金融合规", "客户管理", "宏观政策解读"],
    courses: [
      "FIN3030 Financial Institutions and Markets",
      "FIN3060 Banking",
      "FIN2010 Financial Management",
      "FIN4210 Corporate Finance",
      "ECO3410 Economics of Money and Financial Institutions",
      "ACT3181 Credit Rating and Risk Management",
    ],
  },
  career_investment_manager: {
    skills: ["项目尽调", "估值建模", "投后管理", "VC/PE运作", "商业计划书研判"],
    courses: [
      "FIN2010 Financial Management",
      "FIN3330 Alternative Investments",
      "FIN3340 Financial Innovations and Alternative Investment",
      "FIN4210 Corporate Finance",
      "FIN4230 Value Investing",
      "ACT4213 Financial Statement Analysis",
    ],
  },
  career_mgmt_consultant: {
    skills: ["行业研究", "战略规划", "商业分析", "数据建模", "方案撰写", "案例分析"],
    courses: [
      "ECO2011 Basic Microeconomics",
      "ECO3011 Intermediate Microeconomic Theory",
      "ECO3160 Game Theory and Business Strategy",
      "ECO3480 Industrial Organization and Public Policy",
      "ECO3211 Quantitative Methods for Policy Evaluation",
      "ECO3110 Behavioral Economics",
    ],
  },
  career_strategy_analyst: {
    skills: ["宏观趋势研判", "用户与市场分析", "商业模型分析", "数据驱动决策"],
    courses: [
      "ECO2021 Basic Macroeconomics",
      "ECO3021 Intermediate Macroeconomic Theory",
      "ECO3620 Data Analysis and Macroeconomic Policies",
      "ECO3150 Digital Economics",
      "ECO3110 Behavioral Economics",
    ],
  },
  career_macro_researcher: {
    skills: ["宏观经济预测", "政策分析", "经济指标建模", "行业周期判断"],
    courses: [
      "ECO2021 Basic Macroeconomics",
      "ECO3021 Intermediate Macroeconomic Theory",
      "ECO3630 International Finance",
      "ECO3410 Economics of Money and Financial Institutions",
      "ECO3620 Data Analysis and Macroeconomic Policies",
      "ECO3710 China Economy",
    ],
  },
  career_regulatory_analyst: {
    skills: ["政策评估", "经济统计", "风险监测", "合规分析", "宏观审慎管理"],
    courses: [
      "ECO3430 Public Finance",
      "ECO4121 Intermediate Econometrics",
      "ECO3230 Economic Analysis of Law and Human Behavior",
      "ECO3410 Economics of Money and Financial Institutions",
      "ECO4001 Environmental Economics and Policy",
    ],
  },
  career_big4_auditor: {
    skills: ["财务审计", "内控测试", "审计准则应用", "风险评估", "底稿编制"],
    courses: [
      "ACT2111 Introductory Financial Accounting",
      "ACT3011 Intermediate Financial Accounting",
      "ACT4131 Auditing",
      "ACT4231 Internal Auditing and Risk Management",
      "ACT3141 Accounting Information Systems",
      "ACT3131 Accounting Theory",
    ],
  },
  career_corporate_finance: {
    skills: ["账务处理", "成本核算", "预算管理", "财务报表编制", "资金管理"],
    courses: [
      "ACT2121 Introductory Management Accounting",
      "ACT3011 Intermediate Financial Accounting",
      "ACT3311 Accounting Forecasting and Analysis",
      "ACT4213 Financial Statement Analysis",
      "ACT4121 Strategic Management Accounting",
    ],
  },
  career_tax_advisor: {
    skills: ["税务合规", "税务筹划", "中国税制", "国际税收", "转让定价"],
    courses: [
      "ACT2111 Introductory Financial Accounting",
      "ACT4262 China Taxation",
      "ACT4263 International Taxation",
      "ACT3153 Business and Company Law",
    ],
  },
  career_accountant: {
    skills: ["会计核算", "报表编制", "内控管理", "财务分析", "会计准则执行"],
    courses: [
      "ACT2111 Introductory Financial Accounting",
      "ACT3011 Intermediate Financial Accounting",
      "ACT3131 Accounting Theory",
      "ACT3141 Accounting Information Systems",
      "ACT4213 Financial Statement Analysis",
    ],
  },
  career_quant_trader: {
    skills: ["量化策略开发", "回测", "程序化交易", "风险模型", "统计套利"],
    courses: [
      "FIN2210 Probability for Finance",
      "FIN4110 Options and Futures",
      "FMA4200 Financial Data Analysis",
      "ECO3090 Machine Learning for Financial Economics",
      "MAT4500 Stochastics Differential Equations",
      "STA4003 Time Series",
    ],
  },
  career_fin_model_dev: {
    skills: ["衍生品定价", "风险模型", "数值计算", "蒙特卡洛模拟", "量化建模"],
    courses: [
      "FMA4800 Financial Computation",
      "FIN4110 Options and Futures",
      "STA4001 Stochastic Process",
      "FMA4200 Financial Data Analysis",
      "FIN4231 Asset Pricing",
      "MAT3280 Probability Theory",
    ],
  },
  career_fintech_algo: {
    skills: ["机器学习", "数据分析", "金融算法", "大数据处理", "模型部署"],
    courses: [
      "DDA3020 Machine Learning",
      "ACT4311 Data Mining for Accounting Analytics",
      "FIN3210 Fintech Theory and Practice",
      "FMA4200 Financial Data Analysis",
      "FIN3090 AI Applications in Finance",
      "STA4003 Time Series",
    ],
  },
  career_bi_analyst: {
    skills: ["数据清洗", "统计建模", "可视化", "商业洞察", "报告输出"],
    courses: [
      "DMS3003 Data Analytics and Decision Making",
      "ACT4321 Accounting Database and Data Visualization",
      "MKT3310 Marketing Analytics",
      "ACT4311 Data Mining for Accounting Analytics",
      "STA3010 Regression Analysis",
      "STA3020 Statistical Inference",
    ],
  },
  career_data_ops: {
    skills: ["用户数据分析", "增长运营", "数据监控", "业务指标优化"],
    courses: [
      "MKT3320 Digital Consumer Analytics",
      "MKT3310 Marketing Analytics",
      "DMS3003 Data Analytics and Decision Making",
      "ECO3080 Machine Learning for Business",
      "ACT4321 Accounting Database and Data Visualization",
    ],
  },
  career_digital_analyst: {
    skills: ["流程数字化", "数据治理", "业务分析", "系统需求", "数字化转型"],
    courses: [
      "ACT3141 Accounting Information Systems",
      "DMS3003 Data Analytics and Decision Making",
      "ACT4321 Accounting Database and Data Visualization",
      "MIS2051 IT in Business Applications",
    ],
  },
  career_market_data_specialist: {
    skills: ["市场调研", "用户画像", "营销效果分析", "数据报表", "竞品分析"],
    courses: [
      "MKT4120 Marketing Research",
      "MKT3310 Marketing Analytics",
      "MKT3320 Digital Consumer Analytics",
      "DMS3003 Data Analytics and Decision Making",
      "MKT3060 Quantitative Marketing Methods in the AI Age",
    ],
  },
  career_cross_border_business: {
    skills: ["国际贸易", "跨境运营", "海关合规", "海外市场拓展", "供应链管理"],
    courses: [
      "ECO3610 International Trade",
      "MGT3250 International Business",
      "MKT3050 Global Marketing",
      "DMS2030 Operations Management",
      "ECO3630 International Finance",
      "MGT4250 Cross-Cultural Communication and Negotiation",
    ],
  },
  career_brand_pr: {
    skills: ["品牌管理", "媒体沟通", "危机公关", "活动策划", "舆情管理"],
    courses: [
      "MKT3030 Integrated Marketing Communication",
      "MKT4110 Strategic Brand Management",
      "MGT4250 Cross-Cultural Communication and Negotiation",
    ],
  },
  career_foreign_market_specialist: {
    skills: ["市场调研", "营销策划", "品牌推广", "跨文化沟通", "渠道管理"],
    courses: [
      "MKT2010 Marketing Management",
      "MKT3050 Global Marketing",
      "MKT3020 Consumer Behavior",
      "MGT4250 Cross-Cultural Communication and Negotiation",
      "MGT3250 International Business",
    ],
  },
  career_internet_marketing_ops: {
    skills: ["用户增长", "内容策划", "活动运营", "渠道投放", "数据复盘"],
    courses: [
      "MKT2010 Marketing Management",
      "MKT3320 Digital Consumer Analytics",
      "MKT3020 Consumer Behavior",
      "MKT3310 Marketing Analytics",
      "MKT3080 Strategic Media Planning",
    ],
  },
  career_supply_chain_ops: {
    skills: ["全链协同", "成本管控", "交付管理", "供应链风险应对"],
    courses: [
      "DMS2030 Operations Management",
      "MGT2020 Principles of Management",
      "DMS3003 Data Analytics and Decision Making",
      "MIS2051 IT in Business Applications",
      "SCM3010 Supply Chain Management",
    ],
  },
  career_plan_production_plan: {
    skills: ["需求预测", "产能计划", "库存优化", "交期管控", "生产排程"],
    courses: [
      "DMS2030 Operations Management",
      "FIN2210 Probability for Finance",
      "STA4003 Time Series",
      "ECO3080 Machine Learning for Business",
      "SCM3020 Demand and Inventory Planning",
    ],
  },
  career_procurement_buyer_trade: {
    skills: ["供应商开发", "商务议价", "成本控制", "质量管控", "交付管理"],
    courses: [
      "DMS2030 Operations Management",
      "ACT3153 Business and Company Law",
      "ECO3610 International Trade",
      "SCM3030 Strategic Procurement and Supply",
    ],
  },
  career_warehouse_logistics: {
    skills: ["仓储规划", "物流调度", "配送优化", "WMS系统", "成本管控"],
    courses: [
      "DMS2030 Operations Management",
      "DMS3003 Data Analytics and Decision Making",
      "MIS2051 IT in Business Applications",
      "LGS3010 Logistics and Distribution Management",
    ],
  },
  career_supply_chain_data_analysis: {
    skills: ["数据建模", "流程优化", "供应链仿真", "效率提升", "成本分析"],
    courses: [
      "STA2001 Probability and Statistics I",
      "DMS2030 Operations Management",
      "FMA4200 Financial Data Analysis",
      "STA4003 Time Series",
      "ACT4321 Accounting Database and Data Visualization",
    ],
  },
};

function parseCourseEntry(entry) {
  const text = String(entry || "").trim();
  const sp = text.indexOf(" ");
  if (sp <= 0) {
    const codeOnly = text || "GEN0000";
    return { code: codeOnly, title: text || "Course" };
  }
  return { code: text.slice(0, sp), title: text.slice(sp + 1).trim() };
}

function courseIdFromCode(code) {
  return String(code || "").toLowerCase().replace(/[^a-z0-9]+/g, "_");
}

function buildCourseCatalog() {
  const m = new Map();
  Object.values(CAREER_PROFILES).forEach((p) => {
    (p.courses || []).forEach((entry) => {
      const { code, title } = parseCourseEntry(entry);
      const id = courseIdFromCode(code);
      if (!m.has(id)) {
        m.set(id, {
          id,
          code,
          title: `${code} ${title}`,
          provider: "SME Course Catalog",
          level: "进阶",
          durationHours: 16,
          tags: [code.slice(0, 3), "SME"],
          skills: [],
        });
      }
    });
  });
  return Array.from(m.values());
}

function getCareerCourseIds(careerId) {
  const p = CAREER_PROFILES[careerId];
  if (!p) return [];
  return (p.courses || []).map((entry) => courseIdFromCode(parseCourseEntry(entry).code));
}

function getMajorCourseIds(majorId, careersByMajor) {
  const careers = (careersByMajor && careersByMajor[majorId]) || [];
  const ids = new Set();
  careers.forEach((c) => {
    getCareerCourseIds(c.id).forEach((id) => ids.add(id));
  });
  return Array.from(ids);
}

async function request(path, { method = "GET", headers = {}, body } = {}) {
  const url = `${API_BASE}${path}`;
  const init = {
    method,
    headers: {
      "Accept": "application/json",
      ...headers,
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  };
  if (body !== undefined) init.headers["Content-Type"] = "application/json";

  const res = await fetch(url, init);
  const text = await res.text();
  const json = safeJsonParse(text);
  if (!res.ok) {
    const msg = (json && (json.message || json.error)) || text || `HTTP ${res.status}`;
    const err = new Error(msg);
    err.status = res.status;
    err.payload = json ?? text;
    throw err;
  }
  return json ?? {};
}

// ---------- Mock data ----------
const MOCK = {
  majors: [
    { id: "economics", name: "经济学" },
    { id: "fin", name: "金融学" },
    { id: "intl_business", name: "国际商务" },
    { id: "accounting", name: "专业会计学" },
    { id: "fe", name: "金融工程" },
    { id: "mkt_ib", name: "市场营销与国际商务" },
    { id: "bdm", name: "大数据管理与应用" },
  ],
  careersByMajor: {
    economics: [
      { id: "career_mgmt_consultant", name: "管理咨询顾问" },
      { id: "career_strategy_analyst", name: "互联网大厂战略分析师" },
      { id: "career_macro_researcher", name: "券商宏观研究员" },
      { id: "career_regulatory_analyst", name: "金融监管机构经济分析岗" },
    ],
    fin: [
      { id: "career_ib_analyst", name: "投资银行分析师" },
      { id: "career_securities_trader", name: "证券公司交易员" },
      { id: "career_bank_mt", name: "银行总行管培生" },
      { id: "career_investment_manager", name: "投资经理" },
    ],
    accounting: [
      { id: "career_big4_auditor", name: "四大会计师事务所审计师" },
      { id: "career_corporate_finance", name: "企业财务" },
      { id: "career_tax_advisor", name: "税务师" },
      { id: "career_accountant", name: "会计师" },
    ],
    fe: [
      { id: "career_quant_trader", name: "量化交易员" },
      { id: "career_fin_model_dev", name: "金融模型开发" },
      { id: "career_fintech_algo", name: "金融科技算法工程师" },
    ],
    bdm: [
      { id: "career_bi_analyst", name: "商业数据分析师" },
      { id: "career_data_ops", name: "互联网数据运营" },
      { id: "career_digital_analyst", name: "企业数字化分析师" },
      { id: "career_market_data_specialist", name: "市场数据分析专员" },
    ],
    intl_business: [
      { id: "career_cross_border_business", name: "跨境商务" },
      { id: "career_brand_pr", name: "品牌公关" },
      { id: "career_foreign_market_specialist", name: "外企市场部专员" },
      { id: "career_internet_marketing_ops", name: "互联网市场策划/运营" },
    ],
    mkt_ib: [
      { id: "career_cross_border_business", name: "跨境商务" },
      { id: "career_brand_pr", name: "品牌公关" },
      { id: "career_foreign_market_specialist", name: "外企市场部专员" },
      { id: "career_internet_marketing_ops", name: "互联网市场策划/运营" },
    ],
  },
  courses: buildCourseCatalog(),
  skillTreeByCareer: {
    default: [
      { id: "s1", name: "岗位技能", required: ["专业知识", "分析能力"] },
    ],
  },
};

function mockRecommendation({ majorId, careerId }) {
  const top = getCareerCourseIds(careerId);
  const topSet = new Set(top);
  const items = MOCK.courses
    .map((c) => ({
      ...c,
      score: topSet.has(c.id) ? 0.95 : 0.7,
      reason: topSet.has(c.id) ? "与你选择职业的核心技能高度匹配" : "通用补充课程",
    }))
    .sort((a, b) => b.score - a.score)
    .slice(0, 8);
  return {
    requestId: `mock_${Date.now()}`,
    generatedAt: nowIso(),
    items,
  };
}

// ---------- Public API ----------
export async function loginWithCampusEmail({ email, code }) {
  // Backend contract:
  // POST /api/auth/campus-email/login
  // body: { email, code }
  // returns: { token, user: { id, name, email } }
  try {
    return await request("/auth/campus-email/login", { method: "POST", body: { email, code } });
  } catch {
    await sleep(450);
    return {
      token: "mock_token",
      user: { id: "u_001", name: "同学", email },
    };
  }
}

export async function getMajors() {
  // GET /api/meta/majors -> { items: [{id,name}] }
  try {
    const payload = await request("/meta/majors");
    const items = pickItems(payload);
    if (items.length > 0) return { items };
    throw new Error("Majors payload missing items");
  } catch {
    await sleep(200);
    return { items: MOCK.majors };
  }
}

export async function getCareers({ majorId }) {
  // GET /api/meta/careers?majorId=... -> { items: [{id,name}] }
  try {
    const qs = new URLSearchParams({ majorId: majorId || "" }).toString();
    const payload = await request(`/meta/careers?${qs}`);
    const items = pickItems(payload);
    if (items.length > 0) return { items };
    throw new Error("Careers payload missing items");
  } catch {
    await sleep(220);
    const items = MOCK.careersByMajor[majorId] || MOCK.careersByMajor.fin;
    return { items };
  }
}

export async function searchCourses({ majorId, careerId, q }) {
  // GET /api/courses?majorId=...&careerId=...&q=... -> { items: [...] }
  try {
    const qs = new URLSearchParams({
      majorId: majorId || "",
      careerId: careerId || "",
      q: q || "",
    }).toString();
    const payload = await request(`/courses?${qs}`);
    const items = pickItems(payload);
    if (Array.isArray(payload) || hasAnyListField(payload)) return { items };
    throw new Error("Courses payload missing list field");
  } catch {
    await sleep(260);
    const query = (q || "").trim().toLowerCase();
    const focusIds = getCareerCourseIds(careerId);
    const majorIds = getMajorCourseIds(majorId, MOCK.careersByMajor);
    let items = MOCK.courses;
    if (focusIds.length > 0) {
      const topSet = new Set(focusIds);
      items = MOCK.courses.filter((c) => topSet.has(c.id)).concat(MOCK.courses.filter((c) => !topSet.has(c.id)));
    } else if (majorIds.length > 0) {
      const majorSet = new Set(majorIds);
      items = MOCK.courses.filter((c) => majorSet.has(c.id)).concat(MOCK.courses.filter((c) => !majorSet.has(c.id)));
    }
    if (query) {
      items = items.filter((c) =>
        [c.title, c.provider, c.level, ...(c.tags || [])].join(" ").toLowerCase().includes(query)
      );
    }
    return { items };
  }
}

export async function getSkillTree({ careerId }) {
  // GET /api/skill-tree?careerId=... -> { nodes: [{id,name,required:[...], have?:[...] , gaps?:[...] }] }
  try {
    const qs = new URLSearchParams({ careerId: careerId || "" }).toString();
    return await request(`/skill-tree?${qs}`);
  } catch {
    await sleep(240);
    const profile = CAREER_PROFILES[careerId];
    const skills = profile?.skills || MOCK.skillTreeByCareer.default[0].required;
    const chunk = Math.max(2, Math.ceil(skills.length / 3));
    const built = [];
    for (let i = 0; i < skills.length; i += chunk) {
      built.push({
        id: `s${built.length + 1}`,
        name: `核心技能组 ${built.length + 1}`,
        required: skills.slice(i, i + chunk),
      });
    }
    const nodes = built.map((n) => ({
      ...n,
      have: n.required.slice(0, Math.max(1, Math.floor(n.required.length / 2))),
      gaps: n.required.slice(Math.max(1, Math.floor(n.required.length / 2))),
    }));
    return { nodes };
  }
}

export async function getRecommendations({ majorId, careerId }) {
  // POST /api/recommendations -> { requestId, generatedAt, items:[{id,title,score,reason,...}] }
  try {
    return await request("/recommendations", { method: "POST", body: { majorId, careerId } });
  } catch {
    await sleep(380);
    return mockRecommendation({ majorId, careerId });
  }
}

export async function getMajorCourseLibrary({ majorId }) {
  // GET /api/courses/library?majorId=... -> { items: [...] }
  try {
    const qs = new URLSearchParams({ majorId: majorId || "" }).toString();
    const payload = await request(`/courses/library?${qs}`);
    const items = pickItems(payload);
    if (Array.isArray(payload) || hasAnyListField(payload)) return { items };
    throw new Error("Course library payload missing list field");
  } catch {
    await sleep(180);
    const ids = getMajorCourseIds(majorId, MOCK.careersByMajor);
    const set = new Set(ids);
    const items = ids.length > 0
      ? MOCK.courses.filter((c) => set.has(c.id))
      : MOCK.courses;
    return { items };
  }
}

