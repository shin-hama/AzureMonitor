# The idea of this project

コンセプト: Azure Dev Ops で管理している Work Item を Redmine に関連付けるためのシステム

1. Azure DevOps API ですべての Issue アイテムを取得
2. Issue をそのまま Redmine に登録する
3. 各 Issue の子アイテムを取得する
4. 子アイテムの一覧をチケット説明欄などに記載する
5. 小アイテムが完了するごとに進捗率を上げる
6. 全子アイテムが完了したら100%にする
7. 関連付けされている PR があれば、マージコミットのメッセージを転載する
