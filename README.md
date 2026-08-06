# AWS Student Builder Group — 랜딩 페이지

광운대학교 AWS Student Builder Group 홍보/리크루팅 원 페이지 사이트.

## 로컬에서 띄우기

```bash
python3 serve.py          # http://localhost:5173 (브라우저 자동 실행)
python3 serve.py 8080     # 포트 지정
```

`file://` 로 직접 열면 안 됩니다. `.dc.html` 런타임(`support.js`)이 React/Babel을
CDN에서 받아오고 로컬 폰트도 CORS에 걸리기 때문에 **HTTP로 서빙해야** 합니다.
따라서 첫 로드에는 **인터넷 연결이 필요**합니다.

## 구성

```
serve.py                          로컬 개발 서버 (의존성 없음)
DESIGN_BRIEF.md                   디자인 브리프 (구조/모션 스펙)
AWS Student Builder 웹사이트/      Claude Design 내보내기 결과
  ├─ ASBG Landing.dc.html         마크업 + 하단 <script>에 데이터/로직
  ├─ support.js                   .dc.html 런타임 (수정 금지, 생성물)
  ├─ image-slot.js                <image-slot> 커스텀 엘리먼트
  ├─ assets/                      로고, 아이콘, Amazon Ember 폰트
  └─ uploads/                     디자인 작업 시 참고용 원본 파일
```

## 콘텐츠 수정하는 곳

전부 `ASBG Landing.dc.html` 하단 `<script type="text/x-dc">` 안에 있습니다.

| 대상 | 위치 |
|---|---|
| 지난 기수 활동 | `const PAST = { '4기': [...], ... }` |
| FAQ | `const FAQS = [...]` |
| 리크루팅 일정 | `renderVals()` 안의 `stepData` |
| 현재 진행 단계 (NOW 뱃지) | `data-props` 의 `currentStep` (0부터 시작) |
| 기수 번호 | `data-props` 의 `cohort` |

## 아직 안 채운 것

- [ ] 지원 폼 URL — 현재 `<a id="apply" href="#">`. 폼 주소 나오면 교체
- [ ] 리크루팅 실제 날짜 — `stepData` 값이 placeholder
- [ ] 지난 기수 활동 사진 — 아래 참고
- [ ] 운영진 소개 (FAQ 6번에서 "곧 공개" 로 처리 중)

### 사진에 대해

활동 카드의 `<image-slot>` 은 Claude Design 에디터 안에서만 이미지가 저장됩니다
(에디터 호스트와 postMessage로 통신). 로컬/배포 환경에서는 placeholder만 보입니다.

실제 사진을 넣으려면 이미지를 `assets/photos/` 에 두고 `src` 를 직접 지정하면 됩니다:

```html
<image-slot src="assets/photos/4기-데모데이.jpg" shape="rect"></image-slot>
```

`PAST` 항목에 `photo:false` 를 주면 "NO PHOTO" 상태로 렌더링되므로,
사진이 없는 활동은 그대로 두어도 레이아웃이 깨지지 않습니다.
