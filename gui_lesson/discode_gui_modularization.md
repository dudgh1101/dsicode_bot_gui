# discode_gui.py 모듈화 제안

## 1. 현재 문제점 분석

### 1.1 구조적 문제

| 문제 | 설명 |
|------|------|
| **단일 파일** | 191줄의 코드가 모두 한 파일에 집중 |
| **GUI/Logic 결합** | UI 생성 로직과 명령어 처리 로직이 강하게 결합 |
| **전역 변수 직접 접근** | `discode_bot_test_git.str_commend_line`을 통한 직접 참조 |
| **테스트 어려움** | 의존성이太强하여 단위 테스트 수행이 사실상 불가능 |
| **설정 하드코딩** | commands 딕셔너리가 클래스 내부에 하드코딩됨 |

### 1.2 결합도 문제

현재 코드에서 GUI와 Discord Bot는 다음과 같이 강하게 결합되어 있습니다:

```python
# 실제 코드 예시
discode_bot_test_git.str_commend_line = self.commend  # 직접 참조
discode_bot_test_git.start_bot()  # 모듈 직접 호출
```

이 구조는 다음과 같은 문제를 야기합니다:
- Bot 모듈 변경 시 GUI 코드 수정 필요
- 단위 테스트 시 실제 Bot 없이 테스트 불가
- 재사용성 제한

---

## 2. 권장 모듈화 구조

### 2.1 디렉토리 구조

```
gui_lesson/
├── __init__.py
├── main.py                        # 애플리케이션 실행 엔트리
├── discode_gui.py                 # 기존 파일 (유지 또는 main으로 통합)
├── ui/                            # UI 레이어
│   ├── __init__.py
│   ├── app.py                     # App 클래스 (UI 로직만)
│   ├── widgets.py                 # 버튼, 입력 필드 등 위젯
│   └── frames.py                  # 레이아웃 프레임
├── core/                          # 핵심 비즈니스 로직
│   ├── __init__.py
│   ├── command_manager.py         # 명령어 생성/유효성 검증
│   ├── bot_client.py              # Discord Bot 클라이언트 추상화
│   └── protocol.py               # GUI↔Bot 통신 레이어
└── config/                        # 설정
    ├── __init__.py
    └── commands.py                # 명령어 정의
```

### 2.2 계층 구조도

```
┌─────────────────────────────────────┐
│           main.py (조립)            │
│   - 의존성 주입                     │
│   - 애플리케이션 초기화              │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┐
    ▼                   ▼
┌───────┐         ┌──────────┐
│  UI   │◄──────►│  Core    │
│ Layer │         │ (Logic)  │
│       │         │          │
│ - app │         │ - protocol│
│ -widgets      │ - command │
└───────┘         └────┬─────┘
                       │
                ┌──────┴──────┐
                ▼             ▼
          ┌──────────┐  ┌──────────┐
          │ Bot      │  │ Config   │
          │ Protocol │  │          │
          └──────────┘  └──────────┘
```

---

## 3. 핵심 모듈 상세 설계

### 3.1 통신 프로토콜 추상화 (protocol.py)

**문제**: 현재는 전역 변수를 직접 참조하여 결합도가 높음

**해결**: BotProtocol 클래스로 추상화

```python
# core/protocol.py
from abc import ABC, abstractmethod
from typing import Optional

class BotProtocol(ABC):
    """Discord Bot과의 통신을 추상화한 프로토콜"""
    
    @abstractmethod
    def send_command(self, command: str) -> bool:
        """명령어를 Bot에 전송"""
        pass
    
    @abstractmethod
    def is_running(self) -> bool:
        """Bot 실행 상태 확인"""
        pass
    
    @abstractmethod
    def start(self) -> None:
        """Bot 시작"""
        pass
    
    @abstractmethod
    def stop(self) -> None:
        """Bot 종료"""
        pass


class DirectProtocol(BotProtocol):
    """전역 변수를 사용하는 직접 연결 프로토콜"""
    
    def __init__(self, bot_module):
        self._bot = bot_module
    
    def send_command(self, command: str) -> bool:
        try:
            self._bot.str_commend_line = command
            return True
        except Exception:
            return False
    
    @property
    def is_running(self) -> bool:
        return getattr(self._bot, 'is_running', False)
    
    def start(self) -> None:
        # 별도 스레드에서 Bot 시작 로직
        pass
    
    def stop(self) -> None:
        self._bot.str_commend_line = "!turn_off"


class MockProtocol(BotProtocol):
    """테스트용 Mock 프로토콜"""
    
    def __init__(self):
        self._commands: list[str] = []
        self._running = False
    
    def send_command(self, command: str) -> bool:
        self._commands.append(command)
        return True
    
    @property
    def is_running(self) -> bool:
        return self._running
    
    def start(self) -> None:
        self._running = True
    
    def stop(self) -> None:
        self._running = False
    
    @property
    def sent_commands(self) -> list[str]:
        return self._commands.copy()
```

