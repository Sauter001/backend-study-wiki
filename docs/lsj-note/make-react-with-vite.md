# vite로 react 프로젝트 만드는 법


<!-- TOC START -->

## 목차

- [최신 버전 vite + react + typescript (추천)](#최신-버전-vite-react-typescript-추천)
- [타입스크립트 싫으면 걍 react](#타입스크립트-싫으면-걍-react)
  - [2. 설치 후 디렉토리 이동](#2-설치-후-디렉토리-이동)
  - [개발 모드로 실행](#개발-모드로-실행)

---

<!-- TOC END -->


```bash
# 최신 버전 vite + react + typescript (추천)
npm create vite@latest my-app -- --template react-ts

# 타입스크립트 싫으면 걍 react
npm create vite@latest my-app -- --template react
```

## 2. 설치 후 디렉토리 이동

```bash
cd my-app
npm install
```

## 개발 모드로 실행

```bash
npm run dev
```

터미널에 뜨는 로컬 주소(http://localhost:5173)로 들어가면 기본 React 화면 보임
