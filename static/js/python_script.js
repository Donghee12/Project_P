//메인페이지
function goToMain() {
    window.location.href = "/"; // Flask 라우팅 URL로 이동
}


// Python 코드 생성 요청
function generatePythonCode() {
    fetch('/generate_python_code', { // Flask 엔드포인트 호출
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
            document.getElementById('generated-code-python').innerText = data.code;
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
function executePythonCode() {
    const code = document.getElementById('generated-code').innerText;

    if (!code) {
        alert('Please generate Python code first.');
        return;
    }

    fetch('/execute_python_code', {
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
        const executionResultElement = document.getElementById('execution-result');
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
function generatePythonExplanation() {
    const code = document.getElementById('generated-code-python').innerText;

    if (!code) {
        alert('Please generate Python code first.');
        return;
    }

    fetch('/generate_python_explanation', {
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
            document.getElementById('python-explanation').innerText = data.explanation; // 해설 표시
        } else {
            alert('Error generating Python explanation: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error generating Python explanation:', error);
        alert('An error occurred: ' + error.message);
    });
}
