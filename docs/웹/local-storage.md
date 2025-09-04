# Local storage


<!-- TOC START -->

## 목차

- [저장 특성](#저장-특성)
- [코드 예시](#코드-예시)
  - [간단한 TODO 리스트](#간단한-todo-리스트)
  - [임시 로그인 토큰](#임시-로그인-토큰)
- [활용 방법](#활용-방법)
- [다른 클라이언트 저장소와 비교](#다른-클라이언트-저장소와-비교)
  - [sessionStorage](#sessionstorage)
  - [IndexedDB](#indexeddb)

---

<!-- TOC END -->


localStorage는 브라우저 안에 있는 작은 개인 창고다. 브라우저가 제공하는 키-값 저장소라서 문자열만 저장할 수 있고, 용량은 대략 5MB 정도이다. 쿠키처럼 서버에 자동으로 전송되지는 않는다.

## 저장 특성

- 브라우저를 꺼도 데이터가 계속 저장되어 있다.
- **브라우저를 바꾸거나 기기를 바꾸면 데이터가 사라진다.**, 왜냐면 그 저장소는 해당 브라우저/도메인에 국한되기 때문이다.

## 코드 예시

### 간단한 TODO 리스트

```js
// 로그인 성공 시 토큰 저장
function saveToken(token) {
  localStorage.setItem("accessToken", token);
}

// API 호출할 때 사용
function getToken() {
  return localStorage.getItem("accessToken");
}

// 로그아웃 시
function logout() {
  localStorage.removeItem("accessToken");
}
```

### 임시 로그인 토큰

```js
// 로그인 성공 시 토큰 저장
function saveToken(token) {
  localStorage.setItem("accessToken", token);
}

// API 호출할 때 사용
function getToken() {
  return localStorage.getItem("accessToken");
}

// 로그아웃 시
function logout() {
  localStorage.removeItem("accessToken");
}
```

## 활용 방법

- **로그인 상태 유지(가벼운 경우)**:

  - JWT 토큰 같은 걸 저장해두면 새로고침해도 로그인 상태를 잃지 않는다.
  - 다만 민감한 건 보안 때문에 localStorage보단 httpOnly, Secure 쿠키를 쓰는 게 낫다.

- **사용자 환경 설정**:

  - 다크모드/라이트모드, 언어, 폰트 크기 같은 개인 설정을 기억시킬 때 유용함.

- **클라이언트 캐싱**: 서버에서 불러온 데이터를 한 번 저장해두고 다시 페이지에 들어올 때 빠르게 띄우는 데 쓸 수 있다.

- **폼 임시 저장**:
  - 글 작성하다가 새로고침해도 날아가지 않게 중간 저장소로 쓰기에 좋음.
  - 임시저장 기능

## 다른 클라이언트 저장소와 비교

### sessionStorage

- localStorage랑 API 똑같은데, **브라우저 탭을 닫으면 데이터가 싹 날아간다**. 탭 단위라서 같은 사이트를 두 개 열면 각자 따로 관리된다.

- **사용례**:
  - **일시적인 폼 데이터**: 결제 페이지에서 새로고침해도 입력한 내용 유지
  - **다단계 회원가입**: 1단계→2단계 이동할 때 데이터를 잠시 보관

### IndexedDB

3. IndexedDB

- 로컬 DB. 객체 저장 가능하고, 수백 MB까지도 쓸 수 있다. 구조화된 데이터 저장에 강함. 비동기 API라서 좀 귀찮음.

- 사용례:
  - **오프라인 웹앱**: 구글 드라이브, 노션 같은 애들이 오프라인 모드에서 여기다 파일 저장
  - **대용량 캐싱**: 이미지, 동영상, JSON 같은 거 쌓아두기
