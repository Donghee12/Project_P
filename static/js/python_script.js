//메인페이지
function goToMain() {
    window.location.href = "/"; // Flask 라우팅 URL로 이동
}


// Python 코드 생성 요청
function generatePythonCode(questionId) {
    const questionNumber = questionId.split('-')[1];  

    fetch('python_routes/generate_python_code', { // Flask 엔드포인트 호출
        method: 'POST',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        return response.json(); // JSON 응답 처리
    })
    .then(data => {
        if (data.code) {
            // 생성된 Python 코드를 표시
            document.getElementById(`generated-code-python-${questionNumber}`).innerText = data.code;
        } else {
            alert('Error generating Python code: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error generating Python code:', error);
        alert('An error occurred: ' + error.message);
    });
}


// Python 코드 실행 요청
function executePythonCode(questionId) {
    const questionNumber = questionId.split('-')[1];  
    const code = document.getElementById(`generated-code-python-${questionNumber}`).innerText;

    if (!code) {
        alert('Please generate Python code first.');
        return;
    }

    fetch('/python_routes/execute_python_code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: code }), // 서버로 코드 전송
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error executing Python code: ${response.statusText}`);
        }
        return response.json(); // JSON 응답 처리
    })
    .then(data => {
        const executionResultElement = document.getElementById(`execution-result-python-${questionNumber}`);
        executionResultElement.innerText = ''; // 기존 결과 초기화

        if (data.output) {
            // 정상 실행 결과 표시
            executionResultElement.innerText = `Execution Output:\n${data.output}`;
        } else if (data.original_output && data.fixed_code && data.fixed_output) {
            // 수정된 코드 실행 결과 표시
            executionResultElement.innerText =
                `Original Output:\n${data.original_output}\n\n` +
                `Fixed Code:\n${data.fixed_code}\n\n` +
                `Fixed Output:\n${data.fixed_output}`;
        } else {
            // 예외적인 응답 형식 처리
            alert('Unexpected response format from server.');
        }
    })
    .catch(error => {
        console.error('Error executing Python code:', error); // 디버깅용 콘솔 출력
        alert('Error executing Python code: ' + error.message);
    });
}



// Python 코드 해설 생성 요청
function generatePythonExplanation(questionId) {
    const questionNumber = questionId.split('-')[1];  
    const code = document.getElementById(`generated-code-python-${questionNumber}`).innerText;

    if (!code) {
        alert('Please generate Python code first.');
        return;
    }

    fetch('/python_routes/generate_python_explanation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: code }), // Python 코드 전달
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.explanation) {
            document.getElementById(`python-explanation-${questionNumber}`).innerText = data.explanation; // 해설 표시
        } else {
            alert('Error generating Python explanation: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error generating Python explanation:', error);
        alert('An error occurred: ' + error.message);
    });
}


let questionCount = 0;  // 문제 번호 추적

function addNewQuestion() {
    questionCount++;  // 문제 번호 증가

    const questionId = `question-${questionCount}`;
    const generatedCodeId = `generated-code-python-${questionCount}`;
    const executionResultId = `execution-result-python-${questionCount}`;
    const outputId = `python-explanation-${questionCount}`;

    const newQuestion = document.createElement('div');
    newQuestion.classList.add('question');
    
    // 생성되는 HTML 내에서 각 요소에 id를 올바르게 설정
    newQuestion.innerHTML = `
        <h1>문제 ${questionCount}</h2>
        <button class="action-btn" onclick="generatePythonCode('${questionId}')">Generate Python Code</button>
        <h2>Generated Java Code:</h2>
        <pre id="${generatedCodeId}" class="generated-code code-box"></pre>

        <button class="action-btn" onclick="executePythonCode('${questionId}')">Execute Code</button>
        <h2>Execution Result:</h2>
        <pre id="${executionResultId}" class="execution-result code-box"></pre>

        <button class="action-btn" onclick="generatePythonExplanation('${questionId}')">Generate Explanation</button>
        <h2>Explanation:</h2>
        <pre id="${outputId}" class="output code-box"></pre>
    `;

    const container = document.getElementById('questions-container');
    container.appendChild(newQuestion);


    // DOM에 추가된 후 함수 호출
    setTimeout(() => {
        console.log("New question added and ready to be interacted with.");
    }, 0);  // DOM이 렌더링된 후 다음 이벤트 루프에서 실행하도록 설정
}