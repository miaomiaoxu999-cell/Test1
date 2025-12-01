// 第0天选择题答案检查
function checkAnswers() {
    // 正确答案
    const correctAnswers = {
        q1: 'B',
        q2: 'C',
        q3: 'D'
    };
    
    let allCorrect = true;
    
    // 检查每个问题
    for (const [question, correctAnswer] of Object.entries(correctAnswers)) {
        const selectedOption = document.querySelector(`input[name="${question}"]:checked`);
        const feedback = document.getElementById(`feedback-${question}`);
        
        if (selectedOption) {
            if (selectedOption.value === correctAnswer) {
                feedback.textContent = '✅ 回答正确！';
                feedback.style.color = '#4CAF50';
                selectedOption.parentElement.style.backgroundColor = '#e8f5e9';
            } else {
                feedback.textContent = `❌ 回答错误。正确答案是 ${correctAnswer}。`;
                feedback.style.color = '#f44336';
                selectedOption.parentElement.style.backgroundColor = '#ffebee';
                allCorrect = false;
            }
        } else {
            feedback.textContent = '⚠️ 请选择一个答案。';
            feedback.style.color = '#ff9800';
            allCorrect = false;
        }
    }
    
    // 如果所有答案都正确，显示完成消息
    if (allCorrect) {
        showSuccessMessage('太棒了！选择题全部答对！');
    }
}

// 重置选择题
function resetQuiz() {
    const questions = ['q1', 'q2', 'q3'];
    
    questions.forEach(question => {
        const options = document.querySelectorAll(`input[name="${question}"]`);
        const feedback = document.getElementById(`feedback-${question}`);
        
        options.forEach(option => {
            option.checked = false;
            option.parentElement.style.backgroundColor = '';
        });
        
        feedback.textContent = '';
    });
}

// 第0天填空题答案检查
function checkFillBlanks() {
    // 正确答案（允许部分相似答案）
    const correctAnswers = {
        q4: ['早上', '上午', '早晨'],
        q5: ['46', '四十六']
    };
    
    let allCorrect = true;
    
    // 检查每个问题
    for (const [question, correctAnswersList] of Object.entries(correctAnswers)) {
        const userAnswer = document.getElementById(question).value.trim();
        const feedback = document.getElementById(`feedback-${question}`);
        
        if (userAnswer === '') {
            feedback.textContent = '⚠️ 请输入答案。';
            feedback.style.color = '#ff9800';
            allCorrect = false;
        } else {
            const isCorrect = correctAnswersList.some(answer => 
                userAnswer.includes(answer) || answer.includes(userAnswer)
            );
            
            if (isCorrect) {
                feedback.textContent = '✅ 回答正确！';
                feedback.style.color = '#4CAF50';
                document.getElementById(question).style.borderColor = '#4CAF50';
                document.getElementById(question).style.backgroundColor = '#e8f5e9';
            } else {
                feedback.textContent = `❌ 回答错误。正确答案包括：${correctAnswersList.join('、')}。`;
                feedback.style.color = '#f44336';
                document.getElementById(question).style.borderColor = '#f44336';
                document.getElementById(question).style.backgroundColor = '#ffebee';
                allCorrect = false;
            }
        }
    }
    
    // 如果所有答案都正确，显示完成消息
    if (allCorrect) {
        showSuccessMessage('太棒了！填空题全部答对！');
    }
}

// 重置填空题
function resetFillBlanks() {
    const questions = ['q4', 'q5'];
    
    questions.forEach(question => {
        const input = document.getElementById(question);
        const feedback = document.getElementById(`feedback-${question}`);
        
        input.value = '';
        input.style.borderColor = '';
        input.style.backgroundColor = '';
        feedback.textContent = '';
    });
}

