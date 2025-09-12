@echo off
REM Web3 HMS Setup Script for Windows
REM This script sets up the development environment for Web3 HMS

echo 🏥 Web3 HMS 开发环境设置脚本
echo ==================================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker 未安装，请先安装 Docker Desktop
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose 未安装，请先安装 Docker Compose
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js 未安装，请先安装 Node.js (>= 18.0.0)
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 未安装，请先安装 Python (>= 3.11)
    pause
    exit /b 1
)

echo ✅ 环境检查通过

REM Create environment file if it doesn't exist
if not exist .env (
    echo 📝 创建环境配置文件...
    copy env.example .env
    echo ✅ 环境配置文件已创建，请根据需要修改 .env 文件
)

REM Start database services
echo 🚀 启动数据库服务...
docker-compose up postgres redis ipfs ganache -d

REM Wait for services to be ready
echo ⏳ 等待服务启动...
timeout /t 10 /nobreak >nul

REM Install backend dependencies
echo 📦 安装后端依赖...
cd backend
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt
cd ..

REM Install frontend dependencies
echo 📦 安装前端依赖...
cd frontend
npm install
cd ..

REM Install blockchain dependencies
echo 📦 安装区块链依赖...
cd blockchain
npm install
cd ..

REM Initialize database
echo 🗄️ 初始化数据库...
cd backend
call venv\Scripts\activate.bat
python -c "from app import create_app; from extensions import db; app = create_app(); app.app_context().push(); db.create_all(); print('✅ 数据库表创建成功')"
cd ..

REM Deploy smart contracts
echo 🔗 部署智能合约...
cd blockchain
npx hardhat compile
npx hardhat run scripts/deploy.js --network localhost
cd ..

echo.
echo 🎉 Web3 HMS 开发环境设置完成！
echo.
echo 📋 下一步操作：
echo 1. 启动后端服务: cd backend ^&^& venv\Scripts\activate.bat ^&^& python app.py
echo 2. 启动前端服务: cd frontend ^&^& npm run dev
echo 3. 访问系统: http://localhost:3000
echo.
echo 🔑 默认账户：
echo 管理员: admin@hms.com / admin123
echo 医生: doctor1@hms.com / doctor123
echo 患者: patient1@hms.com / patient123
echo.
echo 📚 更多信息请查看 README.md
pause
