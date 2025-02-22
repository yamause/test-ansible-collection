# yamause.test

自作の ansible collection 管理を検証するためのリポジトリです。

## 使用例

Playbook へのインストール方法

```bash
ansible-galaxy collection install git+https://github.com/yamause/test-ansible-collection.git

# main ブランチ以外からインストールする場合はURLに続けて、カンマと「,」とブランチ名を入力
ansible-galaxy collection install git+https://github.com/yamause/test-ansible-collection.git,branchA

# ファイルからインストールする場合は絶対パスで指定する必要がある。また、ディレクトリがGitで管理されていなければならない。
ansible-galaxy collection install git+file://$(pwd)/
```

インストールしたロールを Playbook で実行する

```yaml
---
- name: Debug message from test01
  hosts: localhost
  gather_facts: false
  roles:
    - role: yamause.test.test01
```
