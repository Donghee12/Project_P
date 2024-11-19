window.addEventListener("load", function() {
    // 페이지 로드가 끝난 후 2초 동안 로딩 화면 유지
    setTimeout(function() {
        const loader = document.getElementById('loader');
        const content = document.getElementById('content');
        
        // 로딩 화면 숨기기
        loader.classList.add('hidden');
        // 콘텐츠 표시
        content.style.display = 'block';
    }, 2000); // 2000ms = 2초
});

// Intersection Observer를 이용한 스크롤 감지
document.addEventListener("DOMContentLoaded", function () {
    const elements = document.querySelectorAll('.scroll-fade'); // 'scroll-fade' 클래스를 가진 모든 요소들

    const observerOptions = {
        root: null, // 기본값, viewport를 root로 사용
        rootMargin: '0px', // viewport의 마진을 설정
        threshold: 0.1 // 10% 이상 보일 때 트리거
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // 한 번만 적용되도록
            }
        });
    }, observerOptions);

    elements.forEach(element => {
        observer.observe(element);
    });
});
