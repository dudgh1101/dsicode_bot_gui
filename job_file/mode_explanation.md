# [analyze-mode] Modes - 해석

---

## 1. [analyze-mode]

**용도**: 문제 해결 전에 먼저 맥락을 수집하는 분석 모드

**실행 방법**:
1. **병렬 컨텍스트 수집**:
   - 1-2개 explore 에이전트 실행 (코드베이스 패턴, 구현 분석)
   - 외부 라이브러리 관련: librarian 에이전트 사용
   - 직접 도구: Grep, AST-grep, LSP로 타겟 검색

2. **복잡한 문제일 경우**:
   - **Oracle**: 전통적인 문제 (아키텍처, 디버깅, 복잡한 로직)
   - **Artistry**: 비전통적인 문제 (새로운 접근 방식 필요)

3. **발견 사항 종합 후 진행**

---

## 2. [search-mode]

**용도**: 최대한 많은 검색을 수행하는 탐색 모드

**실행 방법**:
- 여러 background agents **병렬로 실행**:
  - explore agents (코드베이스 패턴, 파일 구조, ast-grep)
  - librarian agents (원격 저장소, 공식 문서, GitHub 예제)
- 추가 직접 도구: Grep, ripgrep (rg), ast-grep (sg)
- **첫 결과에 멈추지 말고 최대한 많이 검색**

---

## 3. 사용 예시

```
[analyze-mode]
CONTEXT GATHERING (parallel):
- explore agents로 코드베이스 패턴 분석
- 문제를oroughly understanding한 후 진행
```

```
[search-mode]
MAXIMIZE SEARCH EFFORT.
여러 에이전트를 병렬로 실행해서 최대한 많은 정보 수집
```
