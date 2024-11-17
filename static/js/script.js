// 문제 생성 요청
function generateCode() {
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
            const codeElement = document.getElementById('generated-code');
            const resultElement = document.getElementById('execution-result');

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
function executeCode() {
    const code = document.getElementById('generated-code').innerText;
    
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
        // 서버에서 받은 output 확인
        if (data.output) {
            // output이 문자열인 경우 처리
            document.getElementById('execution-result').innerText = data.output;
        } else {
            // output이 문자열이 아닌 경우 처리
            alert('Unexpected response format');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error executing code: ' + error.message);
    });
}

// 해설 생성 요청
function generateExplanation() {
    const code = document.getElementById('generated-code').innerText;

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
        document.getElementById('output').innerHTML = data.explanation || "No explanation found.";
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('output').innerHTML = `해설을 불러오는 데 실패했습니다. 오류 발생: ${error.message}`;
    });
}

