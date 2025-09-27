# 测试文件说明

本文件夹包含用于调试和验证系统功能的测试文件。

## 文件说明

### `test_login.json`
- **用途**: 包含测试用的登录凭据
- **内容**: 管理员用户的邮箱和密码
- **使用方法**: 可与curl命令配合使用测试登录API

### `test_frontend_login.js`
- **用途**: 前端登录功能测试脚本
- **使用方法**: 在浏览器控制台中运行，测试前端登录API
- **功能**: 自动发送登录请求并显示结果

### `test_proxy.sh`
- **用途**: 测试Docker容器间的网络连接和代理配置
- **功能**: 
  - 测试前端容器是否能访问后端健康检查
  - 测试前端代理是否正常转发API请求
  - 测试后端API直接访问
- **使用方法**: 在项目根目录运行 `bash test/test_proxy.sh`

## 使用示例

### 测试登录API
```bash
# 使用test_login.json测试登录
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d @test/test_login.json
```

### 运行网络连接测试
```bash
# 执行代理测试脚本
bash test/test_proxy.sh
```

### 在浏览器中测试前端登录
1. 打开浏览器访问 http://localhost:3000
2. 打开开发者工具控制台
3. 复制并运行 `test_frontend_login.js` 中的代码

## 注意事项

- 这些文件包含测试用的登录凭据，请确保不要在生产环境中使用
- 测试脚本假设服务运行在默认端口（前端3000，后端5000）
- 运行测试前请确保所有Docker容器都已启动