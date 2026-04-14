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

### push命令
1. 看改了什么
cd <file location>
git status

2. 加入暂存区
全部加入：
git add -A
或只加某些文件：
git add web/career.html

3. 提交到本地
git commit -m "<更新详情>"
若提示 “nothing to commit”，说明没有可提交的变更。

4. 推到 GitHub
git push origin main
若默认分支已跟踪远程，也可以直接：
git push


### clone命令
安装 Git（并确保能用 GitHub）
克隆仓库
git clone https://github.com/你的用户名/你的仓库名.git
cd 你的仓库名】

新建分支（推荐，不要直接在 main 改）
git checkout -b feat/my-change

修改代码后提交
git add .
git commit -m "描述这次改动"

推送到 GitHub
git push -u origin feat/my-change

到 GitHub 页面发起 Pull Request 合并到 main

后续每次继续开发
进入项目后先同步最新代码：
git pull


如果你就想直接改 main（不推荐，但可以）
git checkout main
git pull origin main
# 改代码后
git add .
git commit -m "update: xxx"
git push origin main


看提交历史：git log --oneline --graph --decorate -20