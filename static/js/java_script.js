// 메인 페이지
function goToMain() {
    window.location.href = "/"; // Flask 라우팅 URL로 이동
}

// 문제 생성 요청
function generateCode(questionId) {
    const questionNumber = questionId.split('-')[1];  

    fetch('/java_routes/generate_code', {
        method: 'POST',
    })
    .then(response => {
        console.log("Response status:", response.status); // 디버깅용 상태 코드 확인
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log("Server response:", data); // 디버깅용 응답 데이터 확인

        // 생성된 코드 처리
        if (data.code) {
            const codeElement = document.getElementById(`generated-code-${questionNumber}`);
            const resultElement = document.getElementById(`execution-result-${questionNumber}`);

            if (codeElement && resultElement) {
                codeElement.innerText = data.code;
                resultElement.innerText = ''; // 이전 실행 결과 초기화
            } else {
                console.error("HTML elements for 'generated-code' or 'execution-result' not found.");
                alert("Error: Required HTML elements are missing.");
            }
        } else {
            alert('Error generating code: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error in generateCode:', error); // 디버깅용 오류 메시지 출력
        alert('An error occurred while generating the code: ' + error.message);
    });
}

// 코드 실행 요청
function executeCode(questionId) {
    const questionNumber = questionId.split('-')[1];  

    const code = document.getElementById(`generated-code-${questionNumber}`).innerText;

    if (!code) {
        alert('Please generate Java code first.');
        return;
    }

    fetch('/java_routes/execute_code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: code }), // 서버로 코드 전송
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error executing code: ${response.statusText}`);
        }
        return response.json(); // JSON 응답 처리
    })
    .then(data => {
        const executionResultElement = document.getElementById(`execution-result-${questionNumber}`);
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
        console.error('Error:', error); // 디버깅용 콘솔 출력
        alert('Error executing code: ' + error.message);
    });
}




// 해설 생성 요청
function generateExplanation(questionId) {
    const questionNumber = questionId.split('-')[1];  

    const code = document.getElementById(`generated-code-${questionNumber}`).innerText;

    if (!code) {
        alert('Please generate Java code first.');
        return;
    }

    fetch('/java_routes/generate_explanation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: code })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        return response.json();  // 서버 응답을 JSON으로 변환
    })
    .then(data => {
        if (data.error) {
            alert(`Error: ${data.error}`);
            return;
        }

        console.log("Explanation:", data.explanation);
        document.getElementById(`output-${questionNumber}`).innerText = data.explanation || "No explanation found.";
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById(`output-${questionNumber}`).innerText = `Failed to load explanation. Error: ${error.message}`;
    });
}


let questionCount = 0;  // 문제 번호 추적

function addNewQuestion() {
    questionCount++;  // 문제 번호 증가

    const questionId = `question-${questionCount}`;
    const generatedCodeId = `generated-code-${questionCount}`;
    const executionResultId = `execution-result-${questionCount}`;
    const outputId = `output-${questionCount}`;

    const newQuestion = document.createElement('div');
    newQuestion.classList.add('question');
    
    // 생성되는 HTML 내에서 각 요소에 id를 올바르게 설정
    newQuestion.innerHTML = `
        <h1>문제 ${questionCount}</h2>
        <button class="action-btn" onclick="generateCode('${questionId}')">Generate Java Code</button>
        <h2>Generated Java Code:</h2>
        <pre id="${generatedCodeId}" class="generated-code code-box"></pre>

        <button class="action-btn" onclick="executeCode('${questionId}')">Execute Code</button>
        <h2>Execution Result:</h2>
        <pre id="${executionResultId}" class="execution-result code-box"></pre>

        <button class="action-btn" onclick="generateExplanation('${questionId}')">Generate Explanation</button>
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