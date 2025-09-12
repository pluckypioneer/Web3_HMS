#!/bin/bash

# Web3 HMS Setup Script
# This script sets up the development environment for Web3 HMS

set -e

echo "🏥 Web3 HMS 开发环境设置脚本"
echo "=================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装 Node.js (>= 18.0.0)"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 未安装，请先安装 Python (>= 3.11)"
    exit 1
fi

echo "✅ 环境检查通过"

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 创建环境配置文件..."
    cp env.example .env
    echo "✅ 环境配置文件已创建，请根据需要修改 .env 文件"
fi

# Start database services
echo "🚀 启动数据库服务..."
docker-compose up postgres redis ipfs ganache -d

# Wait for services to be ready
echo "⏳ 等待服务启动..."
sleep 10

# Install backend dependencies
echo "📦 安装后端依赖..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "📦 安装前端依赖..."
cd frontend
npm install
cd ..

# Install blockchain dependencies
echo "📦 安装区块链依赖..."
cd blockchain
npm install
cd ..

# Initialize database
echo "🗄️ 初始化数据库..."
cd backend
source venv/bin/activate
python -c "
from app import create_app
from extensions import db
app = create_app()
with app.app_context():
    db.create_all()
    print('✅ 数据库表创建成功')
"
cd ..

# Deploy smart contracts
echo "🔗 部署智能合约..."
cd blockchain
npx hardhat compile
npx hardhat run scripts/deploy.js --network localhost
cd ..

echo ""
echo "🎉 Web3 HMS 开发环境设置完成！"
echo ""
echo "📋 下一步操作："
echo "1. 启动后端服务: cd backend && source venv/bin/activate && python app.py"
echo "2. 启动前端服务: cd frontend && npm run dev"
echo "3. 访问系统: http://localhost:3000"
echo ""
echo "🔑 默认账户："
echo "管理员: admin@hms.com / admin123"
echo "医生: doctor1@hms.com / doctor123"
echo "患者: patient1@hms.com / patient123"
echo ""
echo "📚 更多信息请查看 README.md"
