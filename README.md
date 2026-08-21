# 🎬 EditForm - 剪辑需求全栈自动化工作流

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![WeChat](https://img.shields.io/badge/Miniprogram-Native-07c160)

> 这是一个专为视频创作者、剪辑师和自媒体团队打造的 **轻量级客户需求提单与 CRM 管理系统**。

## ✨ 核心特性 (Features)
- **📱 小程序极速提单**：原生微信小程序，客户扫码即用，标准化采集“视频类型、时长、预算、对标参考”等字段。
- **⚡️ 高性能后端**：基于 Python 3.12 + FastAPI 构建，接口响应毫秒级。
- **📦 零配置数据库**：内置 SQLite 数据库，免安装免运维，开箱即用。
- **📊 一键报表导出**：支持将需求数据一键导出为带 BOM 头的 CSV 格式，完美兼容 Excel / ONLYOFFICE 无乱码。

## 🛠️ 技术栈 (Tech Stack)
- **前端**：微信小程序原生生态 (WXML / WXSS / JS)
- **后端**：Python 3.12, FastAPI, Uvicorn
- **数据持久化**：SQLite3 (轻量级本地文件数据库)
- **开发工具链**：PowerShell CLI, Git, Winget, ONLYOFFICE

## 🚀 极速启动 (Quick Start)
1. **获取代码**：\git clone https://github.com/你的用户名/edit-form.git\
2. **启动后端**：进入 \server\ 目录，运行 \env\Scripts\python.exe -m uvicorn app.main:app --reload\
3. **前端预览**：使用微信开发者工具导入 \miniprogram\ 目录即可。
4. **数据导出**：浏览器访问 \http://127.0.0.1:8000/api/requirements/export\ 即可获取数据表格。

---
*Built with ❤️ by Leo - 环境工程跨界极客*