**장점**:
- 실제 Bot 대신 MockProtocol으로 테스트 가능
- Bot 모듈 변경 시 protocol만 교체
- 의존성 주입으로 테스트 용이

---

### 3.2 명령어 핸들러 분리 (command_manager.py)

**문제**: `text_set()` 메서드에서 50줄에 걸쳐 명령어 검증 로직이 혼합

**해결**: CommandBuilder 클래스로 분리

```python
# core/command_manager.py
from dataclasses import dataclass
from typing import Optional
import re

@dataclass
class CommandResult:
    """명령어 생성 결과"""
    success: bool
    command: Optional[str] = None
    error_message: Optional[str] = None
    error_type: Optional[str] = None  # "format", "validation", "unknown"

class CommandBuilder:
    """명령어 생성 및 유효성 검증"""
    
    TIME_PATTERN = re.compile(r'^\d{2}:\d{2}$')
    
    @classmethod
    def build_add(cls, user_input: str) -> CommandResult:
        """
        !add 명령어 생성
        입력 형식: "12:00 메시지"
        """
        if not user_input or not user_input.strip():
            return CommandResult(
                success=False,
                error_message="메시지를 입력하세요",
                error_type="format"
            )
        
        parts = user_input.strip().split(" ", 1)
        
        if len(parts) < 2:
            return CommandResult(
                success=False,
                error_message="형식: 12:00 메시지 (예: 12:00 점심)",
                error_type="format"
            )
        
        time_str, msg = parts
        
        if not cls._validate_time(time_str):
            return CommandResult(
                success=False,
                error_message="시간 형식: HH:MM (예: 12:00)",
                error_type="validation"
            )
        
        return CommandResult(
            success=True,
            command=f"!add {time_str} {msg}"
        )
    
    @classmethod
    def build_remove(cls, user_input: str) -> CommandResult:
        """
        !remove 명령어 생성
        입력 형식: "12:00" 또는 "all"
        """
        if not user_input or not user_input.strip():
            return CommandResult(
                success=False,
                error_message="시간을 입력하세요 (예: 12:00 또는 all)",
                error_type="format"
            )
        
        user_input = user_input.strip()
        
        if user_input.lower() == "all":
            return CommandResult(
                success=True,
                command="!remove all"
            )
        
        if not cls._validate_time(user_input):
            return CommandResult(
                success=False,
                error_message="시간 형식: HH:MM 또는 all",
                error_type="validation"
            )
        
        return CommandResult(
            success=True,
            command=f"!remove {user_input}"
        )
    
    @staticmethod
    def build_simple(command: str) -> CommandResult:
        """인자 없는 단순 명령어"""
        return CommandResult(success=True, command=command)
    
    @staticmethod
    def _validate_time(time_str: str) -> bool:
        """시간 형식 검증 (HH:MM)"""
        if len(time_str) != 5:
            return False
        if time_str[2] != ":":
            return False
        return bool(CommandBuilder.TIME_PATTERN.match(time_str))
```

---

### 3.3 설정 분리 (config/commands.py)

**문제**: commands 딕셔너리가 클래스 내부에 하드코딩

**해결**: 설정 파일로 분리

