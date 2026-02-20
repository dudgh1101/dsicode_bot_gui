# AI Agent & Tool Permission Test Results

Date: 2026-02-18

## 최종 요약

| Type | Item | Status | Notes |
|------|------|--------|-------|
| **Category** | quick | ✅ | gemini-2.0-flash-exp |
| **Category** | visual-engineering | ✅ | gemini-2.0-flash-exp |
| **Category** | deep | ❌ | Requires gpt-5.3-codex (설정파일 무시됨) |
| **Category** | ultrabrain | ❌ | 설정파일 무시됨 |
| **Category** | artistry | ❌ | Requires gemini-3-pro (설정파일 무시됨) |
| **Category** | unspecified-low | ❌ | 설정파일 무시됨 |
| **Category** | unspecified-high | ❌ | 설정파일 무시됨 |
| **Category** | writing | ❌ | 설정파일 무시됨 |
| **Agent** | explore | ✅ | Works |
| **Agent** | librarian | ❌ | Execution aborted |
| **Agent** | oracle | ❌ | Execution aborted |
| **Agent** | multimodal-looker | ✅ | Works |
| **Agent** | metis | ✅ | Works |
| **Agent** | momus | ❌ | Execution aborted |
| **Skill** | playwright | ✅ | Loads correctly |
| **Skill** | git-master | ✅ | Loads correctly |
| **Skill** | dev-browser | ✅ | Loads correctly |
| **Skill** | frontend-ui-ux | ✅ | Loads correctly |

## 중요 발견

**설정 파일 경로**: `~/.config/opencode/oh-my-opencode.json`

**문제**: oh-my-opencode 프레임워크가 특정 카테고리에 대해 필수 모델을 하드코딩 해둠:
- `deep` → gpt-5.3-codex 필수
- `artistry` → gemini-3-pro 필수
- `ultrabrain`, `unspecified-low`, `unspecified-high`, `writing` → 설정 무시

**설정 파일을 수정해도 프레임워크가 강제로override함**.

## 해결 방법

1. **프레임워크 소스 수정**: oh-my-opencode 프레임워크 자체의 카테고리 필수 모델 설정 제거 필요
2. **사용 가능한 카테고리만 사용**: `quick`, `visual-engineering`만 사용
3. **Provider에서 필요한 모델 구매**: gpt-5.3-codex, gemini-3-pro 등

## 작동하는 조합

가장 안정적으로 작동하는 조합:
- Category: `quick`, `visual-engineering`
- Agent: `explore`, `multimodal-looker`, `metis`
- Skill: `playwright`, `git-master`, `dev-browser`, `frontend-ui-ux`

---

## [analyze-mode] 해석

**설명**: CLI 환경에서 사용하는 분석 모드. 문제 해결 전에 먼저 맥락을 수집하는 단계

### 사용 방법

**1. 병렬 컨텍스트 수집:**
- 1-2개의 explore 에이전트 실행 (코드베이스 패턴, 구현 분석)
- 외부 라이브러리 관련 시: librarian 에이전트 사용
- 직접 도구 활용: Grep, AST-grep, LSP로 타겟 검색

**2. 복잡한 문제:**
- **Oracle 에이전트**: 전통적인 문제 (아키텍처, 디버깅, 복잡한 로직)
- **Artistry 에이전트**: 비전통적인 문제 (새로운 접근 방식 필요)

**3. 발견 사항 종합 후 진행**

### 명령어 예시
```
[analyze-mode]
ANALYSIS MODE. Gather context before diving deep:

CONTEXT GATHERING (parallel):
- 1-2 explore agents (codebase patterns, implementations)
- 1-2 librarian agents (if external library involved)
- Direct tools: Grep, AST-grep, LSP for targeted searches

IF COMPLEX - DO NOT STRUGGLE ALONE. Consult specialists:
- **Oracle**: Conventional problems (architecture, debugging, complex logic)
- **Artistry**: Non-conventional problems (different approach needed)

SYNTHESIZE findings before proceeding.
```

이 모드를 활성화하면 문제를 해결하기 전에 먼저 코드베이스를 분석하고, 관련 정보를 수집한 후 종합해서 접근方式的으로 해결해 나감.
