# Frame lifecycle scenarios and verification

このドキュメントでは、`Mainmenu` 内で `_current_frame` を導入した後の想定シナリオと、
フレーム破棄の手動確認手順をまとめます。

## 操作シナリオ

- **初期表示**
  - アプリ起動時 (`Mainmenu.__init__`) に `action_serveraccess()` が呼び出され、`_current_frame` が
    `ServerAccess` フレームで初期化される。
  - `_current_frame` が `None` から実フレームに遷移し、表示中フレームは常に 1 つだけとなる。
- **別メニューへ切り替え**
  - メニューバーから `EditMacro` や `ServerRegist` を選択すると `_show_frame()` が呼び出される。
  - `_show_frame()` はまず `reset_frame()` を実行し、既存の `_current_frame` を破棄した後で新しい
    フレームを生成して `_current_frame` に保存する。
  - 破棄済みフレームは `_current_frame` から切り離され、再利用されない。
- **同一メニューの再表示**
  - 既に表示済みのメニューを再度選択した場合でも、`reset_frame()` が実行されて旧フレームが破棄される。
  - その後新しいフレームが生成されるため、表示内容が最新状態に保たれ、旧ウィジェットが残存しない。
- **設定ダイアログなどの他カテゴリ**
  - `Settings` → `Edit` のように異なるカテゴリでも同様に `_current_frame` が再生成される。
  - これにより、どのメニューを経由しても画面に複数フレームが積み重なることはない。

## 手動テスト手順

事前に `python -i main.py` でアプリを起動すると、GUI を操作しながら Python REPL から内部状態を
確認できます。

1. **初期状態の確認**
   1. GUI が表示されたら REPL で `app._content_frame.winfo_children()` を実行し、戻り値の長さが `1`
      であることを確認する。
   2. `app._current_frame` が `None` ではなく、表示中フレームのインスタンスであることを確認する。
2. **メニュー切り替えの確認**
   1. GUI で `Action` → `EditMacro` を選択する。
   2. REPL で `app._content_frame.winfo_children()` の長さが再び `1` であること、
      `app._current_frame` が新しいフレームに置き換わっていることを確認する。
3. **同一メニューの再選択**
   1. 再度 `Action` → `EditMacro` を選択する。
   2. REPL で `app._current_frame` の `destroy` メソッドが一度だけ呼び出されていることを
      ログまたはデバッガで確認する（`print` でフックする場合は次の例を参照）。
4. **破棄済みフレームの残存確認**
   1. 任意のメニューを複数回切り替えた後でも `app._content_frame.winfo_children()` の長さが `1`
      から変化しないことを確認する。
   2. `app._current_frame` の `winfo_exists()` を呼び出し、`1` が返るのは表示中のフレームのみであることを確認する。

### destroy 呼び出し回数を可視化する例

```
original_reset = app.reset_frame

def wrapped_reset():
    if app._current_frame is not None:
        print("destroy target:", type(app._current_frame).__name__)
    original_reset()

app.reset_frame = wrapped_reset
```

上記のように `reset_frame()` を一時的にラップすると、GUI 操作に合わせて破棄対象が 1 つずつ出力
され、破棄済みフレームが再利用されていないことを確認できます。
