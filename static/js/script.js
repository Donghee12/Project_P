window.addEventListener("load", function() {
    // 페이지 로드가 끝난 후 2초 동안 로딩 화면 유지
    setTimeout(function() {
        const loader = document.getElementById('loader');
        const content = document.getElementById('content');
        
        // 로딩 화면 숨기기
        loader.style.display = 'none';
        
        // 콘텐츠 표시
        content.style.display = 'block';
    }, 2000); // 2000ms = 2초
});