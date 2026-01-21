def test_create_todo(client, auth_headers):
    # 1. 準備：送信データ
    payload = {
        "title": "テストのTODO",
        "description": "ちゃんと保存されるか確認",
        "completed": False
    }

    # 2. 実行：POSTリクエスト
    response = client.post("/todos", json=payload, headers=auth_headers)

    # 3. 検証：結果が正しいか
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert "id" in data
    assert data["id"] == 1

def test_create_todo_empty_title(client, auth_headers):
    # タイトルを空文字にする
    payload = {
        "title": "",
        "description": "空文字テスト",
        "completed": False
    }

    response = client.post("/todos", json=payload, headers=auth_headers)
    assert response.status_code == 422

def test_delete_todo(client, auth_headers):
    # 1. 準備：まずテスト用のデータを一個作成する
    create_res = client.post("/todos", json={"title": "消される予定のTODO"}, headers=auth_headers)
    print(f"\nResponse JSON: {create_res.json()}")
    todo_id = create_res.json()["id"]

    # 2. 実行：削除APIを叩く
    delete_res = client.delete(f"/todos/{todo_id}", headers=auth_headers)

    # 3. 検証：削除が成功したか
    assert delete_res.status_code == 200
    assert delete_res.json() == {"message": "Successfully deleted"}

    # 4. 追加検証：本当に消えたか一覧を取得して確認
    get_res = client.get("/todos")
    assert len(get_res.json()) == 0

def test_delete_todo_not_found(client, auth_headers):
    # 実行：存在しないID（例：999）を削除しようとする
    response = client.delete("/todos/999", headers=auth_headers)

    # 検証：404エラーが返ってくることを確認
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"