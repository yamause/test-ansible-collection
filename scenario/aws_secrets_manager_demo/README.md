# AWS Secret Manager の検証

Secrets Manager の検証

## 認証について

下記のいずれか

- ~/.aws/credentials や AWS SSO で設定
- 環境変数を設定
    - シークレットキー
        - `AWS_SECRET_ACCESS_KEY` or `AWS_SECRET_KEY`
    - アクセスキー
        - `AWS_ACCESS_KEY_ID` or `AWS_ACCESS_KEY`
    - セッショントークン
        - `AWS_SESSION_TOKEN`
- タスクパラメーターで指定
    - シークレットキー
        - `aws_secret_access_key` or `secret_key`
    - アクセスキー
        - `aws_access_key_id` or `access_key`
    - セッショントークン
        - `aws_session_token` or `session_token`




## Secrets の保存・更新・削除

[community.aws.secretsmanager_secret module](https://docs.ansible.com/ansible/latest/collections/community/aws/secretsmanager_secret_module.html)

```yaml
- name: Add string to AWS Secrets Manager
  community.aws.secretsmanager_secret:
    name: ansible-aws-secrets-manager-demo
    state: present
    secret_type: 'string'
    # Key/Valで保存するには文字列で正しいJSON形式で渡す必要がある。JSON形式でない場合は文字列として保存される
    secret: '{"username": "admin","password": "P@ssw0rd!"}'
    # または下記のようにYAML形式で渡すことも可能。内容は上のsecretと同じ
    # json_secret:
    #   username: admin
    #   password: P@ssw0rd!
    tags:
      CreatedBy: Ansible

- name: Retrieve the secret from AWS Secrets Manager
  community.aws.secretsmanager_secret:
    name: ansible-aws-secrets-manager-demo
    state: absent  # これだけで削除できる
```

## Secrets の取得

[amazon.aws.secretsmanager_secret lookup](https://docs.ansible.com/ansible/latest/collections/amazon/aws/secretsmanager_secret_lookup.html)

```yaml
- name: Display the retrieved secret
  ansible.builtin.debug:
    msg: "The retrieved secret is: {{ lookup('amazon.aws.aws_secret', 'ansible-aws-secrets-manager-demo') }}"

- name: Display the retrieved secret after deletion
  ansible.builtin.debug:
    msg: "The retrieved secret is: {{ lookup('amazon.aws.aws_secret', 'ansible-aws-secrets-manager-demo', on_deleted='warn') }}"
    # on_deletedオプションを指定することで、削除されたシークレットを参照した場合の挙動を制御できる
    # 'error'：エラーメッセージを表示し、タスクを失敗させる（デフォルト）
    # 'warn'：警告メッセージを表示し、空の文字列を返す
    # 'ignore'：何も表示せず、空の文字列を返す

    # on_denied オプションもあり、アクセス拒否された場合の挙動を制御できる
    # on_missing オプションもあり、シークレットが存在しない場合の挙動を制御できる
```
