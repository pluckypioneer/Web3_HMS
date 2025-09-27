// 测试前端登录的脚本 - 可在浏览器控制台运行

// 测试API请求
async function testLogin() {
    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: 'admin@hms.com',
                password: 'password123'
            })
        });
        
        const data = await response.json();
        console.log('登录测试结果:', data);
        
        if (response.ok) {
            console.log('✅ 登录成功!');
            console.log('Token:', data.token);
            console.log('用户信息:', data.user);
        } else {
            console.log('❌ 登录失败:', data.message);
        }
    } catch (error) {
        console.error('❌ 网络错误:', error);
    }
}

// 运行测试
testLogin();