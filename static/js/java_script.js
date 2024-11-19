
// 메인 페이지
function goToMain() {
    window.location.href = "/"; // Flask 라우팅 URL로 이동
}

// 문제 생성 요청
function generateCode(questionId) {
    const questionNumber = questionId.split('-')[1];  // question-1 -> 1 추출
    const generatedCodeElement = document.getElementById(`generated-code-${questionNumber}`);
    const executionResultElement = document.getElementById(`execution-result-${questionNumber}`);

    fetch('/generate_code', {
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
            if (generatedCodeElement && executionResultElement) {
                generatedCodeElement.innerText = data.code;
                executionResultElement.innerText = ''; // 이전 실행 결과 초기화
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
    const questionNumber = questionId.split('-')[1];  // question-1 -> 1 추출
    const generatedCodeElement = document.getElementById(`generated-code-${questionNumber}`);
    const executionResultElement = document.getElementById(`execution-result-${questionNumber}`);
    const fixedCodeElement = document.getElementById(`fixed-code-${questionNumber}`); // 동적으로 수정된 코드 영역

    const code = generatedCodeElement.innerText;

    if (!code) {
        alert('Please generate Java code first.');
        return;
    }

    fetch('/execute_code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: code })  // body에 code 객체를 JSON 형식으로 전달
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error executing code: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        // 서버 응답 데이터 처리
        if (!executionResultElement) {
            alert('Execution result element not found.');
            return;
        }

        // 정상 실행 결과 표시
        if (data.output) {
            executionResultElement.innerText = `Execution Output:\n${data.output}`;
        } else if (data.fixed_code && data.fixed_output) {
            // 수정된 코드와 실행 결과 처리
            executionResultElement.innerText = 
                `Original Output:\n${data.original_output || "N/A"}\n\n` +
                `Fixed Code:\n${data.fixed_code}\n\n` +
                `Fixed Output:\n${data.fixed_output}`;

            // 수정된 코드를 `fixedCodeElement`에 표시
            if (fixedCodeElement) {
                fixedCodeElement.value = data.fixed_code;
            }
        } else {
            // 서버에서 예상치 못한 응답 형식 반환 시 처리
            alert('Unexpected response format from server.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error executing code: ' + error.message);
    });
}


// 해설 생성 요청
function generateExplanation(questionId) {
    const questionNumber = questionId.split('-')[1];  
    const generatedCodeElement = document.getElementById(`generated-code-${questionNumber}`);
    const outputElement = document.getElementById(`output-${questionNumber}`);

    const code = generatedCodeElement.innerText;
    
    if (!code) {
        alert('Please generate Java code first.');
        return;
    }

    fetch('/generate_explanation', {
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
        if (outputElement) {
            outputElement.innerText = data.explanation || "No explanation found.";
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (outputElement) {
            outputElement.innerText = `Failed to load explanation. Error: ${error.message}`;
        }
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
