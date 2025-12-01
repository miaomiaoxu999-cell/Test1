// 页面加载动画
window.addEventListener('load', () => {
    document.body.classList.add('page-transition');
});

// 平滑滚动
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80, // 考虑导航栏高度
                behavior: 'smooth'
            });
        }
    });
});

// 高亮当前页面的导航链接
function highlightActiveNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav a');
    
    navLinks.forEach(link => {
        // 获取链接的路径部分
        const linkPath = new URL(link.href).pathname;
        
        // 比较路径，高亮当前页面
        if (currentPath.endsWith(linkPath) || (currentPath === '/' && linkPath === '/forecast_index.html')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// 数据输入页面功能
function initDataInputPage() {
    // 文件上传功能
    const fileUploadArea = document.getElementById('fileUploadArea');
    const fileInput = document.getElementById('fileInput');
    
    if (fileUploadArea && fileInput) {
        // 点击上传区域触发文件选择
        fileUploadArea.addEventListener('click', () => {
            fileInput.click();
        });
        
        // 拖拽文件功能
        fileUploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileUploadArea.classList.add('dragover');
        });
        
        fileUploadArea.addEventListener('dragleave', () => {
            fileUploadArea.classList.remove('dragover');
        });
        
        fileUploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            fileUploadArea.classList.remove('dragover');
            
            if (e.dataTransfer.files.length > 0) {
                fileInput.files = e.dataTransfer.files;
                handleFileUpload(fileInput.files[0]);
            }
        });
        
        // 文件选择变化事件
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileUpload(e.target.files[0]);
            }
        });
    }
    
    // 表单提交功能
    const dataForm = document.getElementById('dataForm');
    if (dataForm) {
        dataForm.addEventListener('submit', (e) => {
            e.preventDefault();
            handleFormSubmit();
        });
    }
    
    // 添加数据行功能
    const addRowBtn = document.getElementById('addRowBtn');
    const dataTable = document.getElementById('dataTable');
    
    if (addRowBtn && dataTable) {
        addRowBtn.addEventListener('click', () => {
            addDataRow(dataTable);
        });
    }
}

// 处理文件上传
function handleFileUpload(file) {
    const fileNameDisplay = document.getElementById('fileNameDisplay');
    if (fileNameDisplay) {
        fileNameDisplay.textContent = `已选择文件：${file.name}`;
    }
    
    // 这里可以添加文件解析逻辑
    console.log('文件上传:', file);
}

// 处理表单提交
function handleFormSubmit() {
    // 显示加载状态
    showLoading();
    
    // 模拟数据处理延迟
    setTimeout(() => {
        // 隐藏加载状态
        hideLoading();
        
        // 显示成功消息
        showMessage('数据提交成功！正在进行预测计算...', 'success');
        
        // 模拟预测计算延迟后跳转到结果页面
        setTimeout(() => {
            window.location.href = 'forecast_result.html';
        }, 1500);
    }, 2000);
}

// 添加数据行
function addDataRow(table) {
    const tbody = table.querySelector('tbody');
    const newRow = tbody.insertRow();
    
    // 创建单元格
    const cells = [
        { type: 'date', name: 'date[]' },
        { type: 'number', name: 'sales[]', placeholder: '0' },
        { type: 'number', name: 'temperature[]', placeholder: '0' },
        { type: 'number', name: 'rainfall[]', placeholder: '0' },
        { type: 'number', name: 'traffic[]', placeholder: '0' },
        { type: 'select', name: 'holiday[]', options: ['否', '是'] },
        { type: 'button', text: '删除', className: 'btn btn-danger btn-sm delete-row' }
    ];
    
    cells.forEach((cellConfig, index) => {
        const cell = newRow.insertCell();
        
        if (cellConfig.type === 'button') {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = cellConfig.className;
            button.textContent = cellConfig.text;
            button.addEventListener('click', () => {
                newRow.remove();
            });
            cell.appendChild(button);
        } else if (cellConfig.type === 'select') {
            const select = document.createElement('select');
            select.className = 'form-select';
            select.name = cellConfig.name;
            
            cellConfig.options.forEach(optionText => {
                const option = document.createElement('option');
                option.value = optionText;
                option.textContent = optionText;
                select.appendChild(option);
            });
            
            cell.appendChild(select);
        } else {
            const input = document.createElement('input');
            input.type = cellConfig.type;
            input.className = 'form-control';
            input.name = cellConfig.name;
            if (cellConfig.placeholder) {
                input.placeholder = cellConfig.placeholder;
            }
            if (cellConfig.type === 'number') {
                input.step = '0.1';
            }
            cell.appendChild(input);
        }
    });
}

