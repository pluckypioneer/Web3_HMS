# Web3 医院管理系统 (Web3 HMS)

基于区块链技术的现代化医院管理系统，融合 Solidity、Vue 3、Flask 技术栈，实现医疗数据不可篡改存证、全流程数字化管理、多角色协同办公。

> 📌 **项目状态**: 已完成核心功能开发，可以正常运行使用。

## 🚀 项目特色

- **🔗 区块链集成**: 医疗数据哈希存证，确保数据完整性和不可篡改性
- **🏥 医疗专业**: 覆盖患者服务、临床诊疗、住院管理、药品物资等核心场景
- **🔐 数据安全**: 基于 RBAC 的权限控制，支持细粒度数据访问管理
- **📱 现代化UI**: Vue 3 + Element Plus，响应式设计，多端适配
- **🐳 容器化部署**: Docker 容器化，支持一键部署和扩展
- **📊 实时监控**: 区块链状态监控，系统健康检查

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                        用户层                                │
├─────────────────────────────────────────────────────────────┤
│  患者端(Web/H5)  │  医护端(Web)  │  管理端(Web)  │  运维端(Web) │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                      前端层 (Vue 3)                          │
├─────────────────────────────────────────────────────────────┤
│  Element Plus UI  │  Vue Router  │  Pinia状态管理  │  Web3.js  │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                    API网关层 (Flask)                         │
├─────────────────────────────────────────────────────────────┤
│  JWT认证  │  RBAC权限  │  请求限流  │  跨域处理  │  日志记录  │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                    业务逻辑层 (Flask)                        │
├─────────────────────────────────────────────────────────────┤
│ 患者服务 │ 临床诊疗 │ 住院管理 │ 药品物资 │ 运营管理 │ 统计分析 │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                        数据层                                │
├─────────────────────────────────────────────────────────────┤
│ PostgreSQL │ Redis缓存 │ 区块链 │ IPFS存储 │ 文件系统 │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ 技术栈

### 前端技术
- **Vue 3**: 渐进式 JavaScript 框架
- **Element Plus**: Vue 3 组件库
- **Vue Router**: 官方路由管理器
- **Pinia**: 状态管理库
- **Web3.js**: 区块链交互库
- **TypeScript**: 类型安全的 JavaScript
- **Vite**: 现代化构建工具

### 后端技术
- **Flask**: 轻量级 Python Web 框架
- **Flask-RESTful**: RESTful API 开发
- **PyMongo**: MongoDB 驱动
- **MongoDB**: NoSQL 数据库
- **Redis**: 内存数据库
- **JWT**: 身份认证
- **Celery**: 异步任务队列

### 区块链技术
- **Solidity**: 智能合约开发语言
- **Hardhat**: 以太坊开发环境
- **Web3.js**: 前端区块链交互
- **IPFS**: 分布式文件存储

### 部署运维
- **Docker**: 容器化平台
- **Docker Compose**: 多容器编排
- **Nginx**: 反向代理服务器
- **Gunicorn**: WSGI HTTP 服务器

## 📋 核心功能

### 患者服务模块
- ✅ 多渠道预约挂号
- ✅ 电子就诊卡管理
- ✅ 病历查询（本人）
- ✅ 医保结算
- ✅ 检查报告查看

### 临床诊疗模块
- ✅ 电子病历录入
- ✅ 医嘱管理
- ✅ 处方开具与审核
- ✅ 检查检验申请
- ✅ 手术麻醉管理

### 住院管理模块
- ✅ 床位分配与管理
- ✅ 住院费用实时核算
- ✅ 出院结算
- ✅ 护理计划与记录

### 药品与物资模块
- ✅ 药品库存管理
- ✅ 高值耗材溯源
- ✅ 耗材领用与核销

### 区块链功能
- ✅ 医疗数据哈希存证
- ✅ 数据访问权限控制
- ✅ 药品供应链溯源
- ✅ 数据完整性验证

## 🚀 快速开始

### 环境要求

- **Node.js**: >= 18.0.0
- **Python**: >= 3.9
- **Docker**: >= 20.10.0
- **Docker Compose**: >= 2.0.0
- **Git**: >= 2.30.0

### 一键部署

1. **克隆项目**
```bash
git clone https://github.com/pluckypioneer/Web3_HMS
cd Web3_HMS
```

2. **配置环境变量**
```bash
# 复制环境配置文件
cp env.example .env

# 根据实际环境修改配置
vim .env
```

