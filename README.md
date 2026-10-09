# DetoxMate 팀 Skill

Codex와 Claude Code가 같은 Notion 기획·정책을 읽고 수정하기 위한 공개 배포 원본이다. [DetoxMate/detoxmate-skills](https://github.com/DetoxMate/detoxmate-skills)에서 각자 받아 사용한다. 저장소 공개는 팀 Notion 문서의 공개나 접근 권한 부여를 뜻하지 않는다. API 토큰은 포함하지 않는다.

## 배포 상태

스킬 두 개와 기존 설치 프로그램을 먼저 공개한다. 현재 설치 프로그램은 전역 설치용이다. 팀에서 사용할 프로젝트별 설치와 `detoxmate-notion` CLI·인증 설정 배포는 아직 준비 중이다. 저장소를 받는 것만으로 Notion 연동까지 완료되지는 않는다.

## 역할

| 원본 | 관리하는 내용 |
|---|---|
| Notion 문서 DB | 최신 제품 기획·정책 |
| Notion 정책 템플릿 | 새 문서의 형식 |
| 이 저장소의 Skill | 어떤 문서를 읽고 어떻게 생성·수정할지 |
| 각자의 로컬 CLI 설정 | 팀용 내부 연결의 인증정보와 Notion 접근 권한 |

`fetch-notion-wiki`는 조회용, `update-notion-wiki`는 생성·수정용이다. 두 Skill은 일반 Agent Skills 형식으로 작성되어 같은 원본을 두 도구에서 읽는다. 별도 에이전트나 플러그인 없이 시작한다.

## 처음 설치

먼저 저장소를 받는다.

```sh
git clone https://github.com/DetoxMate/detoxmate-skills.git
cd detoxmate-skills
```

아래는 Python 3가 있는 로컬 macOS/Linux 환경에서 사용할 수 있는 **기존 전역 설치 방법**이다. 프로젝트별 설치 절차는 준비 중이므로, 전역 설치를 원하는 경우에만 실행한다.

```sh
python3 install.py codex
```

```sh
python3 install.py claude
```

둘 다 사용하면 `python3 install.py both`를 실행한다.

설치 프로그램은 Codex의 `~/.agents/skills/`, Claude Code의 `~/.claude/skills/` 아래에 원본 폴더를 가리키는 링크를 만든다. 이미 같은 이름의 다른 Skill이 있으면 덮어쓰지 않고 중단한다. 설치된 원본 폴더를 이동하거나 삭제하지 않는다. Windows는 링크 생성 권한과 도구별 경로를 확인해야 하며 이 설치 프로그램으로 검증하지 않았다.

현재 두 Skill의 기본 연결은 팀용 내부 연결로 인증하는 `detoxmate-notion` CLI다. PATH 또는 `~/.local/bin/detoxmate-notion`에서 실행할 수 있어야 한다. 이 명령은 로컬 보관소의 토큰을 읽어 공식 `ntn api`에 전달한다. 게스트 개인의 공식 MCP 로그인으로 자동 전환하지 않는다.

Skill 설치만으로 CLI나 토큰이 설치되지는 않는다. 현재 CLI 연결은 작성자 컴퓨터에서 검증했으며, 팀원용 CLI·인증 설정 배포는 별도 준비가 필요하다. 토큰은 대화·문서·이 저장소에 넣지 않는다. 각 환경에서 아래 DB와 템플릿을 실제로 읽을 수 있는지 확인하고, 편집 검증은 실제 합의된 변경을 반영할 때 수행한다.

- [기획·정책 문서 DB](https://www.notion.so/04b8dff159e44753960b2d950ef6c5f5)
- [정책 template_v1](https://www.notion.so/3ecad7a38ce580a7a8e6c29eb7b33bd1)

설치 후 새 세션에서 Skill이 표시되는지 확인한다. Codex는 `$fetch-notion-wiki`, Claude Code는 `/fetch-notion-wiki`로 호출한다. 수정은 같은 방식으로 `update-notion-wiki`를 호출한다.

## 업데이트

Skill 수정은 이 저장소에서 관리한다. 팀원들은 clone한 폴더에서 다음을 실행한다.

```sh
git pull --ff-only
```

연결된 Skill도 같은 원본을 읽으므로 복사·재설치할 필요가 없다. 업데이트 뒤 새 세션에서 사용한다. Git을 업데이트하지 않은 팀원에게 변경이 자동 배포되는 것은 아니다. 특정 버전을 맞춰야 하면 팀이 정한 동일한 커밋이나 태그를 사용한다.

제품 정책이나 템플릿만 바뀐 경우에는 Git을 바꾸지 않아도 실행할 때 Notion의 현재 내용을 읽는다. DB 위치나 템플릿을 교체한 경우에는 두 Skill에 적힌 위치도 점검한다.

## 첫 사용 확인

1. 조회: “친구를 끊으면 기존 댓글은 어떻게 돼?” — 필요한 문서와 근거 링크를 확인한다.
2. 수정 초안: “새 정책을 가정하지 말고, 기존 친구 문서를 현재 템플릿으로 정리한 초안만 보여줘.” — 원본이 바뀌지 않고 템플릿에 맞는 초안인지 확인한다.
3. 실제 합의된 변경이 있을 때 수정 Skill을 사용한다. 변경된 본문·최신 변경이력·미정 사항을 사람이 검수한다.

연결 권한은 팀원별로 확인해야 한다. 설치 성공과 문서 읽기 성공, 실제 편집 검증은 서로 다르다.

## 공식 설치 규격

- [Codex Skill 위치와 폴더 링크 지원](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code Skill 위치와 폴더 링크 지원](https://code.claude.com/docs/en/skills)

2026-10-01 공식 문서를 확인했다. 이 패키지는 로컬 Codex·Claude Code용이며 클라우드 실행 환경의 설치는 포함하지 않는다.
