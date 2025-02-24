#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

def run_module():
    # モジュールの引数定義
    module_args = dict(
        input_value=dict(type='str', required=True),
    )

    # 結果を格納する辞書
    result = dict(
        changed=False,
        message='',
    )

    # AnsibleModuleオブジェクトの作成
    module = AnsibleModule(argument_spec=module_args)

    # 引数から値を取得
    input_value = module.params['input_value']

    # メッセージを設定
    result['message'] = f"Received value: {input_value}"

    # 結果を返す
    module.exit_json(**result)

if __name__ == '__main__':
    run_module()