3. **启动服务**
```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

4. **访问系统**
- 前端界面: http://localhost:3000
- 后端API: http://localhost:5000
- 区块链节点: http://localhost:8545
- IPFS节点: http://localhost:5001

### 默认账户

| 角色 | 邮箱 | 密码 | 说明 |
|------|------|------|------|
| 管理员 | admin@hms.com | password123 | 系统管理员 |
| 医生 | doctor1@hms.com | password123 | 张医生 |
| 患者 | patient1@hms.com | password123 | 王患者 |

### 需要使用者手动配置的API和数据库相关项

系统运行前需要配置相关环境变量，主要包括：

1. **数据库配置**
   - `MONGO_URI`: 生产环境 MongoDB 连接字符串
   - `DEV_MONGO_URI`: 开发环境 MongoDB 连接字符串
   - `TEST_MONGO_URI`: 测试环境 MongoDB 连接字符串

2. **安全密钥配置**
   - `SECRET_KEY`: Flask 应用密钥
   - `JWT_SECRET_KEY`: JWT 认证密钥

3. **区块链配置**
   - `WEB3_PROVIDER_URL`: 区块链节点URL
   - `MEDICAL_RECORD_HASH_ADDRESS`: 医疗记录哈希合约地址
   - `ACCESS_CONTROL_ADDRESS`: 访问控制合约地址
   - `DRUG_TRACE_ADDRESS`: 药品追溯合约地址

4. **邮件服务配置**
   - `MAIL_SERVER`: 邮件服务器地址
   - `MAIL_PORT`: 邮件服务器端口
   - `MAIL_USERNAME`: 邮箱用户名
   - `MAIL_PASSWORD`: 邮箱密码或应用专用密码

5. **其他配置**
   - `CORS_ORIGINS`: 跨域访问源列表
   - `IPFS_URL`: IPFS节点URL

完整配置项请参考 [env.example](env.example) 文件。

## 🔧 开发指南

### 本地开发环境

1. **启动数据库服务**
```bash
docker-compose up mongodb redis ipfs ganache -d
```

2. **启动后端服务**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

3. **启动前端服务**
```bash
cd frontend
npm install
npm run dev
```

4. **部署智能合约**
```bash
cd blockchain
npm install
npx hardhat compile
npx hardhat run scripts/deploy.js --network localhost
```

### 项目结构

```
Web3_HMS/
├── frontend/                 # Vue 3 前端
│   ├── src/
│   │   ├── components/       # 组件
│   │   ├── views/            # 页面
│   │   ├── stores/           # 状态管理
│   │   ├── router/           # 路由配置
│   │   ├── utils/            # 工具函数
│   │   ├── App.vue           # 根组件
│   │   ├── main.ts           # 入口文件
│   │   └── style.css         # 全局样式
│   ├── package.json          # 前端依赖配置
│   ├── vite.config.ts        # Vite 配置
│   ├── tsconfig.json         # TypeScript 配置
│   └── index.html            # HTML 模板
├── backend/                  # Flask 后端
│   ├── api/                 # API 路由
│   │   ├── resources/       # 资源定义
│   │   └── __init__.py      # API 初始化
│   ├── models/              # 数据模型
│   ├── config.py            # 配置文件
│   ├── app.py               # 应用入口
│   ├── extensions.py         # 扩展模块
│   └── requirements.txt     # 后端依赖配置
├── blockchain/               # 智能合约
│   ├── contracts/           # Solidity 合约
│   ├── scripts/             # 部署脚本
│   ├── hardhat.config.js    # Hardhat 配置
│   └── package.json         # 区块链依赖配置
├── nginx/                   # Nginx 配置
│   └── nginx.conf           # Nginx 配置文件
├── scripts/                 # 脚本文件
│   ├── init-db.sql          # 数据库初始化脚本
│   ├── setup.bat            # Windows 安装脚本
│   └── setup.sh             # Linux/Mac 安装脚本
├── docker-compose.yml       # Docker 编排
├── env.example              # 环境变量示例
└── README.md
```

## 🔐 安全特性

### 数据安全
- **传输加密**: 全接口 HTTPS 加密
- **存储加密**: 敏感数据加密存储
- **访问控制**: 基于 RBAC 的细粒度权限管理
- **审计日志**: 完整的操作审计追踪

### 区块链安全
- **智能合约审计**: Mythril、Slither 安全扫描
- **哈希验证**: SHA-256 数据完整性校验
- **权限管理**: 基于区块链地址的访问控制
- **不可篡改**: 医疗数据哈希永久存证

### 合规性
- **医疗数据合规**: 符合《电子病历应用管理规范》
- **隐私保护**: 遵循《个人信息保护法》
- **区块链合规**: 符合司法存证标准

## 📊 监控与运维

### 健康检查
```bash
# 检查服务状态
curl http://localhost:5000/health

