# Ag grid, React 실습

<!-- TOC START -->

## 목차

- [스테이지 0: 프로젝트 베이스 깔기](#스테이지-0-프로젝트-베이스-깔기)
- [스테이지 1: “Hello, Grid”](#스테이지-1-hello-grid)
- [스테이지 2: 정렬/필터 강화 + 포매터](#스테이지-2-정렬필터-강화-포매터)
- [스테이지 3: 편집 가능 셀 + 검증](#스테이지-3-편집-가능-셀-검증)
- [스테이지 4: 커스텀 셀 렌더러(React)](#스테이지-4-커스텀-셀-렌더러react)
- [스테이지 5: 행 선택 + 툴바 액션](#스테이지-5-행-선택-툴바-액션)
- [스테이지 6: 페이징 + 퀵 필터](#스테이지-6-페이징-퀵-필터)
- [스테이지 7: 비동기 로딩(REST) + 로딩 오버레이](#스테이지-7-비동기-로딩rest-로딩-오버레이)
- [스테이지 8: 컬럼/필터 상태 저장(localStorage)](#스테이지-8-컬럼필터-상태-저장localstorage)
- [스테이지 9: CSV 내보내기(커뮤니티)](#스테이지-9-csv-내보내기커뮤니티)
- [스테이지 10: 성능 튜닝(수천\~수만 행 대응)](#스테이지-10-성능-튜닝수천수만-행-대응)
- [스테이지 11: 테마/스타일 커스텀(Tailwind 곁들임)](#스테이지-11-테마스타일-커스텀tailwind-곁들임)
- [스테이지 12: 퀘스트](#스테이지-12-퀘스트)
- [디버그 팁(삽질 방지)](#디버그-팁삽질-방지)

---

<!-- TOC END -->

# 스테이지 0: 프로젝트 베이스 깔기

- React 앱 생성
- 설치:

  ```bash
  npm i ag-grid-community ag-grid-react
  ```

- 스타일(최신 테마 중 하나):

  ```js
  // main.tsx or App.tsx 상단
  import "ag-grid-community/styles/ag-grid.css";
  import "ag-grid-community/styles/ag-theme-quartz.css"; // 또는 ag-theme-alpine
  ```

---

# 스테이지 1: “Hello, Grid”

가장 기초. 열 정의 + 행 데이터 + 기본 옵션.

```tsx
import { useMemo, useState } from "react";
import { AgGridReact } from "ag-grid-react";
import "./App.css";
import {
  ModuleRegistry,
  AllCommunityModule,
  themeQuartz,
} from "ag-grid-community";

ModuleRegistry.registerModules([AllCommunityModule]);

export default function App() {
  const [rowData] = useState([
    { id: 1, name: "Aiko", age: 21, salary: 2_500_000, city: "Seoul" },
    { id: 2, name: "Bora", age: 27, city: "Busan" },
    { id: 3, name: "Choi", age: 19, salary: 4_000_000, city: "Daegu" },
  ]);

  const colDefs = useMemo(
    () => [
      { field: "id", headerName: "ID", width: 90 },
      { field: "name", headerName: "이름" },
      { field: "age", headerName: "나이" },
      { field: "city", headerName: "도시" },
    ],
    []
  );

  const defaultColDef = useMemo(
    () => ({
      resizable: true,
      sortable: true, // 정렬(커뮤니티 가능)
      filter: true, // 필터(커뮤니티 가능)
    }),
    []
  );

  return (
    <div style={{ height: "100vh", width: "100%" }}>
      <h1>AG Grid 테스트</h1>
      <div style={{ height: 600, width: 600 }}>
        <AgGridReact
          rowData={rowData}
          columnDefs={colDefs}
          defaultColDef={defaultColDef}
          theme={themeQuartz}
        />
      </div>
    </div>
  );
}
```

---

# 스테이지 2: 정렬/필터 강화 + 포매터

- 숫자 천단위 콤마, 날짜 포맷, 값 합성 등.

```tsx
const colDefs = [
  { field: "name", headerName: "이름", floatingFilter: true },
  { field: "age", headerName: "나이", type: "rightAligned" },
  {
    field: "salary",
    headerName: "연봉",
    valueFormatter: (p) => p.value?.toLocaleString?.() ?? "",
  },
  { headerName: "요약", valueGetter: (p) => `${p.data.name} (${p.data.city})` },
];
```

- `floatingFilter: true`로 헤더 아래 미니 필터 추가.

---

# 스테이지 3: 편집 가능 셀 + 검증

- 인라인 수정, 간단한 검증으로 실수 차단.

```tsx
const colDefs = [
  { field: "name", editable: true },
  {
    field: "age",
    editable: true,
    valueParser: (p) => Number(p.newValue),
    cellClassRules: {
      "bg-red-50": (p) => Number.isNaN(p.value) || p.value < 0,
    },
  },
];
```

- `onCellValueChanged={(e)=>{ /* 저장 API 호출 등 */}}`로 서버 반영 훅.
- `bg-red-50` 적용시 빨간색으로 바뀌게 하려면 **tailwind 설치**하거나 링크된 css에 속성 정의 해줘야 함

```css
.bg-red-50 {
  background-color: rgba(255, 0, 0, 0.2);
}
```

---

# 스테이지 4: 커스텀 셀 렌더러(React)

- 버튼/뱃지/아이콘 같은 건 렌더러로.

```tsx
function ActionCellRenderer({ value, data }) {
  return (
    <button onClick={() => alert(`${data.name} 삭제?`)}>삭제</button>
  );
}

// columnDefs
{ headerName: "액션", cellRenderer: ActionCellRenderer, width: 120 }
```

- “React 컴포넌트” 그대로 써서 UI 깔끔하게 하기.

---

# 스테이지 5: 행 선택 + 툴바 액션

- 체크박스 선택, 선택 행 일괄 처리.

```tsx
const colDefs = [
  { checkboxSelection: true, headerCheckboxSelection: true, width: 50 },
  { field: "name" },
  { field: "age" },
  { field: "city" },
];

<AgGridReact
  rowData={rowData}
  columnDefs={colDefs}
  defaultColDef={defaultColDef}
  theme={themeQuartz}
  rowSelection={"multiple"}
/>;

// 선택행 가져오기: gridApi.getSelectedRows()
```

- 상단에 "선택 삭제/CSV" 버튼 두고 `gridApi`로 제어.
- `suppressRowClickSelection`은 deprecated -> `rowSelection.enableClickSelection` 대신 사용

---

# 스테이지 6: 페이징 + 퀵 필터

- 페이징은 커뮤니티에서 제공.

```tsx
<AgGridReact
  pagination
  paginationPageSize={10}
  quickFilterText={quick} // 상단 검색 인풋의 state 바인딩
/>
```

- 상단에 `input`을 두고 `setQuick(e.target.value)`로 실시간 검색.

# 스테이지 7: 비동기 로딩(REST) + 로딩 오버레이

- JSONPlaceholder로 가짜 데이터 받아보기.

```tsx
import { useMemo, useEffect, useRef, useState } from "react";
import { AgGridReact } from "ag-grid-react";
import {
  ModuleRegistry,
  AllCommunityModule,
  themeQuartz,
} from "ag-grid-community";

ModuleRegistry.registerModules([AllCommunityModule]);

export default function App() {
  const gridRef = useRef(null);
  const [rowData, setRowData] = useState([]);
  const [loading, setLoading] = useState(true);
  const URL = "https://jsonplaceholder.typicode.com/users";

  const colDefs = useMemo(
    () => [
      { field: "id", width: 90 },
      { field: "name" },
      { field: "email" },
      { field: "city" },
    ],
    []
  );

  useEffect(() => {
    // 그리드 마운트 전에도 OK
    (async () => {
      try {
        const r = await fetch(URL);
        const users = await r.json();
        setRowData(
          users.map((u) => ({
            id: u.id,
            name: u.name,
            email: u.email,
            city: u.address.city,
          }))
        );
      } finally {
        setLoading(false); // 리액트 로딩 종료
        // 그리드가 이미 준비됐으면 오버레이 끄기
        gridRef.current?.api?.hideOverlay();
      }
    })();
  }, []);

  const defaultColDef = useMemo(
    () => ({
      sortable: true,
      filter: true,
      resizable: true,
    }),
    []
  );

  return (
    <div style={{ height: "100vh", width: "100%" }}>
      <h1>AG Grid 테스트</h1>
      <div className="mb-2 flex gap-2">
        <button onClick={() => gridRef.current?.api.refreshCells()}>
          새로고침
        </button>
      </div>
      <div style={{ height: 480 }}>
        <AgGridReact
          ref={gridRef}
          rowData={rowData}
          columnDefs={colDefs}
          defaultColDef={defaultColDef}
          overlayLoadingTemplate={
            '<span class="ag-overlay-loading-center">불러오는 중…</span>'
          }
          overlayNoRowsTemplate={
            '<span class="ag-overlay-loading-center">데이터 없음</span>'
          }
          onGridReady={(p) => {
            if (loading) p.api.loading = true; // 준비 시점에만 API 호출
            else if (rowData.length === 0) p.api.showNoRowsOverlay();
          }}
          pagination
          paginationPageSize={5}
          paginationPageSizeSelector={[5, 10, 20, 50]}
        />
      </div>
    </div>
  );
}
```

---

# 스테이지 8: 컬럼/필터 상태 저장(localStorage)

- 새로고침 누를 때마다 세팅 날려먹는 뇌절 방지.

```tsx
// 저장
const saveState = () => {
  const colState = gridRef.current.api.getColumnState();
  const filterState = gridRef.current.api.getFilterModel();
  localStorage.setItem("grid:colState", JSON.stringify(colState));
  localStorage.setItem("grid:filterState", JSON.stringify(filterState));
};

// 복원
const restoreState = () => {
  const colState = JSON.parse(localStorage.getItem("grid:colState") || "null");
  const filterState = JSON.parse(
    localStorage.getItem("grid:filterState") || "null"
  );
  if (colState)
    gridRef.current.api.applyColumnState({ state: colState, applyOrder: true });
  if (filterState) gridRef.current.api.setFilterModel(filterState);
};
```

- 초기 `useEffect`에서 `restoreState()` 한 번 호출, 상단에 “상태 저장/복원/초기화” 버튼 배치.

---

# 스테이지 9: CSV 내보내기(커뮤니티)

- 엑셀(xlsx)은 엔터프라이즈지만, CSV는 커뮤니티로 충분.

```tsx
<button
  onClick={() =>
    gridRef.current.api.exportDataAsCsv({
      fileName: "users.csv",
    })
  }
>
  CSV 다운로드
</button>
```

---

# 스테이지 10: 성능 튜닝(수천\~수만 행 대응)

- 그리드는 가상 스크롤로 기본 빡세게 튜닝돼 있지만, 코드가 병목이면 무의미 해짐.

  - `rowData`는 `useState`로 보관하고, 불필요한 재생성 금지.
  - `columnDefs`, `defaultColDef`, 렌더러는 `useMemo`/`useCallback`.
  - `suppressColumnMoveAnimation`, `suppressDragLeaveHidesColumns` 등 불필요한 애니메이션 끄기.
  - 고빈도 업데이트는 트랜잭션 API 사용:

    ```tsx
    gridRef.current.api.applyTransaction({ add: newRows }); // add/update/remove
    ```

  - 셀 렌더러에서 무거운 계산은 값 준비 단계(`valueGetter`, 사전 계산)로 빼기.

---

# 스테이지 11: 테마/스타일 커스텀(Tailwind 곁들임)

- 컨테이너는 테마 클래스 + 고정 높이 필수(부모 높이 없으면 그리드 안 보여).

```tsx
<div className="ag-theme-quartz h-[600px] rounded-2xl p-2">
  <AgGridReact ... />
</div>
```

- CSS 변수로 테마 색 맛만 살짝 바꾸기(프로젝트 CSS):

```css
.ag-theme-quartz {
  --ag-header-background-color: #0f172a; /* slate-900 */
  --ag-header-foreground-color: #e2e8f0; /* slate-200 */
  --ag-odd-row-background-color: #0b1220; /* 어두운 줄무늬 */
}
```

---

# 스테이지 12: 퀘스트

1. “사용자 목록” 로드해서

   - 이름/이메일/도시 컬럼 구성
   - 정렬/필터 활성화
   - 퀵 필터 인풋 연결
   - 선택 행 삭제 버튼 구현

2. 나이/연봉 컬럼 추가하고 편집 가능 + 검증(음수 금지)
3. "상태 저장/복원" 버튼 만들고 localStorage 연동
4. CSV 내보내기 버튼으로 현재 필터 결과만 추출(기본 동작 OK)
5. 2만 행 페이크 데이터 뿌려서 스크롤/검색 성능 측정(렌더러 최소화)

---

- 집계/피벗/행 그룹핑, 서버사이드 로우 모델, 엑셀(xlsx) 내보내기, 마스터/디테일… 이런 건 Enterprise 기능

---

# 디버그 팁(삽질 방지)

- 그리드 안 보이면 99% “부모 높이 없음”이다. 컨테이너 높이 확실히 줘야함.
- 컬럼/데이터가 안 뜨면 콘솔에 `gridRef.current.api` 찍어서 라이프사이클 확인.
- `columnDefs`를 렌더마다 새로 만들면 성능이 죽는다. `useMemo` 넣을 것.
- 데이터는 객체 키 정확히 맞춰. 오타 내면 필드가 비어 보인다. 네가 그 오타의 왕이란 건 알지만 좀 조심하자.
