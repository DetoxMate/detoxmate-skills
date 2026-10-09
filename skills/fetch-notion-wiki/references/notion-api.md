# 내부 연결 CLI로 정책 조회

## 실행 경로와 인증

`command -v detoxmate-notion`으로 실행 경로를 찾는다. PATH에 없으면 `$HOME/.local/bin/detoxmate-notion`의 존재·실행 권한을 확인한다. 아래 `$wiki_cli`는 확인한 실행 경로다. 이 스킬에는 CLI 설치나 인증정보가 포함되어 있지 않다.

새 작업에서 `"$wiki_cli" api v1/users/me -X GET`으로 인증을 확인한다. 응답의 봇 정보를 확인하되, 봇 이름만으로 문서 접근 권한을 판단하지 않는다. 뒤의 데이터 소스·페이지 조회도 성공해야 한다. 토큰 조회 명령이나 환경변수 전체를 출력하지 않는다.

## 필요한 문서만 읽기

| 목적 | API 경로와 방식 |
|---|---|
| DB 속성 확인 | `GET v1/data_sources/0656dd97-8a58-47c1-84f0-edea13a3ce31` |
| 후보 목록·필터 조회 | `POST v1/data_sources/0656dd97-8a58-47c1-84f0-edea13a3ce31/query` |
| 페이지 제목·소속 확인 | `GET v1/pages/{page_id}` |
| 페이지 본문 | `GET v1/pages/{page_id}/markdown` |

호출은 `"$wiki_cli" api "경로" -X GET` 형태다. query의 POST는 읽기 요청이다. 요청 JSON은 파일로 만들고 다음처럼 전달한다.

```sh
"$wiki_cli" api v1/data_sources/0656dd97-8a58-47c1-84f0-edea13a3ce31/query -X POST --data @query.json
```

- 조회한 스키마의 실제 속성 이름·타입으로 필터를 만든다. 예: 제목 속성의 `contains`. 관계 링크를 따라 모든 문서 본문을 읽지 않는다.
- 목록 응답은 선택에 필요한 제목·범위·ID·관련 문서만 추려 읽는다. `has_more`와 `next_cursor`를 확인하고, 필요한 후보를 찾을 때까지 `start_cursor`로 이어간다.
- 페이지 메타데이터의 `parent`로 대상 DB 소속을 확인한다. 메타데이터 응답만으로 본문을 읽었다고 하지 않는다.
- 본문의 `markdown`, `truncated`, `unknown_block_ids`를 확인한다. 누락이 있으면 현재 공식 문서의 방식에 따라 필요한 하위 블록을 추가 조회하고, 읽지 못한 범위는 명시한다.
- 이 스킬에서는 POST query 이외의 생성·수정·삭제 요청을 하지 않는다.

API 형식이 불명확하면 `"$wiki_cli" api "경로" --spec -X GET` 또는 `--docs`로 확인한다. query의 명세 확인에는 `-X POST`를 사용한다. 이 옵션은 명세 조회용이며 실제 문서를 변경하지 않는다.

## 실패 처리

명령 없음은 설치 문제, 401은 인증 문제, 403은 연결 권한 문제로 구분한다. 404는 잘못된 ID 또는 연결에 공유되지 않은 문서일 수 있다. 사용자에게 토큰을 채팅에 붙여넣으라고 요청하지 않고, 실패한 대상과 필요한 로컬 설정을 알린다.

- [CLI API 요청](https://developers.notion.com/cli/guides/api-requests)
- [Markdown 본문 조회](https://developers.notion.com/reference/retrieve-page-markdown)