# 检查区块链连接
curl http://localhost:5000/api/blockchain/status
```

### 日志查看
```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 数据备份
```bash
# 备份数据库
docker-compose exec mongodb mongodump --db hms_db --out /backup

# 恢复数据库
docker-compose exec mongodb mongorestore --db hms_db /backup/hms_db
```

## 🚀 部署指南

### 生产环境部署

1. **环境配置**
```bash
# 复制环境配置文件
cp .env.example .env

# 修改生产环境配置
vim .env
```

2. **SSL 证书配置**
```bash
# 生成 SSL 证书（开发环境）
openssl req -x509 -newkey rsa:4096 -keyout nginx/ssl/key.pem -out nginx/ssl/cert.pem -days 365 -nodes

# 修改 nginx.conf 启用 HTTPS
```

3. **启动生产服务**
```bash
# 构建并启动服务
docker-compose -f docker-compose.prod.yml up -d

# 检查服务状态
docker-compose ps
```

### 扩展部署

```bash
# 水平扩展后端服务
docker-compose up -d --scale backend=3

# 添加负载均衡
docker-compose up -d nginx
```

## 🤝 贡献指南

1. **Fork 项目**
2. **创建特性分支**: `git checkout -b feature/AmazingFeature`
3. **提交更改**: `git commit -m 'Add some AmazingFeature'`
4. **推送分支**: `git push origin feature/AmazingFeature`
5. **提交 Pull Request**

### 本地开发

推荐使用 VS Code 进行开发，项目已配置好调试环境。

### 开发规范

- **代码风格**: 遵循 ESLint 和 Prettier 配置
- **提交信息**: 使用 Conventional Commits 规范
- **测试覆盖**: 确保新功能有对应的测试用例
- **文档更新**: 及时更新相关文档
- **类型安全**: 使用 TypeScript 提供类型安全保障

## 📝 更新日志

### v1.2.0 (2025-09-25)
- ✅ 数据库从 PostgreSQL 迁移至 MongoDB
- ✅ 更新后端依赖配置
- ✅ 修改数据模型以适应文档数据库

### v1.1.0 (2025-09-25)
- ✅ 修复前端组件缺失问题
- ✅ 完善用户认证系统
- ✅ 优化系统架构和代码结构
- ✅ 修复多个TypeScript类型错误
- ✅ 清理冗余文件和代码

### v1.0.0 (2025-09-13)
- ✅ 初始版本发布
- ✅ 核心功能模块完成
- ✅ 区块链集成完成
- ✅ Docker 容器化部署
- ✅ 基础安全防护

## 📄 许可证

本项目采用Apache License 2.0许可证 - 查看 [LICENSE](https://github.com/pluckypioneer/Web3_HMS/blob/main/LICENSE) 文件了解详情。

## 🆘 支持与帮助

### 常见问题

**Q: 如何重置管理员密码？**
A: 通过数据库直接修改 users 集合中的 password_hash 字段。

**Q: 区块链交易失败怎么办？**
A: 检查 Ganache 节点是否正常运行，确认账户余额充足。

**Q: 如何添加新的科室？**
A: 在 departments 集合中插入新文档，或通过管理界面添加。

### 联系方式

- **项目主页**: [GitHub Repository](https://github.com/pluckypioneer/Web3_HMS)
- **问题反馈**: [GitHub Issues](https://github.com/pluckypioneer/Web3_HMS/issues)
- **技术交流**: [Discussion Forum]
- **邮箱联系**: pluckypioneer258@proton.me

## 🙏 致谢

感谢以下开源项目的支持：
- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Element Plus](https://element-plus.org/) - Vue 3 组件库
- [Flask](https://flask.palletsprojects.com/) - Python Web 框架
- [Hardhat](https://hardhat.org/) - 以太坊开发环境
- [Docker](https://www.docker.com/) - 容器化平台

---

**Web3 HMS** - 让医疗数据更安全，让医院管理更智能 🏥✨

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=pluckypioneer/Web3_HMS&type=Date)](https://www.star-history.com/#pluckypioneer/Web3_HMS&Date)