// 预测结果页面功能
function initResultsPage() {
    // 初始化图表
    initCharts();
    
    // 导出结果功能
    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', exportResults);
    }
    
    // 重新预测功能
    const rePredictBtn = document.getElementById('rePredictBtn');
    if (rePredictBtn) {
        rePredictBtn.addEventListener('click', () => {
            window.location.href = 'forecast_input.html';
        });
    }
}

// 初始化图表
function initCharts() {
    // 检查Chart.js是否加载
    if (typeof Chart !== 'undefined') {
        // 示例：创建销量趋势图
        const salesTrendCtx = document.getElementById('salesTrendChart');
        if (salesTrendCtx) {
            new Chart(salesTrendCtx, {
                type: 'line',
                data: {
                    labels: ['1日', '2日', '3日', '4日', '5日', '6日', '7日', '8日', '9日', '10日', '11日', '12日', '13日', '14日', '15日', '16日', '17日', '18日', '19日', '20日', '21日', '22日', '23日', '24日', '25日', '26日', '27日', '28日', '29日', '30日'],
                    datasets: [
                        {
                            label: '历史销量',
                            data: [1200, 1900, 3000, 5000, 2000, 3000, 4000, 3500, 4200, 3800, 4500, 5200, 4800, 5500, 6000, 5800, 6200, 6500, 6300, 6800, 7000, 7200, 7500, 7300, 7800, 8000, 8200, 8500, 8300, 8800],
                            borderColor: 'rgba(54, 162, 235, 1)',
                            backgroundColor: 'rgba(54, 162, 235, 0.2)',
                            tension: 0.1,
                            fill: false
                        },
                        {
                            label: '预测销量',
                            data: [9000, 9200, 8900, 9500, 9300, 9800, 10000, 9700, 10200, 10500, 10300, 10800, 11000, 10700, 11200, 11500, 11300, 11800, 12000, 11700, 12200, 12500, 12300, 12800, 13000, 12700, 13200, 13500, 13300, 13800],
                            borderColor: 'rgba(75, 192, 192, 1)',
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            tension: 0.1,
                            fill: false,
                            borderDash: [5, 5]
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: '未来一个月销量趋势预测'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: '销量（升）'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: '日期'
                            }
                        }
                    }
                }
            });
        }
        
        // 示例：创建概率分布直方图
        const probabilityCtx = document.getElementById('probabilityChart');
        if (probabilityCtx) {
            new Chart(probabilityCtx, {
                type: 'bar',
                data: {
                    labels: ['8000-8500', '8500-9000', '9000-9500', '9500-10000', '10000-10500', '10500-11000', '11000-11500', '11500-12000', '12000-12500', '12500-13000', '13000-13500', '13500-14000'],
                    datasets: [{
                        label: '概率密度',
                        data: [0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.2, 0.15, 0.1, 0.05, 0.03, 0.02],
                        backgroundColor: 'rgba(153, 102, 255, 0.6)',
                        borderColor: 'rgba(153, 102, 255, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: '预测销量概率分布'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: '概率密度'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: '销量区间（升）'
                            }
                        }
                    }
                }
            });
        }
        
        // 示例：创建影响因素雷达图
        const factorsCtx = document.getElementById('factorsChart');
        if (factorsCtx) {
            new Chart(factorsCtx, {
                type: 'radar',
                data: {
                    labels: ['温度', '降雨量', '交通流量', '节假日', '油价', '促销活动'],
                    datasets: [{
                        label: '影响程度',
                        data: [8, 6, 9, 7, 5, 8],
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: '销量影响因素分析'
                        }
                    },
                    scales: {
                        r: {
                            beginAtZero: true,
                            max: 10,
                            ticks: {
                                stepSize: 2
                            }
                        }
                    }
                }
            });
        }
    }
}

