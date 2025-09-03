# 스터디 내용 정리

> 이 파일은 GitHub Actions로 자동 생성/갱신됩니다. 직접 수정하지 마세요.

## 🔍 검색

<input id="q" placeholder="검색어 입력..." style="width:100%;padding:8px;margin:10px 0;font-size:16px;" />
<ul id="results"></ul>

<script src="https://cdn.jsdelivr.net/npm/lunr/lunr.min.js"></script>
<script>
(async function() {
  // search_index.json 은 액션에서 미리 생성해둔다 (docs/search_index.json)
  const res = await fetch('./search_index.json');
  const data = await res.json();

  // lunr 인덱스 구성
  const idx = lunr(function () {
    this.ref('url');
    this.field('title');
    this.field('content');
    data.forEach(doc => this.add(doc));
  });

  const $q = document.getElementById('q');
  const $out = document.getElementById('results');

  function render(hits) {
    if (!hits.length) {
      $out.innerHTML = '<li>검색 결과 없음</li>';
      return;
    }
    $out.innerHTML = hits.map(hit => {
      const doc = data.find(d => d.url === hit.ref);
      return `<li><a href="${doc.url}">${doc.title}</a></li>`;
    }).join('');
  }

  $q.addEventListener('input', e => {
    const q = e.target.value.trim();
    if (!q) { $out.innerHTML = ''; return; }
    const hits = idx.search(q + '*'); // 접두 일치 검색
    render(hits);
  });
})();
</script>

## 네트워크

- [OSI 7 계층](%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC/osi%207%EA%B3%84%EC%B8%B5)
- [TCP(Transport Control Protocol)](%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC/TCP)

### 전송계층

- [UDP](%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC/%EC%A0%84%EC%86%A1%EA%B3%84%EC%B8%B5/udp)

## 운영체제

- [Race condition](%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C/race-condition)
