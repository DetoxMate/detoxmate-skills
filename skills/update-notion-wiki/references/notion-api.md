# 내부 연결 CLI로 정책 작성·수정

## 실행과 사전 조회

`command -v detoxmate-notion` 또는 `$HOME/.local/bin/detoxmate-notion`에서 실행 가능한 명령을 찾는다. 아래 `$wiki_cli`는 확인한 실행 경로다. 이 스킬 설치만으로 CLI나 토큰이 설치되지는 않는다.

새 작업에서는 `"$wiki_cli" api v1/users/me -X GET`으로 인증을 확인한다. 토큰은 실행 명령이 보관소에서 읽으므로 직접 조회·출력하지 않는다. 401은 인증, 403은 연결 권한을 확인하고, 404는 ID 오류와 문서 공유 누락을 모두 고려한다. 재로그인이나 다른 MCP로 우회하지 않는다.

| 목적 | API 경로와 방식 |
|---|---|
| 속성 스키마 | `GET v1/data_sources/0656dd97-8a58-47c1-84f0-edea13a3ce31` |
| 대상·중복 문서 후보 | `POST v1/data_sources/0656dd97-8a58-47c1-84f0-edea13a3ce31/query` |
| 등록된 실제 템플릿 | `GET v1/data_sources/0656dd97-8a58-47c1-84f0-edea13a3ce31/templates` |
| 문서·템플릿 속성과 소속 | `GET v1/pages/{page_id}` |
| 문서·템플릿 본문 | `GET v1/pages/{page_id}/markdown` |

호출은 `"$wiki_cli" api "경로" -X GET` 형태다. 목록의 `has_more`·`next_cursor`와 본문의 `truncated`·`unknown_block_ids`를 확인한다. 필요한 페이지네이션·하위 블록 조회를 완료하기 전에는 자료가 없다고 단정하거나 불완전한 본문을 통째로 덮어쓰지 않는다.

## 쓰기 요청

처음 쓰는 엔드포인트는 `"$wiki_cli" api "경로" --spec -X POST` 또는 `--docs`로 현재 형식을 확인한다. 메서드는 해당 API에 맞춘다. 본문 Markdown 문법은 [공식 형식](https://developers.notion.com/guides/data-apis/enhanced-markdown)을 확인하고, 조회·작성에 같은 Markdown 버전을 사용한다.

| 목적 | API 경로와 방식 |
|---|---|
| 새 문서 | `POST v1/pages` |
| 문서 속성 | `PATCH v1/pages/{page_id}` |
| 본문 부분 수정 | `PATCH v1/pages/{page_id}/markdown` |

새 문서의 `parent`는 위 데이터 소스를 가리키도록 하고, 속성은 조회한 REST 스키마의 타입별 객체로 만든다. 등록된 템플릿을 적용한다면 완료 후 본문이 채워졌는지 확인하고 편집한다. 템플릿 본문을 별도로 덧붙여 중복 생성하지 않는다.

부분 수정 요청의 형태는 다음과 같다. 실제 `old_str`은 방금 읽은 본문의 유일하게 일치하는 구간으로, `new_str`은 합의된 내용으로 바꾼다. 정책과 최신 변경이력을 함께 반영한다.

```json
{
  "type": "update_content",
  "update_content": {
    "content_updates": [
      {"old_str": "현재 본문의 정확한 구간", "new_str": "수정할 내용"}
    ]
  }
}
```

JSON은 직렬화 도구로 임시 파일에 저장한다. 본문이나 JSON을 셸 명령에 직접 끼워 넣지 않는다. 파일에는 토큰을 넣지 않는다.

```sh
"$wiki_cli" api "v1/pages/$wiki_page_id/markdown" -X PATCH --data @update.json
```

본문·속성 수정은 별도 요청이다. 하나만 성공하면 부분 반영으로 보고하고, 성공한 생성 요청을 다시 실행하지 않는다. 응답이 비동기 작업이면 반환된 작업 ID와 현재 작업 조회 명세에 따라 완료를 확인한다. 시간 초과 등으로 결과가 불명확하면 대상과 작업 상태를 조회한 뒤 재시도한다.

저장 후 페이지 속성과 Markdown을 재조회하여 변경·소속·최신 변경이력·기존 내용 보존을 확인한다. 생성·부분 수정은 사용자가 요청한 문서 작업에만 수행한다. 스킬 설치나 연결 확인을 위해 실제 정책을 시험 수정하지 않는다.

- [CLI API 요청](https://developers.notion.com/cli/guides/api-requests)
- [본문 수정](https://developers.notion.com/reference/update-page-markdown)
- [템플릿 목록](https://developers.notion.com/reference/list-data-source-templates)
