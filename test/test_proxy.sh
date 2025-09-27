#!/bin/bash

echo "测试前端代理是否正常工作..."
echo "1. 测试前端容器能否访问后端健康检查:"

# 测试前端容器内部是否能访问后端
docker exec hms-frontend sh -c "wget -q -O - http://backend:5000/health" || echo "❌ 前端容器无法访问后端"

echo ""
echo "2. 测试前端代理是否正常转发API请求:"

# 测试通过前端代理访问API (这将测试Vite的代理配置)
curl -s -X POST "http://localhost:3000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@hms.com","password":"password123"}' || echo "❌ 前端代理转发失败"

echo ""
echo "3. 直接测试后端API:"

# 直接测试后端API
curl -s -X POST "http://localhost:5000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@hms.com","password":"password123"}' || echo "❌ 后端API访问失败"