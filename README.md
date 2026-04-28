# CourseDuck · 选课鸭

CourseDuck 是一个面向学生的课程推荐原型系统，当前版本为前端原型（静态页面 + 本地存储 + 接口占位）。

- GitHub: [https://github.com/TomTzg/CourseDuck](https://github.com/TomTzg/CourseDuck)
- 在线地址: [https://snazzy-conkies-2c1fd2.netlify.app](https://snazzy-conkies-2c1fd2.netlify.app)
- 数据更新时间: `2026/04/27`

## 页面结构

- `web/login.html`: 校园账号登录页
- `web/school.html`: 学院选择页
- `web/info.html`: 专业选择页
- `web/career.html`: 职业选择页
- `web/recommend.html`: 技能展示 + 专业课程库 + 课程推荐
- `web/course-detail.html`: 课程详情页（课程代码/名称/大纲/评分构成）

## 快速启动

可直接双击 HTML 查看静态效果；若要验证接口请求，建议使用本地静态服务器。

### 方式 1: Python

```bash
python -m http.server 5173
```

### 方式 2: Node.js

```bash
npx serve -l 5173
```

启动后访问:

- `http://localhost:5173/web/login.html`

## 关键功能说明

- 登录流程: 校园账号 + 验证码占位，支持协议/隐私弹窗
- 三步选择: 学院 -> 专业 -> 职业（页面底部步骤条高亮当前步骤）
- 推荐页: 技能树展示、课程库勾选已修、推荐卡片实时状态
- 课程详情: 展示课程基础信息、前置课程占位、评分构成占位

## 前端数据与存储

项目当前使用浏览器本地存储维护状态（`localStorage/sessionStorage`），主要包括:

- 登录会话（`courseduck.session`）
- 用户画像（`courseduck.profile`）
- 已修课程记录（按专业+职业区分 key）

## 接口占位（后端可对接）

前端已在 `web/assets/api.js` 预留接口调用，默认走同源 `/api`，并含 mock 兜底逻辑。

- `POST /api/auth/campus-email/login`
- `GET /api/meta/majors`
- `GET /api/meta/careers?majorId=...`
- `GET /api/courses/library?majorId=...`
- `GET /api/courses?majorId=...&careerId=...&q=...`
- `POST /api/recommendations`（body: `majorId`, `careerId`）
- `GET /api/skill-tree?careerId=...`

## 部署说明

本项目是纯静态前端，可直接部署到任意静态托管平台（Netlify/Vercel/Cloudflare Pages）。

- 根目录 `index.html` 可作为入口（跳转至 `web/login.html`）
- 所有页面资源使用相对路径，适合静态部署

## 课程信息补充
- `课程.docx`