// 导出结果
function exportResults() {
    // 这里可以添加结果导出逻辑
    showMessage('结果导出功能开发中...', 'info');
}

// 历史记录页面功能
function initHistoryPage() {
    // 加载历史记录
    loadHistoryRecords();
    
    // 删除记录功能
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('delete-record')) {
            const recordId = e.target.dataset.id;
            deleteHistoryRecord(recordId);
        }
    });
    
    // 查看详情功能
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('view-record')) {
            const recordId = e.target.dataset.id;
            viewHistoryRecord(recordId);
        }
    });
}

// 加载历史记录
function loadHistoryRecords() {
    // 从本地存储加载历史记录
    const historyRecords = JSON.parse(localStorage.getItem('forecastHistory') || '[]');
    const historyContainer = document.getElementById('historyContainer');
    
    if (historyContainer) {
        if (historyRecords.length === 0) {
            historyContainer.innerHTML = '<p class="text-center text-muted py-4">暂无历史记录</p>';
        } else {
            historyContainer.innerHTML = historyRecords.map(record => `
                <div class="history-card">
                    <div class="history-header">
                        <span class="history-date">${record.date}</span>
                        <div class="history-actions">
                            <button class="btn btn-sm btn-primary view-record" data-id="${record.id}">
                                <i class="fas fa-eye"></i> 查看
                            </button>
                            <button class="btn btn-sm btn-danger delete-record" data-id="${record.id}">
                                <i class="fas fa-trash"></i> 删除
                            </button>
                        </div>
                    </div>
                    <div class="history-content">
                        <p><strong>加油站名称：</strong>${record.stationName}</p>
                        <p><strong>预测日期范围：</strong>${record.forecastRange}</p>
                        <p><strong>平均预测销量：</strong>${record.avgSales.toFixed(2)} 升</p>
                        <p><strong>模型类型：</strong>${record.modelType}</p>
                    </div>
                </div>
            `).join('');
        }
    }
}

// 删除历史记录
function deleteHistoryRecord(recordId) {
    if (confirm('确定要删除这条历史记录吗？')) {
        // 从本地存储加载历史记录
        let historyRecords = JSON.parse(localStorage.getItem('forecastHistory') || '[]');
        
        // 过滤掉要删除的记录
        historyRecords = historyRecords.filter(record => record.id !== recordId);
        
        // 保存回本地存储
        localStorage.setItem('forecastHistory', JSON.stringify(historyRecords));
        
        // 重新加载历史记录
        loadHistoryRecords();
        
        // 显示成功消息
        showMessage('历史记录删除成功！', 'success');
    }
}

// 查看历史记录详情
function viewHistoryRecord(recordId) {
    // 这里可以添加查看详情逻辑
    showMessage('查看详情功能开发中...', 'info');
}

// 设置页面功能
function initSettingsPage() {
    // 加载设置
    loadSettings();
    
    // 保存设置功能
    const settingsForm = document.getElementById('settingsForm');
    if (settingsForm) {
        settingsForm.addEventListener('submit', (e) => {
            e.preventDefault();
            saveSettings();
        });
    }
}