// 第0天翻译题答案检查
function checkTranslations() {
    // 正确答案（允许不同的正确翻译）
    const correctAnswers = {
        q6: ['お元気ですか', 'おげんきですか', '元気ですか', 'げんきですか'],
        q7: ['おやすみなさい', 'おやすみ', 'やすみなさい']
    };
    
    let allCorrect = true;
    
    // 检查每个问题
    for (const [question, correctAnswersList] of Object.entries(correctAnswers)) {
        const userAnswer = document.getElementById(question).value.trim();
        const feedback = document.getElementById(`feedback-${question}`);
        
        if (userAnswer === '') {
            feedback.textContent = '⚠️ 请输入答案。';
            feedback.style.color = '#ff9800';
            allCorrect = false;
        } else {
            // 忽略大小写和空格进行比较
            const normalizedUserAnswer = userAnswer.toLowerCase().replace(/\s/g, '');
            const isCorrect = correctAnswersList.some(answer => 
                normalizedUserAnswer === answer.toLowerCase()
            );
            
            if (isCorrect) {
                feedback.textContent = '✅ 翻译正确！';
                feedback.style.color = '#4CAF50';
                document.getElementById(question).style.borderColor = '#4CAF50';
                document.getElementById(question).style.backgroundColor = '#e8f5e9';
            } else {
                feedback.textContent = `❌ 翻译错误。正确翻译包括：${correctAnswersList.join('、')}。`;
                feedback.style.color = '#f44336';
                document.getElementById(question).style.borderColor = '#f44336';
                document.getElementById(question).style.backgroundColor = '#ffebee';
                allCorrect = false;
            }
        }
    }
    
    // 如果所有答案都正确，显示完成消息
    if (allCorrect) {
        showSuccessMessage('太棒了！翻译题全部答对！');
    }
}

// 重置翻译题
function resetTranslations() {
    const questions = ['q6', 'q7'];
    
    questions.forEach(question => {
        const input = document.getElementById(question);
        const feedback = document.getElementById(`feedback-${question}`);
        
        input.value = '';
        input.style.borderColor = '';
        input.style.backgroundColor = '';
        feedback.textContent = '';
    });
}

// 第0天判断题答案检查
function checkTrueFalse() {
    // 正确答案
    const correctAnswers = {
        q8: 'true',
        q9: 'true'
    };
    
    let allCorrect = true;
    
    // 检查每个问题
    for (const [question, correctAnswer] of Object.entries(correctAnswers)) {
        const selectedOption = document.querySelector(`input[name="${question}"]:checked`);
        const feedback = document.getElementById(`feedback-${question}`);
        
        if (selectedOption) {
            if (selectedOption.value === correctAnswer) {
                feedback.textContent = '✅ 回答正确！';
                feedback.style.color = '#4CAF50';
                selectedOption.parentElement.style.backgroundColor = '#e8f5e9';
            } else {
                const correctText = correctAnswer === 'true' ? '正确' : '错误';
                feedback.textContent = `❌ 回答错误。正确答案是 ${correctText}。`;
                feedback.style.color = '#f44336';
                selectedOption.parentElement.style.backgroundColor = '#ffebee';
                allCorrect = false;
            }
        } else {
            feedback.textContent = '⚠️ 请选择一个答案。';
            feedback.style.color = '#ff9800';
            allCorrect = false;
        }
    }
    
    // 如果所有答案都正确，显示完成消息
    if (allCorrect) {
        showSuccessMessage('太棒了！判断题全部答对！');
    }
}

// 重置判断题
function resetTrueFalse() {
    const questions = ['q8', 'q9'];
    
    questions.forEach(question => {
        const options = document.querySelectorAll(`input[name="${question}"]`);
        const feedback = document.getElementById(`feedback-${question}`);
        
        options.forEach(option => {
            option.checked = false;
            option.parentElement.style.backgroundColor = '';
        });
        
        feedback.textContent = '';
    });
}

