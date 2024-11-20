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
    const code = document.getElementById('generated-code-python').innerText;

    if (!code) {
        alert('Please generate Python code first.');
        return;
    }

    fetch('/execute_python_code', { // Flask 엔드포인트 호출
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: code }), // Python 코드를 JSON으로 전달
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.output) {
            // 실행 결과 표시
            document.getElementById('execution-result-python').innerText =
                `Output:\n${data.output}\n\nCPU Time: ${data.cpu_time || 'N/A'}\nMemory: ${data.memory || 'N/A'}`;
        } else if (data.fixed_code && data.fixed_output) {
            // 수정된 코드 및 결과 표시
            document.getElementById('execution-result-python').innerText =
                `Original Output:\n${data.original_output}\n\n` +
                `Fixed Code:\n${data.fixed_code}\n\n` +
                `Fixed Output:\n${data.fixed_output}\n\n` +
                `CPU Time: ${data.cpu_time || 'N/A'}\nMemory: ${data.memory || 'N/A'}`;
        } else {
            alert('Unexpected response format');
        }
    })
    .catch(error => {
        console.error('Error executing Python code:', error);
        alert('An error occurred: ' + error.message);
    });
}


// 수정된 Python 코드 실행 요청
function executeFixedPythonCode() {
    const fixedCode = document.getElementById('fixed-code-python').value; // 수정된 코드 입력 받기

    if (!fixedCode) {
        alert('Please provide fixed Python code.');
        return;
    }

    fetch('/execute_fixed_python_code', { // Flask 엔드포인트 호출
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ fixed_code: fixedCode }), // 수정된 코드 전달
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.output) {
            // 실행 결과 표시
            document.getElementById('execution-result-python').innerText = 
                `Output:\n${data.output}\n\nCPU Time: ${data.cpu_time || 'N/A'}\nMemory: ${data.memory || 'N/A'}`;
        } else {
            alert('Error executing fixed Python code: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error executing fixed Python code:', error);
        alert('An error occurred: ' + error.message);
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
