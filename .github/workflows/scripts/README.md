# Daily Joke Report 😄

Automatically collects 20 network jokes daily and sends them to your email every morning at 9 AM.

## ⚡ Quick Setup

### 1. Add Email Password Secret (必须做)

1. 打开仓库: https://github.com/gameweman/dailyreport
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **"New repository secret"**
4. 名称: `EMAIL_PASSWORD`
5. 密码: 你的邮箱应用密码

### 2. Outlook 邮箱配置 ✅

脚本已经配置好 Outlook SMTP，你可以直接用邮箱密码。

### 3. 测试一下

1. 打开 **Actions** 标签页
2. 选择 **"Daily Joke Report"** 工作流
3. 点击 **"Run workflow"** 按钮
4. 检查你的邮箱!

### 4. 时间设置 (可选)

默认每天早上 9 点 UTC。要改时间编辑 `.github/workflows/daily-report.yml`:

```yaml
cron: '0 9 * * *'