// 第1天练习题答案检查
function checkDay1Answers() {
    // 正确答案（允许不同的正确表达方式）
    const correctAnswers = {
        'day1-q1': ['私は旅行者です', 'わたしはりょこうしゃです', '旅行者です'],
        'day1-q2': ['私は日本に五日間滞在します', 'わたしはにほんにごにちかんたいざいします', '日本に五日間滞在します']
    };
    
    let allCorrect = true;
    
    // 检查每个问题
    for (const [question, correctAnswersList] of Object.entries(correctAnswers)) {
        const userAnswer = document.getElementById(question).value.trim();
        const feedback = document.getElementById(`${question.replace('q', 'feedback-q')}`);
        
        if (userAnswer === '') {
            feedback.textContent = '⚠️ 请输入答案。';
            feedback.style.color = '#ff9800';
            allCorrect = false;
        } else {
            // 忽略大小写和空格进行比较
            const normalizedUserAnswer = userAnswer.toLowerCase().replace(/\s/g, '');
            const isCorrect = correctAnswersList.some(answer => 
                normalizedUserAnswer === answer.toLowerCase()
            );
            
            if (isCorrect) {
                feedback.textContent = '✅ 翻译正确！';
                feedback.style.color = '#4CAF50';
                document.getElementById(question).style.borderColor = '#4CAF50';
                document.getElementById(question).style.backgroundColor = '#e8f5e9';
            } else {
                feedback.textContent = `❌ 翻译错误。可以参考答案：${correctAnswersList[0]}。`;
                feedback.style.color = '#f44336';
                document.getElementById(question).style.borderColor = '#f44336';
                document.getElementById(question).style.backgroundColor = '#ffebee';
                allCorrect = false;
            }
        }
    }
    
    // 如果所有答案都正确，显示完成消息
    if (allCorrect) {
        showSuccessMessage('太棒了！练习题全部答对！');
        // 自动标记为完成
        completeLesson(1);
    }
}

// 重置第1天练习题
function resetDay1Quiz() {
    const questions = ['day1-q1', 'day1-q2'];
    
    questions.forEach(question => {
        const input = document.getElementById(question);
        const feedback = document.getElementById(`${question.replace('q', 'feedback-q')}`);
        
        input.value = '';
        input.style.borderColor = '';
        input.style.backgroundColor = '';
        feedback.textContent = '';
    });
}

// 显示成功消息
function showSuccessMessage(message) {
    // 检查是否已经有消息存在
    let existingMessage = document.querySelector('.success-message');
    if (existingMessage) {
        document.body.removeChild(existingMessage);
    }
    
    // 创建一个消息元素
    const messageElement = document.createElement('div');
    messageElement.className = 'success-message';
    messageElement.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
    messageElement.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: #4CAF50;
        color: white;
        padding: 20px 30px;
        border-radius: 10px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        z-index: 2000;
        font-size: 1.2rem;
        font-weight: bold;
        text-align: center;
        animation: fadeIn 0.3s ease;
    `;
    
    // 添加动画样式
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
            to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(messageElement);
    
    // 3秒后移除消息
    setTimeout(() => {
        messageElement.style.opacity = '0';
        messageElement.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        messageElement.style.transform = 'translate(-50%, -50%) scale(0.8)';
        setTimeout(() => {
            if (document.body.contains(messageElement)) {
                document.body.removeChild(messageElement);
            }
        }, 300);
    }, 3000);
}

// 自动显示答案部分（当用户完成所有测验后）
function showAnswerSection() {
    const answerSection = document.getElementById('answer-section');
    if (answerSection) {
        answerSection.style.display = 'block';
    }
}

// 页面加载时初始化
window.addEventListener('DOMContentLoaded', () => {
    // 检查是否是课程页面，如果是，根据URL显示正确的答案部分
    if (window.location.pathname.includes('day_0.html')) {
        const answerSection = document.getElementById('answer-section');
        if (answerSection) {
            // 默认隐藏，用户完成测验后显示
            answerSection.style.display = 'block';
        }
    }
});