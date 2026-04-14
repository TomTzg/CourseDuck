## CourseDuck 原型（纯前端）

### 页面
- `login.html`：校园邮箱登录
- `school.html`：步骤 2/3，选择并确认学院
- `info.html`：步骤 1/3，选择并确认专业
- `career.html`：步骤 3/3，根据专业选择并确认职业
- `recommend.html`：技能树 + 课程推荐 + 课程详情
- `course-detail.html`：课程代码 + 课程名称 + 课程大纲

### 本地打开
直接双击打开 HTML 也能看静态效果；但如果要测试 `fetch` 到真实后端，建议起一个本地静态服务器（任选其一）：

```bash
# 方式 1：Python（安装了 Python 的话）
python -m http.server 5173
```

```bash
# 方式 2：Node（安装了 Node 的话）
npx serve -l 5173
```

然后访问：
- `http://localhost:5173/web/login.html`

### 生产部署（www.CourseDuck.com, 暂时没有这个DNS， 现已在Netlify部署）
可以用任意静态托管平台（Vercel / Netlify / Cloudflare Pages）。

推荐最短流程（Vercel）：
1. 把当前项目推到 GitHub。
2. 在 Vercel 导入仓库并部署（无需构建命令）。
3. 在 Vercel 的 Domains 中添加：
   - `www.CourseDuck.com`
   - `CourseDuck.com`
4. 按 Vercel 提示到你的域名 DNS 控制台添加记录（通常是：
   - `www` 配置 `CNAME` 到 Vercel 提供的地址
   - 根域 `@` 配置 `A` 记录到 Vercel 指定 IP）
5. 生效后访问：
   - `https://www.CourseDuck.com`

说明：
- 根目录已新增 `index.html`，会自动跳转到 `web/login.html`。
- 页面内部资源都是相对路径，可直接静态部署。

### 后端接口（占位）
前端已预留 `web/assets/api.js`，默认指向同源 `/api`，并带了 mock 兜底：
- `POST /api/auth/campus-email/login`
- `GET /api/meta/majors`
- `GET /api/meta/careers?majorId=...`
- `GET /api/courses/library?majorId=...`
- `GET /api/courses?majorId=...&careerId=...&q=...`
- `POST /api/recommendations`（body: majorId, careerId）
- `GET /api/skill-tree?careerId=...`z

### Github： https://github.com/TomTzg/CourseDuck
### 产品网址：snazzy-conkies-2c1fd2.netlify.app