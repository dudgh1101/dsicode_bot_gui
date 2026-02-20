# Git Commands - 한국어 해석

---

## 작업 영역 시작 (see also: git help tutorial)
| 명령어 | 설명 |
|--------|------|
| `clone` | 저장소를 새 디렉토리에 복제 |
| `init` | 빈 저장소 생성 또는 기존 저장소 다시 초기화 |

---

## 현재 변경사항 작업 (see also: git help everyday)
| 명령어 | 설명 |
|--------|------|
| `add` | 파일 내용을 인덱스에 추가 |
| `mv` | 파일, 디렉토리, 심볼릭 링크 이동 또는 이름 변경 |
| `restore` | 작업 트리 파일 복원 |
| `rm` | 작업 트리 및 인덱스에서 파일 제거 |

---

## 기록 및 상태 확인 (see also: git help revisions)
| 명령어 | 설명 |
|--------|------|
| `bisect` | 이진 검색으로 버그가 도입된 커밋 찾기 |
| `diff` | 커밋 간, 커밋과 작업 트리 간 변경사항 표시 |
| `grep` | 패턴과 일치하는 줄 출력 |
| `log` | 커밋 로그 표시 |
| `show` | 다양한 타입의 객체 표시 |
| `status` | 작업 트리 상태 표시 |

---

## 일반 기록 성장, 표시, 조정
| 명령어 | 설명 |
|--------|------|
| `branch` | 브랜치 목록 생성, 삭제 |
| `commit` | 저장소에 변경사항 기록 |
| `merge` | 두 개 이상의 개발 기록 합치기 |
| `rebase` | 다른 기본 팁 위에 커밋 다시 적용 |
| `reset` | 현재 HEAD를 지정된 상태로 재설정 |
| `switch` | 브랜치 전환 |
| `tag` | GPG로 서명된 태그 객체 생성, 목록, 삭제, 검증 |

---

## 협업 (see also: git help workflows)
| 명령어 | 설명 |
|--------|------|
| `fetch` | 다른 저장소에서 객체 및 refs 다운로드 |
| `pull` | 다른 저장소 또는 로컬 브랜치에서 가져와서 통합 |
| `push` | 관련 객체와 함께 원격 refs 업데이트 |

---

## 자주 사용되는 명령어 요약

```bash
# 시작
git clone <url>      # 저장소 복제
git init             # 저장소 초기화

# 변경사항
git add <file>       # 변경사항 스테이징
git commit -m "msg"  # 커밋
git status           # 상태 확인
git diff             # 변경사항 확인

# 브랜치
git branch           # 브랜치 목록
git switch <name>    # 브랜치 전환
git merge <branch>   # 병합

# 협업
git pull             # 가져와서 병합
git push             # 원격에推送
git fetch            # 다운로드만
```