```python
# config/commands.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Command:
    """명령어 정의"""
    key: str
    description: str
    requires_input: bool = False
    input_placeholder: str = ""
    example: Optional[str] = None

# 명령어 정의
COMMANDS = [
    Command(
        key="!add",
        description="예약 추가 (시간 + 메시지)",
        requires_input=True,
        input_placeholder="12:00 점심알림",
        example="12:00 점심시간 알림"
    ),
    Command(
        key="!remove",
        description="예약 삭제 (시간)",
        requires_input=True,
        input_placeholder="12:00",
        example="12:00"
    ),
    Command(
        key="!remove all",
        description="모든 예약 삭제",
        requires_input=False
    ),
    Command(
        key="!list",
        description="예약 목록 보기",
        requires_input=False
    ),
    Command(
        key="!call_in",
        description="음성 채널 입장",
        requires_input=False
    ),
    Command(
        key="!call_out",
        description="음성 채널 퇴장",
        requires_input=False
    ),
    Command(
        key="!commend_list",
        description="명령어 목록 보기",
        requires_input=False
    ),
    Command(
        key="!turn_off",
        description="봇 종료",
        requires_input=False
    ),
]

# 딕셔너리 변환 유틸리티
def get_command_dict() -> dict[str, str]:
    """GUI용 {명령어: 설명} 딕셔너리"""
    return {cmd.key: cmd.description for cmd in COMMANDS}

def get_command(key: str) -> Optional[Command]:
    """명령어 조회"""
    for cmd in COMMANDS:
        if cmd.key == key:
            return cmd
    return None

def get_commands_requiring_input() -> list[str]:
    """입력이 필요한 명령어 목록"""
    return [cmd.key for cmd in COMMANDS if cmd.requires_input]
```

---

### 3.4 UI 레이어 분리

```python
# ui/app.py
class App:
    """UI 로직만 담당하는 App 클래스"""
    
    def __init__(self, root, protocol: BotProtocol):
        self.root = root
        self.protocol = protocol  # 의존성 주입
        self._setup_ui()
    
    def _setup_ui(self):
        # UI 초기화 로직
        pass
```

```python
# ui/widgets.py
class CommandButtonFactory:
    """명령어 버튼 생성 팩토리"""
    
    @staticmethod
    def create_buttons(parent, commands: list[Command], callback):
        """버튼 그리드 생성"""
        buttons = []
        for i, cmd in enumerate(commands):
            if i % 2 == 0:
                frame = tk.Frame(parent)
                frame.pack()
            
            btn = tk.Button(
                frame,
                text=cmd.key,
                command=lambda c=cmd.key: callback(c),
                width=12
            )
            btn.pack(side=tk.LEFT, padx=5)
            buttons.append(btn)
        
        return buttons
```

---

## 4. 의존성 주입을 통한 조립

### 4.1 main.py (애플리케이션 조립)

```python
# main.py
import tkinter as tk
from ui.app import App
from core.protocol import DirectProtocol, MockProtocol
from py_discordBot import discode_bot_test_git

class ApplicationBuilder:
    """애플리케이션 조립기"""
    
    def __init__(self, use_mock: bool = False):
        self.use_mock = use_mock
    
    def build(self) -> App:
        # 프로토콜 선택 (실제 또는 Mock)
        if self.use_mock:
            from core.protocol import MockProtocol
            protocol = MockProtocol()
        else:
            protocol = DirectProtocol(discode_bot_test_git)
        
        # GUI 애플리케이션 생성
        root = tk.Tk()
        root.title("디스코드 GUI 앱")
        root.geometry("700x500")
        
        app = App(root, protocol)
        
        return app

if __name__ == "__main__":
    # 실제 실행
    builder = ApplicationBuilder(use_mock=False)
    app = builder.build()
    app.root.mainloop()
```

### 4.2 테스트용 구성

```python
# tests/test_command_manager.py
import pytest
from core.command_manager import CommandBuilder, CommandResult

class TestCommandBuilder:
    
    def test_build_add_success(self):
        result = CommandBuilder.build_add("12:00 점심시간")
        assert result.success is True
        assert result.command == "!add 12:00 점심시간"
    
    def test_build_add_invalid_format(self):
        result = CommandBuilder.build_add("점심시간")
        assert result.success is False
        assert result.error_type == "format"
    
    def test_build_add_invalid_time(self):
        result = CommandBuilder.build_add("12:000 점심")
        assert result.success is False
        assert result.error_type == "validation"
    
    def test_build_remove_all(self):
        result = CommandBuilder.build_remove("all")
        assert result.success is True
        assert result.command == "!remove all"
    
    def test_build_remove_time(self):
        result = CommandBuilder.build_remove("15:30")
        assert result.success is True
        assert result.command == "!remove 15:30"


class TestMockProtocol:
    
    def test_send_command(self):
        from core.protocol import MockProtocol
        
        protocol = MockProtocol()
        result = protocol.send_command("!add 12:00 테스트")
        
        assert result is True
        assert "!add 12:00 테스트" in protocol.sent_commands
    
    def test_is_running(self):
        from core.protocol import MockProtocol
        
        protocol = MockProtocol()
        assert protocol.is_running is False
        
        protocol.start()
        assert protocol.is_running is True
```