// 加载设置
function loadSettings() {
    // 从本地存储加载设置
    const settings = JSON.parse(localStorage.getItem('forecastSettings') || JSON.stringify({
        defaultModel: 'arima',
        confidenceLevel: 0.95,
        showConfidenceInterval: true,
        emailNotifications: false
    }));
    
    // 设置表单值
    document.getElementById('defaultModel').value = settings.defaultModel;
    document.getElementById('confidenceLevel').value = settings.confidenceLevel;
    document.getElementById('showConfidenceInterval').checked = settings.showConfidenceInterval;
    document.getElementById('emailNotifications').checked = settings.emailNotifications;
}

// 保存设置
function saveSettings() {
    // 获取表单值
    const settings = {
        defaultModel: document.getElementById('defaultModel').value,
        confidenceLevel: parseFloat(document.getElementById('confidenceLevel').value),
        showConfidenceInterval: document.getElementById('showConfidenceInterval').checked,
        emailNotifications: document.getElementById('emailNotifications').checked
    };
    
    // 保存到本地存储
    localStorage.setItem('forecastSettings', JSON.stringify(settings));
    
    // 显示成功消息
    showMessage('设置保存成功！', 'success');
}

// 工具函数：显示加载状态
function showLoading() {
    const loadingElement = document.createElement('div');
    loadingElement.className = 'loading-overlay';
    loadingElement.innerHTML = `
        <div class="loading-content">
            <div class="loading-spinner"></div>
            <p class="mt-3">正在处理数据...</p>
        </div>
    `;
    loadingElement.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(255, 255, 255, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    `;
    
    document.body.appendChild(loadingElement);
}

// 工具函数：隐藏加载状态
function hideLoading() {
    const loadingElement = document.querySelector('.loading-overlay');
    if (loadingElement) {
        loadingElement.remove();
    }
}

// 工具函数：显示消息
function showMessage(message, type = 'info') {
    // 创建消息元素
    const messageElement = document.createElement('div');
    messageElement.className = `alert alert-${type}`;
    messageElement.textContent = message;
    messageElement.style.cssText = `
        position: fixed;
        top: 90px;
        right: 20px;
        z-index: 9998;
        min-width: 300px;
        animation: slideInRight 0.3s ease;
    `;
    
    // 添加动画样式
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(messageElement);
    
    // 3秒后移除消息
    setTimeout(() => {
        messageElement.style.animation = 'slideInRight 0.3s ease reverse';
        setTimeout(() => {
            messageElement.remove();
        }, 300);
    }, 3000);
}

// 保存预测结果到历史记录
function saveToHistory(forecastData) {
    // 从本地存储加载历史记录
    const historyRecords = JSON.parse(localStorage.getItem('forecastHistory') || '[]');
    
    // 创建新记录
    const newRecord = {
        id: Date.now().toString(),
        date: new Date().toLocaleDateString(),
        stationName: forecastData.stationName || '未知加油站',
        forecastRange: `${forecastData.startDate} 至 ${forecastData.endDate}`,
        avgSales: forecastData.avgSales || 0,
        modelType: forecastData.modelType || '未知模型',
        data: forecastData
    };
    
    // 添加到历史记录
    historyRecords.unshift(newRecord);
    
    // 限制历史记录数量（最多保存20条）
    if (historyRecords.length > 20) {
        historyRecords.pop();
    }
    
    // 保存回本地存储
    localStorage.setItem('forecastHistory', JSON.stringify(historyRecords));
}

// 页面初始化
function initPage() {
    // 高亮当前导航链接
    highlightActiveNavLink();
    
    // 根据当前页面初始化相应功能
    const currentPath = window.location.pathname;
    
    if (currentPath.includes('forecast_input.html')) {
        initDataInputPage();
    } else if (currentPath.includes('forecast_result.html')) {
        initResultsPage();
    } else if (currentPath.includes('forecast_history.html')) {
        initHistoryPage();
    } else if (currentPath.includes('forecast_settings.html')) {
        initSettingsPage();
    }
}

// 页面加载完成后初始化
window.addEventListener('DOMContentLoaded', initPage);