---

## 5. 모듈화 우선순위 제안

### 5.1 단계별 진행 계획

| 단계 | 항목 | 예상工作量 | 효과 |
|------|------|----------|------|
| **1단계** | BotProtocol 클래스 생성 | 小 | 테스트 가능 + 결합도 ↓ |
| **2단계** | CommandBuilder 분리 | 中 | 검증 로직 단위 테스트 가능 |
| **3단계** | commands → config 분리 | 小 | 설정 변경 시 코드 수정 불필요 |
| **4단계** | UI 위젯별 파일 분리 | 中 | 가독성 + 재사용성 ↑ |
| **5단계** | 의존성 주입 적용 | 中 | 테스트 완전 가능 |

### 5.2 단계별 상세 내용

#### 1단계: BotProtocol 생성

- `core/protocol.py` 생성
- `DirectProtocol`, `MockProtocol` 클래스 구현
- GUI에서 `BotProtocol`을 인터페이스로 사용
- **테스트**: MockProtocol으로 명령어 전송 테스트

#### 2단계: CommandBuilder 분리

- `core/command_manager.py` 생성
- `text_set()` 검증 로직 이동
- **테스트**: 다양한 입력에 대한 검증 테스트

#### 3단계: 설정 분리

- `config/commands.py` 생성
- 하드코딩된 commands 딕셔너리 제거
- 새로운 명령어 추가 시 코드 수정 불필요

#### 4단계: UI 분리

- `ui/widgets.py`, `ui/frames.py` 분리
- 버튼 생성 로직 재사용 가능하도록 설계

#### 5단계: 의존성 주입

- `main.py`에서 ApplicationBuilder 구현
- 프로토콜 선택을 통한 테스트/실제 모드 전환

---

## 6. 모듈화 기대효과

### 6.1 단위 테스트 가능

| 이전 | 이후 |
|------|------|
| 전체 앱 실행 없이는 테스트 불가 | CommandBuilder 단독 테스트 가능 |
| Discord Bot 필수 | MockProtocol으로 테스트 가능 |
| 수동 테스트만 가능 | 자동화된 테스트 구축 |

### 6.2 유지보수성 향상

| 이전 | 이후 |
|------|------|
| 191줄 단일 파일 | 역할별 분리 (5+ 파일) |
| Bot 변경 시 GUI 영향 | Protocol 추상화로 영향 최소화 |
| 새로운 명령어 추가 시 코드 수정量大 | 설정 파일만 수정 |

### 6.3 확장성

| 이전 | 이후 |
|------|------|
| GUI ↔ Bot만 가능 | Protocol 교체로 다양한 연결 방식 지원 |
| Tkinter만 지원 | UI 추상화로 다른 프레임워크 가능 |
| 하드코딩된 명령어 | 동적 명령어 로드 가능 |

---

## 7. 결론

현재 `discode_gui.py`는 기능적으로 동작하지만, 확장성과 유지보수 측면에서 개선이 필요한 상태입니다.

**모듈화 목표**:
1. **단위 테스트 가능**: 각 모듈을 독립적으로 테스트
2. **GUI/Bot 독립적 변경**: 한 模块 변경 시 다른 模块 영향 최소화
3. **설정 외부화**: 코드 수정 없이 설정 변경 가능
4. **재사용성 향상**: 위젯/로직 재사용

**권장 접근법**:
한 번에 전체를重构하면 위험하므로, **1단계(BotProtocol) → 2단계(CommandBuilder) → 3단계(config)** 순서로 점진적으로 진행하는 것을 권장합니다.

각 단계에서 테스트를 추가하면서 진행하면 안전하게 모듈화를 완료할 수 있습니다.
